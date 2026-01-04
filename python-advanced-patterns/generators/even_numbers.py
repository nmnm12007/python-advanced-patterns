"""
generator to yield even numbers
"""

from log_and_time import log_and_time


def even_number_generator(limit):
    """generator to yield even numbers"""
    for i in range(limit):
        if i % 2 == 0:
            yield i


@log_and_time
def even_number_stream(n):
    """stream to yield even numbers"""
    even_gen = even_number_generator(n)
    while True:
        try:
            a = next(even_gen)
        except StopIteration:
            break
        print(a)


if __name__ == "__main__":
    even_number_stream(10)
