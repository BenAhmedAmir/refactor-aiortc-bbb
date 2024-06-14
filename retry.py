import asyncio
import logging
import random


def retry(retries=5, delay=1, backoff=2, exceptions=(Exception,), logger=None):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            _retries, _delay = retries, delay
            while _retries > 0:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    _retries -= 1
                    if logger:
                        logger.warning(
                            f"{func.__name__} failed with {e}, {_retries} retries left, retrying in {_delay} seconds...")
                    await asyncio.sleep(_delay)
                    _delay *= backoff
            raise Exception(f"{func.__name__} failed after {retries} retries")

        return wrapper

    return decorator
