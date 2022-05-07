from flask import Flask, request
import config
from constants import Status, RedisKeyNotFound, TooManyRequests
from redis_proxy.proxy import Proxy

app = Flask(__name__)
proxy = Proxy()


@app.route("/get")
def get():
    response, status = "", Status.NOT_FOUND
    try:
        response = proxy.get_record(request.args.get("key"))
        status = Status.OK
    except RedisKeyNotFound:
        response = "key_not_found"
        status = Status.INVALID
    except TooManyRequests:
        response = "too_many_requests"
        status = Status.TOO_MANY_REQUESTS
    except Exception as e:
        response = str(e)
        status = Status.INVALID
    finally:
        return response, status.value[0]


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT)
