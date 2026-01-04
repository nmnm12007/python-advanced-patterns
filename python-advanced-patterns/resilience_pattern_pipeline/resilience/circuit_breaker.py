import time
from enum import Enum
from functools import wraps


class UserErr(Exception):
    pass


class Downstream5xx(Exception):
    pass


class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreakerOpen(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 5.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.circuit_state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # ---- OPEN STATE ----
            if self.circuit_state == CircuitState.OPEN:
                elapsed = time.time() - self.last_failure_time
                if elapsed >= self.recovery_timeout:
                    self.circuit_state = CircuitState.HALF_OPEN
                    print("[CB] State transition OPEN → HALF_OPEN")
                else:
                    raise CircuitBreakerOpen(f"[CB] OPEN — calls blocked to {func.__name__}")

            try:
                result = func(*args, **kwargs)
            except UserErr as e:
                raise e
            except Exception:  # includes the Dowsstream5xx
                self._on_failure(func)
                raise

            else:
                self._on_success(func)
                return result

        return wrapper

    def _on_failure(self, func):
        self.failure_count += 1
        self.last_failure_time = time.time()

        print(f"[CB] Failure calling {func.__name__} (count={self.failure_count})")

        if self.failure_count >= self.failure_threshold:
            if self.circuit_state != CircuitState.OPEN:
                print("[CB] State transition → OPEN")
            self.circuit_state = CircuitState.OPEN

    def _on_success(self, func):
        if self.circuit_state == CircuitState.HALF_OPEN:
            print("[CB] State transition HALF_OPEN → CLOSED")

        self.failure_count = 0
        self.circuit_state = CircuitState.CLOSED
