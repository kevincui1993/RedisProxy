import redis


class RedisFence:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = redis.Redis(host=self.host, port=self.port)

    def get_client(self):
        return self.client
