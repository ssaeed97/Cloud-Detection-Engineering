import json
import logging
import time
import uuid
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


def get_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def json_log(logger: logging.Logger, event: str, **fields: Any) -> None:
    record = {"event": event, **fields}
    logger.info(json.dumps(record, separators=(",", ":"), default=str))


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Adds:
      - X-Request-ID (generated if missing)
      - request.state.request_id
      - request.state.start_ts
    Logs a structured request completion event.
    """

    def __init__(self, app, logger: logging.Logger):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = req_id
        request.state.start_ts = time.time()

        response: Response
        try:
            response = await call_next(request)
            return response
        finally:
            duration_ms = int((time.time() - request.state.start_ts) * 1000)

            # best-effort client IP (works behind ALB if you pass X-Forwarded-For)
            xff = request.headers.get("x-forwarded-for")
            src_ip = (xff.split(",")[0].strip() if xff else request.client.host) if request.client else None

            json_log(
                self.logger,
                "http_request",
                request_id=req_id,
                method=request.method,
                path=request.url.path,
                status_code=getattr(response, "status_code", None),
                duration_ms=duration_ms,
                src_ip=src_ip,
                user_agent=request.headers.get("user-agent"),
            )
