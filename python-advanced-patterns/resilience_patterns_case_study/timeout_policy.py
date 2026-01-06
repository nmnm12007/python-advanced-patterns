"""
class to check and hold Timeout Policy
"""


class TimeoutPolicy:
    def __init__(self, timeout_seconds: float) -> None:
        self.timeout_seconds = timeout_seconds
