import logging
from threading import BoundedSemaphore
import time
from heapq import heapify, heappush, heappop

logger = logging.getLogger()


class CacheRecord:
    def __init__(self, value, timestamp):
        self.value = value
        self.timestamp = timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp


class Cache:
    def __init__(self, timeout, capacity):
        self.capacity = capacity
        self.sem = BoundedSemaphore(1)
        self.timeout = timeout
        self.cache_dict = {}
        self.cache_heap = []
        heapify(self.cache_heap)

    def get(self, key):
        try:
            self.sem.acquire()
            if key in self.cache_dict:
                cache_record = self.cache_dict.get(key)
                if self.is_expired(cache_record.timestamp):
                    del self.cache_dict[key]
                    return False, "expired"
                else:
                    return True, cache_record.value
            else:
                return False, "not_found"
        finally:
            self.sem.release()

    def set(self, key, value):
        try:
            self.sem.acquire()
            if len(self.cache_heap) >= self.capacity:
                expired_key = heappop(self.cache_heap)
                if expired_key in self.cache_dict:
                    del self.cache_dict[expired_key]
                else:
                    logger.warning(f"'{expired_key}' does not exist in cache_dict")

            heappush(self.cache_heap, key)
            self.cache_dict[key] = CacheRecord(value, int(time.time()))
        finally:
            self.sem.release()

    def is_expired(self, timestamp):
        diff = int(time.time()) - timestamp
        return diff > self.timeout
