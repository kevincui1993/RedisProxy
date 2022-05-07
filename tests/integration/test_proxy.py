from config import REDIS_CONNECTION_POOL_SIZE
from redis_proxy.proxy import Proxy


def test_get_client_from_pool():
    proxy = Proxy()
    assert len(proxy.redis_client_pool) == REDIS_CONNECTION_POOL_SIZE

    client1 = proxy.get_client_from_pool()

    for i in range(10):
        client2 = proxy.get_client_from_pool()
        if client2 != client1:
            return

    assert False
