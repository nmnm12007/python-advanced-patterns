import logging
import threading
from contextlib import contextmanager


class BulkheadException(Exception):
    pass


class Bulkhead:
    def __init__(self, max_concurrency):
        if max_concurrency <= 0:
            raise ValueError("[BULKHEAD]:: max_concurrency < 1 ")
        self._bulkhead_semaphore = threading.Semaphore(max_concurrency)

    @contextmanager
    def acquire(self):
        acquired_yes = self._bulkhead_semaphore.acquire(blocking=False)

        if not acquired_yes:
            logging.error("[BULKHEAD] :: Bulkhead Limit Exceeded")
            raise BulkheadException("[BULKHEAD] :: Bulkhead Limit Exceeded")
        else:
            logging.info("[BULKHEAD] :: Bulkhead Semaphore acquired")
        try:
            yield
        # except Exception as e:  NEVER catch a downstream exception here
        finally:
            self._bulkhead_semaphore.release()
            logging.info("[BULKHEAD] :: Bulkhead Semaphore released")
