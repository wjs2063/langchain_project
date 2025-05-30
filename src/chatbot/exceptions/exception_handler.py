from starlette.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi import Request, Response, FastAPI


class CustomException(Exception):
    def __init__(self, status_code: int, detail: str, trace: str):
        super().__init__()
        self.status_code = status_code
        self.detail = detail
        self.trace = trace


class TimeoutException(Exception):
    def __init__(self, status_code: int, detail: str, trace: str):
        super().__init__()
        self.status_code = status_code
        self.detail = detail
        self.trace = trace


class UndefinedException(Exception):
    def __init__(self, status_code: int, detail: str, trace: str):
        super().__init__()
        self.status_code = status_code
        self.detail = detail
        self.trace = trace


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(CustomException)
    async def handle_custom_exception(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_code": "CUSTOM_ERROR",
                "error_message": exc.detail,
                "trace": exc.trace,
            },
        )

    @app.exception_handler(TimeoutException)
    async def handle_timeout_exception(request: Request, exc: TimeoutException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_code": "TIMEOUT_ERROR",
                "error_message": exc.detail,
                "trace": exc.trace,
            },
        )

    @app.exception_handler(UndefinedException)
    async def handle_undefined_exception(request: Request, exc: UndefinedException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_code": "UNDEFINED_ERROR",
                "error_message": exc.detail,
                "trace": exc.trace,
            },
        )

    # 모든 예외에 대한 fallback 핸들러도 등록 가능
    @app.exception_handler(Exception)
    async def handle_general_exception(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error_code": "INTERNAL_SERVER_ERROR",
                "error_message": str(exc),
            },
        )
