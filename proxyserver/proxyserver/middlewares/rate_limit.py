from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from redis.asyncio import Redis
from redis.exceptions import RedisError
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    For each ip update the redis counter.
    If in exceed the request limit of `MAX_REQUESTS_PER_SECOND`, return 429.
    """
    MAX_REQUESTS_PER_SECOND: int = 20
    RATE_LIMIT_DURATION: int = 1
    REDIS_KEY_PREFIX: str = "ratelimit:"

    def __init__(self, app, redis_client: Redis):
        super().__init__(app)
        self.redis = redis_client

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        try:
            is_rate_limited, request_count = await self._check_rate_limit(client_ip)

            if is_rate_limited:
                logger.info(f"Rate limit exceeded", extra=dict(client_ip=client_ip, request_count=request_count))
                return self._create_rate_limit_response()

            return await call_next(request)

        except RedisError as e:
            pass
            logger.exception("Redis error", exc_info=e, extra=dict(client_ip=client_ip))
            return await call_next(request)

    async def _check_rate_limit(self, ip_address: str) -> tuple[bool, int]:
        """
        Checks if the rate limit for a specific IP address has been exceeded.

        :param ip_address: The IP address of the client making the request.
        :type ip_address: str
        :return: A tuple containing a boolean indicating whether the rate limit has
            been exceeded and the current request count for the IP address.
        :rtype: Tuple[bool, int]
        """
        redis_key = f"{self.REDIS_KEY_PREFIX}{ip_address}"
        request_count = await self.redis.incr(redis_key)

        if request_count == 1:
            await self.redis.expire(redis_key, self.RATE_LIMIT_DURATION)

        return request_count > self.MAX_REQUESTS_PER_SECOND, request_count

    def _create_rate_limit_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            content={"error": "Too many requests"}
        )
