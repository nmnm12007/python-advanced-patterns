import logging

from requests.exceptions import RetryError

import retry
import pybreaker
from pybreaker import CircuitBreakerState
import requests

logging.basicConfig(level=logging.DEBUG)

circuit_breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=5)


class CBListener(pybreaker.CircuitBreakerListener):
    def state_change(
        self,
        cb: pybreaker.CircuitBreaker,
        old_state: CircuitBreakerState | None,
        new_state: CircuitBreakerState,
    ) -> None:
        logging.debug(f"CBListener.state_change({old_state}, ->   {new_state})")


circuit_breaker.add_listener(CBListener())


# @bulkhead
@circuit_breaker
@retry.retry_cb(
    3, 0.1, (ConnectionError, TimeoutError, RetryError), True, (500, 503, 504, 505, 506)
)
def call_service_b(url_str: str):
    logging.debug("call_service_b: Request={}".format(url_str))
    result = requests.get(url_str)
    result.raise_for_status()
    logging.debug("call_service_b: result={}".format(result))
