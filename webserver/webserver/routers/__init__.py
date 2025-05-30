from webserver.routers.countries import countries_router
from webserver.routers.ips import ips_router
from webserver.routers.user import user_router

__all__ = [
    "user_router",
    "ips_router",
    "countries_router"
]
