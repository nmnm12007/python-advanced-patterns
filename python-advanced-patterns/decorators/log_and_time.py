import time
from functools import wraps
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "execution.log"

"""
Decorator:: to log date/time
"""


def log_and_time(f):
    """Decorator to log execution metadata with timestamps."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        f_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))

        out_put = f(*args, **kwargs)

        end_time = time.time()
        f_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
        time_taken = end_time - start_time
        desc = (f.__doc__ or "").strip()

        with open(LOG_FILE, "a") as log:
            log.write(
                f" \n[{f_start}] :: \n {desc}::"
                f"{f.__name__} : args={args} : kwargs={kwargs} :: "
                f"\n[{f_end}]  :: \n Time Taken for run ::  {time_taken} "
                f"\n"
            )
        return out_put

    return wrapper


@log_and_time
def fun_add(a, b):
    """Adds two numbers and returns the sum"""
    return a + b


if __name__ == "__main__":
    print(fun_add(1, 2))
