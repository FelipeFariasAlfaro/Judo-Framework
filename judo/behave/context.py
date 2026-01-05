"""
Behave Context Integration
Provides Judo Framework integration with Behave context
"""

import os
from pathlib import Path
from judo import Judo
from typing import Any, Dict, Optional


def _load_env_file():
    """
    Load .env file from project root first, then from current directory.
    By convention, .env files are always in the project root.
    """
    try:
        from dotenv import load_dotenv
        
        # Try to find project root by looking for common markers
        current_dir = Path.cwd()
        project_root = None
        
        # Look for project root markers (features/, setup.py, pyproject.toml, .git/)
        for parent in [current_dir] + list(current_dir.parents):
            if any([
                (parent / 'features').exists(),
                (parent / 'setup.py').exists(),
                (parent / 'pyproject.toml').exists(),
                (parent / '.git').exists(),
            ]):
                project_root = parent
                break
        
        # Try loading from project root first
        if project_root:
            env_path = project_root / '.env'
            if env_path.exists():
                load_dotenv(dotenv_path=env_path)
                return
        
        # Fallback: load from current directory
        load_dotenv()
        
    except ImportError:
        # python-dotenv not installed, just use os.getenv
        pass


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
        
        # Request/Response logging configuration
        self.save_requests_responses = False
        self.output_directory = None
        self.current_scenario_name = None
        self.request_counter = 0
        
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
        
        # Configure request/response logging from environment variables
        import os
        self.save_requests_responses = os.getenv('JUDO_SAVE_REQUESTS_RESPONSES', 'false').lower() == 'true'
        self.output_directory = os.getenv('JUDO_OUTPUT_DIRECTORY', 'judo_output')
    
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
    
    # Request/Response Logging Configuration
    def configure_request_response_logging(self, enabled: bool, output_directory: str = None):
        """
        Configure automatic request/response logging
        
        Args:
            enabled: True to enable logging, False to disable
            output_directory: Directory where to save the files (default: 'judo_output')
        """
        self.save_requests_responses = enabled
        if output_directory:
            self.output_directory = output_directory
        
        if enabled and not self.output_directory:
            self.output_directory = 'judo_output'
    
    def set_current_scenario(self, scenario_name: str):
        """Set the current scenario name for file organization"""
        self.current_scenario_name = scenario_name
        self.request_counter = 0  # Reset counter for new scenario
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize scenario name for use as directory name"""
        import re
        # Remove or replace invalid characters for filenames
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
        # Replace spaces with underscores
        sanitized = sanitized.replace(' ', '_')
        # Remove multiple consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        return sanitized
    
    def _save_request_response(self, method: str, endpoint: str, request_data: dict, response_data: dict):
        """
        Save request and response data to JSON files
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            request_data: Request data including headers, body, etc.
            response_data: Response data including status, headers, body, etc.
        """
        if not self.save_requests_responses or not self.current_scenario_name:
            return
        
        import os
        import json
        from pathlib import Path
        from datetime import datetime
        
        try:
            # Create directory structure: output_dir/scenario_name/
            scenario_dir_name = self._sanitize_filename(self.current_scenario_name)
            scenario_path = Path(self.output_directory) / scenario_dir_name
            scenario_path.mkdir(parents=True, exist_ok=True)
            
            # Increment counter for this request
            self.request_counter += 1
            
            # Create filenames with counter and method
            timestamp = datetime.now().strftime("%H%M%S")
            base_filename = f"{self.request_counter:02d}_{method}_{timestamp}"
            
            request_filename = f"{base_filename}_request.json"
            response_filename = f"{base_filename}_response.json"
            
            # Save request
            request_path = scenario_path / request_filename
            with open(request_path, 'w', encoding='utf-8') as f:
                json.dump(request_data, f, indent=2, ensure_ascii=False, default=str)
            
            # Save response
            response_path = scenario_path / response_filename
            with open(response_path, 'w', encoding='utf-8') as f:
                json.dump(response_data, f, indent=2, ensure_ascii=False, default=str)
            
            # Log the saved files (optional, can be enabled with environment variable)
            if os.getenv('JUDO_LOG_SAVED_FILES', 'false').lower() == 'true':
                print(f"💾 Saved request: {request_path}")
                print(f"💾 Saved response: {response_path}")
                print(f"📁 Files saved in: {scenario_path}")
                
        except Exception as e:
            # Don't fail the test if logging fails, just log the error
            print(f"⚠️ Warning: Could not save request/response files: {e}")
    
    # HTTP Methods
    def make_request(self, method: str, endpoint: str, **kwargs):
        """Make HTTP request and store response"""
        method = method.upper()
        
        # Interpolate endpoint
        endpoint = self.interpolate_string(endpoint)
        
        # Apply chaos engineering if enabled
        if hasattr(self, 'chaos_injector') and self.chaos_injector.enabled:
            # Apply latency
            self.chaos_injector.apply_latency()
            
            # Check if error should be injected
            if self.chaos_injector.should_inject_error():
                raise Exception(f"Chaos Engineering: Simulated error (error rate: {self.chaos_injector.error_rate * 100}%)")
            
            # Check if timeout should be injected
            if self.chaos_injector.should_inject_timeout():
                raise TimeoutError(f"Chaos Engineering: Simulated timeout")
        
        # Apply rate limiting if configured
        if hasattr(self, 'rate_limiter'):
            self.rate_limiter.wait_if_needed()
        
        # Apply throttling if configured
        if hasattr(self, 'throttle'):
            self.throttle.wait_if_needed()
        
        # Apply adaptive rate limiting if configured
        if hasattr(self, 'adaptive_rate_limiter'):
            self.adaptive_rate_limiter.wait_if_needed()
        
        # Prepare request data for logging
        request_data = None
        if self.save_requests_responses:
            # Capture all headers (default + any additional from kwargs)
            all_headers = {}
            
            # Get default headers from Judo client
            if hasattr(self.judo.http_client, 'default_headers'):
                all_headers.update(dict(self.judo.http_client.default_headers))
            
            # Add any headers from kwargs
            if 'headers' in kwargs:
                all_headers.update(kwargs['headers'])
            
            # Get query parameters
            all_params = {}
            if hasattr(self.judo.http_client, 'default_params'):
                all_params.update(dict(self.judo.http_client.default_params))
            if 'params' in kwargs:
                all_params.update(kwargs['params'])
            
            request_data = {
                "method": method,
                "url": f"{self.judo.url}{endpoint}" if self.judo.url else endpoint,
                "endpoint": endpoint,
                "headers": all_headers,
                "query_parameters": all_params,
                "timestamp": self._get_timestamp(),
                "scenario": self.current_scenario_name
            }
            
            # Add body data if present
            if 'json' in kwargs:
                request_data['body'] = kwargs['json']
                request_data['body_type'] = 'application/json'
            elif 'data' in kwargs:
                request_data['body'] = kwargs['data']
                request_data['body_type'] = 'application/x-www-form-urlencoded'
            elif 'files' in kwargs:
                request_data['files'] = str(kwargs['files'])  # Convert to string for JSON serialization
                request_data['body_type'] = 'multipart/form-data'
            else:
                request_data['body'] = None
                request_data['body_type'] = None
        
        # Check cache for GET requests
        if method == 'GET' and hasattr(self, 'response_cache'):
            cached_response = self.response_cache.get(method, endpoint, kwargs.get('params'))
            if cached_response:
                self.response = cached_response
                return
        
        # Make request based on method (with retry if configured)
        try:
            if method == 'GET':
                if hasattr(self, 'retry_policy'):
                    self.response = self.retry_policy.execute(self.judo.get, endpoint, **kwargs)
                else:
                    self.response = self.judo.get(endpoint, **kwargs)
            elif method == 'POST':
                if hasattr(self, 'retry_policy'):
                    self.response = self.retry_policy.execute(self.judo.post, endpoint, **kwargs)
                else:
                    self.response = self.judo.post(endpoint, **kwargs)
            elif method == 'PUT':
                if hasattr(self, 'retry_policy'):
                    self.response = self.retry_policy.execute(self.judo.put, endpoint, **kwargs)
                else:
                    self.response = self.judo.put(endpoint, **kwargs)
            elif method == 'PATCH':
                if hasattr(self, 'retry_policy'):
                    self.response = self.retry_policy.execute(self.judo.patch, endpoint, **kwargs)
                else:
                    self.response = self.judo.patch(endpoint, **kwargs)
            elif method == 'DELETE':
                if hasattr(self, 'retry_policy'):
                    self.response = self.retry_policy.execute(self.judo.delete, endpoint, **kwargs)
                else:
                    self.response = self.judo.delete(endpoint, **kwargs)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        except Exception as e:
            # If chaos engineering injected an error, re-raise it
            if "Chaos Engineering" in str(e):
                raise
            # Otherwise, let it propagate
            raise
        
        # Cache GET responses
        if method == 'GET' and hasattr(self, 'response_cache') and self.response:
            self.response_cache.set(method, endpoint, self.response, kwargs.get('params'))
        
        # Always capture request/response data for HTML reports (regardless of file logging)
        if self.response:
            # Capture all headers (default + any additional from kwargs)
            all_headers = {}
            
            # Get default headers from Judo client
            if hasattr(self.judo.http_client, 'default_headers'):
                all_headers.update(dict(self.judo.http_client.default_headers))
            
            # Add any headers from kwargs
            if 'headers' in kwargs:
                all_headers.update(kwargs['headers'])
            
            # Get query parameters
            all_params = {}
            if hasattr(self.judo.http_client, 'default_params'):
                all_params.update(dict(self.judo.http_client.default_params))
            if 'params' in kwargs:
                all_params.update(kwargs['params'])
            
            # Prepare request data for HTML report
            html_request_data = {
                "method": method,
                "url": f"{self.judo.url}{endpoint}" if self.judo.url else endpoint,
                "endpoint": endpoint,
                "headers": all_headers,
                "query_parameters": all_params,
                "timestamp": self._get_timestamp(),
                "scenario": self.current_scenario_name
            }
            
            # Add body data if present
            if 'json' in kwargs:
                html_request_data['body'] = kwargs['json']
                html_request_data['body_type'] = 'application/json'
            elif 'data' in kwargs:
                html_request_data['body'] = kwargs['data']
                html_request_data['body_type'] = 'application/x-www-form-urlencoded'
            elif 'files' in kwargs:
                html_request_data['files'] = str(kwargs['files'])  # Convert to string for JSON serialization
                html_request_data['body_type'] = 'multipart/form-data'
            else:
                html_request_data['body'] = None
                html_request_data['body_type'] = None
            
            # Capture response headers with better handling
            response_headers = {}
            if hasattr(self.response, 'headers') and self.response.headers:
                response_headers = dict(self.response.headers)
            
            # Determine content type from response
            content_type = response_headers.get('content-type', response_headers.get('Content-Type', 'unknown'))
            
            # Try to parse JSON body safely
            json_body = None
            text_body = None
            
            try:
                if hasattr(self.response, 'json') and self.response.json is not None:
                    json_body = self.response.json
                if hasattr(self.response, 'text') and self.response.text is not None:
                    text_body = self.response.text
            except Exception:
                # If JSON parsing fails, just capture as text
                if hasattr(self.response, 'text'):
                    text_body = self.response.text
            
            html_response_data = {
                "status_code": self.response.status,
                "status_text": getattr(self.response, 'reason', 'Unknown'),
                "headers": response_headers,
                "content_type": content_type,
                "body": json_body,
                "text": text_body,
                "size_bytes": len(text_body.encode('utf-8')) if text_body else 0,
                "elapsed_ms": getattr(self.response, 'elapsed', 0) * 1000 if hasattr(self.response, 'elapsed') else 0,
                "timestamp": self._get_timestamp(),
                "scenario": self.current_scenario_name
            }
            
            # Send data to HTML reporter system
            try:
                from ..reporting.reporter import get_reporter
                reporter = get_reporter()
                
                # Debug: Log reporter state (can be enabled with JUDO_DEBUG_REPORTER env var)
                debug_enabled = os.getenv('JUDO_DEBUG_REPORTER', 'false').lower() == 'true'
                if debug_enabled:
                    print(f"[DEBUG] Reporter: {reporter is not None}")
                    if reporter:
                        print(f"[DEBUG] Current step: {reporter.current_step is not None}")
                        if reporter.current_step:
                            print(f"[DEBUG] Step text: {reporter.current_step.step_text}")
                
                if reporter and reporter.current_step:
                    # Add request data to current step
                    from ..reporting.report_data import RequestData, ResponseData
                    
                    # Create RequestData object
                    request_obj = RequestData(
                        method=method,
                        url=html_request_data['url'],
                        headers=all_headers,
                        params=all_params,
                        body=html_request_data.get('body'),
                        body_type=html_request_data.get('body_type', 'json')
                    )
                    
                    # Create ResponseData object
                    response_obj = ResponseData(
                        status_code=self.response.status,
                        headers=response_headers,
                        body=json_body,
                        body_type=content_type,
                        elapsed_time=getattr(self.response, 'elapsed', 0)
                    )
                    
                    # Add to current step
                    reporter.current_step.request_data = request_obj
                    reporter.current_step.response_data = response_obj
                    
                    if debug_enabled:
                        print(f"[DEBUG] Request/Response data added to step")
                        
                elif reporter:
                    if debug_enabled:
                        print(f"[DEBUG] ❌ Reporter exists but current_step is None")
                else:
                    if debug_enabled:
                        print(f"[DEBUG] ❌ No reporter available")
                    
            except Exception as e:
                # Don't fail the test if reporter integration fails
                print(f"⚠️ Warning: Could not integrate with HTML reporter: {e}")
                import traceback
                if os.getenv('JUDO_DEBUG_REPORTER', 'false').lower() == 'true':
                    traceback.print_exc()
            
            # Save to files if logging is enabled
            if self.save_requests_responses and request_data:
                self._save_request_response(method, endpoint, request_data, html_response_data)
            
            # Record performance metrics if performance monitor is enabled
            if hasattr(self, 'performance_monitor'):
                elapsed_ms = html_response_data.get('elapsed_ms', 0)
                status_code = self.response.status
                error = None
                
                # Check if there was an error
                if status_code >= 400:
                    error = f"HTTP {status_code}"
                
                self.performance_monitor.record_request(elapsed_ms, status_code, error)
        
        return self.response
    
    def _get_timestamp(self):
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
    
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
    
    def set_header_from_env(self, header_name: str, env_var_name: str):
        """
        Set request header from environment variable (.env file)
        
        Args:
            header_name: Name of the header to set
            env_var_name: Name of the environment variable to read from
        """
        import os
        
        # Load .env file from project root
        _load_env_file()
        
        value = os.getenv(env_var_name)
        if value is None:
            raise ValueError(f"Environment variable '{env_var_name}' not found in .env file or environment")
        
        self.judo.header(header_name, value)
    
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
        # Preserve logging configuration
        save_logging_config = self.save_requests_responses
        save_output_dir = self.output_directory
        
        self.response = None
        self.variables.clear()
        self.test_data.clear()
        
        # Reset HTTP client state
        self.judo.http_client.default_headers.clear()
        self.judo.http_client.default_params.clear()
        self.judo.http_client.default_cookies.clear()
        
        # Re-setup defaults
        self._setup_defaults()
        
        # Restore logging configuration (in case _setup_defaults changed it)
        self.save_requests_responses = save_logging_config
        self.output_directory = save_output_dir
        
        # Note: current_scenario_name is NOT reset here - it will be set by the hook