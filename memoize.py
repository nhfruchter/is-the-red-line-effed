from decorator import decorator
from time import time

# From Sean Blanchfield: http://seanblanchfield.com/python-memoize-with-expiry/
def memoize_with_expiry(expiry_time=0, _cache=None, num_args=None):
    def _memoize_with_expiry(func, *args, **kw):
        # Determine what cache to use - the supplied one, or one we create inside the
        # wrapped function.
        if _cache is None and not hasattr(func, '_cache'):
            func._cache = {}
        cache = _cache or func._cache
        
        mem_args = args[:num_args]
        # frozenset is used to ensure hashability
        if kw: 
            key = mem_args, frozenset(kw.iteritems())
        else:
            key = mem_args
        if key in cache:
            result, timestamp = cache[key]
            # Check the age.
            age = time() - timestamp
            if not expiry_time or age < expiry_time:
                return result
        result = func(*args, **kw)
        cache[key] = (result, time())
        return result
    return decorator(_memoize_with_expiry)
