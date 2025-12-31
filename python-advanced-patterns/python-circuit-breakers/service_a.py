from flask import Flask, Response
from circuit_breaker import safe_call

app = Flask(__name__)


@app.route("/call")
def call():
	result, status = safe_call()
	return Response(result, status = status)


if __name__ == "__main__":
	app.run(port = 5000)

# from flask import Flask
#
#
# from circuit_breaker import safe_call
#
# app = Flask(__name__)
#
# @app.route("/call")
# def call():
# 	return safe_call()
#
# if __name__ == "__main__":
# 	app.run(port=5000)
