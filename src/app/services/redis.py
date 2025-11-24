import json

from redis import RedisError

from src.db.redis_client import get_redis_connection
from src.app.utils.config import Config
from src.app.utils.custom_exceptions import RedisException


class RedisService:
    """
    Contains methods to work with Redis database
    """

    def __init__(self):
        self.redis = get_redis_connection(db=1, decode_responses=True)

    def analysis_result_save(self, user_id: str, data: dict) -> None:
        p = self.redis.pipeline()
        try:
            p.lpush(user_id, json.dumps(data))
            p.expire(user_id, Config.redis_record_expire)
            p.ltrim(user_id, 0, Config.redis_max_count)
            p.execute()
        except RedisError as e:
            raise RedisException(exception=e)

    def analysis_result_get(self, user_id: str, analysis_id: str) -> dict | None:
        for record in self.redis.lrange(user_id, 0, Config.redis_max_count):
            try:
                d = json.loads(record)
                if d.get("id") == analysis_id:
                    return d
            except json.JSONDecodeError:
                continue
        return None

    def analysis_result_clear(self, user_id: str) -> None:
        try:
            self.redis.delete(user_id)
        except RedisError as e:
            raise RedisException(exception=e)

    def analysis_history_get(self, user_id: str):
        try:
            raw_list = self.redis.lrange(user_id, 0, Config.redis_max_count)
            return [
                {"id": d["id"], "short_preview": d["short_preview"]}
                for item in raw_list
                if (d := json.loads(item))
            ]
        except RedisError as e:
            raise RedisException(exception=e)
