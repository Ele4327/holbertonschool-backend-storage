#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance
of the Redis client as a private variable named _redis
(using redis.Redis()) and flush the instance using flushdb.
"""
from typing import Any, Optional, Callable, Union
import redis
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Counts the number of times a function is called."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ Wrapper function for the method. """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return(wrapper)


def call_history(method: Callable) -> Callable:
    """ Returns a list of all the calls made to a function. """
    inputs_list = method.__qualname__ + ":inputs"
    outputs_list = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args) -> bytes:
        """ Wrapper function for the method. """
        self._redis.rpush(inputs_list, str(args))
        output_value = method(self, *args)
        self._redis.rpush(outputs_list, output_value)
        return output_value
    return(wrapper)


def replay(method: Callable) -> None:
    """ Replays the calls made to a function. """
    redis = method.__self__._redis
    qual_name = method.__qualname__
    calls_value = redis.get(qual_name).decode("utf-8")
    print("{} was called {} times:".format(qual_name, calls_value))
    inputs = qual_name + ":inputs"
    outputs = qual_name + ":outputs"
    inputs_lists = redis.lrange(inputs, 0, -1)
    outputs_lists = redis.lrange(outputs, 0, -1)
    zip_list = list(zip(inputs_lists, outputs_lists))
    for key_value, value in zip_list:
        key_value = key_value.decode("utf-8")
        value = value.decode("utf-8")
        print("{}(*{}) -> {}".format(qual_name, key_value, value))


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
