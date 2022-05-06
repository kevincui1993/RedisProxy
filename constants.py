from enum import Enum


class Status(Enum):
    OK = (200,)
    INVALID = (403,)
    NOT_FOUND = 404


class RedisKeyNotFound(Exception):
    pass
