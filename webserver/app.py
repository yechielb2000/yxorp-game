from contextlib import asynccontextmanager
from datetime import datetime
from http import HTTPStatus
from typing import Optional

import ipwhois
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.params import Depends
from loguru import logger
from pydantic import IPvAnyAddress, PositiveInt
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette.responses import JSONResponse

from webserver.adapters.postgresql import pg_engine, BasePG
from webserver.controllers.ips import get_ips_controller, IpsController
from webserver.logger_setup import setup_logger


@asynccontextmanager
async def lifespan(a: FastAPI):
    load_dotenv()
    setup_logger()
    conn: AsyncConnection
    async with pg_engine.begin() as conn:
        await conn.run_sync(BasePG.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/ips/{ip}/country')
async def get_ip_info(ip: IPvAnyAddress, ips_controller: IpsController = Depends(get_ips_controller)):
    logger.info("Request query for ip started", extra={'ip_address': ip})
    whois = ipwhois.IPWhois(ip)
    results = whois.lookup_rdap()
    country = results.get('network', {}).get('country')
    if country:
        return ips_controller.upsert_ip_info(str(ip), country)
    logger.debug("IP info not found", extra={'ip_address': ip})
    return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content={"error": "IP info not found"})


@app.get('/countries/{country}/ips')
async def get_country_ips(
        country: str,
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        ips_controller: IpsController = Depends(get_ips_controller)
):
    logger.info("Request ips of country", extra={"country": country, "start_time": start_time, "end_time": end_time})
    return ips_controller.get_ips_by_country(country, start_time=start_time, end_time=end_time)


@app.get('/countries/top')
async def get_top_queried_countries(top: PositiveInt, ips_controller: IpsController = Depends(get_ips_controller)):
    logger.info("Request most queried countries", extra={"top": top})
    return ips_controller.get_top_queried_countries(top)


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8001)
