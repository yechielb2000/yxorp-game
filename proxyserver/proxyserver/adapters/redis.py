from redis.asyncio import Redis

from settings import settings


def get_redis() -> Redis:
    return Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        decode_responses=True
    )
