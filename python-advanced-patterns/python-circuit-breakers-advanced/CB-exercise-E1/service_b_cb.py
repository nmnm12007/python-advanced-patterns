import logging

from flask import Flask

app = Flask(__name__)


@app.route("/calling_service_b")
def calling_service_b():
	# print("[Service B] : calling_service_b  ::  called")
	for counter in range(6):
		if counter <= 2:
			status_text = ("[Service B] : calling_service_b  :: Time Delay "
			               "ERROR in attempt %s "), counter + 1
			logging.error(status_text)
			return [status_text,200]
		elif counter == 3 or counter == 4:
			status_text = ('[Service B] : calling_service_b  :: ACCESS ERROR in '
			               'CALLING Service B in attempt %s'), counter + 1
			logging.error(status_text)
			return [status_text, "503"]
		else:
			status_text = ("[Service B] : calling_service_b  :: SUCCESS in "
			               "attempt %s"), counter + 1
			logging.info(status_text)
			return [status_text, 200]
	return ["Completed", 200]



if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 5001, debug = True)
