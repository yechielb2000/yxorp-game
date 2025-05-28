from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    For each ip update the redis counter.
    If in exceed the request limit of `MAX_REQUESTS_PER_SECOND`, return 429.
    """
    MAX_REQUESTS_PER_SECOND = 20

    def __init__(self, app, redis_client: Redis):
        super().__init__(app)
        self.redis = redis_client

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        key = f"ratelimit:{ip}"

        count = await self.redis.incr(key)
        if count == 1:
            await self.redis.expire(key, 1)

        if count > self.MAX_REQUESTS_PER_SECOND:
            return JSONResponse(status_code=HTTPStatus.TOO_MANY_REQUESTS, content={"error": "Too many requests"})

        return await call_next(request)
