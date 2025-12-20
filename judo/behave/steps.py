"""
Behave Step Definitions for Judo Framework
Provides comprehensive Gherkin step definitions for API testing
"""

import json
import yaml
import traceback
from behave import given, when, then, step
from .context import JudoContext
from ..reporting.reporter import get_reporter
from ..reporting.report_data import StepStatus


# Context Setup Steps

@step('I have a Judo API client')
def step_setup_judo_client(context):
    """Initialize Judo context"""
    if not hasattr(context, 'judo_context'):
        context.judo_context = JudoContext(context)


# Additional missing step definitions for showcase compatibility


@step('the base URL is "{base_url}"')
def step_set_base_url(context, base_url):
    """Set the base URL for API calls"""
    if not hasattr(context, 'judo_context'):
        context.judo_context = JudoContext(context)
    context.judo_context.set_base_url(base_url)


@step('I set the variable "{name}" to "{value}"')
def step_set_variable_string(context, name, value):
    """Set a string variable"""
    context.judo_context.set_variable(name, value)


@step('I set the variable "{name}" to {value:d}')
def step_set_variable_int(context, name, value):
    """Set an integer variable"""
    context.judo_context.set_variable(name, value)


@step('I set the variable "{name}" to the JSON')
def step_set_variable_json(context, name):
    """Set a variable to JSON data from step text"""
    json_data = json.loads(context.text)
    context.judo_context.set_variable(name, json_data)


# Authentication Steps

@step('I use bearer token "{token}"')
def step_set_bearer_token(context, token):
    """Set bearer token authentication"""
    token = context.judo_context.interpolate_string(token)
    context.judo_context.set_auth_header('Bearer', token)


@step('I use basic authentication with username "{username}" and password "{password}"')
def step_set_basic_auth(context, username, password):
    """Set basic authentication"""
    username = context.judo_context.interpolate_string(username)
    password = context.judo_context.interpolate_string(password)
    context.judo_context.set_basic_auth(username, password)


@step('I set the header "{name}" to "{value}"')
def step_set_header(context, name, value):
    """Set a request header"""
    value = context.judo_context.interpolate_string(value)
    context.judo_context.set_header(name, value)


@step('I set the header "{header_name}" from env "{env_var_name}"')
def step_set_header_from_env(context, header_name, env_var_name):
    """Set a request header from environment variable (.env file)"""
    context.judo_context.set_header_from_env(header_name, env_var_name)


@step('I set the query parameter "{name}" to "{value}"')
def step_set_query_param_string(context, name, value):
    """Set a query parameter (string)"""
    value = context.judo_context.interpolate_string(value)
    context.judo_context.set_query_param(name, value)


@step('I set the query parameter "{name}" to {value:d}')
def step_set_query_param_int(context, name, value):
    """Set a query parameter (integer)"""
    context.judo_context.set_query_param(name, value)


# HTTP Request Steps

@step('I send a GET request to "{endpoint}"')
def step_send_get_request(context, endpoint):
    """Send GET request"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    context.judo_context.make_request('GET', endpoint)


# Variable-based request steps (must come BEFORE specific method steps to avoid conflicts)
@step('I send a {method} request to "{endpoint}" with the variable "{var_name}"')
def step_send_request_with_variable(context, method, endpoint, var_name):
    """Send request with JSON data from variable"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    json_data = context.judo_context.get_variable(var_name)
    context.judo_context.make_request(method, endpoint, json=json_data)


@step('I send a POST request to "{endpoint}"')
def step_send_post_request(context, endpoint):
    """Send POST request without body"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    context.judo_context.make_request('POST', endpoint)


@step('I send a POST request to "{endpoint}" with JSON')
def step_send_post_request_with_json(context, endpoint):
    """Send POST request with JSON body"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    
    # Replace variables in JSON text
    json_text = context.text
    for var_name, var_value in context.judo_context.variables.items():
        json_text = json_text.replace(f"{{{var_name}}}", str(var_value))
    
    json_data = json.loads(json_text)
    context.judo_context.make_request('POST', endpoint, json=json_data)


