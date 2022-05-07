import logging
from random import randint

import config
from constants import RedisKeyNotFound
from redis_proxy.cache import Cache
from redis_proxy.redis_fence import RedisFence

logger = logging.getLogger()


class Proxy:
    def __init__(self):
        self.redis_host = config.REDIS_HOST
        self.redis_port = config.REDIS_PORT
        self.redis_client_pool = []
        for _ in range(config.REDIS_CONNECTION_POOL_SIZE):
            self.redis_client_pool.append(RedisFence(self.redis_host, self.redis_port))
        self.cache = Cache(config.CACHE_EXPIRY_SECONDS, config.CACHE_CAPACITY)

    def get_record(self, key):
        found, value = self.cache.get(key)
        redis_client = self.get_client_from_pool()

        if found:
            return value
        elif redis_client.exists(key):
            value = redis_client.get(key)
            self.set_record(key, value)
            return value
        else:
            logger.warning(f"'{key}' does not exist")
            raise RedisKeyNotFound

    def set_record(self, key, value):
        self.cache.set(key, value)

    def get_client_from_pool(self):
        if len(self.redis_client_pool) == 0:
            logger.warning("There is no available redis client from the pool")
            self.redis_client_pool.append(RedisFence(self.redis_host, self.redis_port))

        index = randint(0, len(self.redis_client_pool) - 1)
        return self.redis_client_pool[index].get_client()
