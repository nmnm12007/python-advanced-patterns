import logging

from flask import Flask, Response
import cb

app = Flask(__name__)


@app.route("/call_b_from_a")
def call_b_from_a():
    logging.info("[Service A] : call_b_from_a")

    outcome_a, status = cb.safe_call_service_b()
    logging.info("[Service A] : outcome_a = %s  status = %s", outcome_a, status)
    print(f"[Service A] : outcome_a = {outcome_a} , Status = {status}")

    return Response(response=outcome_a, status=status)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
