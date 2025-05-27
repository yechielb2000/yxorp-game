from contextlib import asynccontextmanager

import ipwhois
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.params import Depends
from loguru import logger
from pydantic import IPvAnyAddress

from webserver.adapters.postgresql import pg_engine, BasePG
from webserver.controllers.ips import get_ips_controller, IpsController
from webserver.logger_setup import setup_logger


@asynccontextmanager
async def lifespan(a: FastAPI):
    load_dotenv()
    setup_logger()
    async with pg_engine.begin() as conn:
        await conn.run_sync(BasePG.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/geolocation/{ip_address}')
async def get_ip_info(ip_address: IPvAnyAddress, ips_controller: IpsController = Depends(get_ips_controller)):
    logger.info("Request query for ip started", extra={'ip_address': ip_address})
    whois = ipwhois.IPWhois(ip_address)
    results = whois.lookup_rdap()
    country = results.get('network', {}).get('country')
    if country:
        ips_controller.create_ip_info(country)
    else:
        logger.debug("ip info not found", extra={'ip_address': ip_address})
    return


if __name__ == '__main__':
    uvicorn.run("cnc:app", host="0.0.0.0", port=8000)
