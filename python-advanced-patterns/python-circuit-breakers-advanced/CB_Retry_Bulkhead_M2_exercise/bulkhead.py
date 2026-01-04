import threading


class BulkheadFull(Exception):
    pass


class SemaphoreBulkhead:
    def __init__(self, max_concurrent):
        self.semaphore = threading.BoundedSemaphore(max_concurrent)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            acquired = self.semaphore.acquire(blocking=False)
            if not acquired:
                raise BulkheadFull("Bulkhead limit reached")

            try:
                return func(*args, **kwargs)
            finally:
                self.semaphore.release()

        return wrapper
