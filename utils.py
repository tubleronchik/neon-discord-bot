import typing as tp
import asyncio
import functools
import json

def to_thread(func: tp.Callable) -> tp.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

def read_config() -> dict:
    with open("config/config.json") as f:
        config = json.load(f)
    return config