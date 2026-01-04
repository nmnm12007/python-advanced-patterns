from flask import Flask
import time

app = Flask(__name__)

counter = 0


@app.route("/process")
def process():
    global counter
    counter += 1

    print(f" service B is called :: time counter :: [{counter}]")

    # First 2 calls → slow (timeout)
    if counter <= 2:
        time.sleep(3)
        return "Service B  ::  too Slow", 200
    # Next 2 calls → failure
    if counter <= 6:
        return "Service B :: Failure", 500

    # then simulate recovered
    return "Service B : success", 200


if __name__ == "__main__":
    app.run(port=5001, debug=False, use_reloader=False)
