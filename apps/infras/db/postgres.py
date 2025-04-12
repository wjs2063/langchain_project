import os
from functools import partial
from typing import AsyncGenerator

import redis.asyncio as redis
from pydantic_settings import BaseSettings
from redis.cluster import RedisCluster as Cluster
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import RegisterTortoise

DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "localhost",
                "port": "8080",
                "user": "postgres",
                "password": "postgres",
                "database": "postgres",
                "min_size": 1,  # 최소 연결 수
                "max_size": 100,  # 최대 연결 수
                "ssl": False,  # SSL 사용 여부
                "timeout": 60,  # 연결 타임아웃
            },
        }
    },
    # 내가 등록할 앱네임들 지정
    "apps": {
        "models": {
            # models 가 정의된 app 내의 경로
            "models": ["apps.infras.repository.user_repository.model"],
            "default_connection": "default",
        },
    },
    "use_tz": False,  # 타임존 사용 여부
    "timezone": "UTC",  # 타임존 설정 (use_tz가 True일 경우 유효)
}


async def init():
    await Tortoise.init(DB_CONFIG)
    await Tortoise.generate_schemas()


# run_async(init())

register_orm = partial(
    RegisterTortoise,
    db_url=os.getenv("DB_URL", "sqlite://db.sqlite3"),
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


class RedisConfig(BaseSettings):
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


redis_config = RedisConfig()


class RedisPool:
    def __init__(self, redis_url: str):
        self._redis_url = redis_url
        self._pool = None

    async def _initialize_pool(self):
        if self._pool is None:
            self._pool = redis.ConnectionPool.from_url(self._redis_url)

    async def get_redis_pool(self) -> redis.ConnectionPool:
        if self._pool is None:
            await self._initialize_pool()
        return self._pool


redis_pool = RedisPool(redis_url=redis_config.redis_url)


async def get_redis_client() -> AsyncGenerator[redis.Redis.client, None]:
    _redis_pool = await redis_pool.get_redis_pool()
    _redis_client = redis.Redis.from_pool(_redis_pool)
    try:
        yield _redis_client
    except ConnectionError:
        raise ConnectionError
    except Exception as e:
        raise Exception(f"An Unknown Error raised. {e}")
    finally:
        await _redis_client.aclose()
