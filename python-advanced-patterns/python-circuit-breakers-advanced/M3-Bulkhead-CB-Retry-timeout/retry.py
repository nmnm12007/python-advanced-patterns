import functools
import time


class RetryExhaustedException(Exception):
    pass


class Retry:
    def __init__(self, max_attempts=3, delays=(0.1, 0.3)):
        self.max_attempts = max_attempts
        self.delays = delays

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, self.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt == self.max_attempts:
                        break
                    time.sleep(self.delays[min(attempt - 1, len(self.delays) - 1)])
            raise RetryExhaustedException(
                "[RETRY] Attempts exhausted"
            ) from last_exc

        return wrapper
