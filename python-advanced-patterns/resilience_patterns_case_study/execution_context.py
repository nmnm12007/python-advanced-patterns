"""
    Define the Execution Context for retry, cb, bk
ExecutionContext
====================
├─ request_id (correlation)
├─ attempt (retry counter)
├─ start_time (latency tracking)
├─ last_exception (failure reason)
"""

import uuid
import time


class ExecutionContext:
    """
    Execution Context for retry, cb, bk
    class holds the values of unique request ID,
    timestamp of the request, attempt number, last_exception
    """

    def __init__(self):
        self.req_id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.attempt = 0
        self.last_exception = None
