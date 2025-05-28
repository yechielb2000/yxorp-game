from redis.asyncio import Redis

from settings import settings


def get_redis() -> Redis:
    return Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        username=settings.redis_user,
        password=settings.redis_password,
        decode_responses=True,
        retry_on_timeout=True,
        db=0,
    )

redis_instance = get_redis()
