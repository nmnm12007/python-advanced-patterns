"""
Implements Resilience Executor
"""

import logging
import time
from functools import wraps

from resilience_patterns_case_study.bulkhead import Bulkhead
from resilience_patterns_case_study.bulkhead_policy import BulkheadPolicy
from resilience_patterns_case_study.cb_policy import CircuitBreakerPolicy
from resilience_patterns_case_study.cb_state import CircuitBreakerState
from resilience_patterns_case_study.execution_context import ExecutionContext
from resilience_patterns_case_study.retry_policy import RetryPolicy
from resilience_patterns_case_study.timeout_policy import TimeoutPolicy
from resilience_patterns_case_study.timeout_executor import TimeoutExecutor

logger = logging.getLogger(__name__)


class ResilienceExecutor:
    """
    Implements Resilience Executor policy/state
    """

    def __init__(self, retry_policy, cb_policy, bulkhead_policy, timeout_policy):
        self.retry_policy = retry_policy
        self.cb_policy = cb_policy
        self.bulkhead_policy = bulkhead_policy
        self.timeout_policy = timeout_policy

        self.cb_state = CircuitBreakerState()
        self.bulkhead = Bulkhead(bulkhead_policy)
        self.timeout_executor = TimeoutExecutor(timeout_policy)

    def execute(self, func, *args, **kwargs):
        """
        Implements Resilience Executor Logic
        """
        ctx = ExecutionContext()
        logger.debug(f"[RE]:[{ctx.timestamp}] : Executing {func.__name__}")
        # DONT USE THIS :: with self.bulkhead.semaphore.acquire(  # REFER TO
        # THE CHAT DISCUSSIONS
        acquired = self.bulkhead.semaphore.acquire(timeout=self.bulkhead.acquire_timeout)
        if not acquired:
            raise RuntimeError("[BK] : Bulkhead Limit Exceeded, Try again later")
        if self._is_circuit_open():
            logger.debug("[CB] : Circuit Breaker State is OPEN")
            raise RuntimeError("[CB] : Circuit Breaker State is OPEN")
        while ctx.attempt < self.retry_policy.max_retries:
            ctx.attempt += 1
            logger.debug(
                "[CB]: REQUEST:{ctx.req_id} :attempt #: "
                "{ctx.attempt} out of {"
                "self.retry_policy.max_retries}:"
                " at {ctx.timestamp}: is done."
            )
            try:
                # result = func(*args, **kwargs)
                result = self.timeout_executor.execute(func, *args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure(ctx, e)
                time.sleep(self.retry_policy.delay_seconds)

                if ctx.attempt >= self.retry_policy.max_retries:
                    raise

            finally:
                self.bulkhead.semaphore.release()

        raise RuntimeError("[CB]:Failure with Exception:{e}")

    def _is_circuit_open(self):
        if self.cb_state.state == "OPEN":
            logger.debug("[CB]:Circuit Breaker State is OPEN, Fail-Fast now, Try again later")
            elapsed_time = time.time() - self.cb_state.last_failure_time
            if elapsed_time >= self.cb_policy.recovery_timeout:
                self.cb_state.state = "HALF_OPEN"
                logger.debug("[CB]:State Transition :: OPEN -> HALF-OPEN")
                return False
            logger.debug("[CB]:Current State : {cb_state.state}")
            return True
        return False

    def _on_success(self):
        logger.debug(
            "[CB]: Attempt {ctx.attempt} out of {self.retry_policy.max_retries} is a success."
        )
        if self.cb_state.state == "HALF_OPEN":
            logger.info("[CB] : State Transition :: HALF-OPEN -> CLOSED")
        self.cb_state.state = "CLOSED"
        self.cb_state.failure_count = 0

    def _on_failure(self, ctx, e):
        self.cb_state.failure_count += 1
        self.cb_state.last_failure_time = ctx.timestamp
        ctx.last_exception = e
        logger.error(
            "[CB]:[{ctx.timestamp}]:Attempt {ctx.attempt} out of {"
            "self.retry_policy.max_retries} failed with {ctx.last_exception}."
        )
        if self.cb_state.failure_count >= self.cb_policy.failure_threshold:
            self.cb_state.state = "OPEN"
        logging.error(
            "[CB]: State Transition :: CLOSED -> OPEN done. Current State : {cb_state.state}"
        )


def resilient(
    retry_policy: RetryPolicy,
    cb_policy: CircuitBreakerPolicy,
    bulkhead_policy: BulkheadPolicy,
    timeout_policy: TimeoutPolicy,
):
    """
    definition and implementation of Resilience Decorator
    """

    executor = ResilienceExecutor(retry_policy, cb_policy, bulkhead_policy, timeout_policy)

    def decorator(func):
        """
        Decorator for Resilience Decorator
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper for Resilience Decorator
            """
            result = executor.execute(func, *args, **kwargs)
            return result

        return wrapper

    return decorator
