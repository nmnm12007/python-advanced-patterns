import logging
import time
from functools import wraps
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "execution.log"


def log_success(func, result):
    start_time = time.time()
    f_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    tmp_str = f"[{f_start}] : [Success] : {func.__name__} with is successful :  {result} \n"
    print(tmp_str)
    logging.log(logging.INFO, tmp_str)
    with open(LOG_FILE, "a") as file_obj:
        file_obj.write(tmp_str)


def log_failure(func, attempt, retries, last_exception):
    start_time = time.time()
    f_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    tmp_str = (
        f"[{f_start}] : [ERROR] : Attempt {attempt + 1} on {func.__name__} failed with exception:"
        f" {last_exception}, "
        f" Attempts Failed \n"
    )
    logging.log(logging.ERROR, tmp_str)
    with open(LOG_FILE, "a") as file_obj:
        file_obj.write(tmp_str)


def log_retry(func, attempt, retries, last_exception, time_delay):
    start_time = time.time()
    f_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    tmp_str = (
        f"[{f_start}] : [WARNING] : Attempt {attempt + 1} out of "
        f"Retries {retries} on {func.__name__} failed with exception:"
        f" {last_exception}, "
        f" Attempts will be done again in : {time_delay} \n"
    )

    logging.log(logging.ERROR, tmp_str)
    with open(LOG_FILE, "a") as file_obj:
        file_obj.write(tmp_str)


def retry(
    retries=3,
    retry_on=(),
    base_delay=0.5,
    idempotent=True,
    on_retry=log_retry,
    on_success=log_success,
    on_failure=log_failure,
):
    def retry_idempotency_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            # args_1 = list(*args)
            # kwargs_1 = dict(**kwargs)
            for i in range(retries):
                try:
                    result = func(*args, **kwargs)
                    on_success(func, result)
                    return result
                except retry_on as e:
                    last_exception = e
                    if idempotent:
                        time_delay = base_delay * (2 ** (i - 1))
                        time.sleep(time_delay)
                        on_retry(func, i, retries, last_exception, time_delay)
                    else:
                        on_failure(func, i, retries, last_exception)
                        raise last_exception

            raise last_exception

        return wrapper

    return retry_idempotency_decorator
