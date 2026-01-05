"""
Rate Limiting and Throttling
Control request rate to respect API limits
"""

import time
from typing import Optional
from collections import deque
from datetime import datetime, timedelta


class RateLimiter:
    """
    Token bucket rate limiter
    Allows N requests per second
    """
    
    def __init__(self, requests_per_second: float = 10.0):
        """
        Initialize rate limiter
        
        Args:
            requests_per_second: Maximum requests per second
        """
        self.requests_per_second = requests_per_second
        self.tokens = requests_per_second
        self.last_update = time.time()
        self.lock = None  # For thread safety if needed
    
    def acquire(self, tokens: float = 1.0, timeout: Optional[float] = None) -> bool:
        """
        Acquire tokens from bucket
        
        Args:
            tokens: Number of tokens to acquire
            timeout: Maximum time to wait in seconds
        
        Returns:
            True if tokens acquired, False if timeout
        """
        start_time = time.time()
        
        while True:
            now = time.time()
            elapsed = now - self.last_update
            
            # Add tokens based on elapsed time
            self.tokens = min(
                self.requests_per_second,
                self.tokens + elapsed * self.requests_per_second
            )
            self.last_update = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            # Check timeout
            if timeout is not None:
                elapsed_total = time.time() - start_time
                if elapsed_total >= timeout:
                    return False
            
            # Wait a bit before retrying
            time.sleep(0.01)
    
    def wait_if_needed(self, tokens: float = 1.0):
        """Wait until tokens are available"""
        while not self.acquire(tokens, timeout=None):
            pass


class Throttle:
    """
    Simple throttle - fixed delay between requests
    """
    
    def __init__(self, delay_ms: float = 100):
        """
        Initialize throttle
        
        Args:
            delay_ms: Delay in milliseconds between requests
        """
        self.delay_seconds = delay_ms / 1000.0
        self.last_request_time = None
    
    def wait_if_needed(self):
        """Wait if needed to maintain throttle"""
        if self.last_request_time is None:
            self.last_request_time = time.time()
            return
        
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay_seconds:
            time.sleep(self.delay_seconds - elapsed)
        
        self.last_request_time = time.time()
    
    def reset(self):
        """Reset throttle"""
        self.last_request_time = None


class AdaptiveRateLimiter:
    """
    Adaptive rate limiter that adjusts based on response headers
    Respects X-RateLimit-* headers from API
    """
    
    def __init__(self, initial_rps: float = 10.0):
        """
        Initialize adaptive rate limiter
        
        Args:
            initial_rps: Initial requests per second
        """
        self.rate_limiter = RateLimiter(initial_rps)
        self.limit = None
        self.remaining = None
        self.reset_time = None
    
    def update_from_headers(self, headers: dict):
        """
        Update rate limit from response headers
        
        Supports:
        - X-RateLimit-Limit
        - X-RateLimit-Remaining
        - X-RateLimit-Reset
        - RateLimit-Limit (GitHub style)
        - RateLimit-Remaining
        - RateLimit-Reset
        """
        # Try different header formats
        limit = headers.get("X-RateLimit-Limit") or headers.get("RateLimit-Limit")
        remaining = headers.get("X-RateLimit-Remaining") or headers.get("RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset") or headers.get("RateLimit-Reset")
        
        if limit:
            self.limit = int(limit)
        if remaining:
            self.remaining = int(remaining)
        if reset:
            self.reset_time = int(reset)
        
        # Adjust rate if we're running low
        if self.remaining is not None and self.limit is not None:
            if self.remaining < self.limit * 0.1:  # Less than 10%
                # Reduce rate by 50%
                self.rate_limiter.requests_per_second *= 0.5
    
    def acquire(self, tokens: float = 1.0) -> bool:
        """Acquire tokens"""
        return self.rate_limiter.acquire(tokens)
    
    def wait_if_needed(self, tokens: float = 1.0):
        """Wait if needed"""
        self.rate_limiter.wait_if_needed(tokens)
    
    def get_status(self) -> dict:
        """Get rate limiter status"""
        return {
            "limit": self.limit,
            "remaining": self.remaining,
            "reset_time": self.reset_time,
            "current_rps": self.rate_limiter.requests_per_second,
            "available_tokens": self.rate_limiter.tokens
        }
