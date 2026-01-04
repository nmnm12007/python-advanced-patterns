import time
import logging


class CircuitOpen(Exception):
    pass


class CircuitBreaker:
    def __init__(self, fail_max=2, reset_timeout=5):
        self._fail_max = fail_max
        self._reset_timeout = reset_timeout
        self.fail_count = 0
        self.state = "CLOSED"
        self.opened_at = None

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if self.state == "OPEN":
                if time.time() - self.opened_at >= self._reset_timeout:
                    self.state = "HALF OPEN"
                    logging.info("[CB] HALF_OPEN")
                else:
                    logging.error("[CB] OPEN - fail fast")
                    raise CircuitOpen("Circuit is OPEN")

            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception:
                self._on_failure()
                raise

        return wrapper

    def _on_success(self):
        self.fail_count = 0
        self.state = "CLOSED"

    def _on_failure(self):
        self.fail_count += 1
        logging.warning(f"[CB] Failure: {self.fail_count} fail fast")
        if self.fail_count >= self._fail_max:
            self.state = "OPEN"
            self.opened_at = time.time()
            logging.error(f"[CB] Circuit OPENED :: Failure: {self.fail_count} fail fast")
