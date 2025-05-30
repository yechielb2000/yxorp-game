import ipaddress
from http import HTTPStatus

import ipwhois
from fastapi import APIRouter, Depends
from ipwhois import IPDefinedError
from pydantic import IPvAnyAddress
from starlette.responses import JSONResponse

from webserver.controllers.ips import IpsController, get_ips_controller
from webserver.utils.jwt_token import get_current_user
from webserver.utils.logger_setup import get_user_logger, get_infra_logger

ips_router = APIRouter(
    prefix="/ips",
    dependencies=[Depends(get_current_user)]
)


@ips_router.get('/{ip}/country')
async def get_ip_info(ip: IPvAnyAddress, ips_controller: IpsController = Depends(get_ips_controller)):
    # TODO: fix not an ip bug 8.8.4.4
    get_user_logger().info("Request query for ip started", extra={'ip_address': ip})
    ip = str(ip)

    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_global:
            get_infra_logger().info("Looking up ip info for ip: ", extra={'ip_address': ip})
            whois = ipwhois.IPWhois(ip)
            search_result = whois.lookup_rdap()
            country = search_result.get('network', {}).get('country')
            if country:
                get_infra_logger().info("Found country for ip: ", extra={'ip_address': ip})
                return await ips_controller.upsert_ip_info(ip, country)
        else:
            get_infra_logger().info("IP is not global", extra={'ip_address': ip})
            raise IPDefinedError("IP is not global")
    except IPDefinedError as e:
        get_infra_logger().error("IP defined error", extra={'ip_address': ip}, exc_info=e)

    get_infra_logger().info("IP country not found", extra={'ip_address': ip})
    return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content="Could not find country for ip")
