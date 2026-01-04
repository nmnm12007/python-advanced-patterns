from functools import wraps
from logging import log
from time import sleep


def retry(retries=3, retry_on=(TimeoutError, ConnectionError, ValueError), base_delay=0.5):
    def ret_dec_basedelay(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tmp_str = ""
            last_exception = None
            for i in range(1, retries + 1):
                try:
                    result = func(*args, **kwargs)
                    tmp_str = f" Attempt: {i} of {retries} of {func.__name__}  is successful "
                    return result

                except retry_on as e:
                    last_exception = e
                    time_delay = base_delay * (2 ** (i - 1))
                    sleep(time_delay)
                    tmp_str = (
                        f"Attempt {i} of {retries} of "
                        f"{func.__name__}  failed: with "
                        f"exception ::  {last_exception}"
                        f"time_delay ::  {time_delay}"
                    )

                finally:
                    log(1, tmp_str)
                    with open("log.txt", "a") as file_obj:
                        file_obj.write(tmp_str + "\n")

            raise last_exception

        return wrapper

    return ret_dec_basedelay
