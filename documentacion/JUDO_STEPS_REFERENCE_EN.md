# Judo Framework - Complete Steps Reference (English)

**✅ VERIFIED**: All steps extracted from actual source code v1.5.9.1

## Configuration Steps

### `I have a Judo API client`
Initialize Judo context for API testing.

### `the base URL is "{base_url}"`
Set the base URL for all subsequent HTTP requests.

### `I set the base URL to "{base_url}"`
Alternative syntax to set the base URL.

### `I set the variable "{name}" to "{value}"`
Create or update a string variable.

### `I set the variable "{name}" to {value:d}`
Create or update an integer variable.

### `I set the variable "{name}" to the JSON`
Set a variable to JSON data from step text.

### `I get the value "{env_var_name}" from env and store it in "{variable_name}"`
Get value from environment variable and store in a variable.

## Authentication Steps

### `I use bearer token "{token}"`
Set bearer token authentication for all subsequent requests.

### `I use basic authentication with username "{username}" and password "{password}"`
Set basic authentication with username and password.

### `I set the header "{name}" to "{value}"`
Add a custom HTTP header to all subsequent requests.

### `I set the header "{header_name}" from env "{env_var_name}"`
Set a request header from environment variable.

### `I set the query parameter "{name}" to "{value}"`
Add a query parameter (string) to the next request.

### `I set the query parameter "{name}" to {value:d}`
Add a query parameter (integer) to the next request.

## HTTP Request Steps

### `I send a GET request to "{endpoint}"`
Send HTTP GET request to retrieve data.

### `I send a {method} request to "{endpoint}" with the variable "{var_name}"`
Send HTTP request with JSON data from a variable.

### `I send a POST request to "{endpoint}"`
Send HTTP POST request without body.

### `I send a POST request to "{endpoint}" with JSON`
Send HTTP POST request with JSON body from step text.

### `I send a PUT request to "{endpoint}" with JSON`
Send HTTP PUT request with JSON body from step text.

### `I send a PATCH request to "{endpoint}" with JSON`
Send HTTP PATCH request with JSON body from step text.

### `I send a DELETE request to "{endpoint}"`
Send HTTP DELETE request.

## Response Validation Steps

### `the response status should be {status:d}`
Validate HTTP response status code.

### `the response should be successful`
Validate that response has successful status (2xx).

### `the response should contain "{key}"`
Validate that response contains a specific field.

### `the response field "{key}" should equal "{value}"`
Validate that response field equals specific string value.

### `the response field "{key}" should equal {value:d}`
Validate that response field equals specific integer value.

### `the response "{json_path}" should be "{expected_value}"`
Validate JSONPath expression result (string).

### `the response "{json_path}" should be {expected_value:d}`
Validate JSONPath expression result (integer).

### `the response "{json_path}" should match "{pattern}"`
Validate JSONPath expression result against pattern.

### `the response should match the schema`
Validate response against JSON schema from step text.

### `the response should be valid JSON`
Validate that response is valid JSON.

### `the response time should be less than {max_time:f} seconds`
Validate response time is below threshold.

## Data Extraction Steps

### `I extract "{json_path}" from the response as "{variable_name}"`
Extract value from response using JSONPath and store as variable.

### `I store the response as "{variable_name}"`
Store entire response as variable.

## Utility Steps

### `I wait {seconds:f} seconds`
Pause test execution for specified seconds.

### `I print the response`
Print response to console for debugging.

## Test Data Steps

### `I load test data "{data_name}" from JSON`
Load test data from JSON in step text.

### `I load test data "{data_name}" from YAML`
Load test data from YAML in step text.

### `I load test data "{data_name}" from file "{file_path}"`
Load test data from external file.

## File Operations Steps

### `I POST to "{endpoint}" with JSON file "{file_path}"`
Send POST request with JSON data loaded from file.

