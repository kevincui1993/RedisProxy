from unittest.mock import patch, MagicMock

import redis

from constants import RedisKeyNotFound
from redis_proxy.proxy import Proxy


@patch("redis.Redis")
def test_get_record_not_found(mock_redis):
    mock_redis_conn = MagicMock()
    mock_redis_conn.exists.return_value = False
    mock_redis.return_value = mock_redis_conn

    try:
        Proxy().get_record("test")
        raise False
    except RedisKeyNotFound:
        assert True
    except Exception:
        assert False


@patch("redis.Redis")
def test_get_record_from_redis_and_cache(mock_redis):
    mock_redis_conn = MagicMock()
    mock_redis_conn.exists.return_value = True
    mock_redis_conn.get.return_value = "some value"
    mock_redis.return_value = mock_redis_conn
    proxy = Proxy()

    assert mock_redis_conn.get.call_count == 0
    res = proxy.get_record("test")
    assert mock_redis_conn.get.call_count == 1
    cache = proxy.get_record("test")
    assert mock_redis_conn.get.call_count == 1
    assert res == "some value"
    assert res == cache


@patch("redis.Redis")
def test_set_record(mock_redis):
    mock_redis_conn = MagicMock()
    mock_redis_conn.exists.return_value = True
    mock_redis.return_value = mock_redis_conn
    proxy = Proxy()

    proxy.set_record("test", "some value")
    res = proxy.get_record("test")

    assert res == "some value"
    assert mock_redis_conn.exists.call_count == 0


@patch("redis.Redis")
def test_rety_on_redis_get(mock_redis):
    mock_redis_conn = MagicMock()
    mock_redis_conn.get.side_effect = redis.ConnectionError(
        "Connection to Redis failed"
    )
    mock_redis.return_value = mock_redis_conn

    try:
        proxy = Proxy()
        proxy.redis_get(proxy.get_client_from_pool(), "key")
        assert AssertionError()
    except redis.ConnectionError:
        assert mock_redis_conn.get.call_count == 3


@patch("redis.Redis")
def test_rety_on_redis_exist(mock_redis):
    mock_redis_conn = MagicMock()
    mock_redis_conn.exist.side_effect = redis.ConnectionError(
        "Connection to Redis failed"
    )
    mock_redis.return_value = mock_redis_conn

    try:
        proxy = Proxy()
        proxy.redis_exists(proxy.get_client_from_pool(), "key")
        assert AssertionError()
    except redis.ConnectionError:
        assert mock_redis_conn.get.call_count == 3
