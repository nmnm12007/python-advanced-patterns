import threading, logging

from contextlib import contextmanager

class BulkheadFull(Exception):
    """ Raised when bulkhead is full"""
    pass

class Bulkhead:
    def __init__(self, max_concurrency:int):
        self._semaphore = threading.Semaphore(max_concurrency)

    @contextmanager
    def acquire(self):
        acquire_yes = self._semaphore.acquire(blocking=False)
        if not acquire_yes:
            logging.error("[Bulkhead]:: Limit Exceeded. Bulkhead acquire failed")
            raise BulkheadFull("Limit Exceeded. Bulkhead acquire failed")
        try:
            yield
        finally:
            self._semaphore.release()

            