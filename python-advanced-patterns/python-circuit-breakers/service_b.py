from flask import Flask

app = Flask(__name__)

failure_counter = 0


@app.route("/process")
def process():
	global failure_counter
	failure_counter += 1

	# Force first 5 calls to fail
	if failure_counter <= 5:
		return "Forced failure", 500

	return "Service B success", 200


if __name__ == "__main__":
	app.run(port = 5001)

# from flask import Flask
# import random
# app = Flask(__name__)
#
# def process():
#
# 	if random.random() < 0.7:
# 		return "Service B failed ", 500
# 	else:
# 		return "Service B passed ", 200
#
#
# if __name__ == '__main__':
# 	app.run(port=5001)
