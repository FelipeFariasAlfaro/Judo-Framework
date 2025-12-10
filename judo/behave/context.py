"""
Behave Context Integration
Provides Judo Framework integration with Behave context
"""

from judo import Judo
from typing import Any, Dict, Optional


class JudoContext:
    """
    Enhanced context for Behave integration with Judo Framework
    Provides seamless integration between Gherkin steps and Judo DSL
    """
    
    def __init__(self, behave_context=None):
        """Initialize Judo context"""
        self.behave_context = behave_context
        self.judo = Judo()
        self.response = None
        self.variables = {}
        self.test_data = {}
        
        # Initialize default configuration
        self._setup_defaults()
    
    def _setup_defaults(self):
        """Setup default configuration"""
        # Set default headers
        self.judo.headers({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Judo-Framework-Behave/1.0"
        })
    
    # URL Management
    def set_base_url(self, url: str):
        """Set base URL for API calls"""
        self.judo.url = url
        self.variables['baseUrl'] = url
    
    def get_base_url(self) -> str:
        """Get current base URL"""
        return self.judo.url
    
    # Variable Management
    def set_variable(self, name: str, value: Any):
        """Set a variable"""
        self.variables[name] = value
        self.judo.set(name, value)
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """Get a variable"""
        return self.variables.get(name, self.judo.get_var(name, default))
    
    def interpolate_string(self, text: str) -> str:
        """Interpolate variables in string"""
        result = text
        for key, value in self.variables.items():
            result = result.replace(f"{{{key}}}", str(value))
            result = result.replace(f"${{{key}}}", str(value))
        return result
    
    # HTTP Methods
    def make_request(self, method: str, endpoint: str, **kwargs):
        """Make HTTP request and store response"""
        method = method.upper()
        
        # Interpolate endpoint
        endpoint = self.interpolate_string(endpoint)
        
        # Make request based on method
        if method == 'GET':
            self.response = self.judo.get(endpoint, **kwargs)
        elif method == 'POST':
            self.response = self.judo.post(endpoint, **kwargs)
        elif method == 'PUT':
            self.response = self.judo.put(endpoint, **kwargs)
        elif method == 'PATCH':
            self.response = self.judo.patch(endpoint, **kwargs)
        elif method == 'DELETE':
            self.response = self.judo.delete(endpoint, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        return self.response
    
    # Response Validation
    def validate_status(self, expected_status: int):
        """Validate response status code"""
        if not self.response:
            raise AssertionError("No response available. Make a request first.")
        
        actual_status = self.response.status
        assert actual_status == expected_status, \
            f"Expected status {expected_status}, but got {actual_status}"
    
    def validate_json_path(self, json_path: str, expected_value: Any):
        """Validate JSON response using JSONPath"""
        if not self.response:
            raise AssertionError("No response available. Make a request first.")
        
        actual_value = self.judo.json_path(self.response.json, json_path)
        
        # Use Judo's matcher for validation
        assert self.judo.match(actual_value, expected_value), \
            f"JSONPath {json_path}: expected {expected_value}, but got {actual_value}"
    
    def validate_response_contains(self, key: str, expected_value: Any = None):
        """Validate that response contains a key or key-value pair"""
        if not self.response:
            raise AssertionError("No response available. Make a request first.")
        
        json_data = self.response.json
        
        if isinstance(json_data, dict):
            assert key in json_data, f"Response does not contain key: {key}"
            
            if expected_value is not None:
                actual_value = json_data[key]
                assert self.judo.match(actual_value, expected_value), \
                    f"Key {key}: expected {expected_value}, but got {actual_value}"
        else:
            raise AssertionError("Response is not a JSON object")
    
    def validate_response_schema(self, schema: Dict):
        """Validate response against JSON schema"""
        if not self.response:
            raise AssertionError("No response available. Make a request first.")
        
        assert self.judo.match(self.response.json, schema), \
            "Response does not match expected schema"
    
    # Authentication
    def set_auth_header(self, auth_type: str, token: str):
        """Set authentication header"""
        if auth_type.lower() == 'bearer':
            self.judo.bearer_token(token)
        elif auth_type.lower() == 'basic':
            # Assume token is base64 encoded username:password
            self.judo.header('Authorization', f'Basic {token}')
        else:
            self.judo.header('Authorization', f'{auth_type} {token}')
    
    def set_basic_auth(self, username: str, password: str):
        """Set basic authentication"""
        self.judo.basic_auth(username, password)
    
    # Headers and Parameters
    def set_header(self, name: str, value: str):
        """Set request header"""
        value = self.interpolate_string(value)
        self.judo.header(name, value)
    
    def set_query_param(self, name: str, value: Any):
        """Set query parameter"""
        self.judo.param(name, value)
    
    # Test Data Management
    def load_test_data(self, data_name: str, data: Dict):
        """Load test data for use in scenarios"""
        self.test_data[data_name] = data
    
    def get_test_data(self, data_name: str) -> Dict:
        """Get test data by name"""
        return self.test_data.get(data_name, {})
    
    def load_test_data_from_file(self, data_name: str, file_path: str):
        """Load test data from file"""
        data = self.judo.read(file_path)
        self.test_data[data_name] = data
        return data
    
    # File Operations
    def read_file(self, file_path: str) -> Any:
        """Read file using Judo's file loader"""
        return self.judo.read(file_path)
    
    def read_json_file(self, file_path: str) -> Any:
        """Read JSON file"""
        return self.judo.read_json(file_path)
    
    def read_yaml_file(self, file_path: str) -> Any:
        """Read YAML file"""
        return self.judo.read_yaml(file_path)
    
    # Utility Methods
    def wait(self, seconds: float):
        """Wait for specified seconds"""
        self.judo.sleep(seconds)
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message"""
        self.judo.log(message, level)
        if self.behave_context:
            print(f"[{level}] {message}")
    
    def print_response(self):
        """Print current response for debugging"""
        if self.response:
            print(self.response.pretty_print())
        else:
            print("No response available")
    
    def reset(self):
        """Reset context for new scenario"""
        self.response = None
        self.variables.clear()
        self.test_data.clear()
        
        # Reset HTTP client state
        self.judo.http_client.default_headers.clear()
        self.judo.http_client.default_params.clear()
        self.judo.http_client.default_cookies.clear()
        
        # Re-setup defaults
        self._setup_defaults()