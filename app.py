from flask import Flask, request

from constants import Status, RedisKeyNotFound
from redis_proxy.proxy import Proxy

app = Flask(__name__)
proxy = None


@app.route("/get")
def result():
    response, status = "", Status.NOT_FOUND
    try:
        response = proxy.get_record(request.args.get("key"))
        status = Status.OK
    except RedisKeyNotFound:
        response = "key_not_found"
        status = Status.INVALID
    finally:
        return response, status


if __name__ == "__main__":
    proxy = Proxy()
    app.run(host="localhost", port=8000, debug=True)
