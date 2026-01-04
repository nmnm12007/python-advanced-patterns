import time
from functools import wraps

"""
Decorators with arguments
"""


def log_meta_date(func):
    """
    Decorator that logs meta date of function
    :param func: service function
    :return: function result
    :wrapper decorator that logs meta date of function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        args = list(args)
        kwargs = dict(kwargs)
        time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        fun_res = func(*args, **kwargs)

        with open("log.txt", "a") as file_obj:
            file_obj.write(
                f"[{time_stamp}]:: {func.__name__}::"
                f"{(func.__doc__ or '').rstrip()}::"
                f"Result:: {fun_res}\n"
            )

        return fun_res

    return wrapper
