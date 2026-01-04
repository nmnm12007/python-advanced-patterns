from random import random

from flask import Flask
import time

app = Flask(__name__)


@app.route("/call_inside_b")
def call_in_a():
    r = random()

    if r < 0.3:
        time.sleep(2)  # timeout

    elif r < 0.6:
        return "Service B failure", 503

    return "Service B success", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
