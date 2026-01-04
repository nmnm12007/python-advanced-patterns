from flask import Flask, jsonify
import random

app = Flask(__name__)


@app.route("/process")
def service_b_fluctuate():
    behaviour = random.choice(["slow", "UserErr", "error"])
    if behaviour == "slow":
        return jsonify({"status": "SLOW-Response"}), 200
    if behaviour == "error":
        return jsonify({"status": "ERRONEOUS-Response"}), 500
    if behaviour == "UserErr":
        return jsonify({"status": "USER:ERROR-Response"}), 400
    return jsonify({"status": "OK"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
