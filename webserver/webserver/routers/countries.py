from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from webserver.utils.jwt_token import get_current_user
from webserver.controllers.ips import IpsController, get_ips_controller
from webserver.utils.logger_setup import get_user_logger

countries_router = APIRouter(
    prefix="/countries",
    dependencies=[Depends(get_current_user)]
)


@countries_router.get('/top')
async def get_top_queried_countries(top: PositiveInt, ips_controller: IpsController = Depends(get_ips_controller)):
    get_user_logger().info("Request most queried countries", extra={"top": top})
    return await ips_controller.get_top_queried_countries(top)


@countries_router.get('/{country}/ips')
async def get_country_ips(
        country: str,
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        ips_controller: IpsController = Depends(get_ips_controller)
):
    get_user_logger().info("Request ips of country",
                           extra={"country": country, "start_time": start_time, "end_time": end_time})
    return await ips_controller.get_ips_by_country(country, start_time=start_time, end_time=end_time)
