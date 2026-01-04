import retry_decorator_idempotency
#
#
# @decorator_3_call_scenario.log_meta_date
# @retry_decorator.retry_dec_attempt(5)
# @retry_decorator_basedelay.retry(retries = 4, retry_on = (ValueError,),
#                                  base_delay = 0.2)
# def fun_add(a, b):
# 	""" Adds two numbers """
# 	return a + b
#
#
# counter = 0
#
#
# @decorator_3_call_scenario.log_meta_date
# @retry_decorator.retry_dec_attempt(5)
# @retry_decorator_basedelay.retry(retries = 4, retry_on = (ValueError,),
#                                  base_delay =
#                                  0.2)
# def flaky():
# 	""" Raise ValueError TEST function """
# 	global counter
# 	counter += 1
# 	if counter < 4:
# 		raise ValueError("Temporary issue")
# 	return "OK"
#
#
# @decorator_3_call_scenario.log_meta_date
# @retry_decorator_basedelay.retry(retries = 4, retry_on = (ValueError,),
#                                  base_delay = 0.2)
# def sub(a, b):
# 	""" Subtracts two numbers """
# 	return a - b

#
counter = 0


@retry_decorator_idempotency.retry(
    retries=4, retry_on=(ValueError,), idempotent=True, base_delay=0.2
)
def flaky_idempotency():
    global counter
    counter += 1
    if counter < 3:
        raise ValueError("Temporary glitch")
    return "OK"


@retry_decorator_idempotency.retry(
    retries=4,
    retry_on=(ValueError,),
)
def func_add(a, b):
    """Adds two numbers"""
    return a + b


#
# print(flaky_idempotency())

if __name__ == "__main__":
    func_add(10, 20)
    flaky_idempotency()
