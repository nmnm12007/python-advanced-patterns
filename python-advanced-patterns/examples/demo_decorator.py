from decorators.log_and_time import log_and_time


@log_and_time
def fun_add(a, b):
    """Adds two numbers and returns the sum."""
    return a + b


if __name__ == "__main__":
    print(fun_add(1, 2))
