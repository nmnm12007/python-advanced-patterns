from decorators import log_and_time
from generators.even_numbers import even_number_generator


@log_and_time
def even_number_stream(n):
    """Stream even numbers to stdout."""
    for value in even_number_generator(n):
        print(value)


if __name__ == "__main__":
    even_number_stream(10)
