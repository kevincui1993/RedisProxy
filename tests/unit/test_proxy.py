from unittest.mock import patch, MagicMock

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
