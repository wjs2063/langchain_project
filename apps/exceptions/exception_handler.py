from starlette.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi import Request, Response


class BaseException(Exception):

    def __init__(self, status_code: int, detail: str, trace: str):
        self.status_code = status_code
        self.detail = detail
        self.trace = trace


class InvalidRequest(BaseException):
    def __init__(self, status_code, detail: str, trace: str):
        super().__init__(status_code, detail, trace)


class CustomException(BaseException):
    def __init__(self, status_code: int, detail: str, trace: str):
        super().__init__(status_code, detail, trace)


async def custom_exception_handler(request: Request, exc: str):
    print(request.headers)
    print(exc)

    return JSONResponse(status_code=499, content={"error": exc})
