import redis

from src.app.utils.config import Config


def get_redis_connection(db: int = 0, decode_responses: bool = True):
    return redis.Redis(
        host="redis",
        port=Config.redis_port,
        db=db,
        decode_responses=decode_responses,
    )
