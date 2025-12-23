from functools import wraps


def retry_dec_attempt(retry_times = 3):
	"""
	Retry decorator
	:param retry_times:
	:return: decorator
	"""
	
	def decorator_add(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			
			attempt = 0
			last_exception = None
			while attempt < retry_times:
				try:
					result = func(*args, **kwargs)
					tmp_str = (f" Attempt: {attempt} of Retry:{retry_times} "
					           f"of {func.__name__}  is successful : with  "
					           f"result ::  {result}  \n")
					print(tmp_str)
					return result
				
				except Exception as e:
					last_exception = e
					tmp_str = (
							f"Attempt {attempt} of {retry_times} of "
							f"{func.__name__}  failed: with "
							f"exception ::  {last_exception}")
					print(tmp_str)
					attempt += 1
				
				finally:
					with open("log.txt", "a") as file_obj:
						file_obj.write(tmp_str + "\n")
			raise last_exception
		
		return wrapper
	
	return decorator_add


def retry_on_exception(retry_times = 3, retry_on=("ValueError","TimeoutError")):
	def decorator_retry_on_exception(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			attempt = 0
			last_exception = None
			try:
				result = func(*args, **kwargs)
				tmp_str = f" Attempt: {attempt} of {retry_times} of {func.__name__}  is successful "
				return result
			except Exception in retry_on:
				last_exception = e
				tmp_str = ()
				
			
				
				
			
			
			
			
			while attempt < retry_times:
				try:
					result = func(*args, **kwargs)
					tmp_str = (f" Attempt: {attempt} of Retry:{retry_times} "
					           f"of {func.__name__}  is successful : with  "
					           f"result ::  {result}  \n")
					print(tmp_str)
					return result
				
				except Exception as e:
					last_exception = e
					tmp_str = (
							f"Attempt {attempt} of {retry_times} of "
							f"{func.__name__}  failed: with "
							f"exception ::  {last_exception}")
					print(tmp_str)
					attempt += 1
				
				finally:
					with open("log.txt", "a") as file_obj:
						file_obj.write(tmp_str + "\n")
				raise last_exception
