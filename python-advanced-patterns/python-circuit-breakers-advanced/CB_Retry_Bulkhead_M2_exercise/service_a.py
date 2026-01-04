import main_func

from flask import Flask

app = Flask(__name__)


@app.route("/call_to_b_fr_a")
def call():
    # call safe_call_to_b_fr_a from cb
    main_func.safe_call_in_cb("http://127.0.0.1:5000/")
