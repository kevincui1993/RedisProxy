from app import app
from redis_proxy.redis_fence import RedisFence


def test_get():
    redis_client = RedisFence("127.0.0.1", 6379).get_client()
    redis_client.delete("test_get")

    with app.test_client() as c:
        res = c.get("get?key=test_get")
        assert res.status_code == 403

        redis_client.set("test_get", "this is a get test")

        res = c.get("get?key=test_get")
        assert res.status_code == 200
        assert res.data == b"this is a get test"
