from time import sleep
import functools
from utils.config_loader import RETRY  # make sure this file exists

def retry_robot(max_attempts=RETRY, wait=1):
    """Decorator to retry Python functions called from Robot Framework."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"[Attempt {attempt}] Running {func.__name__}")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[Attempt {attempt}] Failed: {e}")
                    if attempt == max_attempts:
                        raise
                    sleep(wait)
        return wrapper
    return decorator
