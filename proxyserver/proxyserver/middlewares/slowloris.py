import asyncio
from http import HTTPStatus

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class SlowlorisMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.REQUEST_TIMEOUT = 10
        self.MIN_UPLOAD_SPEED = 500

    async def dispatch(self, request: Request, call_next):
        """
        Prevent from slowloris attack to hold uncompleted connections open.
        Set timeout for request body reading and check upload speed.
        If it is too slow, return 408 error.
        """
        try:
            # Set a timeout for reading the entire request body
            body = await asyncio.wait_for(
                self._read_body_with_speed_check(request),
                timeout=self.REQUEST_TIMEOUT
            )

            # Store body for downstream middleware
            async def set_body():
                return body

            request._body = set_body

            return await call_next(request)

        except asyncio.TimeoutError:
            logger.warning(f"Slowloris attempt detected", extra=dict(
                client_ip=request.client.host,
                request_path=request.url.path
            ))
            return Response(content=b"Request timeout - too slow", status_code=HTTPStatus.REQUEST_TIMEOUT)
        except Exception as e:
            logger.exception("Error in slowloris protection", exc_info=e)
            return Response(content=b"Request processing error", status_code=HTTPStatus.BAD_REQUEST)

    async def _read_body_with_speed_check(self, request: Request) -> bytes:
        body = b""
        start_time = asyncio.get_event_loop().time()
        async for chunk in request.stream():
            body += chunk

            # Check upload speed
            elapsed_time = asyncio.get_event_loop().time() - start_time
            if elapsed_time > 0:
                upload_speed = len(body) / elapsed_time
                if upload_speed < self.MIN_UPLOAD_SPEED:
                    raise asyncio.TimeoutError("Upload too slow")

        return body
