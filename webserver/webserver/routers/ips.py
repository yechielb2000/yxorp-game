from http import HTTPStatus

import ipwhois
from fastapi import APIRouter, Depends
from geoip2fast import GeoIP2Fast
from pydantic import IPvAnyAddress
from starlette.responses import JSONResponse

from webserver.adapters.geoip import get_geoip
from webserver.controllers.ips import IpsController, get_ips_controller
from webserver.utils.jwt_token import get_current_user
from webserver.utils.logger_setup import get_user_logger, get_infra_logger

ips_router = APIRouter(
    prefix="/ips",
    dependencies=[Depends(get_current_user)]
)


@ips_router.get('/{ip}/country')
async def get_ip_info(
        ip: IPvAnyAddress,
        ips_controller: IpsController = Depends(get_ips_controller),
        geo_ip: GeoIP2Fast = Depends(get_geoip)
):
    get_user_logger().info("Request query for ip started", extra={'ip_address': ip})
    ip = str(ip)

    ip_info = geo_ip.lookup(ip)

    get_infra_logger().info("Checking if IP is private", extra={'ip_address': ip})

    if ip_info.is_private:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content="IP is private")

    get_infra_logger().info("Looking up ip country", extra={'ip_address': ip})
    if not ip_info.country_code:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content="Could not find country for ip")

    get_infra_logger().info("Found country for ip: ", extra={'ip_address': ip})
    return await ips_controller.upsert_ip_info(ip, ip_info.country_code)
