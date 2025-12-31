import pybreaker
import requests

import logging, circuit_breaker


def safe_call_in_cb(url_str: str):
    logging.debug("safe_call_in_cb()")
    try:
        circuit_breaker.call_service_b(url_str)
        logging.debug("safe_call_in_cb: success")
        return "Success", 200
    except pybreaker.CircuitBreakerError as e:
        logging.debug("[FAIL-FAST] :: safe_call_in_cb: e={}".format(e))
        return "Fail with 503", 503
    except requests.exceptions.ConnectionError as e:
        logging.debug("[ERROR] :: safe_call_in_cb: e={}".format(e))
        return "Fail with 500", 503
    except Exception as e:
        logging.debug("[ERROR] :: safe_call_in_cb: e={}".format(e))
        return "Fail with 500", 503


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
