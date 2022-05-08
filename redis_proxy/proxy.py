import logging
from random import randint

import backoff
import redis

import config
from constants import RedisKeyNotFound, TooManyRequests
from redis_proxy.cache import Cache
from redis_proxy.redis_fence import RedisFence

logger = logging.getLogger()


class Proxy:
    def __init__(self):
        self.redis_host = config.REDIS_HOST
        self.redis_port = config.REDIS_PORT

        # create a pool of redis connections to reuse
        self.redis_client_pool = []
        for _ in range(config.REDIS_CONNECTION_POOL_SIZE):
            self.redis_client_pool.append(RedisFence(self.redis_host, self.redis_port))

        self.cache = Cache(config.CACHE_EXPIRY_SECONDS, config.CACHE_CAPACITY)
        self.concurrency_count = 0

    def get_record(self, key):
        if self.is_too_many_requests():
            raise TooManyRequests

        try:
            self.concurrency_count += 1
            found, value = self.cache.get(key)
            redis_client = self.get_client_from_pool()

            if found:
                logger.info(f"Found record from cache: ({key}, {value}")
                return value
            elif self.redis_exists(redis_client, key):
                value = self.redis_get(redis_client, key)
                self.set_record(key, value)
                logger.info(f"Retrieved record from redis: ({key}, {value}")
                return value
            else:
                logger.warning(f"'{key}' does not exist")
                raise RedisKeyNotFound
        finally:
            self.concurrency_count -= 1

    def set_record(self, key, value):
        self.cache.set(key, value)

    def get_client_from_pool(self):
        if len(self.redis_client_pool) == 0:
            logger.warning("There is no available redis client from the pool")
            self.redis_client_pool.append(RedisFence(self.redis_host, self.redis_port))

        index = randint(0, len(self.redis_client_pool) - 1)
        return self.redis_client_pool[index]

    @backoff.on_exception(
        backoff.expo,
        (
            redis.exceptions.ConnectionError,
            redis.exceptions.TimeoutError,
            redis.exceptions.RedisError,
        ),
        max_tries=3,
        max_time=3,
    )
    def redis_exists(self, redis_client, key):
        return redis_client.get_client().exists(key)

    @backoff.on_exception(
        backoff.expo,
        (
            redis.exceptions.ConnectionError,
            redis.exceptions.TimeoutError,
            redis.exceptions.RedisError,
        ),
        max_tries=3,
        max_time=3,
    )
    def redis_get(self, redis_client, key):
        return redis_client.get_client().get(key)

    def is_too_many_requests(self):
        return self.concurrency_count > config.MAX_CONCURRENCY
