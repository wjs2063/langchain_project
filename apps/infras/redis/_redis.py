import os

from redis import Redis

_redis_url = 'redis://localhost:6378'
redis_url = os.environ.get('REDIS_URL', _redis_url)


def get_redis_client():
    return Redis.from_url(redis_url)