@step('I send a PUT request to "{endpoint}" with JSON')
def step_send_put_request_with_json(context, endpoint):
    """Send PUT request with JSON body"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    
    # Replace variables in JSON text
    json_text = context.text
    for var_name, var_value in context.judo_context.variables.items():
        json_text = json_text.replace(f"{{{var_name}}}", str(var_value))
    
    json_data = json.loads(json_text)
    context.judo_context.make_request('PUT', endpoint, json=json_data)


@step('I send a PATCH request to "{endpoint}" with JSON')
def step_send_patch_request_with_json(context, endpoint):
    """Send PATCH request with JSON body"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    
    # Replace variables in JSON text
    json_text = context.text
    for var_name, var_value in context.judo_context.variables.items():
        json_text = json_text.replace(f"{{{var_name}}}", str(var_value))
    
    json_data = json.loads(json_text)
    context.judo_context.make_request('PATCH', endpoint, json=json_data)


@step('I send a DELETE request to "{endpoint}"')
def step_send_delete_request(context, endpoint):
    """Send DELETE request"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    context.judo_context.make_request('DELETE', endpoint)


# Response Validation Steps

@step('the response status should be {status:d}')
def step_validate_status(context, status):
    """Validate response status code"""
    context.judo_context.validate_status(status)


@step('the response should be successful')
def step_validate_success(context):
    """Validate that response is successful (2xx)"""
    response = context.judo_context.response
    assert response.is_success(), f"Expected successful response, but got {response.status}"


@step('the response should contain "{key}"')
def step_validate_response_contains_key(context, key):
    """Validate that response contains a key"""
    context.judo_context.validate_response_contains(key)


@step('the response field "{key}" should equal "{value}"')
def step_validate_response_field_string(context, key, value):
    """Validate that response field equals specific string value"""
    value = context.judo_context.interpolate_string(value)
    context.judo_context.validate_response_contains(key, value)


@step('the response field "{key}" should equal {value:d}')
def step_validate_response_field_int(context, key, value):
    """Validate that response field equals specific integer value"""
    context.judo_context.validate_response_contains(key, value)


@step('the response "{json_path}" should be "{expected_value}"')
def step_validate_json_path_string(context, json_path, expected_value):
    """Validate JSONPath expression result (string)"""
    expected_value = context.judo_context.interpolate_string(expected_value)
    context.judo_context.validate_json_path(json_path, expected_value)


@step('the response "{json_path}" should be {expected_value:d}')
def step_validate_json_path_int(context, json_path, expected_value):
    """Validate JSONPath expression result (integer)"""
    context.judo_context.validate_json_path(json_path, expected_value)


@step('the response "{json_path}" should match "{pattern}"')
def step_validate_json_path_pattern(context, json_path, pattern):
    """Validate JSONPath expression result against pattern"""
    context.judo_context.validate_json_path(json_path, pattern)


@step('the response should match the schema')
def step_validate_response_schema(context):
    """Validate response against JSON schema"""
    schema = json.loads(context.text)
    context.judo_context.validate_response_schema(schema)


@step('the response should be valid JSON')
def step_validate_json_response(context):
    """Validate that response is valid JSON"""
    response = context.judo_context.response
    assert response.is_json(), "Response is not valid JSON"


@step('the response time should be less than {max_time:f} seconds')
def step_validate_response_time(context, max_time):
    """Validate response time"""
    response = context.judo_context.response
    actual_time = response.elapsed
    assert actual_time < max_time, \
        f"Response time {actual_time:.3f}s exceeds maximum {max_time}s"


# Data Extraction Steps

@step('I extract "{json_path}" from the response as "{variable_name}"')
def step_extract_from_response(context, json_path, variable_name):
    """Extract value from response and store as variable"""
    response = context.judo_context.response
    value = context.judo_context.judo.json_path(response.json, json_path)
    context.judo_context.set_variable(variable_name, value)


@step('I store the response as "{variable_name}"')
def step_store_response(context, variable_name):
    """Store entire response as variable"""
    response = context.judo_context.response
    context.judo_context.set_variable(variable_name, response.json)


# Utility Steps

@step('I wait {seconds:f} seconds')
def step_wait(context, seconds):
    """Wait for specified seconds"""
    context.judo_context.wait(seconds)


@step('I print the response')
def step_print_response(context):
    """Print response for debugging"""
    context.judo_context.print_response()


@step('I load test data "{data_name}" from JSON')
def step_load_test_data_json(context, data_name):
    """Load test data from JSON in step text"""
    data = json.loads(context.text)
    context.judo_context.load_test_data(data_name, data)


@step('I load test data "{data_name}" from YAML')
def step_load_test_data_yaml(context, data_name):
    """Load test data from YAML in step text"""
    data = yaml.safe_load(context.text)
    context.judo_context.load_test_data(data_name, data)


# File-based step definitions

@step('I load test data "{data_name}" from file "{file_path}"')
def step_load_test_data_from_file(context, data_name, file_path):
    """Load test data from external file"""
    context.judo_context.load_test_data_from_file(data_name, file_path)


@step('I POST to "{endpoint}" with JSON file "{file_path}"')
def step_send_post_request_with_json_file(context, endpoint, file_path):
    """Send POST request with JSON body from file"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    json_data = context.judo_context.read_json_file(file_path)
    context.judo_context.make_request('POST', endpoint, json=json_data)


