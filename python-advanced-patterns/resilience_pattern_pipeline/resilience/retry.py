import time
from functools import wraps
from typing import Tuple, Type


def retry_resilience(
    max_retries: int = 3,
    backoff: float = 2.0,
    delay: float = 1.0,
    retry_on_exception: Tuple[Type[Exception], ...] = (Exception,),
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry = 0
            curr_delay = delay
            while retry <= max_retries:
                try:
                    return func(*args, **kwargs)
                except retry_on_exception as e:
                    print(f"[RETRY] :: Attempt {retry} failed due to Exception {e}")
                    retry += 1
                    curr_delay *= backoff
                    time.sleep(curr_delay)

            if retry > max_retries:
                print(f"[RETRY] :: All Retry Attempts Failed. for {func.__name__}")
            raise

        return wrapper

    return decorator
