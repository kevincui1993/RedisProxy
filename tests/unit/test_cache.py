import time
from time import sleep

import pytest
from redis_proxy.cache import Cache, DoubleLinkedList, CacheNode


@pytest.fixture(autouse=True)
def cache():
    return Cache(timeout=2, capacity=2)


def test_set_get(cache):
    assert cache.sem._value == 1
    cache.set("test", "this is a test")
    found, detail = cache.get("test")

    assert cache.sem._value == 1
    assert found is True
    assert detail == "this is a test"


def test_get_not_found(cache):
    found, detail = cache.get("test")

    assert found is False
    assert detail == "not_found"


def test_get_expired(cache):
    cache.set("test", "this is a test")
    sleep(3)
    found, detail = cache.get("test")

    assert found is False
    assert detail == "expired"


def test_set_over_capacity(cache):
    cache.set("test1", "this is test one")
    cache.set("test2", "this is test two")
    cache.set("test3", "this is test three")

    assert cache.get("test1")[0] is False
    assert cache.get("test2")[0] is True
    assert cache.get("test3")[0] is True


def test_remove_lru(cache):
    cache.set("test1", "this is test one")
    cache.set("test2", "this is test two")
    cache.get("test1")
    cache.set("test3", "this is test three")

    assert cache.get("test1")[0] is True
    assert cache.get("test2")[0] is False
    assert cache.get("test3")[0] is True


def test_is_expired_true(cache):
    res = cache.is_expired(time.time() - cache.timeout - 1)
    assert res is True


def test_is_expired_false(cache):
    res = cache.is_expired(time.time())
    assert res is False


def test_insert_front():
    linked_list = DoubleLinkedList()
    node = CacheNode("test", "this is a test", 123)
    linked_list.insert_front(node)
    assert linked_list.root.next is node


def test_move_front():
    linked_list = DoubleLinkedList()
    node1 = CacheNode("test", "this is a test", 123)
    node2 = CacheNode("test2", "this is second test", 456)

    linked_list.insert_front(node1)
    linked_list.insert_front(node2)
    linked_list.move_front(node1)
    assert linked_list.root.next is node1
    assert linked_list.root.next.next is node2


def test_remove_tail():
    linked_list = DoubleLinkedList()
    node1 = CacheNode("test", "this is a test", 123)
    node2 = CacheNode("test2", "this is second test", 456)

    linked_list.insert_front(node1)
    linked_list.insert_front(node2)
    removed_node = linked_list.remove_tail()

    assert removed_node is node1
    assert linked_list.capacity == 1