### `I PUT to "{endpoint}" with JSON file "{file_path}"`
Send PUT request with JSON data loaded from file.

### `I PATCH to "{endpoint}" with JSON file "{file_path}"`
Send PATCH request with JSON data loaded from file.

### `I {method} to "{endpoint}" with data file "{file_path}"`
Send request with data from file (auto-detect format).

### `the response should match JSON file "{file_path}"`
Validate response matches JSON data from file.

### `the response should match schema file "{file_path}"`
Validate response against schema from file.

### `I save the response to file "{file_path}"`
Save response to file.

### `I save the variable "{var_name}" to file "{file_path}"`
Save variable content to file.

## Array/Collection Validation Steps

### `the response should be an array`
Validate that response is a JSON array.

### `the response array should have {count:d} items`
Validate array has exact number of items.

### `the response array should contain an item with "{key}" equal to "{value}"`
Validate array contains item with specific key-value pair.

### `the response array "{array_path}" should contain an item with "{key}" equal to "{value}"`
Validate nested array contains item with specific key-value pair.

### `each item in the response array should have "{key}"`
Validate each array item has a specific field.

### `the response array should contain objects with structure`
Validate that response array contains objects with expected structure from table.

## Type Validation Steps

### `the response "{json_path}" should be a string`
Validate JSONPath result is string type.

### `the response "{json_path}" should be a number`
Validate JSONPath result is number type.

### `the response "{json_path}" should be a boolean`
Validate JSONPath result is boolean type.

### `the response "{json_path}" should be an array`
Validate JSONPath result is array type.

### `the response "{json_path}" should be an object`
Validate JSONPath result is object type.

### `the response "{json_path}" should be null`
Validate JSONPath result is null.

### `the response "{json_path}" should not be null`
Validate JSONPath result is not null.

### `the response "{json_path}" should be a valid email`
Validate JSONPath result is valid email format.

### `the response "{json_path}" should be a valid URL`
Validate JSONPath result is valid URL format.

### `the response "{json_path}" should be a valid UUID`
Validate JSONPath result is valid UUID format.

## Variable Validation Steps

### `I should have variable "{variable_name}" with value "{expected_value}"`
Validate that a variable has the expected value.

### `the response should contain`
Validate response contains fields from table.

## Logging Steps

### `I enable request/response logging`
Enable automatic request/response logging.

### `I disable request/response logging`
Disable automatic request/response logging.

### `I enable request/response logging to directory "{directory}"`
Enable logging with custom directory.

### `I set the output directory to "{directory}"`
Set output directory for logging.

## Advanced Features - Circuit Breaker

### `I set retry policy with max_retries={max_retries:d} and backoff_strategy="{strategy}"`
Set retry policy with backoff strategy.

### `I set retry policy with max_retries={max_retries:d}, initial_delay={initial_delay:f}, and max_delay={max_delay:f}`
Set retry policy with custom delay parameters.

### `I create circuit breaker "{name}" with failure_threshold={threshold:d}`
Create circuit breaker to prevent cascading failures.

### `I create circuit breaker "{name}" with failure_threshold={failure_threshold:d}, success_threshold={success_threshold:d}, and timeout={timeout:d}`
Create circuit breaker with custom thresholds and timeout.

### `circuit breaker "{name}" should be in state {state}`
Validate circuit breaker state (CLOSED, OPEN, HALF_OPEN).

### `circuit breaker should remain in CLOSED state`
Validate circuit breaker remained closed.

## Advanced Features - Rate Limiting

### `I set rate limit to {requests_per_second:f} requests per second`
Configure rate limiter with requests per second.

### `I set adaptive rate limit with initial {rps:f} requests per second`
Configure adaptive rate limiter that adjusts based on response times.

### `the rate limiter should have {remaining:d} requests remaining`
Validate remaining requests in rate limiter.

## Advanced Features - WebSocket

### `I connect to WebSocket "{url}"`
Connect to WebSocket server at specified URL.

