from fastapi import FastAPI
from apps.apis.v1.v1_endpoint import chat_router
from chainlit.utils import mount_chainlit
from tortoise.contrib.fastapi import register_tortoise, RegisterTortoise
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from tortoise import Tortoise, generate_config, run_async
from apps.apis.api_routes import router
import os
from apps.infras.db.postgres import DB_CONFIG


@asynccontextmanager
async def lifespan_test(_app: FastAPI) -> AsyncGenerator[None, None]:
    config = generate_config(
        os.getenv("TORTOISE_TEST_DB", "sqlite://:memory:"),
        app_modules={
            "apps": ["entities.auth.model"],
        },
        testing=True,
        connection_label="default",
    )
    async with RegisterTortoise(
        app=_app,
        config=config,
        generate_schemas=True,
        add_exception_handlers=True,
        _create_db=True,
    ):
        # db connected
        # print(Tortoise.get_connection("default"))
        yield
        # app teardown
    # db connections closed
    await Tortoise.close_connections()
    # await Tortoise._drop_databases()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    if getattr(_app.state, "testing", None):
        async with lifespan_test(_app) as _:
            yield
    else:
        # app startup
        async with RegisterTortoise(
            app=_app,
            config=DB_CONFIG,
            generate_schemas=True,
            add_exception_handlers=True,
        ):
            yield


app = FastAPI(title="Langchain ChatBot Apps", lifespan=lifespan)

app.include_router(chat_router)
app.include_router(router)


@app.post("/")
async def root():
    return {"message": "Hello World"}


mount_chainlit(app=app, target="./apps/services/chain_lit_service.py", path="/chainlit")
