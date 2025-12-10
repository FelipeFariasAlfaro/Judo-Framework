"""
Unit tests for Judo Framework core functionality
"""

import pytest
from judo import Judo, JudoResponse
from judo.core.matcher import Matcher
from judo.core.variables import VariableManager


class TestJudoCore:
    """Test core Judo functionality"""
    
    def setup_method(self):
        """Setup for each test"""
        self.judo = Judo()
    
    def test_variable_management(self):
        """Test variable operations"""
        # Set and get variables
        self.judo.set("testVar", "testValue")
        assert self.judo.get_var("testVar") == "testValue"
        
        # Set complex data
        test_data = {"key": "value", "number": 42}
        self.judo.set("complexVar", test_data)
        assert self.judo.get_var("complexVar") == test_data
        
        # Remove variable
        self.judo.remove("testVar")
        assert self.judo.get_var("testVar") is None
    
    def test_url_management(self):
        """Test URL handling"""
        # Set base URL
        self.judo.url = "https://api.example.com"
        assert self.judo.url == "https://api.example.com"
        
        # Build path
        full_url = self.judo.path("/users/1")
        assert full_url == "https://api.example.com/users/1"
    
    def test_header_management(self):
        """Test header operations"""
        # Set single header
        self.judo.header("Content-Type", "application/json")
        assert self.judo.http_client.default_headers["Content-Type"] == "application/json"
        
        # Set multiple headers
        headers = {
            "Authorization": "Bearer token",
            "X-Custom": "value"
        }
        self.judo.headers(headers)
        
        for key, value in headers.items():
            assert self.judo.http_client.default_headers[key] == value
    
    def test_utility_functions(self):
        """Test utility functions"""
        # UUID generation
        uuid_val = self.judo.uuid()
        assert len(uuid_val) == 36  # Standard UUID length
        
        # Random string
        random_str = self.judo.random_string(10)
        assert len(random_str) == 10
        
        # Random int
        random_int = self.judo.random_int(1, 100)
        assert 1 <= random_int <= 100
        
        # Timestamp
        timestamp = self.judo.timestamp()
        assert isinstance(timestamp, int)
        assert timestamp > 0


class TestMatcher:
    """Test matching functionality"""
    
    def setup_method(self):
        """Setup for each test"""
        self.judo = Judo()
        self.matcher = Matcher(self.judo)
    
    def test_exact_matching(self):
        """Test exact value matching"""
        assert self.matcher.match("hello", "hello")
        assert self.matcher.match(42, 42)
        assert self.matcher.match(True, True)
        assert not self.matcher.match("hello", "world")
    
    def test_special_matchers(self):
        """Test special matcher patterns"""
        # String matcher
        assert self.matcher.match("hello", "##string")
        assert not self.matcher.match(42, "##string")
        
        # Number matcher
        assert self.matcher.match(42, "##number")
        assert self.matcher.match(3.14, "##number")
        assert not self.matcher.match("hello", "##number")
        
        # Boolean matcher
        assert self.matcher.match(True, "##boolean")
        assert self.matcher.match(False, "##boolean")
        assert not self.matcher.match("true", "##boolean")
        
        # Array matcher
        assert self.matcher.match([1, 2, 3], "##array")
        assert not self.matcher.match("not array", "##array")
        
        # Object matcher
        assert self.matcher.match({"key": "value"}, "##object")
        assert not self.matcher.match("not object", "##object")
        
        # Null matchers
        assert self.matcher.match(None, "##null")
        assert self.matcher.match("value", "##notnull")
        assert not self.matcher.match(None, "##notnull")
    
    def test_parameterized_matchers(self):
        """Test parameterized matchers"""
        # String length
        assert self.matcher.match("hello", "##string[5]")
        assert not self.matcher.match("hi", "##string[5]")
        
        # String length range
        assert self.matcher.match("hello", "##string[3,10]")
        assert not self.matcher.match("hi", "##string[3,10]")
        
        # Number range
        assert self.matcher.match(50, "##number[1,100]")
        assert not self.matcher.match(150, "##number[1,100]")
        
        # Array size
        assert self.matcher.match([1, 2, 3], "##array[3]")
        assert not self.matcher.match([1, 2], "##array[3]")
    
    def test_list_matching(self):
        """Test list/array matching"""
        # Exact list match
        assert self.matcher.match([1, 2, 3], [1, 2, 3])
        assert not self.matcher.match([1, 2, 3], [1, 2, 4])
        
        # List with patterns
        assert self.matcher.match([1, "hello", True], ["##number", "##string", "##boolean"])
    
    def test_dict_matching(self):
        """Test dictionary/object matching"""
        # Exact dict match
        data = {"name": "John", "age": 30}
        pattern = {"name": "John", "age": 30}
        assert self.matcher.match(data, pattern)
        
        # Dict with patterns
        pattern = {"name": "##string", "age": "##number"}
        assert self.matcher.match(data, pattern)
    
    def test_contains_matching(self):
        """Test contains matching"""
        # List contains
        assert self.matcher.match_contains([1, 2, 3], 2)
        assert not self.matcher.match_contains([1, 2, 3], 4)
        
        # Dict contains
        data = {"name": "John", "age": 30, "city": "NYC"}
        pattern = {"name": "John", "age": 30}
        assert self.matcher.match_contains(data, pattern)
        
        # String contains
        assert self.matcher.match_contains("hello world", "world")
        assert not self.matcher.match_contains("hello", "world")


class TestVariableManager:
    """Test variable manager"""
    
    def setup_method(self):
        """Setup for each test"""
        self.vm = VariableManager()
    
    def test_basic_operations(self):
        """Test basic variable operations"""
        # Set and get
        self.vm.set("key", "value")
        assert self.vm.get("key") == "value"
        
        # Default value
        assert self.vm.get("nonexistent", "default") == "default"
        
        # Remove
        self.vm.remove("key")
        assert self.vm.get("key") is None
    
    def test_global_variables(self):
        """Test global variable handling"""
        self.vm.set_global("global_key", "global_value")
        assert self.vm.get("global_key") == "global_value"
        
        # Local overrides global
        self.vm.set("global_key", "local_value")
        assert self.vm.get("global_key") == "local_value"
    
    def test_interpolation(self):
        """Test variable interpolation"""
        self.vm.set("name", "John")
        self.vm.set("age", 30)
        
        # Simple interpolation
        result = self.vm.interpolate("Hello #{name}")
        assert result == "Hello John"
        
        # Multiple variables
        result = self.vm.interpolate("#{name} is #{age} years old")
        assert result == "John is 30 years old"
        
        # Non-existent variable
        result = self.vm.interpolate("Hello #{unknown}")
        assert result == "Hello #{unknown}"  # Should remain unchanged
    
    def test_dict_like_access(self):
        """Test dictionary-like access"""
        self.vm["key"] = "value"
        assert self.vm["key"] == "value"
        assert "key" in self.vm
        assert "nonexistent" not in self.vm


if __name__ == "__main__":
    pytest.main([__file__])