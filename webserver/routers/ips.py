from http import HTTPStatus

import ipwhois
from fastapi import APIRouter, Depends
from loguru import logger
from pydantic import IPvAnyAddress
from starlette.responses import JSONResponse

from webserver.controllers.ips import IpsController, get_ips_controller

ips_router = APIRouter(
    prefix="/ips",
    dependencies=[]
)


@ips_router.get('/{ip}/country')
async def get_ip_info(ip: IPvAnyAddress, ips_controller: IpsController = Depends(get_ips_controller)):
    logger.info("Request query for ip started", extra={'ip_address': ip})
    whois = ipwhois.IPWhois(ip)
    results = whois.lookup_rdap()
    country = results.get('network', {}).get('country')
    if country:
        return ips_controller.upsert_ip_info(str(ip), country)
    logger.debug("IP info not found", extra={'ip_address': ip})
    return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content={"error": "IP info not found"})
