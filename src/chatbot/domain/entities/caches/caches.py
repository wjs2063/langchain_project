from langchain.globals import set_llm_cache
from langchain_redis import RedisCache

from chatbot.infra.redis._redis import _redis_url

redis_cache = RedisCache(redis_url=_redis_url)

set_llm_cache(redis_cache)
