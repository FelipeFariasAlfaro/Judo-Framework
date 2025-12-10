"""
Matcher class - Comprehensive matching and validation engine
Implements Karate's powerful matching capabilities
"""

import re
import json
from typing import Any, Dict, List, Optional, Union
from jsonschema import validate, ValidationError


class Matcher:
    """
    Comprehensive matcher implementing Karate's matching logic
    """
    
    def __init__(self, judo_instance):
        self.judo = judo_instance
    
    def match(self, actual: Any, expected: Any) -> bool:
        """
        Main match method - implements Karate's match operator
        Supports all Karate matching patterns
        """
        try:
            return self._match_recursive(actual, expected)
        except Exception as e:
            self.judo.log(f"Match failed: {e}", "ERROR")
            return False
    
    def _match_recursive(self, actual: Any, expected: Any) -> bool:
        """Recursive matching logic"""
        
        # Handle special matchers (strings starting with ##)
        if isinstance(expected, str) and expected.startswith('##'):
            return self._match_special(actual, expected)
        
        # Handle regex patterns
        if isinstance(expected, str) and expected.startswith('#regex'):
            pattern = expected[6:].strip()
            return bool(re.match(pattern, str(actual)))
        
        # Handle JSONPath expressions
        if isinstance(expected, str) and expected.startswith('$.'):
            return self._match_jsonpath(actual, expected)
        
        # Handle schema validation
        if isinstance(expected, dict) and expected.get('type'):
            return self._match_schema(actual, expected)
        
        # Exact match for primitives
        if isinstance(expected, (str, int, float, bool)) and not isinstance(expected, str):
            return actual == expected
        
        # String exact match (unless it's a special pattern)
        if isinstance(expected, str) and not expected.startswith(('#', '$')):
            return str(actual) == expected
        
        # None/null matching
        if expected is None:
            return actual is None
        
        # List matching
        if isinstance(expected, list):
            return self._match_list(actual, expected)
        
        # Dictionary matching
        if isinstance(expected, dict):
            return self._match_dict(actual, expected)
        
        # Default exact match
        return actual == expected
    
    def _match_special(self, actual: Any, pattern: str) -> bool:
        """Handle special matchers like ##string, ##number, etc."""
        
        matchers = {
            '##string': lambda x: isinstance(x, str),
            '##number': lambda x: isinstance(x, (int, float)),
            '##boolean': lambda x: isinstance(x, bool),
            '##array': lambda x: isinstance(x, list),
            '##object': lambda x: isinstance(x, dict),
            '##null': lambda x: x is None,
            '##notnull': lambda x: x is not None,
            '##present': lambda x: x is not None,
            '##notpresent': lambda x: x is None,
            '##ignore': lambda x: True,
            '##uuid': lambda x: self._is_uuid(x),
            '##email': lambda x: self._is_email(x),
            '##url': lambda x: self._is_url(x),
            '##date': lambda x: self._is_date(x),
            '##datetime': lambda x: self._is_datetime(x),
        }
        
        # Handle parameterized matchers
        if pattern.startswith('##string['):
            # ##string[5] - exact length
            # ##string[3,10] - length range
            length_spec = pattern[9:-1]
            if ',' in length_spec:
                min_len, max_len = map(int, length_spec.split(','))
                return isinstance(actual, str) and min_len <= len(actual) <= max_len
            else:
                expected_len = int(length_spec)
                return isinstance(actual, str) and len(actual) == expected_len
        
        if pattern.startswith('##number['):
            # ##number[1,100] - number range
            range_spec = pattern[9:-1]
            min_val, max_val = map(float, range_spec.split(','))
            return isinstance(actual, (int, float)) and min_val <= actual <= max_val
        
        if pattern.startswith('##array['):
            # ##array[5] - exact size
            # ##array[1,10] - size range
            size_spec = pattern[8:-1]
            if ',' in size_spec:
                min_size, max_size = map(int, size_spec.split(','))
                return isinstance(actual, list) and min_size <= len(actual) <= max_size
            else:
                expected_size = int(size_spec)
                return isinstance(actual, list) and len(actual) == expected_size
        
        matcher_func = matchers.get(pattern)
        return matcher_func(actual) if matcher_func else False
    
    def _match_jsonpath(self, actual: Any, jsonpath: str) -> bool:
        """Match using JSONPath expression"""
        try:
            from jsonpath_ng import parse
            jsonpath_expr = parse(jsonpath)
            matches = [match.value for match in jsonpath_expr.find(actual)]
            return len(matches) > 0
        except Exception:
            return False
    
    def _match_schema(self, actual: Any, schema: Dict) -> bool:
        """Validate against JSON schema"""
        try:
            validate(instance=actual, schema=schema)
            return True
        except ValidationError:
            return False
    
    def _match_list(self, actual: Any, expected: List) -> bool:
        """Match lists/arrays"""
        if not isinstance(actual, list):
            return False
        
        if len(actual) != len(expected):
            return False
        
        for i, expected_item in enumerate(expected):
            if not self._match_recursive(actual[i], expected_item):
                return False
        
        return True
    
    def _match_dict(self, actual: Any, expected: Dict) -> bool:
        """Match dictionaries/objects"""
        if not isinstance(actual, dict):
            return False
        
        for key, expected_value in expected.items():
            if key not in actual:
                return False
            if not self._match_recursive(actual[key], expected_value):
                return False
        
        return True
    
    def match_contains(self, actual: Any, expected: Any) -> bool:
        """Match that actual contains expected"""
        if isinstance(actual, list):
            return any(self._match_recursive(item, expected) for item in actual)
        elif isinstance(actual, dict) and isinstance(expected, dict):
            for key, value in expected.items():
                if key not in actual or not self._match_recursive(actual[key], value):
                    return False
            return True
        elif isinstance(actual, str):
            return str(expected) in actual
        return False
    
    def match_contains_only(self, actual: List, expected: List) -> bool:
        """Match that actual contains only expected items (order doesn't matter)"""
        if not isinstance(actual, list) or not isinstance(expected, list):
            return False
        
        if len(actual) != len(expected):
            return False
        
        expected_copy = expected.copy()
        for item in actual:
            found = False
            for i, exp_item in enumerate(expected_copy):
                if self._match_recursive(item, exp_item):
                    expected_copy.pop(i)
                    found = True
                    break
            if not found:
                return False
        
        return len(expected_copy) == 0
    
    def match_contains_any(self, actual: List, expected: List) -> bool:
        """Match that actual contains any of expected items"""
        if not isinstance(actual, list) or not isinstance(expected, list):
            return False
        
        for exp_item in expected:
            if any(self._match_recursive(item, exp_item) for item in actual):
                return True
        
        return False
    
    def match_each(self, actual: List, expected: Any) -> bool:
        """Match each item in actual against expected pattern"""
        if not isinstance(actual, list):
            return False
        
        return all(self._match_recursive(item, expected) for item in actual)
    
    # Helper methods for special matchers
    
    def _is_uuid(self, value: str) -> bool:
        """Check if value is a valid UUID"""
        import uuid
        try:
            uuid.UUID(str(value))
            return True
        except ValueError:
            return False
    
    def _is_email(self, value: str) -> bool:
        """Check if value is a valid email"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, str(value)))
    
    def _is_url(self, value: str) -> bool:
        """Check if value is a valid URL"""
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(url_pattern, str(value)))
    
    def _is_date(self, value: str) -> bool:
        """Check if value is a valid date (YYYY-MM-DD)"""
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        return bool(re.match(date_pattern, str(value)))
    
    def _is_datetime(self, value: str) -> bool:
        """Check if value is a valid datetime (ISO format)"""
        datetime_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
        return bool(re.match(datetime_pattern, str(value)))