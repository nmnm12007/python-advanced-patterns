from flask import Flask, Response
from circuit_breaker import safe_call
import logging

app = Flask(__name__)
logger = logging.getLogger("service-a")
logger.setLevel(logging.INFO)

# logger.info("Service A started")
logging.basicConfig(
    level=logging.INFO,
    filename="service_a.log",
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(message)s",
)


@app.route("/call")
def call():
    result, status = safe_call()
    return Response(response=str(result), status=status)


if __name__ == "__main__":
    app.run(port=5000, debug=False, use_reloader=False)
