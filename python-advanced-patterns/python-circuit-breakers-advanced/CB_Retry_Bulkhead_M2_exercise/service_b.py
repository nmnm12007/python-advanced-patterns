from flask import Flask
app = Flask(__name__)

counter = 0

@app.route("/call_inside_b")
def call():
	global counter
	counter += 1
	
	if counter % 2 == 0:
		return "Service B"
	else:
		return "Service B"
	
if __name__ == "__main__":
	app.run(port=5001, debug = True)
