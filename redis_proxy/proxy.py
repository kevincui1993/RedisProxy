import logging

import config
from constants import RedisKeyNotFound
from redis_proxy.cache import Cache
from redis_proxy.redis_fence import RedisFence

logger = logging.getLogger()


class Proxy:
    def __init__(self):
        self.redis_host = config.REDIS_HOST
        self.redis_port = config.REDIS_PORT
        self.redis_client = RedisFence(self.redis_host, self.redis_port).get_client()
        self.cache = Cache(config.CACHE_EXPIRY_SECONDS, config.CACHE_CAPACITY)

    def get_record(self, key):
        found, value = self.cache.get(key)
        if found:
            return value
        elif self.redis_client.exists(key):
            value = self.redis_client.get(key)
            self.set_record(key, value)
            return value
        else:
            logger.warning(f"'{key}' does not exist")
            raise RedisKeyNotFound

    def set_record(self, key, value):
        self.cache.set(key, value)
