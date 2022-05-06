import logging
from threading import BoundedSemaphore
import time

logger = logging.getLogger()


class Cache:
    def __init__(self, timeout, capacity):
        self.capacity = capacity
        self.sem = BoundedSemaphore(1)
        self.timeout = timeout
        self.cache_dict = {}
        self.cache_list = []

    def get(self, key):
        try:
            self.sem.acquire()
            if key in self.cache_dict:
                value, timestamp = self.cache_dict.get(key)
                if self.is_expired(timestamp):
                    self.cache_list.remove(key)
                    del self.cache_dict[key]
                    return False, "expired"
                else:
                    return True, self.cache_dict.get(key)
            else:
                return False, "not_found"
        finally:
            self.sem.release()

    def set(self, key, value):
        try:
            self.sem.acquire()
            while len(self.cache_list) >= self.capacity:
                expired_key = self.cache_list.pop(0)
                if expired_key in self.cache_dict:
                    del self.cache_dict[expired_key]
                else:
                    logger.warning(f"'{expired_key}' does not exist in cache_dict")

            self.cache_list.append(key)
            self.cache_dict[key] = (value, int(time.time()))
        finally:
            self.sem.release()

    def is_expired(self, timestamp):
        diff = int(time.time()) - timestamp
        return diff > self.timeout
