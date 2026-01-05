"""
Performance Monitoring and Metrics
Track and analyze API performance
"""

import time
from typing import Dict, List, Optional, Callable
from collections import defaultdict
from statistics import mean, median, stdev
from datetime import datetime


class PerformanceMetrics:
    """Container for performance metrics"""
    
    def __init__(self):
        self.response_times: List[float] = []
        self.status_codes: Dict[int, int] = defaultdict(int)
        self.errors: List[str] = []
        self.start_time = datetime.now()
        self.end_time = None
    
    def add_response_time(self, elapsed_ms: float):
        """Add response time measurement"""
        self.response_times.append(elapsed_ms)
    
    def add_status_code(self, status_code: int):
        """Record status code"""
        self.status_codes[status_code] += 1
    
    def add_error(self, error: str):
        """Record error"""
        self.errors.append(error)
    
    def get_avg_response_time(self) -> float:
        """Get average response time in ms"""
        return mean(self.response_times) if self.response_times else 0
    
    def get_median_response_time(self) -> float:
        """Get median response time in ms"""
        return median(self.response_times) if self.response_times else 0
    
    def get_percentile(self, percentile: float) -> float:
        """Get response time percentile"""
        if not self.response_times:
            return 0
        
        sorted_times = sorted(self.response_times)
        index = int(len(sorted_times) * percentile / 100)
        return sorted_times[min(index, len(sorted_times) - 1)]
    
    def get_min_response_time(self) -> float:
        """Get minimum response time"""
        return min(self.response_times) if self.response_times else 0
    
    def get_max_response_time(self) -> float:
        """Get maximum response time"""
        return max(self.response_times) if self.response_times else 0
    
    def get_stdev_response_time(self) -> float:
        """Get standard deviation of response times"""
        if len(self.response_times) < 2:
            return 0
        return stdev(self.response_times)
    
    def get_error_rate(self) -> float:
        """Get error rate as percentage"""
        total = len(self.response_times)
        if total == 0:
            return 0
        error_count = len(self.errors)
        return (error_count / total) * 100
    
    def get_throughput(self) -> float:
        """Get throughput (requests per second)"""
        if self.end_time is None:
            self.end_time = datetime.now()
        
        elapsed_seconds = (self.end_time - self.start_time).total_seconds()
        if elapsed_seconds == 0:
            return 0
        
        return len(self.response_times) / elapsed_seconds
    
    def to_dict(self) -> Dict:
        """Convert metrics to dictionary"""
        return {
            "total_requests": len(self.response_times),
            "avg_response_time_ms": round(self.get_avg_response_time(), 2),
            "median_response_time_ms": round(self.get_median_response_time(), 2),
            "min_response_time_ms": round(self.get_min_response_time(), 2),
            "max_response_time_ms": round(self.get_max_response_time(), 2),
            "p95_response_time_ms": round(self.get_percentile(95), 2),
            "p99_response_time_ms": round(self.get_percentile(99), 2),
            "stdev_response_time_ms": round(self.get_stdev_response_time(), 2),
            "error_rate_percent": round(self.get_error_rate(), 2),
            "throughput_rps": round(self.get_throughput(), 2),
            "status_codes": dict(self.status_codes),
            "error_count": len(self.errors)
        }


class PerformanceMonitor:
    """Monitor and track API performance"""
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.alerts: List["PerformanceAlert"] = []
    
    def record_request(self, elapsed_ms: float, status_code: int, error: Optional[str] = None):
        """Record a request"""
        self.metrics.add_response_time(elapsed_ms)
        self.metrics.add_status_code(status_code)
        
        if error:
            self.metrics.add_error(error)
        
        # Check alerts
        self._check_alerts(elapsed_ms, status_code)
    
    def add_alert(self, alert: "PerformanceAlert"):
        """Add performance alert"""
        self.alerts.append(alert)
    
    def _check_alerts(self, elapsed_ms: float, status_code: int):
        """Check if any alerts should trigger"""
        for alert in self.alerts:
            alert.check(elapsed_ms, status_code, self.metrics)
    
    def get_metrics(self) -> Dict:
        """Get current metrics"""
        self.metrics.end_time = datetime.now()
        return self.metrics.to_dict()
    
    def reset(self):
        """Reset metrics"""
        self.metrics = PerformanceMetrics()


class PerformanceAlert:
    """Alert triggered when performance threshold exceeded"""
    
    def __init__(
        self,
        metric: str,
        threshold: float,
        callback: Optional[Callable] = None
    ):
        """
        Initialize alert
        
        Args:
            metric: Metric to monitor ('response_time', 'error_rate', 'throughput')
            threshold: Threshold value
            callback: Function to call when alert triggers
        """
        self.metric = metric
        self.threshold = threshold
        self.callback = callback or self._default_callback
        self.triggered_count = 0
    
    def check(self, elapsed_ms: float, status_code: int, metrics: PerformanceMetrics):
        """Check if alert should trigger"""
        should_trigger = False
        
        if self.metric == "response_time":
            should_trigger = elapsed_ms > self.threshold
        elif self.metric == "error_rate":
            should_trigger = metrics.get_error_rate() > self.threshold
        elif self.metric == "throughput":
            should_trigger = metrics.get_throughput() < self.threshold
        
        if should_trigger:
            self.triggered_count += 1
            self.callback(self, elapsed_ms, metrics)
    
    @staticmethod
    def _default_callback(alert: "PerformanceAlert", elapsed_ms: float, metrics: PerformanceMetrics):
        """Default callback - print warning"""
        if alert.metric == "response_time":
            print(f"⚠️ Performance Alert: Response time {elapsed_ms}ms exceeds {alert.threshold}ms")
        elif alert.metric == "error_rate":
            print(f"⚠️ Performance Alert: Error rate {metrics.get_error_rate():.2f}% exceeds {alert.threshold}%")
        elif alert.metric == "throughput":
            print(f"⚠️ Performance Alert: Throughput {metrics.get_throughput():.2f} rps below {alert.threshold} rps")
