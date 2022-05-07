from enum import Enum


class Status(Enum):
    OK = (200,)
    INVALID = (403,)
    NOT_FOUND = (404,)
    TOO_MANY_REQUESTS = (429,)


class RedisKeyNotFound(Exception):
    pass


class TooManyRequests(Exception):
    pass
