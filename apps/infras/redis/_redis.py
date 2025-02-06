import os

from redis import Redis

redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6378')


def get_redis_client():
    return Redis.from_url(redis_url)
