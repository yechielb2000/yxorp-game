from http import HTTPStatus

from fastapi import Request
from httpx import AsyncClient
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from loguru import logger
from settings import settings

class ProxyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.target_url = settings.webserver_url.rstrip('/')
        
    async def dispatch(self, request: Request, call_next):
        """
        Forwarding the request to the target_url and return the response from the target server.

        :param request: A `Request` object representing the incoming HTTP request, including
            its method, headers, body, and other details.
        :type request: Request
        :param call_next: A callable for passing the request to the next layer of processing
            if needed by the framework.
        :type call_next: callable
        :return: A `Response` object containing the HTTP response received from the target server
            or an error response in case of failure.
        :rtype: Response
        """
        path = request.url.path
        target_url = f"{self.target_url}{path}"
        if request.query_params:
            target_url = f"{target_url}?{request.query_params}"

        try:
            async with AsyncClient() as client:
                response = await client.request(
                    method=request.method,
                    url=target_url,
                    headers=dict(request.headers),
                    content=await request.body()
                )
                
                return Response(
                    content=response.content,
                    status_code=response.status_code,
                    headers=dict(response.headers)
                )
        except Exception as e:
            logger.exception("Proxy error", exc_info=e, extra=dict(target_url=target_url))
            return Response(
                content=b"Proxy error",
                status_code=HTTPStatus.BAD_GATEWAY
            )