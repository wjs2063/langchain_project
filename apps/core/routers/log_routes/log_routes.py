from typing import List, Callable, Awaitable, Coroutine, Any
from fastapi import Request, BackgroundTasks, Response
from fastapi.routing import APIRoute
import json
from apps.infras.utils.loggings.root import logger
from entities.chains.base_chain import response_schemas


def log_handler(log_data: dict):
    request_headers = log_data.get("request", {}).get("headers", {})
    request_body = log_data.get("request", {}).get("body", {})
    # request_query_params = log_data.get("request", {}).get("param", {})
    # request_path_params = log_data.get("request", {}).get("path_params", {})
    response_body = log_data.get("response", {}).get("body", {})
    log_data = {
        "request_info": {
            "headers": request_headers,
            "session_id": request_body.get("session_id", "not found"),
            "question": request_body.get("question", "not found"),
        },
        "response_info": response_body,
    }
    logger.info(log_data)


class LogRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)
            request_headers = dict(request.headers)
            request_body = await request.body()
            request_body = (
                json.loads(request_body.decode("utf-8")) if request_body else {}
            )
            response_body = (
                json.loads(response.body.decode("utf-8")) if response.body else {}
            )
            request_path_params = dict(request.path_params)
            request_query_params = dict(request.query_params)
            log_data = {
                "request": {
                    "headers": request_headers,
                    "param": request_query_params,
                    "body": request_body,
                    "path_params": request_path_params,
                },
                "response": {"body": response_body},
            }

            original_background = response.background
            response.background = BackgroundTasks()
            if original_background:
                response.background = BackgroundTasks([original_background])

            response.background.add_task(func=log_handler, log_data=log_data)
            return response

        return custom_route_handler
