"""
Advanced Logging
Detailed logging and debugging capabilities
"""

import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path


class AdvancedLogger:
    """Advanced logging for Judo Framework"""
    
    def __init__(self, name: str = "judo", log_file: Optional[str] = None, level: str = "INFO"):
        """
        Initialize advanced logger
        
        Args:
            name: Logger name
            log_file: Optional log file path
            level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, level))
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs, default=str)}"
        self.logger.debug(message)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs, default=str)}"
        self.logger.info(message)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs, default=str)}"
        self.logger.warning(message)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs, default=str)}"
        self.logger.error(message)
    
    def log_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict] = None,
        body: Optional[Any] = None,
        params: Optional[Dict] = None
    ):
        """Log HTTP request"""
        self.info(
            f"📤 {method} {url}",
            headers=headers,
            params=params,
            body=body
        )
    
    def log_response(
        self,
        status_code: int,
        headers: Optional[Dict] = None,
        body: Optional[Any] = None,
        elapsed_time: float = 0
    ):
        """Log HTTP response"""
        self.info(
            f"📥 Status {status_code} ({elapsed_time:.2f}s)",
            headers=headers,
            body=body
        )
    
    def log_assertion(self, assertion: str, passed: bool):
        """Log assertion result"""
        status = "✅" if passed else "❌"
        level = "info" if passed else "error"
        getattr(self, level)(f"{status} Assertion: {assertion}")
    
    def log_variable(self, name: str, value: Any):
        """Log variable assignment"""
        self.debug(f"📝 Variable: {name} = {value}")
    
    def log_error_details(self, error: Exception, context: Optional[Dict] = None):
        """Log detailed error information"""
        self.error(
            f"❌ Error: {str(error)}",
            error_type=type(error).__name__,
            context=context
        )
    
    def log_performance(self, operation: str, duration_ms: float):
        """Log performance metric"""
        self.info(f"⏱️ {operation}: {duration_ms:.2f}ms")
    
    def set_level(self, level: str):
        """Set logging level"""
        self.logger.setLevel(getattr(logging, level))
        for handler in self.logger.handlers:
            handler.setLevel(getattr(logging, level))


class RequestLogger:
    """Log all requests and responses to file"""
    
    def __init__(self, log_dir: str = "request_logs"):
        """
        Initialize request logger
        
        Args:
            log_dir: Directory to store request logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.request_count = 0
    
    def log_request_response(
        self,
        method: str,
        url: str,
        request_headers: Dict,
        request_body: Any,
        status_code: int,
        response_headers: Dict,
        response_body: Any,
        elapsed_time: float
    ):
        """Log request and response to file"""
        self.request_count += 1
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "request_number": self.request_count,
            "request": {
                "method": method,
                "url": url,
                "headers": request_headers,
                "body": request_body
            },
            "response": {
                "status_code": status_code,
                "headers": response_headers,
                "body": response_body,
                "elapsed_time_seconds": elapsed_time
            }
        }
        
        # Write to file
        log_file = self.log_dir / f"request_{self.request_count:04d}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_entry, f, indent=2, default=str)
    
    def get_logs(self) -> list:
        """Get all logged requests"""
        logs = []
        for log_file in sorted(self.log_dir.glob("request_*.json")):
            with open(log_file, 'r', encoding='utf-8') as f:
                logs.append(json.load(f))
        return logs
    
    def clear_logs(self):
        """Clear all logs"""
        for log_file in self.log_dir.glob("request_*.json"):
            log_file.unlink()
        self.request_count = 0
