from time import sleep

import requests

import config
from app import app

from redis_proxy.redis_fence import RedisFence


def disable_test_get():
    redis_client = RedisFence("127.0.0.1", 6379).get_client()
    redis_client.delete("test_get")

    with app.test_client() as c:
        res = c.get("get?key=test_get")
        assert res.status_code == 403

        redis_client.set("test_get", "this is a get test")

        res = c.get("get?key=test_get")
        assert res.status_code == 200
        assert res.data == b"this is a get test"


# this requires a running proxy server and backing redis server
def test_end_2_end():
    url = f"http://{config.HOST}:{config.PORT}/get"
    params = {"key": "test_get"}
    redis_client = RedisFence("127.0.0.1", 6379).get_client()
    redis_client.delete("test_get")
    sleep(0.5)

    # sending get request and saving the response as response object
    res = requests.get(url=url, params=params)
    assert res.status_code == 403
    redis_client.set("test_get", "this is a get test")

    sleep(0.5)
    res = requests.get(url=url, params=params)
    assert res.status_code == 200
    assert res.content == b"this is a get test"

    records = [
        ("test_get1", "this is a get test1"),
        ("test_get2", "this is a get test2"),
        ("test_get3", "this is a get test3"),
    ]
    for r in records:
        redis_client.set(r[0], r[1])

    for i in range(100):
        r = records[i % len(records)]
        params["key"] = r[0]
        res = requests.get(url=url, params=params)
        assert res.status_code == 200
        assert res.content == r[1].encode("utf-8")
