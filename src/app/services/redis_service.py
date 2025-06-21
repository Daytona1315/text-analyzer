import json

from src.db.redis_client import get_redis_connection
from src.app.utils.env_loader import Config


class RedisService:
    """
    Contains methods to work with Redis database
    """
    def __init__(self):
        self.redis = get_redis_connection(db=1, decode_responses=True)

    def analysis_result_save(self, user_id: str, data: dict):
        self.redis.lpush(user_id, json.dumps(data))
        if self.redis.ttl(user_id) == -1:
            self.redis.expire(user_id, Config.redis_record_expire)
        self.redis.ltrim(user_id, 0, Config.redis_max_count)

    def analysis_result_get(self, user_id: str, analysis_id: str) -> dict | None:
        user_data: list = self.redis.lrange(user_id, 0, Config.redis_max_count)
        for record in user_data:
            dictionary: dict = json.loads(record)
            if dictionary['id'] == analysis_id:
                return dictionary
        return None

    def analysis_result_clear(self, user_id: str):
        self.redis.delete(user_id)

    def analysis_history_get(self, user_id: str) -> list:
        raw_list = self.redis.lrange(user_id, 0, Config.redis_max_count)
        return [
            {
                'id': data['id'],
                'short_preview': data['short_preview']
            }
            for item in raw_list
            for data in [json.loads(item)]
        ]
