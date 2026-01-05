"""
Chaos Engineering
Inject failures for resilience testing
"""

import random
import time
from typing import Optional, Callable


class ChaosInjector:
    """Inject chaos into requests for resilience testing"""
    
    def __init__(self, enabled: bool = False):
        """
        Initialize chaos injector
        
        Args:
            enabled: Whether chaos injection is enabled
        """
        self.enabled = enabled
        self.latency_min_ms = 0
        self.latency_max_ms = 0
        self.error_rate = 0.0
        self.timeout_probability = 0.0
    
    def inject_latency(self, min_ms: float = 0, max_ms: float = 100):
        """
        Inject random latency into requests
        
        Args:
            min_ms: Minimum latency in milliseconds
            max_ms: Maximum latency in milliseconds
        """
        self.latency_min_ms = min_ms
        self.latency_max_ms = max_ms
    
    def inject_error_rate(self, percentage: float = 10.0):
        """
        Inject errors with given probability
        
        Args:
            percentage: Error probability (0-100)
        """
        self.error_rate = percentage / 100.0
    
    def inject_timeout(self, probability: float = 0.05):
        """
        Inject timeouts with given probability
        
        Args:
            probability: Timeout probability (0-1)
        """
        self.timeout_probability = probability
    
    def apply_latency(self):
        """Apply injected latency"""
        if not self.enabled or self.latency_max_ms == 0:
            return
        
        latency = random.uniform(self.latency_min_ms, self.latency_max_ms)
        time.sleep(latency / 1000.0)
    
    def should_inject_error(self) -> bool:
        """Check if error should be injected"""
        if not self.enabled or self.error_rate == 0:
            return False
        
        return random.random() < self.error_rate
    
    def should_inject_timeout(self) -> bool:
        """Check if timeout should be injected"""
        if not self.enabled or self.timeout_probability == 0:
            return False
        
        return random.random() < self.timeout_probability
    
    def enable(self):
        """Enable chaos injection"""
        self.enabled = True
    
    def disable(self):
        """Disable chaos injection"""
        self.enabled = False
    
    def reset(self):
        """Reset all chaos settings"""
        self.latency_min_ms = 0
        self.latency_max_ms = 0
        self.error_rate = 0.0
        self.timeout_probability = 0.0
    
    def get_status(self) -> dict:
        """Get chaos injector status"""
        return {
            "enabled": self.enabled,
            "latency_range_ms": (self.latency_min_ms, self.latency_max_ms),
            "error_rate_percent": self.error_rate * 100,
            "timeout_probability": self.timeout_probability
        }


class ResilienceTestBuilder:
    """Build resilience tests with chaos injection"""
    
    def __init__(self, chaos_injector: ChaosInjector):
        """
        Initialize resilience test builder
        
        Args:
            chaos_injector: ChaosInjector instance
        """
        self.chaos_injector = chaos_injector
        self.test_scenarios = []
    
    def add_scenario(
        self,
        name: str,
        latency_ms: Optional[float] = None,
        error_rate: Optional[float] = None,
        timeout_probability: Optional[float] = None
    ) -> "ResilienceTestBuilder":
        """
        Add test scenario
        
        Args:
            name: Scenario name
            latency_ms: Latency to inject
            error_rate: Error rate to inject
            timeout_probability: Timeout probability
        
        Returns:
            Self for chaining
        """
        self.test_scenarios.append({
            "name": name,
            "latency_ms": latency_ms,
            "error_rate": error_rate,
            "timeout_probability": timeout_probability
        })
        return self
    
    def run_scenarios(self, test_func: Callable) -> list:
        """
        Run test function with all scenarios
        
        Args:
            test_func: Function to test
        
        Returns:
            List of results
        """
        results = []
        
        for scenario in self.test_scenarios:
            # Reset chaos injector
            self.chaos_injector.reset()
            
            # Apply scenario settings
            if scenario["latency_ms"]:
                self.chaos_injector.inject_latency(0, scenario["latency_ms"])
            
            if scenario["error_rate"]:
                self.chaos_injector.inject_error_rate(scenario["error_rate"])
            
            if scenario["timeout_probability"]:
                self.chaos_injector.inject_timeout(scenario["timeout_probability"])
            
            # Enable chaos
            self.chaos_injector.enable()
            
            # Run test
            try:
                result = test_func()
                results.append({
                    "scenario": scenario["name"],
                    "status": "passed",
                    "result": result,
                    "error": None
                })
            except Exception as e:
                results.append({
                    "scenario": scenario["name"],
                    "status": "failed",
                    "result": None,
                    "error": str(e)
                })
            finally:
                # Disable chaos
                self.chaos_injector.disable()
        
        return results
