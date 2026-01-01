class CircuitOpenException(Exception):
    pass


class CircuitBreaker:
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

    def __init__(self, fail_max=3, reset_timeout=5):
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.fail_count = 0
        self.state = self.CLOSED
        self.opened_at = None

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self._before_call()

            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise
        return wrapper

    def _before_call(self):
        if self.state == self.OPEN:
            if time.time() - self.opened_at >= self.reset_timeout:
                self.state = self.HALF_OPEN
            else:
                raise CircuitOpenException("[CB] Circuit OPEN")

    def _on_success(self):
        self.fail_count = 0
        self.state = self.CLOSED

    def _on_failure(self):
        self.fail_count += 1
        if self.fail_count >= self.fail_max:
            self.state = self.OPEN
            self.opened_at = time.time()
