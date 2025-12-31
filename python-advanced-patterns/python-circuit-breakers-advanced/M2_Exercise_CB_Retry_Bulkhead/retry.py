import time, logging, functools


class RetryExhaustedException(Exception):
    pass


def retry(max_attempts=3, delays=(0.1, 0.3),
          retry_on_exceptions=(), retry_on_status=()):
    """
    Stateless retry decorator
    Does NOT decide HTTP response code.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    logging.info("Retrying (attempt #%d): %s", attempt, last_exc)
                    result = func(*args, **kwargs)

                    if hasattr(result, 'status_code') and \
                            result.status_code in retry_on_status:
                                raise RuntimeError(f"Retrying HTTP code {result.status_code}")

                    return result
                except retry_on_exceptions as e:
                    last_exc = e
                    logging.warning("Retrying (attempt #%d): "
                                    "%s", attempt, last_exc)
                except RuntimeError as e:
                    last_exc = e
                    logging.warning("Retrying (attempt #%d): "
                                    "Exception: %s", attempt, last_exc)

                if attempt < max_attempts:
                    delay = delays[min(attempt -1, len(delays) - 1)]
                    time.sleep(delay)

            raise RetryExhaustedException(" Retry Attempts Exhausted") from last_exc
        return wrapper
    return decorator




