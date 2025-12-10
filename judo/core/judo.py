"""
Main Judo class - Core framework implementation
Provides the complete DSL interface similar to Karate Framework
"""

import json
import os
import time
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin, urlparse

from ..http.client import HttpClient
from ..core.response import JudoResponse
from ..core.matcher import Matcher
from ..core.variables import VariableManager
from ..utils.helpers import *
from ..mock.server import MockServer
from ..reporting.reporter import get_reporter


class Judo:
    """
    Main Judo Framework class providing complete Karate-like DSL
    """
    
    def __init__(self, base_url: str = None, config: Dict = None, enable_reporting: bool = True):
        """Initialize Judo instance"""
        self.config = config or {}
        self.base_url = base_url
        self.variables = VariableManager()
        self.http_client = HttpClient(self)
        self.matcher = Matcher(self)
        self.mock_server = None
        self.enable_reporting = enable_reporting
        self.reporter = get_reporter() if enable_reporting else None
        
        # Initialize default variables
        self._init_default_vars()
    
    def _init_default_vars(self):
        """Initialize default variables"""
        self.variables.set("karate.env", os.getenv("KARATE_ENV", "dev"))
        self.variables.set("karate.properties", {})
        
    # ==================== URL Management ====================
    
    @property
    def url(self) -> str:
        """Get current base URL"""
        return self.base_url
    
    @url.setter  
    def url(self, value: str):
        """Set base URL"""
        self.base_url = value
        
    def path(self, path_segment: str) -> str:
        """Build URL path"""
        if self.base_url:
            return urljoin(self.base_url, path_segment)
        return path_segment
    
    # ==================== Variable Management ====================
    
    def set(self, name: str, value: Any) -> None:
        """Set variable (equivalent to Karate's * def)"""
        self.variables.set(name, value)
        
        # Log variable assignment to reporter
        if self.reporter:
            self.reporter.log_variable_set(name, value)
    
    def get_var(self, name: str, default: Any = None) -> Any:
        """Get variable value"""
        value = self.variables.get(name, default)
        
        # Log variable usage to reporter
        if self.reporter and value is not None:
            self.reporter.log_variable_used(name, value)
        
        return value
    
    def remove(self, name: str) -> None:
        """Remove variable"""
        self.variables.remove(name)
        
    def get_env(self, name: str, default: str = None) -> str:
        """Get environment variable"""
        return os.getenv(name, default)
    
    # ==================== HTTP Methods ====================
    
    def get(self, url: str, **kwargs) -> JudoResponse:
        """HTTP GET request"""
        return self.http_client.get(url, **kwargs)
    
    def post(self, url: str, **kwargs) -> JudoResponse:
        """HTTP POST request"""
        return self.http_client.post(url, **kwargs)
    
    def put(self, url: str, **kwargs) -> JudoResponse:
        """HTTP PUT request"""
        return self.http_client.put(url, **kwargs)
    
    def patch(self, url: str, **kwargs) -> JudoResponse:
        """HTTP PATCH request"""
        return self.http_client.patch(url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> JudoResponse:
        """HTTP DELETE request"""
        return self.http_client.delete(url, **kwargs)
    
    def head(self, url: str, **kwargs) -> JudoResponse:
        """HTTP HEAD request"""
        return self.http_client.head(url, **kwargs)
    
    def options(self, url: str, **kwargs) -> JudoResponse:
        """HTTP OPTIONS request"""
        return self.http_client.options(url, **kwargs)
    
    # ==================== Request Configuration ====================
    
    def header(self, name: str, value: str) -> None:
        """Set request header"""
        self.http_client.set_header(name, value)
    
    def headers(self, headers_dict: Dict[str, str]) -> None:
        """Set multiple headers"""
        self.http_client.set_headers(headers_dict)
    
    def param(self, name: str, value: Any) -> None:
        """Set query parameter"""
        self.http_client.set_param(name, value)
    
    def params(self, params_dict: Dict[str, Any]) -> None:
        """Set multiple query parameters"""
        self.http_client.set_params(params_dict)
    
    def cookie(self, name: str, value: str) -> None:
        """Set cookie"""
        self.http_client.set_cookie(name, value)
    
    def cookies(self, cookies_dict: Dict[str, str]) -> None:
        """Set multiple cookies"""
        self.http_client.set_cookies(cookies_dict)
    
    def form_field(self, name: str, value: Any) -> None:
        """Set form field"""
        self.http_client.set_form_field(name, value)
    
    def multipart_field(self, name: str, value: Any, filename: str = None) -> None:
        """Set multipart form field"""
        self.http_client.set_multipart_field(name, value, filename)
    
    # ==================== Authentication ====================
    
    def basic_auth(self, username: str, password: str) -> None:
        """Set basic authentication"""
        self.http_client.set_basic_auth(username, password)
    
    def bearer_token(self, token: str) -> None:
        """Set bearer token authentication"""
        self.http_client.set_bearer_token(token)
    
    def oauth2(self, token: str) -> None:
        """Set OAuth2 token"""
        self.bearer_token(token)
    
    # ==================== Validation/Matching ====================
    
    def match(self, actual: Any, expected: Any) -> bool:
        """Match actual value against expected (Karate's match operator)"""
        result = self.matcher.match(actual, expected)
        
        # Log assertion to reporter
        if self.reporter:
            self.reporter.log_assertion(
                description=f"match({actual}, {expected})",
                expected=expected,
                actual=actual,
                passed=result
            )
        
        return result
    
    def match_contains(self, actual: Any, expected: Any) -> bool:
        """Match that actual contains expected"""
        return self.matcher.match_contains(actual, expected)
    
    def match_contains_only(self, actual: List, expected: List) -> bool:
        """Match that actual contains only expected items"""
        return self.matcher.match_contains_only(actual, expected)
    
    def match_contains_any(self, actual: List, expected: List) -> bool:
        """Match that actual contains any of expected items"""
        return self.matcher.match_contains_any(actual, expected)
    
    def match_each(self, actual: List, expected: Any) -> bool:
        """Match each item in actual against expected"""
        return self.matcher.match_each(actual, expected)
    
    # ==================== JSON/XML Processing ====================
    
    def json_path(self, json_data: Any, path: str) -> Any:
        """Extract value using JSONPath"""
        from jsonpath_ng import parse
        jsonpath_expr = parse(path)
        matches = [match.value for match in jsonpath_expr.find(json_data)]
        return matches[0] if len(matches) == 1 else matches
    
    def xml_path(self, xml_data: str, xpath: str) -> Any:
        """Extract value using XPath"""
        from lxml import etree
        root = etree.fromstring(xml_data.encode())
        results = root.xpath(xpath)
        return results[0] if len(results) == 1 else results
    
    # ==================== Utility Methods ====================
    
    def sleep(self, seconds: float) -> None:
        """Sleep for specified seconds"""
        time.sleep(seconds)
    
    def print(self, *args) -> None:
        """Print values (for debugging)"""
        print(*args)
    
    def log(self, message: str, level: str = "INFO") -> None:
        """Log message"""
        print(f"[{level}] {message}")
    
    def uuid(self) -> str:
        """Generate UUID"""
        import uuid
        return str(uuid.uuid4())
    
    def random_string(self, length: int = 10) -> str:
        """Generate random string"""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def random_int(self, min_val: int = 0, max_val: int = 100) -> int:
        """Generate random integer"""
        import random
        return random.randint(min_val, max_val)
    
    def timestamp(self) -> int:
        """Get current timestamp"""
        return int(time.time())
    
    def format_date(self, format_str: str = "%Y-%m-%d") -> str:
        """Format current date"""
        from datetime import datetime
        return datetime.now().strftime(format_str)
    
    # ==================== File Operations ====================
    
    def read(self, filepath: str) -> Any:
        """
        Read file and auto-detect format (Karate-style)
        Supports JSON, YAML, CSV, and text files
        """
        from ..utils.file_loader import read
        return read(filepath)
    
    def read_file(self, filepath: str) -> str:
        """Read file content"""
        from ..utils.file_loader import read_text
        return read_text(filepath)
    
    def read_json(self, filepath: str) -> Any:
        """Read JSON file"""
        from ..utils.file_loader import read_json
        return read_json(filepath)
    
    def read_yaml(self, filepath: str) -> Any:
        """Read YAML file"""
        from ..utils.file_loader import read_yaml
        return read_yaml(filepath)
    
    def read_csv(self, filepath: str) -> List[Dict]:
        """Read CSV file"""
        from ..utils.file_loader import read_csv
        return read_csv(filepath)
    
    def write_file(self, filepath: str, content: str) -> None:
        """Write content to file"""
        from ..utils.file_loader import write_text
        write_text(content, filepath)
    
    def write_json(self, filepath: str, data: Any) -> None:
        """Write data to JSON file"""
        from ..utils.file_loader import write_json
        write_json(data, filepath)
    
    def write_yaml(self, filepath: str, data: Any) -> None:
        """Write data to YAML file"""
        from ..utils.file_loader import write_yaml
        write_yaml(data, filepath)
    
    def file_exists(self, filepath: str) -> bool:
        """Check if file exists"""
        from ..utils.file_loader import file_exists
        return file_exists(filepath)
    
    # ==================== Mock Server ====================
    
    def start_mock(self, port: int = 8080) -> MockServer:
        """Start mock server"""
        if not self.mock_server:
            self.mock_server = MockServer(port)
        self.mock_server.start()
        return self.mock_server
    
    def stop_mock(self) -> None:
        """Stop mock server"""
        if self.mock_server:
            self.mock_server.stop()
    
    # ==================== Configuration ====================
    
    def configure(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    # ==================== Reporting ====================
    
    def start_scenario(self, name: str, tags: list = None):
        """Start a new test scenario for reporting"""
        if self.reporter:
            return self.reporter.start_scenario(name, tags)
    
    def start_step(self, step_text: str):
        """Start a new test step for reporting"""
        if self.reporter:
            return self.reporter.start_step(step_text)
    
    def finish_step(self, passed: bool = True, error_message: str = None):
        """Finish current test step"""
        if self.reporter:
            from ..reporting.report_data import StepStatus
            status = StepStatus.PASSED if passed else StepStatus.FAILED
            self.reporter.finish_step(status, error_message)
    
    def finish_scenario(self, passed: bool = True, error_message: str = None):
        """Finish current test scenario"""
        if self.reporter:
            from ..reporting.report_data import ScenarioStatus
            status = ScenarioStatus.PASSED if passed else ScenarioStatus.FAILED
            self.reporter.finish_scenario(status, error_message)
    
    def generate_html_report(self, filename: str = None) -> str:
        """Generate HTML test report"""
        if self.reporter:
            return self.reporter.generate_html_report(filename)
        return None