from fastapi import Request
from fastapi.responses import JSONResponse

from backend.exceptions.custom_exception import (
    CustomException
)

from backend.exceptions.error_response import (
    ErrorResponse
)

from backend.exceptions.error_code import (
    ErrorCode
)


async def custom_exception_handler(
        request: Request,
        exc: CustomException
):

    error_code = exc.error_code

    return JSONResponse(

        status_code=error_code.status_code,

        content=ErrorResponse(
            status=error_code.status_code,
            message=error_code.message
        ).dict()
    )


async def global_exception_handler(
        request: Request,
        exc: Exception
):

    return JSONResponse(

        status_code=500,

        content=ErrorResponse(
            status=500,
            message=ErrorCode.INTERNAL_SERVER_ERROR.message
        ).dict()
    )