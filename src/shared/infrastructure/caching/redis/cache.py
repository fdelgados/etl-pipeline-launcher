import redis
from typing import Any
from datetime import timedelta

from shared import settings

from shared.domain.service.caching.cache import Cache


class RedisCache(Cache):
    def __init__(self):
        self.client = redis.Redis(host=settings.redis_host(), port=settings.redis_port())

    def write(self, key: str, value: str) -> None:
        self.client.setex(key, timedelta(days=self.TTL_IN_DAYS), value)

    def read(self, key: str) -> Any:
        return self.client.get(key)
