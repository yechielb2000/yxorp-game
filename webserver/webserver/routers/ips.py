from http import HTTPStatus

import ipwhois
from fastapi import APIRouter, Depends
from pydantic import IPvAnyAddress
from starlette.responses import JSONResponse

from webserver.utils.jwt_token import get_current_user
from webserver.controllers.ips import IpsController, get_ips_controller
from webserver.utils.logger_setup import get_user_logger, get_infra_logger

ips_router = APIRouter(
    prefix="/ips",
    dependencies=[Depends(get_current_user)]
)


@ips_router.get('/{ip}/country')
async def get_ip_info(ip: IPvAnyAddress, ips_controller: IpsController = Depends(get_ips_controller)):
    ip = str(ip)
    get_user_logger().info("Request query for ip started", extra={'ip_address': ip})
    whois = ipwhois.IPWhois(ip)
    get_infra_logger().info("Looking up ip info for ip: ", extra={'ip_address': ip})
    results = whois.lookup_rdap()
    country = results.get('network', {}).get('country')
    if country:
        get_infra_logger().info("Found country for ip: ", extra={'ip_address': ip})
        return await ips_controller.upsert_ip_info(ip, country)
    get_infra_logger().info("IP info not found", extra={'ip_address': ip})
    return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content={"error": "IP info not found"})
