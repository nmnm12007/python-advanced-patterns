import pybreaker
import requests
import logging

from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log

logging.basicConfig(level = logging.INFO,
                    format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
                    )

# ----------------------------
# Circuit Breaker
# ----------------------------
circuit_breaker = pybreaker.CircuitBreaker(fail_max = 3, reset_timeout = 10)


class CBListener(pybreaker.CircuitBreakerListener):
	def state_change(self, cb, old_state, new_state):
		logging.warning(f"CBListener changed state from {old_state} to"
		                f" {new_state}")


circuit_breaker.add_listener(CBListener())


# ------------------
# Retry {inside CB}
# ------------------

@retry(stop = stop_after_attempt(2), wait = wait_fixed(1), before_sleep =
before_sleep_log(logging.getLogger(__name__), logging.WARNING))
@circuit_breaker
def call_service_b():
	logging.info(
			"DEBUG: state=%s | current_state=%s | types=%s %s",
			circuit_breaker.state,
			circuit_breaker.current_state,
			type(circuit_breaker.state),
			type(circuit_breaker.current_state),
			)
	
	logging.info(f"[CALL]: Service B :: http://127.0.0.1:5001/process :: CB "
	             f"State:  " f"%s",
	            circuit_breaker.state.__class__.__name__)
	
	logging.info(
			"[CALL] → Service B | CB State=%s | Fail Counter=%s",
			circuit_breaker.state,
			circuit_breaker.fail_counter,
			)
	
	
	response = requests.get(f"http://127.0.0.1:5001/process", timeout = 2)
	response.raise_for_status()
	return response.text


def safe_call():
	try:
		return call_service_b(), 200
	except pybreaker.CircuitBreakerError:
		logging.error(
				"[FAIL-FAST] Circuit OPEN → Service B NOT called"
				)
		return "Fallback: Service B is down : Circuit is OPEN", 503
	
	except Exception as ex:
		logging.error(
				f"[DOWNSTREAM FAILURE] {ex}"
				)
		return (f"Fallback: Exception: Downstream Failure: due to : {[ex]} "
		        f"\n"), 502
