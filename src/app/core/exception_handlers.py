"""
This is adapted from Roy Pasternak work
Link : https://github.com/roy-pstr/fastapi-custom-exception-handlers-and-logs/blob/master/exception_handlers.py
"""

import sys
from typing import Union
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response

from app.core.logger import logger


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    This is a wrapper to the default RequestValidationException handler of FastAPI.
    This function will be called when client input is not valid.
    """
    logger.debug("Our custom request_validation_exception_handler was called")
    query_params = request.query_params._dict  # pylint: disable=protected-access
    detail = {"errors": exc.errors(), "body": exc.body, "query_params": query_params}
    logger.debug(detail)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": "The following validation errors were encountered:",
                "errors": detail.get("errors")
            }
        )
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> Union[JSONResponse, Response]:
    """
    This is a wrapper to the default HTTPException handler of FastAPI.
    This function will be called when a HTTPException is explicitly raised.
    """
    logger.debug("Our custom http_exception_handler was called")

    return await _http_exception_handler(request, exc)


async def unhandled_exception_handler(request: Request, exc: Exception) -> PlainTextResponse:
    """
    This middleware will log all unhandled exceptions.
    Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
    """
    logger.debug("Our custom unhandled_exception_handler was called")
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    exception_type, exception_value, _ = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    logger.error(
        f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {exception_value}>'
    )

    return PlainTextResponse(str(exc), status_code=500)
