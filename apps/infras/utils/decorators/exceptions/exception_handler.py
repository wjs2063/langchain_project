# apps/infras/utils/decorators.py
import asyncio
import traceback
from functools import wraps
from apps.exceptions.exception_handler import CustomException, TimeoutException
from exceptions.exception_handler import UndefinedException
import inspect


# 모든 에러는 해당 함수에 기재
def _handle_exception(e: Exception) -> Exception:
    trace = traceback.format_exc()

    if isinstance(e, CustomException):
        return CustomException(status_code=e.status_code, detail=str(e), trace=trace)

    if isinstance(e, asyncio.TimeoutError):
        return TimeoutException(status_code=408, detail=str(e), trace=trace)

    return UndefinedException(status_code=500, detail=str(e), trace=trace)


def register_exception_handler(func):
    is_coroutine = inspect.iscoroutinefunction(func)

    if is_coroutine:

        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                raise _handle_exception(e)

        return wrapper
    else:

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise _handle_exception(e)

        return wrapper


# def sync_exception_handler(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             trace = traceback.format_exc()
#             raise UndefinedException(status_code=500, detail=str(e), trace=trace)
#
#     return wrapper
