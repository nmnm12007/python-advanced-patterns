import concurrent
from functools import wraps

""" Timeout class implementation using ThreadPoolExecutor """


class TimeoutErrorExceptionHandler(Exception):
    pass


def timeout(time_duration: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future_1 = executor.submit(func, *args, **kwargs)
                try:
                    return future_1.result(timeout=time_duration)
                except concurrent.futures.TimeoutError:
                    raise TimeoutErrorExceptionHandler(
                        f"[TIMEOUT] :: Timed out waiting for {func.__name__} to complete.    "
                    )
                except Exception as exc:
                    raise Exception(
                        f"Error occurred while waiting for {func.__name__} to complete. ::  {exc}"
                    )

        return wrapper

    return decorator
