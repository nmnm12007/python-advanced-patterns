import logging
import requests

from bulkhead import Bulkhead, BulkheadFull
from circuit_breaker import CircuitOpen, CircuitBreaker
from retry import retry

logging.basicConfig(level=logging.INFO)

bulkhead = Bulkhead(max_concurrency=2)
circuit_breaker = CircuitBreaker(fail_max=2, reset_timeout=5)


@circuit_breaker
@retry(max_attempts=3, retry_on_exceptions=(requests.exceptions.Timeout,), retry_on_status=(503,))
def call_service_b(url: str):
    return requests.get(url, timeout=1)


def safe_call_service_b(url: str):
    try:
        with bulkhead.acquire():
            result = call_service_b(url)
            return result.text, 200

    except BulkheadFull:
        return "Too many requests", 429

    except CircuitOpen:
        return "Service unavailable [Circuit Open]", 503

    except requests.exceptions.HTTPError as e:
        return str(e), 502

    except Exception as e:
        logging.exception(e)
        return "Internal Server Error", 500
