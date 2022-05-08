import logging
from threading import BoundedSemaphore
import time

logger = logging.getLogger()


class CacheNode:
    def __init__(self, key, value, timestamp):
        self.key = key
        self.value = value
        self.timestamp = timestamp
        self.next = None
        self.prev = None

    def __lt__(self, other):
        return self.timestamp < other.timestamp


class DoubleLinkedList:
    def __init__(self):
        self.root = CacheNode(None, None, None)
        self.capacity = 0
        self.root.next = self.root
        self.root.prev = self.root

    def insert_front(self, node):
        if node is None:
            return None
        self.move_front(node)
        self.capacity += 1
        return node

    def move_front(self, node):
        if node is None:
            return None
        elif node.prev is not None and node.next is not None:
            self.pop(node)

        node.prev = self.root
        node.next = self.root.next

        self.root.next.prev = node
        self.root.next = node
        return node

    def remove_tail(self):
        if self.capacity == 0:
            return None

        removed = self.pop(self.root.prev)
        self.capacity -= 1
        return removed

    def remove(self, node):
        removed = self.pop(node)
        self.capacity -= 1
        return removed

    def pop(self, node):
        node.next.prev = node.prev
        node.prev.next = node.next
        node.next = None
        node.prev = None
        return node


class Cache:
    def __init__(self, timeout, capacity):
        self.capacity = capacity
        self.sem = BoundedSemaphore(1)
        self.timeout = timeout
        self.cache_dict = {}
        self.cache_list = DoubleLinkedList()

    def get(self, key):
        try:
            self.sem.acquire()
            if key in self.cache_dict:
                cache_node = self.cache_dict.get(key)
                if self.is_expired(cache_node.timestamp):
                    self.cache_list.remove(cache_node)
                    del self.cache_dict[key]
                    return False, "expired"
                else:
                    self.cache_list.move_front(cache_node)
                    return True, cache_node.value
            else:
                return False, "not_found"
        finally:
            self.sem.release()

    def set(self, key, value):
        try:
            self.sem.acquire()
            if key in self.cache_dict:
                # if key already exists, update the value and move to front
                node = self.cache_dict[key]
                node.value = value
                self.cache_list.move_front(node)
                return

            if self.cache_list.capacity >= self.capacity:
                # remove the least recent used cache entry
                removed_cache_node = self.cache_list.remove_tail()
                if removed_cache_node.key in self.cache_dict:
                    del self.cache_dict[removed_cache_node.key]
                else:
                    logger.warning(
                        f"'{removed_cache_node.key}' does not exist in cache_dict"
                    )

            node = CacheNode(key, value, int(time.time()))
            self.cache_list.insert_front(node)
            self.cache_dict[key] = node
        finally:
            self.sem.release()

    def is_expired(self, timestamp):
        diff = int(time.time()) - timestamp
        return diff > self.timeout
