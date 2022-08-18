#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance
of the Redis client as a private variable named _redis
(using redis.Redis()) and flush the instance using flushdb.
"""
from typing import Any, Optional, Callable, Union
import redis
import uuid


class Cache:
    """Create a store method that takes a data
    argument and returns a string. The method should
    generate a random key (e.g. using uuid), store the
    input data in Redis using the random key
    and return the key.

    Type-annotate store correctly. Remember that data can
    be a str, bytes, int or float."""

    def __init__(self):
        """Initialize a Redis client and flush it."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data) -> Any[str, bytes, int, float]:
        """Store data in Redis and return the key."""
        key_value = str(uuid.uuid4())
        self._redis.set(key_value, data)
        return(key_value)

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Get data from Redis and return it. If the data is not found,"""
        data_value = self._redis.get(key)
        return fn(data_value) if fn else data_value

    def get_str(self, key: str) -> str:
        """Get str data from Redis and return it."""
        data_value = self._redis.get(key)
        return data_value.decode("utf-8") if data_value is not None else None

    def get_int(self, key: str) -> int:
        """Get int data from Redis and return it."""
        data_value = self._redis.get(key)
        return (int(data_value.decode("utf-8"))
                if data_value is not None else None)
