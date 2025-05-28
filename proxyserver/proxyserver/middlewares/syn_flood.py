import time
from collections import defaultdict
from http import HTTPStatus

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class SynFloodMiddleware(BaseHTTPMiddleware):
    MAX_CONNECTIONS_PER_IP: int = 50
    TIME_WINDOW: int = 1
    redis_key: str

    def __init__(self, app):
        super().__init__(app)
        self.connection_tracker = defaultdict(list)

    def _clean_old_connections(self, ip: str, current_time: float):
        self.connection_tracker[ip] = [
            t for t in self.connection_tracker[ip]
            if current_time - t < self.TIME_WINDOW
        ]

    async def dispatch(self, request: Request, call_next):
        """
        Prevent SYN flood by checking the number of connections per IP address.
        For each IP address, only the last `TIME_WINDOW` seconds are considered.
        If the number of connections exceeds `MAX_CONNECTIONS_PER_IP`, return 429.
        """
        client_ip = request.client.host
        current_time = time.time()

        self._clean_old_connections(client_ip, current_time)

        if len(self.connection_tracker[client_ip]) >= self.MAX_CONNECTIONS_PER_IP:
            logger.warning(f"Potential SYN flood detected from {client_ip}")
            return Response(content=b"Too many connection attempts", status_code=HTTPStatus.TOO_MANY_REQUESTS)

        self.connection_tracker[client_ip].append(current_time)

        return await call_next(request)
