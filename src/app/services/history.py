from src.db.redis import get_redis_connection


r = get_redis_connection(db=1)


class HistoryService:
    """
    Contains methods to work with requests history
    """

    @classmethod
    def save_history(cls, user_id: str, data: str) -> None:
        key = f"history:{user_id}"
        r.rpush(key, data)

    @classmethod
    def get_history(cls, user_id: str, count: int = 10) -> list:
        key = f"history:{user_id}"
        return r.lrange(key, -count, -1)

    @classmethod
    def clear_history(cls, user_id: str) -> None:
        key = f"history:{user_id}"
        r.delete(key)
