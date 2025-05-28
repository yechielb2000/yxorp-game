import redis.asyncio as redis
from settings import settings

import redis

def create_redis():
  return redis.ConnectionPool(
    host=settings.redis_host,
    port=settings.redis_port,
    db=0,
    decode_responses=True
  )

redis_instance = create_redis()

def get_redis():
  return redis.Redis(connection_pool=redis_instance)