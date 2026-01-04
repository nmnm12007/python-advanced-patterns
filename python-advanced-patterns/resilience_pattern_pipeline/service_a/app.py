from flask import Flask, jsonify
import requests
from resilience_pattern_pipeline.resilience.timeout_resilience import TimeoutErrorExceptionHandler
from resilience_pattern_pipeline.resilience.retry import retry_resilience
from resilience_pattern_pipeline.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerOpen,
    Downstream5xx,
    UserErr,
)

app = Flask(__name__)

cb = CircuitBreaker(failure_threshold=3, recovery_timeout=10)


@cb
@retry_resilience(
    max_retries=3,
    delay=1,
    backoff=2,
    retry_on_exception=(
        TimeoutErrorExceptionHandler,
        Downstream5xx,
        requests.exceptions.RequestException,
    ),
)
def call_service_b():
    """
    call_service_b calls the service
    """
    try:
        resp = requests.get("http://localhost:5001/process", timeout=(1, 2))
    except requests.exceptions.Timeout:
        raise TimeoutErrorExceptionHandler("HTTP Timeout Calling B Service")
    if resp.status_code == 400:  # NEVER RETRY 4xx as it is user behaviour
        # print("[DEBUG] Service B returned:", resp.status_code)
        raise UserErr("400 Bad Request :: User Err")
    if resp.status_code >= 500:
        raise Downstream5xx("5xx from Service B")

    return resp.json()


@app.route("/api")
def api():
    try:
        result = call_service_b()
        return jsonify(result), 200
    except CircuitBreakerOpen as e:
        return jsonify({"error": str(e)}), 503
    except TimeoutErrorExceptionHandler as e:
        return jsonify({"error": str(e)}), 504
    except UserErr as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
