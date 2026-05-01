from typing import Any, Dict

from django.conf import settings
from redis import Redis


class RedisClient(Redis):
    def __init__(self, host: str, port: int, db: int, decode_responses: bool = True):
        super().__init__(host, port, db, decode_responses)

    def get_next_task_id(self) -> int:
        """Atomically generates the next ID for the task"""
        return int(self.incr("task:next_id"))


redis_client = RedisClient(
    host=settings.REDIS_HOST,
    port=int(settings.REDIS_PORT),
    db=int(settings.REDIS_DB),
)
