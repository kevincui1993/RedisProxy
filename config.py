"""
Host that the proxy listens on
"""
HOST = "127.0.0.1"

"""
Port that the proxy listens on
"""
PORT = 8000

"""
Redis Host
"""
REDIS_HOST = "127.0.0.1"

"""
Redis Port
"""
REDIS_PORT = 6379

"""
Global cache expiry time in seconds
"""
CACHE_EXPIRY_SECONDS = 1

"""
How much record can the cache hold
"""
CACHE_CAPACITY = 5

"""
Maximum number of concurrent requests
"""
MAX_CONCURRENCY = 100

"""
Number of active redis connections in the pool
"""
REDIS_CONNECTION_POOL_SIZE = 5
