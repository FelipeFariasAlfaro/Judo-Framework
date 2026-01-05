"""
Advanced Assertions and Matchers
More powerful validation capabilities
"""

import re
import json
from typing import Any, List, Dict, Pattern, Callable, Optional
from datetime import datetime


class AdvancedAssertions:
    """Advanced assertion methods for API responses"""
    
    def __init__(self, response: Any = None):
        """Initialize with optional response"""
        self.response = response
    
    def assert_response_time_less_than(self, max_ms: float, response: Any = None):
        """Assert response time is less than threshold"""
        resp = response or self.response
        if not hasattr(resp, 'elapsed_time'):
            raise AssertionError("Response does not have elapsed_time attribute")
        
        elapsed_ms = resp.elapsed_time * 1000
        assert elapsed_ms < max_ms, f"Response time {elapsed_ms}ms exceeds {max_ms}ms"
    
    def assert_response_time_between(self, min_ms: float, max_ms: float, response: Any = None):
        """Assert response time is between min and max"""
        resp = response or self.response
        if not hasattr(resp, 'elapsed_time'):
            raise AssertionError("Response does not have elapsed_time attribute")
        
        elapsed_ms = resp.elapsed_time * 1000
        assert min_ms <= elapsed_ms <= max_ms, \
            f"Response time {elapsed_ms}ms not between {min_ms}ms and {max_ms}ms"
    
    def assert_json_schema_valid(self, schema: Dict, response: Any = None):
        """Assert response matches JSON schema"""
        try:
            import jsonschema
        except ImportError:
            raise ImportError("jsonschema required: pip install jsonschema")
        
        resp = response or self.response
        body = resp.json if hasattr(resp, 'json') else resp
        
        try:
            jsonschema.validate(body, schema)
        except jsonschema.ValidationError as e:
            raise AssertionError(f"JSON schema validation failed: {e.message}")
    
    def assert_response_contains_all(self, fields: List[str], response: Any = None):
        """Assert response contains all specified fields"""
        resp = response or self.response
        body = resp.json if hasattr(resp, 'json') else resp
        
        if not isinstance(body, dict):
            raise AssertionError("Response body is not a dictionary")
        
        missing = [f for f in fields if f not in body]
        assert not missing, f"Response missing fields: {missing}"
    
    def assert_response_contains_any(self, fields: List[str], response: Any = None):
        """Assert response contains at least one of specified fields"""
        resp = response or self.response
        body = resp.json if hasattr(resp, 'json') else resp
        
        if not isinstance(body, dict):
            raise AssertionError("Response body is not a dictionary")
        
        found = [f for f in fields if f in body]
        assert found, f"Response contains none of: {fields}"
    
    def assert_response_matches_regex(self, pattern: str, response: Any = None):
        """Assert response text matches regex pattern"""
        resp = response or self.response
        text = resp.text if hasattr(resp, 'text') else str(resp)
        
        regex = re.compile(pattern)
        assert regex.search(text), f"Response does not match pattern: {pattern}"
    
    def assert_response_not_matches_regex(self, pattern: str, response: Any = None):
        """Assert response text does not match regex pattern"""
        resp = response or self.response
        text = resp.text if hasattr(resp, 'text') else str(resp)
        
        regex = re.compile(pattern)
        assert not regex.search(text), f"Response matches pattern: {pattern}"
    
    def assert_array_length(self, length: int, path: str = "$", response: Any = None):
        """Assert array at path has specific length"""
        resp = response or self.response
        body = resp.json if hasattr(resp, 'json') else resp
        
        if path == "$":
            array = body
        else:
            array = self._get_by_path(body, path)
        
        assert isinstance(array, list), f"Value at {path} is not an array"
        assert len(array) == length, f"Array length {len(array)} != {length}"
    
    def assert_array_length_greater_than(self, min_length: int, path: str = "$", response: Any = None):
        """Assert array at path has length greater than minimum"""
        resp = response or self.response
        body = resp.json if hasattr(resp, 'json') else resp
        
        if path == "$":
            array = body
        else:
            array = self._get_by_path(body, path)
        
        assert isinstance(array, list), f"Value at {path} is not an array"
        assert len(array) > min_length, f"Array length {len(array)} not > {min_length}"
    
    def assert_array_contains(self, value: Any, path: str = "$", response: Any = None):
        """Assert array at path contains value"""
        resp = response or self.response
        body = resp.json if hasattr(resp, 'json') else resp
        
        if path == "$":
            array = body
        else:
            array = self._get_by_path(body, path)
        
        assert isinstance(array, list), f"Value at {path} is not an array"
        assert value in array, f"Array does not contain {value}"
    
    def assert_field_type(self, field_path: str, expected_type: type, response: Any = None):
        """Assert field has expected type"""
        resp = response or self.response
        body = resp.json if hasattr(resp, 'json') else resp
        
        value = self._get_by_path(body, field_path)
        actual_type = type(value)
        
        assert isinstance(value, expected_type), \
            f"Field {field_path} type {actual_type.__name__} != {expected_type.__name__}"
    
    def assert_field_not_null(self, field_path: str, response: Any = None):
        """Assert field is not null"""
        resp = response or self.response
        body = resp.json if hasattr(resp, 'json') else resp
        
        value = self._get_by_path(body, field_path)
        assert value is not None, f"Field {field_path} is null"
    
    def assert_field_matches_pattern(self, field_path: str, pattern: str, response: Any = None):
        """Assert field matches regex pattern"""
        resp = response or self.response
        body = resp.json if hasattr(resp, 'json') else resp
        
        value = self._get_by_path(body, field_path)
        regex = re.compile(pattern)
        
        assert regex.match(str(value)), \
            f"Field {field_path} value '{value}' does not match pattern {pattern}"
    
    def assert_field_in_range(self, field_path: str, min_val: float, max_val: float, response: Any = None):
        """Assert numeric field is in range"""
        resp = response or self.response
        body = resp.json if hasattr(resp, 'json') else resp
        
        value = self._get_by_path(body, field_path)
        assert isinstance(value, (int, float)), f"Field {field_path} is not numeric"
        assert min_val <= value <= max_val, \
            f"Field {field_path} value {value} not in range [{min_val}, {max_val}]"
    
    def assert_response_headers_contain(self, headers: Dict[str, str], response: Any = None):
        """Assert response contains all specified headers"""
        resp = response or self.response
        resp_headers = resp.headers if hasattr(resp, 'headers') else {}
        
        for key, expected_value in headers.items():
            assert key in resp_headers, f"Header '{key}' not found in response"
            actual_value = resp_headers[key]
            assert actual_value == expected_value, \
                f"Header '{key}' value '{actual_value}' != '{expected_value}'"
    
    @staticmethod
    def _get_by_path(obj: Any, path: str) -> Any:
        """Get value from object by dot notation path"""
        if path == "$":
            return obj
        
        keys = path.split(".")
        current = obj
        
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            elif isinstance(current, list):
                try:
                    index = int(key)
                    current = current[index]
                except (ValueError, IndexError):
                    return None
            else:
                return None
        
        return current
