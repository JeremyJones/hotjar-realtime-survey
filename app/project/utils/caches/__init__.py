from . import redis

def cached_or_cache(func):
    """If we have a cached version of the function then return
    that. Otherwise run the function and cache it.
    """
    def wrapper():
        func()
