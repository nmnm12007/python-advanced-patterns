"""
Timeout with ThreadPoolExecutor
"""

from concurrent.futures import ThreadPoolExecutor


class TimeoutExecutor:
    """
    TimeoutExecutor - Runs the Timeout Logic
    """

    def __init__(self, timeout_policy):
        self.timeout_policy = timeout_policy
        self.executor = ThreadPoolExecutor(max_workers=1)

    def execute(self, func, *args, **kwargs):
        """
        the function to be run is fed to the executor.
        """
        future_1 = self.executor.submit(func, *args, **kwargs)
        try:
            return future_1.result(timeout=self.timeout_policy.timeout_seconds)
        except TimeoutError:
            future_1.cancel()
            raise TimeoutError(
                f"[TIMEOUT]:: Timeout Error : Execution "
                f"Exceeded {self.timeout_policy.timeout_seconds}"
            )
