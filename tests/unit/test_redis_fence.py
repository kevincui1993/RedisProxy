from unittest.mock import patch

from redis_proxy.redis_fence import RedisFence


@patch("redis.Redis")
def test_get_client(mock_redis):
    RedisFence("127.0.0.1", 6739).get_client()
    assert mock_redis.call_count == 1
