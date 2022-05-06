import time
from time import sleep

import pytest
from redis_proxy.cache import Cache


@pytest.fixture(autouse=True)
def cache():
    return Cache(timeout=2, capacity=2)


def test_set_get(cache):
    assert cache.sem._value == 1
    cache.set("test", "this is a test")
    found, detail = cache.get("test")

    assert cache.sem._value == 1
    assert found is True
    assert detail[0] == "this is a test"


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


def test_is_expired_true(cache):
    res = cache.is_expired(time.time() - cache.timeout - 1)
    assert res is True


def test_is_expired_false(cache):
    res = cache.is_expired(time.time())
    assert res is False
