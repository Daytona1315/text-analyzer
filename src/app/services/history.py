from src.db.redis import get_redis_connection


r = get_redis_connection(db=1)


class HistoryService:
    """
    Contains methods to work with requests history
    """

    @classmethod
    def history_save(cls, user_id: str, data: str) -> None:
        key = f"history:{user_id}"
        r.rpush(key, data)

    @classmethod
    def history_get(cls, user_id: str, count: int = 10) -> list:
        key = f"history:{user_id}"
        return r.lrange(key, -count, -1)

    @classmethod
    def history_clear(cls, user_id: str) -> None:
        key = f"history:{user_id}"
        r.delete(key)
