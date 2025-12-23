import decorator_3_call_scenario, retry_decorator

@decorator_3_call_scenario.log_meta_date
@retry_decorator.retry_dec_attempt(5)
def fun_add(a, b):
	""" Adds two numbers """
	return a + b


counter = 0
@decorator_3_call_scenario.log_meta_date
@retry_decorator.retry_dec_attempt(5)
def flaky():
	""" Raise ValueError TEST function """
	global counter
	counter += 1
	if counter < 5:
		raise ValueError("Temporary issue")
	return "OK"

@retry_decorator.retry_dec_attempt(5)
def sub(a,b):
	""" Subtracts two numbers """
	return a - b



if __name__ == '__main__':
	print("fun_add::" + str(fun_add(10, 20)))
	print("flaky:: " + flaky())
