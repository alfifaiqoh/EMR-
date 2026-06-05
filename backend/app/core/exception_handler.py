from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = exc.errors()

    for error in errors:
        field = error["loc"][-1]

        if field == "status":
            return JSONResponse(
                status_code=422,
                content={
                    "message":
                    "Status harus WAITING, IN_PROGRESS, COMPLETED atau CANCELLED"
                }
            )

    return JSONResponse(
        status_code=422,
        content={
            "message": "Data tidak valid"
        }
    )