import http
import time
from datetime import datetime
from fastapi import Request
from app.core.logger import logger


async def log_request_middleware(request: Request, call_next):
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    timestamp = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")

    try:
        status_phrase = http.HTTPStatus(response.status_code).phrase
    except ValueError:
        status_phrase = ""

    logger.info(
        f"{host}:{port} - {timestamp} - "
        f"\"{request.method} {url}\" - "
        f"{response.status_code} {status_phrase} {formatted_process_time} ms"
    )

    return response