@step('I PUT to "{endpoint}" with JSON file "{file_path}"')
def step_send_put_request_with_json_file(context, endpoint, file_path):
    """Send PUT request with JSON body from file"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    json_data = context.judo_context.read_json_file(file_path)
    context.judo_context.make_request('PUT', endpoint, json=json_data)


@step('I PATCH to "{endpoint}" with JSON file "{file_path}"')
def step_send_patch_request_with_json_file(context, endpoint, file_path):
    """Send PATCH request with JSON body from file"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    json_data = context.judo_context.read_json_file(file_path)
    context.judo_context.make_request('PATCH', endpoint, json=json_data)


@step('I {method} to "{endpoint}" with data file "{file_path}"')
def step_send_request_with_data_from_file(context, method, endpoint, file_path):
    """Send request with data from file (auto-detect format)"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    data = context.judo_context.read_file(file_path)
    context.judo_context.make_request(method, endpoint, json=data)


@step('the response should match JSON file "{file_path}"')
def step_validate_response_matches_json_file(context, file_path):
    """Validate that response matches JSON from file"""
    expected_data = context.judo_context.read_json_file(file_path)
    response = context.judo_context.response
    
    # Use Judo's matcher for comparison
    assert context.judo_context.judo.match(response.json, expected_data), \
        f"Response does not match expected JSON from {file_path}"


@step('the response should match schema file "{file_path}"')
def step_validate_response_matches_schema_file(context, file_path):
    """Validate response against schema from file"""
    schema = context.judo_context.read_json_file(file_path)
    context.judo_context.validate_response_schema(schema)


@step('I save the response to file "{file_path}"')
def step_save_response_to_file(context, file_path):
    """Save response to file"""
    response = context.judo_context.response
    context.judo_context.judo.write_json(file_path, response.json)


@step('I save the variable "{var_name}" to file "{file_path}"')
def step_save_variable_to_file(context, var_name, file_path):
    """Save variable to file"""
    data = context.judo_context.get_variable(var_name)
    context.judo_context.judo.write_json(file_path, data)


# Array/Collection Validation Steps

@step('the response should be an array')
def step_validate_array_response(context):
    """Validate that response is an array"""
    response = context.judo_context.response
    assert isinstance(response.json, list), "Response is not an array"


@step('the response array should have {count:d} items')
def step_validate_array_count(context, count):
    """Validate array length"""
    response = context.judo_context.response
    actual_count = len(response.json)
    assert actual_count == count, \
        f"Expected {count} items, but got {actual_count}"


@step('the response array should contain an item with "{key}" equal to "{value}"')
def step_validate_array_contains_item(context, key, value):
    """Validate that array contains item with specific key-value"""
    response = context.judo_context.response
    value = context.judo_context.interpolate_string(value)
    
    # Try to convert to int if it's a numeric string
    try:
        numeric_value = int(value)
    except ValueError:
        numeric_value = None
    
    found = False
    for item in response.json:
        if isinstance(item, dict):
            item_value = item.get(key)
            # Check both string and numeric comparison
            if item_value == value or (numeric_value is not None and item_value == numeric_value):
                found = True
                break
    
    assert found, f"Array does not contain item with {key}={value}"


@step('the response array "{array_path}" should contain an item with "{key}" equal to "{value}"')
def step_validate_nested_array_contains_item(context, array_path, key, value):
    """Validate that nested array contains item with specific key-value"""
    response = context.judo_context.response
    value = context.judo_context.interpolate_string(value)
    
    # Get the array
    array_data = response.json
    
    # If response is already an array directly, use it
    if isinstance(array_data, list):
        # Response is directly the array
        pass
    else:
        # Navigate to the nested array
        for path_part in array_path.split('.'):
            if isinstance(array_data, dict):
                array_data = array_data.get(path_part)
                if array_data is None:
                    assert False, f"Path '{array_path}' not found in response"
            else:
                assert False, f"Cannot navigate to '{array_path}' - invalid path"
    
    # Validate it's an array
    assert isinstance(array_data, list), f"'{array_path}' is not an array, it's {type(array_data).__name__}"
    
    # Try to convert to int if it's a numeric string
    try:
        numeric_value = int(value)
    except ValueError:
        numeric_value = None
    
    # Search for the item
    found = False
    for item in array_data:
        if isinstance(item, dict):
            item_value = item.get(key)
            # Check both string and numeric comparison
            if item_value == value or (numeric_value is not None and item_value == numeric_value):
                found = True
                break
    
    assert found, f"Array '{array_path}' does not contain item with {key}={value}"


@step('each item in the response array should have "{key}"')
def step_validate_each_item_has_key(context, key):
    """Validate that each array item has a specific key"""
    response = context.judo_context.response
    
    for i, item in enumerate(response.json):
        assert isinstance(item, dict), f"Item {i} is not an object"
        assert key in item, f"Item {i} does not have key '{key}'"


# Advanced Matching Steps

@step('the response "{json_path}" should be a string')
def step_validate_json_path_string_type(context, json_path):
    """Validate that JSONPath result is a string"""
    context.judo_context.validate_json_path(json_path, "##string")


@step('the response "{json_path}" should be a number')
def step_validate_json_path_number_type(context, json_path):
    """Validate that JSONPath result is a number"""
    context.judo_context.validate_json_path(json_path, "##number")


@step('the response "{json_path}" should be a boolean')
def step_validate_json_path_boolean_type(context, json_path):
    """Validate that JSONPath result is a boolean"""
    context.judo_context.validate_json_path(json_path, "##boolean")


@step('the response "{json_path}" should be an array')
def step_validate_json_path_array_type(context, json_path):
    """Validate that JSONPath result is an array"""
    context.judo_context.validate_json_path(json_path, "##array")


@step('the response "{json_path}" should be an object')
def step_validate_json_path_object_type(context, json_path):
    """Validate that JSONPath result is an object"""
    context.judo_context.validate_json_path(json_path, "##object")


@step('the response "{json_path}" should be null')
def step_validate_json_path_null(context, json_path):
    """Validate that JSONPath result is null"""
    context.judo_context.validate_json_path(json_path, "##null")


@step('the response "{json_path}" should not be null')
def step_validate_json_path_not_null(context, json_path):
    """Validate that JSONPath result is not null"""
    context.judo_context.validate_json_path(json_path, "##notnull")


@step('the response "{json_path}" should be a valid email')
def step_validate_json_path_email(context, json_path):
    """Validate that JSONPath result is a valid email"""
    context.judo_context.validate_json_path(json_path, "##email")


@step('the response "{json_path}" should be a valid URL')
def step_validate_json_path_url(context, json_path):
    """Validate that JSONPath result is a valid URL"""
    context.judo_context.validate_json_path(json_path, "##url")


@step('the response "{json_path}" should be a valid UUID')
def step_validate_json_path_uuid(context, json_path):
    """Validate that JSONPath result is a valid UUID"""
    context.judo_context.validate_json_path(json_path, "##uuid")


# Additional steps for table-based validation

@step('I set the base URL to "{base_url}"')
def step_set_base_url_alt(context, base_url):
    """Alternative step for setting base URL"""
    if not hasattr(context, 'judo_context'):
        context.judo_context = JudoContext(context)
    context.judo_context.set_base_url(base_url)


@step('the response should contain')
def step_validate_response_contains_table(context):
    """Validate response contains fields from table"""
    if not hasattr(context, 'judo_context'):
        context.judo_context = JudoContext(context)
    
    response = context.judo_context.response
    
    for row in context.table:
        field = row['field']
        expected_value = row['value']
        
        # Handle different value types
        if expected_value.startswith('##'):
            # It's a matcher pattern
            actual_value = response.json.get(field)
            context.judo_context.judo.match(actual_value, expected_value)
        else:
            # It's an exact value
            try:
                # Try to convert to int if it's numeric
                if expected_value.isdigit():
                    expected_value = int(expected_value)
                elif expected_value.replace('.', '').isdigit():
                    expected_value = float(expected_value)
            except:
                pass
            
            actual_value = response.json.get(field)
            assert actual_value == expected_value, \
                f"Field '{field}': expected {expected_value}, got {actual_value}"


@step('the response should match "{json_path}" with "{matcher}"')
def step_validate_json_path_with_matcher(context, json_path, matcher):
    """Validate JSONPath with matcher pattern"""
    if not hasattr(context, 'judo_context'):
        context.judo_context = JudoContext(context)
    
    response = context.judo_context.response
    
    # Simple JSONPath handling for common cases
    if json_path == "$.address.city":
        actual_value = response.json.get("address", {}).get("city")
    elif json_path.startswith("$."):
        # Remove $. and split by dots
        path_parts = json_path[2:].split('.')
        actual_value = response.json
        for part in path_parts:
            if isinstance(actual_value, dict):
                actual_value = actual_value.get(part)
            else:
                actual_value = None
                break
    else:
        actual_value = response.json.get(json_path)
    
    # Use Judo's matcher
    context.judo_context.judo.match(actual_value, matcher)


# Auto-registration mechanism for steps
def _register_all_steps():
    """Force registration of all step definitions"""
    import inspect
    import behave
    
    # Get all functions in this module that are step definitions
    current_module = inspect.getmodule(inspect.currentframe())
    
    for name, obj in inspect.getmembers(current_module):
        if inspect.isfunction(obj) and hasattr(obj, '_behave_step_registry'):
            # This is a step definition, ensure it's registered
            pass

# Call registration when module is imported
_register_all_steps()


# Request/Response Logging Steps

@step('I enable request/response logging')
def step_enable_request_response_logging(context):
    """Enable automatic request/response logging"""
    context.judo_context.configure_request_response_logging(True)


@step('I disable request/response logging')
def step_disable_request_response_logging(context):
    """Disable automatic request/response logging"""
    context.judo_context.configure_request_response_logging(False)


@step('I enable request/response logging to directory "{directory}"')
def step_enable_request_response_logging_with_directory(context, directory):
    """Enable automatic request/response logging with custom directory"""
    context.judo_context.configure_request_response_logging(True, directory)


@step('I set the output directory to "{directory}"')
def step_set_output_directory(context, directory):
    """Set the output directory for request/response logging"""
    context.judo_context.output_directory = directory


# Generic Environment Variable Steps

@step('I get the value "{env_var_name}" from env and store it in "{variable_name}"')
def step_get_env_value_and_store(context, env_var_name, variable_name):
    """Get value from environment variable and store it in a variable"""
    import os
    from judo.behave.context import _load_env_file
    
    # Load environment variables from .env file (project root first)
    _load_env_file()
    
    # Get the value from environment variable
    env_value = os.getenv(env_var_name)
    
    if env_value is None:
        raise ValueError(f"Environment variable '{env_var_name}' not found")
    
    # Store in context variable
    context.judo_context.set_variable(variable_name, env_value)





# Also ensure steps are available when imported with *
__all__ = [name for name, obj in globals().items() 
           if callable(obj) and hasattr(obj, '_behave_step_registry')]

@step('I should have variable "{variable_name}" with value "{expected_value}"')
def step_validate_variable_value(context, variable_name, expected_value):
    """Validate that a variable has the expected value"""
    # Interpolate the expected value in case it contains variables
    expected_value = context.judo_context.interpolate_string(expected_value)
    
    # Get the actual value
    actual_value = context.judo_context.get_variable(variable_name)
    
    # Compare values
    assert actual_value == expected_value, \
        f"Variable '{variable_name}': expected '{expected_value}', but got '{actual_value}'"