import concurrent.futures


class TimeoutException(Exception):
    pass


class Timeout:
    def __init__(self, time_out_duration: int):
        self.time_out_duration = time_out_duration

    def run_timeout(self, func, *args, **kwargs):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            try:
                return future.result(timeout=self.time_out_duration)
            except concurrent.futures.TimeoutError:
                raise TimeoutException("[TIMEOUT] : API operation timed out")


# The below signal module runs ONLY in LINUX/UNIX not on WIN
#
#
#
#
# import signal
#
# from contextlib import contextmanager
#
#
# class TimeoutException(Exception):
#     pass
#
# class Timeout:
#     def __init__(self,_duration_elapsed:int):
#         self._duration_elapsed = _duration_elapsed
#
#     @contextmanager
#     def apply_timeout(self):
#         def handler(signum, frame):
#             raise TimeoutException("[Timeout]:: Operation Timed Out")
#
#         signal.signal(signal.SIGALRM, handler)
#         signal.alarm(self._duration_elapsed)
#
#         try:
#             yield
#         finally:
#             signal.alarm(0)
#
