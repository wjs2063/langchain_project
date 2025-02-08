from langchain_redis import RedisCache
from langchain.globals import set_llm_cache

redis_cache = RedisCache(redis_url="redis://127.0.0.1:6378")

set_llm_cache(redis_cache)
