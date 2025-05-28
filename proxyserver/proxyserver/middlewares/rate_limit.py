from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

MAX_REQUESTS_PER_SECOND = 20


async def rate_limiter_middleware(request: Request, call_next):
    ip = request.client.host
    key = f"ratelimit:{ip}"

    count = await request.state.redis_client.incr(key)
    if count == 1:
        await request.state.redis_client.expire(key, 1)

    if count > MAX_REQUESTS_PER_SECOND:
        return JSONResponse(status_code=HTTPStatus.TOO_MANY_REQUESTS, content={"error": "Too many requests"})

    return await call_next(request)
