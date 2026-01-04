import pybreaker
import logging
import requests
from pybreaker import CircuitBreaker, CircuitBreakerState
from requests.exceptions import RetryError

from tenacity import stop_after_attempt, wait_fixed, before_sleep_log, retry

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s || %(name)s || %(levelname)s || %(message)s"
)

circuit_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=10)


class CBListener(pybreaker.CircuitBreakerListener):
    def state_change(
        self,
        cb: CircuitBreaker,
        old_state: CircuitBreakerState | None,
        new_state: CircuitBreakerState,
    ) -> None:
        logging.debug(f"CBListener.state_change({old_state}, ->   {new_state})")


circuit_breaker.add_listener(CBListener())


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(3),
    before_sleep=before_sleep_log(logging.getLogger(), logging.DEBUG),
)
@circuit_breaker
def call_service_b():
    logging.debug("call_service_b()")

    outcome = requests.get("http://127.0.0.1:5001/calling_service_b")
    outcome.raise_for_status()
    print(outcome.json())
    logging.info(
        "[INFO]: In call_service_b()",
        "old state %s :: ->  current state  ::  RESULT : %s ",
        circuit_breaker.state,
        circuit_breaker.current_state,
        outcome.text,
    )
    return outcome.text


def safe_call_service_b():
    logging.debug("safe_call_service_b()")
    try:
        return call_service_b(), 200
    except pybreaker.CircuitBreakerError as e:
        logging.error(" [FAIL-FAST] Circuit OPEN for Service B ")
        return e, 503
    except RetryError as e:
        logging.error(" [FAIL-RETRY] Retry for Service B ")
        return e, 503
    except Exception as e:
        logging.error("[FAIL-FAST] :: Exception occurred in calling Service B :: %s ", e)
        return e, 502
