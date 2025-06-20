# cache.py
import logging
from datetime import datetime, timedelta
from functools import wraps

logger = logging.getLogger("cache")

class TTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl   = timedelta(seconds=ttl_seconds)
        self.store : dict = {}
        self.hits  = 0
        self.misses = 0

    def __call__(self, fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            key = (fn.__name__, args, frozenset(kwargs.items()))
            entry = self.store.get(key)
            now = datetime.utcnow()
            if entry and now - entry[0] < self.ttl:
                self.hits += 1
                logger.debug(f"CACHE HIT {fn.__name__} key={key} (hits={self.hits})")
                return entry[1]
            # cache miss
            self.misses += 1
            logger.debug(f"CACHE MISS {fn.__name__} key={key} (misses={self.misses})")
            result = fn(*args, **kwargs)
            self.store[key] = (now, result)
            return result
        return wrapped
# instances
stock_cache   = TTLCache(ttl_seconds=30)
reports_cache = TTLCache(ttl_seconds=30)