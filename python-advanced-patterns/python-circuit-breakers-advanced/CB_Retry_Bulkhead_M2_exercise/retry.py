import logging, time
from functools import wraps
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "retry.log"

def on_success(tmp_str):
	logging.info(tmp_str)
	with open(LOG_FILE, "a") as file_obj:
		file_obj.write(tmp_str)

def on_failure(tmp_str):
	logging.error(tmp_str)
	with open(LOG_FILE, "a") as file_obj:
		file_obj.write(tmp_str)

def on_retry(tmp_str):
	logging.debug(tmp_str)
	with open(LOG_FILE, "a") as file_obj:
		file_obj.write(tmp_str)

def retry_cb(max_attempts = 3, base_delay = 0.1, retry_on = (), idempotent =
True, func_stat= (), _on_success=None, _on_failure=None, _on_retry=None):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			curr_delay = base_delay
			last_exception = None
			outcome_status = 0

			for attempt in range(1, max_attempts + 1):
				try:
					time_s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
					outcome_result = func(*args, **kwargs)
					outcome_status = 200
					tmp_str=(f"[{time_s}]::[SUCCESS]::{func.__name__} with "
					         f"args: {str(args)} and kwargs: {str(kwargs)} "
					         f"completed with result :: {outcome_result} and "
					         f"status :: {outcome_status}")
					_on_success(tmp_str)
					return outcome_result, outcome_status
				except retry_on as e:
					time_s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
					last_exception = e
					outcome_status = 502 if outcome_status == 500 else 503
					tmp_str= f"[{time_s}]::[ERROR]::{func.__name__} with "
					f"args: {str(args)} and kwargs: {str(kwargs)} "
					f"failed with status :: {outcome_status}"
					_on_failure(tmp_str)
					if idempotent:
						if outcome_status in func_stat:
							time.sleep(curr_delay)
							curr_delay = curr_delay + 0.2
							tmp_str = f"[{time_s}]::[RETRY]::{func.__name__} with "
							f"args: {str(args)} and kwargs: {str(kwargs)} "
							f"will be retried after a delay of {curr_delay} seconds"
							_on_retry(tmp_str)
					else:
						raise
			raise last_exception
		return wrapper
	return decorator
