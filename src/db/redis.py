import redis
from PIL.DdsImagePlugin import item1

from src.app.utils.env_loader import Config


def get_redis_connection(db: int = 0, decode_responses: bool = True):
    return redis.Redis(
        host=Config.redis_host,
        port=Config.redis_port,
        db=db,
        decode_responses=decode_responses,
    )
