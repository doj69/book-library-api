import contextvars
import errno
import json
import logging
import os
import random
import string
import sys
import time

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

http_request_context = contextvars.ContextVar(
    "http_request_context", default=dict({})
)


def mkdir_p(path):
    try:
        os.makedirs(path, exist_ok=True)
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        http_request = {
            "requestMethod": request.method,
            "requestUrl": request.url.path,
            "requestSize": sys.getsizeof(request),
            "remoteIp": request.client.host,
            "protocol": request.url.scheme,
        }

        if "referrer" in request.headers:
            http_request["referrer"] = request.headers.get("referrer")

        if "user-agent" in request.headers:
            http_request["userAgent"] = request.headers.get("user-agent")

        http_request_context.set(http_request)

        try:
            logger.info(json.dumps(http_request, indent=4))
            return await call_next(request)
        except Exception as ex:
            logger.error(f"Request failed: {ex}", exc_info=True)
            message = str(ex)
            return JSONResponse(
                status_code=500, content={"success": False, "message": message}
            )


class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        idem = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        logger.info(f"rid={idem} start request path={request.url.path}")
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)
        logger.info(
            f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
        )

        return response
