import redis


class RedisFence:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = redis.Redis(host=self.host, port=self.port)

    def get_client(self):
        try:
            self.client.ping()
        except Exception:
            self.client = redis.Redis(host=self.host, port=self.port)
        finally:
            return self.client
