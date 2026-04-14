import logging
import time
import uuid
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.core.logging import request_id_ctx

logger = logging.getLogger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        rid = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        token = request_id_ctx.set(rid)
        start = time.perf_counter()
        try:
            response = await call_next(request)
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.info(
                "%s %s -> %d %.2fms",
                request.method,
                request.url.path,
                response.status_code,
                elapsed_ms,
            )
            response.headers["X-Request-ID"] = rid
            return response
        finally:
            request_id_ctx.reset(token)