### `I send WebSocket message`
Send WebSocket message using step text as message content.

### `I should receive WebSocket message within {timeout:f} seconds`
Wait to receive WebSocket message within timeout period.

### `I close WebSocket connection`
Close the WebSocket connection.

### `I disconnect from WebSocket`
Disconnect from WebSocket (alternative syntax).

## Advanced Features - GraphQL

### `I execute GraphQL query`
Execute GraphQL query using the step text as the query.

### `I execute GraphQL mutation`
Execute GraphQL mutation using the step text as the mutation.

## Advanced Features - Interceptors

### `I add timestamp interceptor with header name "{header_name}"`
Add timestamp to all requests with specified header.

### `I add a timestamp interceptor with header name "{header_name}"`
Add timestamp interceptor (with article 'a').

### `I add authorization interceptor with token "{token}"`
Add authorization token to all requests.

### `I add an authorization interceptor with token "{token}"`
Add authorization interceptor (with article 'an').

### `I add a logging interceptor`
Add logging interceptor to log all requests.

### `I add a response logging interceptor`
Add response logging interceptor to log all responses.

## Contract Validation Steps

### `I load OpenAPI spec from "{spec_file}"`
Load OpenAPI specification.

### `response should match OpenAPI contract for {method} {path}`
Validate response against OpenAPI contract.

### `I load OpenAPI contract from "{contract_file}"`
Load OpenAPI contract specification.

### `I load AsyncAPI contract from "{contract_file}"`
Load AsyncAPI contract specification.

### `the response should match the contract schema`
Validate response against loaded OpenAPI contract schema.

### `the response should match schema "{schema_name}"`
Validate response against specific schema from contract.

### `the response field "{field_path}" should be of type "{expected_type}"`
Validate that a specific field has the expected data type.

### `the response should have required fields`
Validate response has all required fields from step table.

### `the response should conform to JSON Schema`
Validate response against JSON Schema from step text.

### `the response should conform to JSON Schema from file "{schema_file}"`
Validate response against JSON Schema from file.

### `the response field "{field_path}" should match pattern "{pattern}"`
Validate field matches regex pattern.

### `the response should have consistent data types across array items`
Validate all array items have consistent data types.

### `I validate the API contract endpoints`
Validate all endpoints in contract are accessible.

### `the message should match AsyncAPI contract for channel "{channel}"`
Validate message against AsyncAPI contract for specific channel.

### `I load AsyncAPI spec from "{file_path}"`
Load AsyncAPI specification.

## Advanced Data Format Validation Steps

### `the response field "{field_path}" should be a valid email`
Validate field contains valid email address format.

### `the response field "{field_path}" should be a valid URL`
Validate field contains valid URL format.

### `the response field "{field_path}" should be a valid UUID`
Validate field contains valid UUID format.

### `the response field "{field_path}" should be a valid ISO date`
Validate field contains valid ISO date format.

### `the response should have nested structure`
Validate response has expected nested structure from step text.

### `I validate request body against contract for {method} {path}`
Validate request body against OpenAPI contract specification.

### `I validate response headers against contract`
Validate response headers against OpenAPI contract.

### `the response should match data contract specification`
Comprehensive validation against loaded contract including headers and body.

## Additional Validation Steps

### `I enable request logging to directory "{directory}"`
Enable request logging.

### `the cache should contain {count:d} entries`
Validate number of cache entries.

### `the token should contain claim "{claim}" with value "{value}"`
Validate JWT token contains specific claim.

### `the response should contain all fields: {fields}`
Validate response contains all specified fields.

---

**Notes:**
- All steps work with any Gherkin keyword (Given, When, Then, And, But)
- Variable interpolation uses `{variableName}` syntax
- Steps with `from env` load variables from .env files
- JSONPath uses standard syntax like `$.field.subfield`

*Judo Framework v1.5.9.1 - All steps verified against source code*