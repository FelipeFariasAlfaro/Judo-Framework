"""
Retry Policy and Circuit Breaker Pattern
Handles transient failures and cascading failures
"""

import time
import random
from typing import Callable, Optional, Any, Type
from enum import Enum
from datetime import datetime, timedelta


class BackoffStrategy(Enum):
    """Backoff strategies for retries"""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    RANDOM = "random"
    FIBONACCI = "fibonacci"


class RetryPolicy:
    """
    Retry policy with configurable backoff strategies
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        jitter: bool = True,
        retryable_exceptions: tuple = (Exception,),
        retryable_status_codes: list = None
    ):
        """
        Initialize retry policy
        
        Args:
            max_retries: Maximum number of retry attempts
            backoff_strategy: Strategy for calculating delay between retries
            initial_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            jitter: Add randomness to delay
            retryable_exceptions: Tuple of exceptions to retry on
            retryable_status_codes: List of HTTP status codes to retry on
        """
        self.max_retries = max_retries
        self.backoff_strategy = backoff_strategy
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions
        self.retryable_status_codes = retryable_status_codes or [408, 429, 500, 502, 503, 504]
        self.attempt_count = 0
        self.last_exception = None
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number"""
        if self.backoff_strategy == BackoffStrategy.LINEAR:
            delay = self.initial_delay * attempt
        elif self.backoff_strategy == BackoffStrategy.EXPONENTIAL:
            delay = self.initial_delay * (2 ** attempt)
        elif self.backoff_strategy == BackoffStrategy.FIBONACCI:
            delay = self._fibonacci_delay(attempt)
        else:  # RANDOM
            delay = random.uniform(self.initial_delay, self.max_delay)
        
        # Cap at max_delay
        delay = min(delay, self.max_delay)
        
        # Add jitter
        if self.jitter:
            delay = delay * (0.5 + random.random())
        
        return delay
    
    @staticmethod
    def _fibonacci_delay(n: int) -> float:
        """Calculate Fibonacci number for delay"""
        if n <= 1:
            return 1.0
        a, b = 1, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return float(b)
    
    def should_retry(self, exception: Optional[Exception] = None, status_code: Optional[int] = None) -> bool:
        """Determine if should retry"""
        if self.attempt_count >= self.max_retries:
            return False
        
        if exception and isinstance(exception, self.retryable_exceptions):
            return True
        
        if status_code and status_code in self.retryable_status_codes:
            return True
        
        return False
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry logic"""
        self.attempt_count = 0
        
        while self.attempt_count <= self.max_retries:
            try:
                result = func(*args, **kwargs)
                
                # Check if response has retryable status code
                if hasattr(result, 'status_code') and result.status_code in self.retryable_status_codes:
                    if self.attempt_count < self.max_retries:
                        self.attempt_count += 1
                        delay = self.calculate_delay(self.attempt_count)
                        time.sleep(delay)
                        continue
                
                return result
            
            except Exception as e:
                self.last_exception = e
                
                if self.should_retry(exception=e):
                    self.attempt_count += 1
                    delay = self.calculate_delay(self.attempt_count)
                    time.sleep(delay)
                else:
                    raise
        
        if self.last_exception:
            raise self.last_exception
        
        return None


class CircuitBreaker:
    """
    Circuit Breaker pattern to prevent cascading failures
    States: CLOSED -> OPEN -> HALF_OPEN -> CLOSED
    """
    
    class State(Enum):
        CLOSED = "closed"  # Normal operation
        OPEN = "open"  # Failing, reject requests
        HALF_OPEN = "half_open"  # Testing if service recovered
    
    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout: int = 60,
        name: str = "default"
    ):
        """
        Initialize circuit breaker
        
        Args:
            failure_threshold: Number of failures to open circuit
            success_threshold: Number of successes to close circuit
            timeout: Seconds before trying half-open state
            name: Circuit breaker name
        """
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout
        self.name = name
        
        self.state = self.State.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.last_state_change = datetime.now()
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function through circuit breaker"""
        if self.state == self.State.OPEN:
            if self._should_attempt_reset():
                self.state = self.State.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception(f"Circuit breaker '{self.name}' is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        
        if self.state == self.State.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self._change_state(self.State.CLOSED)
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self._change_state(self.State.OPEN)
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True
        
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout
    
    def _change_state(self, new_state: State):
        """Change circuit breaker state"""
        old_state = self.state
        self.state = new_state
        self.last_state_change = datetime.now()
        print(f"🔌 Circuit breaker '{self.name}': {old_state.value} -> {new_state.value}")
    
    def reset(self):
        """Manually reset circuit breaker"""
        self._change_state(self.State.CLOSED)
        self.failure_count = 0
        self.success_count = 0
    
    def get_status(self) -> dict:
        """Get circuit breaker status"""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_state_change": self.last_state_change.isoformat(),
            "last_failure_time": self.last_failure_time.isoformat() if self.last_failure_time else None
        }
