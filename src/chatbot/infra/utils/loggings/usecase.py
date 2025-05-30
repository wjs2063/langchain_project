import inspect
from functools import wraps

# def trace(logger, before=True, after=True):
#     if not logger:
#         raise ValueError("logger is required")
#
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             if before:
#                 logger.info(f"before {func.__name__} called")
#             result = func(*args, **kwargs)
#             if after:
#                 logger.info(f"after {func.__name__} called")
#             return result
#
#         return wrapper
#
#     return decorator


# def trace(logger, before=True, after=True):
#     if not logger:
#         raise ValueError("logger is required")
#
#     def decorator(func):
#         is_coroutine = inspect.iscoroutinefunction(func)
#
#         if is_coroutine:
#
#             @wraps(func)
#             async def async_wrapper(*args, **kwargs):
#                 if before:
#                     logger.info(msg=func.__name__, extra={"input": f"{kwargs}"})
#                 result = await func(*args, **kwargs)
#                 if after:
#                     logger.info(msg=func.__name__, extra={"output": result})
#                 return result
#
#             return async_wrapper
#         else:
#
#             @wraps(func)
#             def sync_wrapper(*args, **kwargs):
#                 if before:
#                     logger.info(msg=func.__name__, extra={"input": f"{kwargs}"})
#                 result = func(*args, **kwargs)
#                 if after:
#                     logger.info(msg=func.__name__, extra={"output": result})
#                 return result
#
#             return sync_wrapper
#
#     return decorator


def trace(logger, before=True, after=True):
    if not logger:
        raise ValueError("logger is required")

    def decorator(func):
        is_coroutine = inspect.iscoroutinefunction(func)

        def get_qualified_name(args):
            """첫 번째 인자에서 클래스 이름 추출"""
            if args:
                instance_or_cls = args[0]
                cls = (
                    instance_or_cls.__class__
                    if not isinstance(instance_or_cls, type)
                    else instance_or_cls
                )
                return f"{cls.__name__}.{func.__name__}"
            return func.__name__

        if is_coroutine:

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                name = get_qualified_name(args)
                if before:
                    logger.info(msg=name, extra={"input": kwargs})
                result = await func(*args, **kwargs)
                if after:
                    logger.info(msg=name, extra={"output": str(result)})
                return result

            return async_wrapper
        else:

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                name = get_qualified_name(args)
                if before:
                    logger.info(msg=name, extra={"input": kwargs})
                result = func(*args, **kwargs)
                if after:
                    logger.info(msg=name, extra={"output": str(result)})
                return result

            return sync_wrapper

    return decorator
