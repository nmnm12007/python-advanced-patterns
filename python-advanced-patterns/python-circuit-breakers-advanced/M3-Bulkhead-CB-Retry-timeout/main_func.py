import time

from bulkhead import Bulkhead
from circuit_breaker import CircuitBreaker
from retry import Retry
from timeout import Timeout


def call_f():
    print("call_f")
    time.sleep(3)
    return "OK"


bulkhead = Bulkhead(1)
circuit_breaker = CircuitBreaker(3, 5)
retry = Retry(2, (1,))
timeout = Timeout(2)


@retry
@circuit_breaker
def protected_call_f():
    print("protected_call_f")
    return timeout.run_timeout(call_f)


def main_func():
    with bulkhead.acquire():
        return protected_call_f()


if __name__ == "__main__":
    try:
        print(main_func())
    except Exception as e:
        print("Exception:", e)
