from flask import Flask
from main_func import safe_call_service_b

app = Flask(__name__)


@app.route("/call_to_b")
def call_b_url():
    body, status = safe_call_service_b("http://localhost:5000/call_to_b")
    return body, status


if __name__ == "__main__":
    app.run(debug=True, port=5000)
