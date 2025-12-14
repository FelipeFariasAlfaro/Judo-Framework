# Complete Steps Reference - Judo Framework (English)

This is the complete reference of all **VERIFIED** steps available in Judo Framework v1.3.36 in English.

**⚠️ IMPORTANT**: This documentation has been verified against the framework source code. It only includes steps that actually exist and work.

## 📋 Table of Contents

- [Configuration](#configuration)
- [Authentication](#authentication)
- [HTTP Requests](#http-requests)
- [Response Validation](#response-validation)
- [Data Extraction](#data-extraction)
- [Variables](#variables)
- [Arrays and Collections](#arrays-and-collections)
- [File Operations](#file-operations)
- [Utilities](#utilities)
- [Logging](#logging)

---

## Configuration

### `Given I have a Judo API client`
Initializes the Judo Framework context to begin API testing.

### `Given the base URL is "{url}"`
Sets the base URL that will be used for all subsequent HTTP requests.

### `Given I set the base URL to "{base_url}"`
Alternative step for setting the base URL.

### `Given I set the variable "{name}" to "{value}"`
Creates or updates a string variable that can be reused in other steps.

### `Given I set the variable "{name}" to {value:d}`
Creates or updates a numeric (integer) variable.

### `Given I set the variable "{name}" to the JSON`
Stores a complete JSON object in a variable using the step text.

### `I get the value "{env_var_name}" from env and store it in "{variable_name}"`
Gets the value from an environment variable (.env) and stores it in a variable for later use. Useful for dynamic configurations like base URLs, tokens, etc.

---

## Authentication

### `Given I use bearer token "{token}"`
Configures Bearer Token (JWT) authentication for all subsequent requests.

### `Given I use basic authentication with username "{username}" and password "{password}"`
Configures HTTP Basic authentication with username and password.

### `Given I set the header "{name}" to "{value}"`
Adds a custom HTTP header to all subsequent requests.

### `Given I set the header "{header_name}" from env "{env_var_name}"`
Sets an HTTP header using the value from an environment variable or .env file.

### `Given I set the query parameter "{name}" to "{value}"`
Adds a query string parameter to the next HTTP request.

### `Given I set the query parameter "{name}" to {value:d}`
Adds a numeric query string parameter to the next HTTP request.

---

## HTTP Requests

### `When I send a GET request to "{endpoint}"`
Sends an HTTP GET request to retrieve data from the server.

### `When I send a POST request to "{endpoint}"`
Sends an HTTP POST request without a data body.

### `When I send a POST request to "{endpoint}" with JSON`
Sends an HTTP POST request with JSON data in the body using the step text.

### `When I send a PUT request to "{endpoint}" with JSON`
Sends an HTTP PUT request with JSON data to completely replace a resource.

### `When I send a PATCH request to "{endpoint}" with JSON`
Sends an HTTP PATCH request with JSON data to partially update a resource.

### `When I send a DELETE request to "{endpoint}"`
Sends an HTTP DELETE request to remove a resource from the server.

### `When I send a {method} request to "{endpoint}" with the variable "{var_name}"`
Sends an HTTP request of any method using JSON data stored in a variable.

---

## Response Validation

### `Then the response status should be {status:d}`
Validates that the HTTP response status code matches the expected value.

### `Then the response should be successful`
Validates that the response has a successful status code (2xx).

### `Then the response should contain "{key}"`
Verifies that the JSON response contains a specific field.

### `Then the response field "{key}" should equal "{value}"`
Validates that a specific field has exactly the expected string value.

### `Then the response field "{key}" should equal {value:d}`
Validates that a specific field has exactly the expected numeric value.

### `Then the response field "{key}" should equal the variable "{variable}"`
Compares a field value with the value stored in a variable.

### `Then the response should match the schema`
Validates the response structure against a JSON schema defined in the step text.

### `Then the response should be valid JSON`
Verifies that the response is valid and well-formed JSON.

### `Then the response time should be less than {max_time:f} seconds`
Validates that the HTTP request response time is less than the specified limit.

### `Then the response "{json_path}" should be "{expected_value}"`
Validates the value of a specific JSONPath against an expected value.

### `Then the response "{json_path}" should be {expected_value:d}`
Validates the numeric value of a specific JSONPath.

### `Then the response "{json_path}" should match "{pattern}"`
Validates a JSONPath expression result against a pattern.

---

## Data Extraction

### `When I extract "{json_path}" from the response as "{variable_name}"`
Extracts a value from the response and stores it in a variable for later use.

### `When I store the response as "{variable_name}"`
Stores the entire JSON response in a variable.

---

## Variables

### `Then the variable "{var1}" should equal the variable "{var2}"`
Compares that two variables have exactly the same value.

### `Then the variable "{var1}" should not equal the variable "{var2}"`
Verifies that two variables have different values.

---

## Arrays and Collections

### `Then the response should be an array`
Validates that the response is a JSON array (list).

### `Then the response array should have {count:d} items`
Verifies that the response array has exactly the specified number of elements.

### `Then each item in the response array should have "{key}"`
Validates that all elements in the array have a specific field.

### `Then the response array should contain an item with "{key}" equal to "{value}"`
Searches the response array for an element that has a field with a specific value.

### `Then the response array "{array_path}" should contain an item with "{key}" equal to "{value}"`
Searches in a nested or root-level array for an element with a specific field-value pair.

---

## File Operations

### `When I POST to "{endpoint}" with JSON file "{file_path}"`
Sends a POST request using JSON data loaded from an external file.

### `When I PUT to "{endpoint}" with JSON file "{file_path}"`
Sends a PUT request using JSON data loaded from an external file.

### `When I PATCH to "{endpoint}" with JSON file "{file_path}"`
Sends a PATCH request using JSON data loaded from an external file.

### `When I {method} to "{endpoint}" with data file "{file_path}"`
Sends a request with data from a file (auto-detects format).

### `Then the response should match JSON file "{file_path}"`
Validates that the response matches JSON data from an external file.

### `Then the response should match schema file "{file_path}"`
Validates the response against a JSON schema stored in an external file.

### `When I save the response to file "{file_path}"`
Saves the complete response to a file for later analysis or debugging.

### `When I save the variable "{var_name}" to file "{file_path}"`
Saves the content of a variable to an external file.

### `When I load test data "{data_name}" from file "{file_path}"`
Loads test data from an external file (JSON, YAML, CSV).

### `When I load test data "{data_name}" from JSON`
Loads test data from inline JSON in the step text.

### `When I load test data "{data_name}" from YAML`
Loads test data from inline YAML in the step text.

---

## Type Validation

### `Then the response "{json_path}" should be a string`
Validates that the value at the specified JSONPath is of type string.

### `Then the response "{json_path}" should be a number`
Validates that the value at the specified JSONPath is of type number.

### `Then the response "{json_path}" should be a boolean`
Validates that the value at the specified JSONPath is of type boolean.

### `Then the response "{json_path}" should be an array`
Validates that the value at the specified JSONPath is of type array.

### `Then the response "{json_path}" should be an object`
Validates that the value at the specified JSONPath is of type object.

### `Then the response "{json_path}" should be null`
Validates that the value at the specified JSONPath is null.

### `Then the response "{json_path}" should not be null`
Validates that the value at the specified JSONPath is not null.

### `Then the response "{json_path}" should be a valid email`
Validates that the value at the specified JSONPath has a valid email format.

### `Then the response "{json_path}" should be a valid URL`
Validates that the value at the specified JSONPath has a valid URL format.

### `Then the response "{json_path}" should be a valid UUID`
Validates that the value at the specified JSONPath has a valid UUID format.

---

## Utilities

### `When I wait {seconds:f} seconds`
Pauses test execution for the specified number of seconds.

### `When I print the response`
Prints the complete response to the console for debugging purposes.

---

## Logging

### `When I enable request/response logging`
Enables automatic saving of all HTTP interactions to JSON files.

### `When I disable request/response logging`
Disables automatic saving of HTTP interactions.

### `When I enable request/response logging to directory "{directory}"`
Enables HTTP logging with a custom directory for the files.

### `When I set the output directory to "{directory}"`
Configures the directory where request/response logs will be saved.

---

## Advanced Features

### `Then the response should contain`
Validates response contains fields from a table (used with Behave tables).

### `Then the response should match "{json_path}" with "{matcher}"`
Validates a JSONPath with a matcher pattern (supports Karate-style patterns).

---

## Important Notes

- **Variable Interpolation**: Use `{variableName}` syntax in URLs, headers, and JSON bodies.
- **.env Files**: Steps with `from env` automatically load variables from .env files.
- **JSONPath**: Use standard JSONPath syntax like `$.field.subfield` to navigate JSON structures.
- **Data Types**: The framework automatically handles conversions between strings and numbers when appropriate.
- **Automatic Logging**: When enabled, automatically saves requests/responses with timestamps and metadata.
- **Pattern Matching**: Supports Karate-style patterns like `##string`, `##number`, `##email`, etc.
- **File Formats**: Supports JSON, YAML, and CSV files for test data.
- **Verification**: This documentation has been verified against the source code v1.3.36.

---

*Judo Framework v1.3.36 - Documentation verified against source code*