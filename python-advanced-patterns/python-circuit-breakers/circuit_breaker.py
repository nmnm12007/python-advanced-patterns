import pybreaker
import requests
import logging
from tenacity import retry, stop_after_attempt


logging.basicConfig(level = logging.INFO)

circuit_breaker = pybreaker.CircuitBreaker(
		fail_max = 3,
		reset_timeout = 10
		)

@retry(stop = stop_after_attempt(2))
@circuit_breaker
def call_service_b():
	logging.info(
			f"[CB STATE - BEFORE CALL] {circuit_breaker.current_state}"
			)
	
	response = requests.get(
			"http://localhost:5001/process", timeout = 2
			)
	response.raise_for_status()
	
	logging.info(
			f"[CB STATE - AFTER CALL] {circuit_breaker.current_state}"
			)
	return response.text


def safe_call():
	try:
		return call_service_b(), 200

	except pybreaker.CircuitBreakerError:
		# Circuit is OPEN — service B NOT called
		return "Fallback: CIRCUIT OPEN (fail-fast)",503

	except Exception as ex:
		# Service B was called and failed
		return f"Fallback: DOWNSTREAM FAILURE ({ex})", 502


class CBListener(pybreaker.CircuitBreakerListener):
	def state_change(self, cb, old_state, new_state):
		logging.warning(
				f"🔥 CB TRANSITION: {old_state} → {new_state}"
				)
		
circuit_breaker.add_listener(CBListener())


# import pybreaker
# import requests
#
# circuit_breaker = pybreaker.CircuitBreaker(fail_max = 3, reset_timeout = 10)
#
# @circuit_breaker
# def call_service_b():
# 	response = requests.get('http://127.0.0.1:5000/process', timeout = 2)
# 	response.raise_for_status()
# 	return response.text
#
#
# def safe_call():
# 	try:
# 		return call_service_b()
# 	except pybreaker.CircuitBreakerError:
# 		return "Fallback: Service B is not available"
# 	except Exception as e:
# 		return f"Fallback: {e}"


#
# def safe_call():
# 	try:
# 		result = call_service_b()
# 		logging.info(
# 				f"[CB STATE - SUCCESS] {circuit_breaker.current_state}"
# 				)
# 		return result
#
# 	except pybreaker.CircuitBreakerError:
# 		logging.error(
# 				f"[CB STATE - OPEN] {circuit_breaker.current_state}"
# 				)
# 		return "Fallback: Circuit is OPEN"
#
# 	except Exception as ex:
# 		logging.error(
# 				f"[CB STATE - FAILURE] {circuit_breaker.current_state}"
# 				)
# 		return f"Fallback: {ex}"
