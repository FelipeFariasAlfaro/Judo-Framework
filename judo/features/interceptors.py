"""
Request and Response Interceptors
Allows modification of requests/responses before/after transmission
"""

from typing import Callable, List, Optional, Dict, Any
from datetime import datetime


class RequestInterceptor:
    """Base class for request interceptors"""
    
    def intercept(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intercept and modify request
        
        Args:
            request: Request dict with keys: method, url, headers, params, body, cookies
        
        Returns:
            Modified request dict
        """
        raise NotImplementedError


class ResponseInterceptor:
    """Base class for response interceptors"""
    
    def intercept(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intercept and modify response
        
        Args:
            response: Response dict with keys: status_code, headers, body, elapsed_time
        
        Returns:
            Modified response dict
        """
        raise NotImplementedError


class TimestampInterceptor(RequestInterceptor):
    """Add timestamp to requests"""
    
    def __init__(self, header_name: str = "X-Request-Timestamp"):
        self.header_name = header_name
    
    def intercept(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Add timestamp header"""
        if "headers" not in request:
            request["headers"] = {}
        request["headers"][self.header_name] = datetime.utcnow().isoformat()
        return request


class AuthorizationInterceptor(RequestInterceptor):
    """Add authorization header to requests"""
    
    def __init__(self, token: str, scheme: str = "Bearer"):
        self.token = token
        self.scheme = scheme
    
    def intercept(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Add authorization header"""
        if "headers" not in request:
            request["headers"] = {}
        request["headers"]["Authorization"] = f"{self.scheme} {self.token}"
        return request


class LoggingInterceptor(RequestInterceptor):
    """Log request details"""
    
    def __init__(self, logger: Optional[Callable] = None):
        self.logger = logger or print
    
    def intercept(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Log request"""
        self.logger(f"📤 {request.get('method', 'GET')} {request.get('url', '')}")
        if request.get("headers"):
            self.logger(f"   Headers: {request['headers']}")
        if request.get("body"):
            self.logger(f"   Body: {request['body']}")
        return request


class ResponseLoggingInterceptor(ResponseInterceptor):
    """Log response details"""
    
    def __init__(self, logger: Optional[Callable] = None):
        self.logger = logger or print
    
    def intercept(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Log response"""
        status = response.get("status_code", "?")
        elapsed = response.get("elapsed_time", 0)
        self.logger(f"📥 Status: {status} ({elapsed:.2f}s)")
        if response.get("body"):
            body_preview = str(response["body"])[:100]
            self.logger(f"   Body: {body_preview}...")
        return response


class InterceptorChain:
    """Chain multiple interceptors together"""
    
    def __init__(self):
        self.request_interceptors: List[RequestInterceptor] = []
        self.response_interceptors: List[ResponseInterceptor] = []
    
    def add_request_interceptor(self, interceptor: RequestInterceptor) -> "InterceptorChain":
        """Add request interceptor"""
        self.request_interceptors.append(interceptor)
        return self
    
    def add_response_interceptor(self, interceptor: ResponseInterceptor) -> "InterceptorChain":
        """Add response interceptor"""
        self.response_interceptors.append(interceptor)
        return self
    
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process request through all interceptors"""
        for interceptor in self.request_interceptors:
            request = interceptor.intercept(request)
        return request
    
    def process_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process response through all interceptors"""
        for interceptor in self.response_interceptors:
            response = interceptor.intercept(response)
        return response
    
    def clear_request_interceptors(self):
        """Clear all request interceptors"""
        self.request_interceptors.clear()
    
    def clear_response_interceptors(self):
        """Clear all response interceptors"""
        self.response_interceptors.clear()
    
    def clear_all(self):
        """Clear all interceptors"""
        self.clear_request_interceptors()
        self.clear_response_interceptors()
