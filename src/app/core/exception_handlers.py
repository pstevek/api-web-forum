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
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response
from datetime import datetime

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


async def pydantic_validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": "Data validation error",
                "errors": str(exc)
            }
        )
    )
