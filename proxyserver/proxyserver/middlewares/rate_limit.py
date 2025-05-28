from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse
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
        try:
            ip = request.client.host
            key = f"{self.REDIS_KEY_PREFIX}{ip}"

            count = await self.redis.incr(key)
            if count == 1:
                await self.redis.expire(key, self.RATE_LIMIT_DURATION)

            if count > self.MAX_REQUESTS_PER_SECOND:
                return self._create_rate_limit_response()
            return await call_next(request)
        except RedisError:
            pass
            # TODO: log this out!
            return await call_next(request)

    def _create_rate_limit_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            content={"error": "Too many requests"}
        )
