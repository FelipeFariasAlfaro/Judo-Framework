# Complete Steps Reference - Judo Framework (English)

This is the complete reference of all **VERIFIED** steps available in Judo Framework v1.5.0 in English.

**⚠️ IMPORTANT**: This documentation has been verified against the framework source code. It only includes steps that actually exist and work.

**💡 Note**: All steps use the `@step()` decorator, which means they work with any keyword (Given, When, Then, And, But). This provides maximum flexibility in writing your test scenarios.

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
- [Advanced Features - Tier 1](#advanced-features---tier-1-robustness--reliability)
- [Advanced Features - Tier 2](#advanced-features---tier-2-performance--modern-apis)
- [Advanced Features - Tier 3](#advanced-features---tier-3-enterprise-features)

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

## New steps in v1.7.0

### HTTP settings, files, XML/SOAP basics, security headers, polling, SQL, pagination

#### `I poll "{endpoint}" until the response "{json_path}" equals "{expected}" within {seconds:d} seconds`
Repeat GET until a JSON path equals the expected value or time runs out.
#### `I poll "{endpoint}" until the status is {status:d} within {seconds:d} seconds`
Repeat GET until the status code matches or time runs out.
#### `I connect to the SQLite database "{path}"`
Open a SQLite database for data setup and verification.
#### `I execute the SQL "{sql}"`
Execute a SQL statement (INSERT, UPDATE, DELETE, DDL).
#### `I save the first value of the SQL query "{sql}" as "{variable}"`
Run a SQL query and store the first column of the first row in a variable.
#### `the SQL query "{sql}" should return {count:d} rows`
Validate the number of rows a SQL query returns.
#### `the SQL query "{sql}" should return the value "{expected}"`
Validate the first value returned by a SQL query.
#### `I collect all pages from "{endpoint}" using the "{page_param}" parameter up to {max_pages:d} pages as "{variable}"`
Walk a paginated GET endpoint and store all items in a variable.
#### `I set the timeout to {seconds:g} seconds`
Set the HTTP request timeout.
#### `I disable SSL verification`
Disable TLS certificate verification (testing only).
#### `I use the CA bundle "{path}"`
Verify TLS using a custom CA bundle file.
#### `I use the client certificate "{cert}" and key "{key}"`
Use a client certificate and key (mutual TLS).
#### `I use the proxy "{url}"`
Send requests through an HTTP proxy.
#### `I connect to the database "{url}"`
Connect to SQLite, PostgreSQL or MySQL using a URL.
#### `I upload the file "{path}" as "{field}" to "{endpoint}"`
Upload a file as multipart/form-data with POST.
#### `the response SHA-256 should be "{expected}"`
Validate the SHA-256 digest of the response body.
#### `the response header "{name}" should be "{value}"`
Validate a response header value.
#### `the response header "{name}" should exist`
Validate a response header is present.
#### `the response should include security headers`
Validate HSTS, nosniff and clickjacking protection headers.
#### `the response XML "{xpath}" should be "{expected}"`
Validate the first value selected by an XPath.
#### `the response XML "{xpath}" should select {count:d} nodes`
Validate how many nodes an XPath selects.
#### `I extract the XML "{xpath}" as "{variable}"`
Store the first value selected by an XPath in a variable.
#### `the response should equal the JSON ignoring "{fields}"`
Compare the response with the JSON in the step text, ignoring volatile fields.
#### `I send a SOAP request to "{endpoint}" with action "{action}"`
Send the XML in the step text as a SOAP request.
#### `the response status should be a client error`
Validate the status is 4xx.
#### `the response status should be a server error`
Validate the status is 5xx.
#### `the response status should be one of "{codes}"`
Validate the status is one of a comma separated list of codes.

### Conditional and control-flow steps (if / otherwise, loops, retry, soft assertions, skip). The block of steps goes in a docstring; use ''' for a docstring nested inside it

#### `if the response status is {status:d} then run`
Run the docstring steps when the response status matches.
#### `if the response status is not {status:d} then run`
Run the docstring steps when the response status differs.
#### `if the response "{json_path}" equals "{expected}" then run`
Run the docstring steps when a JSON path equals a value.
#### `if the response "{json_path}" exists then run`
Run the docstring steps when a JSON path exists.
#### `if the response "{json_path}" does not exist then run`
Run the docstring steps when a JSON path does not exist.
#### `if the response "{json_path}" contains "{text}" then run`
Run the docstring steps when a JSON value (or array item) contains the text.
#### `if the response "{json_path}" is greater than {number:g} then run`
Run the docstring steps when a numeric JSON value is greater than a number.
#### `if the response "{json_path}" is less than {number:g} then run`
Run the docstring steps when a numeric JSON value is less than a number.
#### `if the variable "{name}" equals "{expected}" then run`
Run the docstring steps when a variable equals a value.
#### `if the variable "{name}" is defined then run`
Run the docstring steps when a variable is defined.
#### `if the variable "{name}" is not defined then run`
Run the docstring steps when a variable is not defined.
#### `if the variable "{name}" is empty then run`
Run the docstring steps when a variable is missing or empty.
#### `if the environment is "{env}" then run`
Run the docstring steps when JUDO_ENV / KARATE_ENV equals the value.
#### `if the environment variable "{name}" is set then run`
Run the docstring steps when an OS environment variable is set.
#### `if the scenario has the tag "{tag}" then run`
Run the docstring steps when the scenario carries a tag.
#### `if the file "{path}" exists then run`
Run the docstring steps when a file exists.
#### `if the response header "{name}" exists then run`
Run the docstring steps when a response header is present.
#### `if the response body contains "{text}" then run`
Run the docstring steps when the raw response body contains the text.
#### `if the response time is greater than {ms:d} milliseconds then run`
Run the docstring steps when the response was slower than the limit.
#### `otherwise run`
Run the docstring steps when the previous 'if' condition was false.
#### `I skip the scenario if the variable "{name}" equals "{expected}"`
Skip the rest of the scenario when a variable equals a value.
#### `I skip the scenario if the environment is "{env}"`
Skip the rest of the scenario in a given environment.
#### `I skip the scenario if the response status is {status:d}`
Skip the rest of the scenario when the response status matches.
#### `I fail the test with the message "{message}"`
Fail the scenario with a custom message.
#### `the variable "{name}" should be defined`
Validate a variable is defined.
#### `the variable "{name}" should not be defined`
Validate a variable is not defined.
#### `the variable "{name}" should be empty`
Validate a variable is missing or empty.
#### `the environment should be "{env}"`
Validate the current environment name.
#### `I repeat {count:d} times`
Run the docstring steps N times (variable ${iteration} = 1..N).
#### `I repeat until the response "{json_path}" equals "{expected}" up to {count:d} times`
Run the docstring steps until a JSON path equals a value, at most N times.
#### `for each item in the response "{json_path}" run`
Run the docstring steps for each array element (variables ${item} and ${index}).
#### `I retry the following steps up to {count:d} times with {seconds:g} seconds delay`
Retry the docstring steps while they fail.
#### `I verify all of the following`
Run each docstring line as a step and report every failure at the end.

### Non-JSON services: XML/SOAP, forms, text, CSV, binary downloads, Server-Sent Events, GraphQL

#### `the response should be valid XML`
Validate the response body is well-formed XML.
#### `the response XML "{xpath}" should exist`
Validate an XPath selects at least one node.
#### `the response XML "{xpath}" should not exist`
Validate an XPath selects nothing.
#### `the response XML "{xpath}" should contain "{text}"`
Validate a node selected by an XPath contains a text.
#### `the response XML "{xpath}" should match "{pattern}"`
Validate the first node selected by an XPath matches a regex.
#### `the response XML should conform to the XSD "{path}"`
Validate the response XML against an XSD schema (needs lxml).
#### `the SOAP response should not be a fault`
Validate the SOAP response is not a fault.
#### `the SOAP fault code should be "{code}"`
Validate the SOAP fault code.
#### `the SOAP fault message should contain "{text}"`
Validate the SOAP fault message contains a text.
#### `I send a SOAP 1.2 request to "{endpoint}" with action "{action}"`
Send the XML in the step text as a SOAP 1.2 request.
#### `I send the SOAP envelope file "{path}" to "{endpoint}" with action "{action}"`
Send a SOAP 1.1 request whose envelope is read from a file.
#### `I send an XML POST to "{endpoint}"`
POST the XML in the step text with Content-Type application/xml.
#### `I send a form POST to "{endpoint}"`
POST application/x-www-form-urlencoded using a table with columns field | value.
#### `I set the form field "{name}" to "{value}"`
Stage a form field for the next 'I submit the form'.
#### `I submit the form to "{endpoint}"`
POST the staged form fields as application/x-www-form-urlencoded.
#### `the response text should contain "{text}"`
Validate the response text contains a string.
#### `the response text should not contain "{text}"`
Validate the response text does not contain a string.
#### `the response text should match "{pattern}"`
Validate the response text matches a regular expression.
#### `the response text should equal "{text}"`
Validate the whole response text (trimmed).
#### `the response content type should be "{content_type}"`
Validate the Content-Type header starts with a value.
#### `the response size should be less than {size:d} bytes`
Validate the response body size.
#### `the response should be a CSV with {count:d} rows`
Validate the number of CSV data rows (header excluded).
#### `the CSV column "{column}" should contain "{value}"`
Validate a CSV column has a value in some row.
#### `the response bytes should equal the file "{path}"`
Validate the response bytes are identical to a file.
#### `I download "{endpoint}" to the file "{path}"`
GET an endpoint and save the raw bytes to a file.
#### `the response should have the download filename "{name}"`
Validate the filename in Content-Disposition.
#### `I save the response text as "{variable}"`
Store the raw response text in a variable.
#### `I open the SSE stream "{endpoint}"`
Open a Server-Sent Events stream and collect events in the background.
#### `I should receive an SSE event "{event}" within {seconds:g} seconds`
Wait for an SSE event by name.
#### `I should receive an SSE event with data containing "{text}" within {seconds:g} seconds`
Wait for an SSE event whose data contains a text.
#### `I should receive {count:d} SSE events within {seconds:g} seconds`
Wait until at least N SSE events have arrived.
#### `the last SSE event data "{json_path}" should be "{expected}"`
Validate a JSON field of the last SSE event data.
#### `I close the SSE stream`
Close the SSE stream.
#### `I set the GraphQL variables`
Set the variables (JSON in the step text) for the next GraphQL request.
#### `I send the GraphQL query to "{endpoint}"`
Send the GraphQL query in the step text.
#### `I send the GraphQL mutation to "{endpoint}"`
Send the GraphQL mutation in the step text.
#### `the GraphQL response should not have errors`
Validate the GraphQL response has no errors.
#### `the GraphQL response should have an error containing "{text}"`
Validate a GraphQL error message contains a text.
#### `the GraphQL data "{json_path}" should be "{expected}"`
Validate a value inside the GraphQL data.
#### `the GraphQL data "{json_path}" should exist`
Validate a path exists inside the GraphQL data.
#### `the GraphQL data "{json_path}" should have {count:d} items`
Validate the size of an array inside the GraphQL data.
#### `I save the GraphQL data "{json_path}" as "{variable}"`
Store a value of the GraphQL data in a variable.
#### `I introspect the GraphQL schema at "{endpoint}"`
Run the introspection query.
#### `the GraphQL schema should have the type "{name}"`
Validate a type exists in the introspected schema.

### gRPC through server reflection (needs `pip install "judo-framework[grpc]"`)

#### `I connect to the gRPC server "{target}"`
Open an insecure gRPC channel (host:port).
#### `I connect to the gRPC server "{target}" with TLS`
Open a TLS gRPC channel using the system trust store.
#### `I set the gRPC metadata "{key}" to "{value}"`
Add a metadata (header) sent with every gRPC call.
#### `I set the gRPC timeout to {seconds:g} seconds`
Set the deadline of gRPC calls.
#### `I send the gRPC request "{method}"`
Call a unary method; the request (JSON) goes in the step text.
#### `I send the gRPC streaming request "{method}"`
Call a server-streaming method; the request (JSON) goes in the step text.
#### `the gRPC status should be "{status}"`
Validate the gRPC status code name (OK, NOT_FOUND, UNAUTHENTICATED, ...).
#### `the gRPC response "{json_path}" should be "{expected}"`
Validate a field of the gRPC response.
#### `the gRPC response should contain "{field}"`
Validate the gRPC response has a field.
#### `I save the gRPC response "{json_path}" as "{variable}"`
Store a field of the gRPC response in a variable.
#### `the gRPC server should expose the service "{service}"`
Validate (via reflection) that a service is exposed.
#### `the gRPC server should expose the method "{method}"`
Validate (via reflection) that a method exists.
#### `the gRPC stream should return {count:d} messages`
Validate how many messages the server stream returned.
#### `the gRPC stream message {index:d} "{json_path}" should be "{expected}"`
Validate a field of one stream message (0-based index).
#### `the gRPC call should take less than {ms:d} milliseconds`
Validate the duration of the last gRPC call.
#### `I close the gRPC connection`
Close the gRPC channel.
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

## Advanced Features - Tier 1: Robustness & Reliability

### Retry Policy

#### `Given I set retry policy with max_retries={count:d} and backoff_strategy="{strategy}"`
Configures automatic retry policy for failed requests with specified backoff strategy.

**Supported Strategies:**
- `linear` - Delay increases linearly
- `exponential` - Delay increases exponentially (default)
- `fibonacci` - Delay follows Fibonacci sequence
- `random` - Random delay between min and max

#### `Given I set retry policy with max_retries={count:d}, initial_delay={delay:f}, and max_delay={max_delay:f}`
Configures retry policy with custom delay parameters.

### Circuit Breaker

#### `Given I create a circuit breaker named "{name}" with failure_threshold={threshold:d}`
Creates a circuit breaker to prevent cascading failures.

#### `Given I create a circuit breaker named "{name}" with failure_threshold={threshold:d}, success_threshold={success:d}, and timeout={timeout:d}`
Creates a circuit breaker with custom success threshold and timeout.

#### `Then circuit breaker "{name}" should be in state {state}`
Validates the current state of a circuit breaker (CLOSED, OPEN, HALF_OPEN).

### Request Interceptors

#### `Given I add a timestamp interceptor with header name "{header_name}"`
Adds a timestamp to all requests with the specified header name.

#### `Given I add an authorization interceptor with token "{token}"`
Adds Bearer token authorization to all requests.

#### `Given I add an authorization interceptor with token "{token}" and scheme "{scheme}"`
Adds custom authorization scheme to all requests.

#### `Given I add a logging interceptor`
Enables logging of all requests.

#### `Given I add a response logging interceptor`
Enables logging of all responses.

### Rate Limiting & Throttling

#### `Given I set rate limit to {requests:d} requests per second`
Configures token bucket rate limiter.

#### `Given I set throttle with delay {delay:d} milliseconds`
Configures fixed delay throttling between requests.

#### `Given I set adaptive rate limit with initial {rps:d} requests per second`
Configures adaptive rate limiting that respects API headers.

#### `Then the rate limiter should have {remaining:d} requests remaining`
Validates remaining requests in rate limiter.

### Advanced Assertions

#### `Then the response time should be less than {max_time:d} milliseconds`
Validates response time is below threshold in milliseconds.

#### `Then the response should match JSON schema`
Validates response against JSON schema defined in step text.

#### `Then the response array should have more than {count:d} items`
Validates array has more than specified number of items.

#### `Then the response array should have less than {count:d} items`
Validates array has fewer than specified number of items.

#### `Then the response should contain all fields: {fields}`
Validates response contains all specified fields.

#### `Then the response field "{field}" should be of type "{type}"`
Validates field is of specified type (string, number, boolean, array, object).

#### `Then the response field "{field}" should match pattern "{pattern}"`
Validates field matches regex pattern.

#### `Then the response field "{field}" should be in range {min:d} to {max:d}`
Validates numeric field is within range.

---

## Advanced Features - Tier 2: Performance & Modern APIs

### Data-Driven Testing

#### `Given I load test data from file "{file_path}"`
Loads test data from CSV, JSON, or Excel file.

#### `When I run data-driven test for each row`
Executes test scenario for each row in loaded test data.

#### `Then all tests should complete successfully`
Validates all data-driven tests completed without errors.

### Performance Monitoring

#### `When I send {count:d} GET requests to "{endpoint}"`
Sends multiple GET requests for performance testing.

#### `Then I should have performance metrics`
Validates performance metrics were collected (used with table).

#### `Then the average response time should be less than {max_time:d} milliseconds`
Validates average response time across requests.

#### `Then the p95 response time should be less than {max_time:d} milliseconds`
Validates 95th percentile response time.

#### `Then the error rate should be less than {percentage:d} percent`
Validates error rate is below threshold.

### Response Caching

#### `Given I enable response caching with TTL {ttl:d} seconds`
Enables automatic caching of GET responses with time-to-live.

#### `When I send the same GET request to "{endpoint}" again`
Sends identical GET request (used to test cache).

#### `Then the second response should come from cache`
Validates response was served from cache.

#### `Then the cache should contain {count:d} entries`
Validates number of entries in cache.

### GraphQL

#### `Given I set the base URL to "{url}"`
Sets base URL for GraphQL endpoint.

#### `When I execute GraphQL query`
Executes GraphQL query defined in step text.

#### `When I execute GraphQL mutation`
Executes GraphQL mutation defined in step text.

#### `Then the response should contain "{field}"`
Validates GraphQL response contains field.

### WebSocket

#### `Given I connect to WebSocket "{url}"`
Establishes WebSocket connection.

#### `When I send WebSocket message`
Sends message through WebSocket (message in step text).

#### `Then I should receive a WebSocket message within {seconds:d} seconds`
Validates WebSocket message received within timeout.

#### `When I disconnect from WebSocket`
Closes WebSocket connection.

### OAuth2 Authentication

#### `Given I setup OAuth2 with`
Configures OAuth2 authentication (used with table of client_id, client_secret, token_url).

#### `Then the request should include Authorization header`
Validates Authorization header is present in request.

#### `Then the OAuth2 token should be valid`
Validates OAuth2 token is valid.

### JWT Authentication

#### `Given I setup JWT with secret "{secret}" and algorithm "{algorithm}"`
Configures JWT with secret and algorithm (HS256, RS256, etc.).

#### `When I create JWT token with payload`
Creates JWT token with payload from step text.

#### `Then the token should be valid`
Validates JWT token is valid and properly signed.

#### `Then the token should contain claim "{claim}" with value "{value}"`
Validates JWT token contains specific claim.

---

## Advanced Features - Tier 3: Enterprise Features

### Reporting

#### `When I execute test suite`
Executes complete test suite for reporting.

#### `Then I should generate reports in formats`
Generates reports in specified formats (used with table).

#### `Then the report should be generated in "{format}" format`
Validates report was generated in specified format (html, json, junit, allure).

### Contract Validation

#### `Given I load OpenAPI spec from "{file_path}"`
Loads OpenAPI specification for contract validation.

#### `Then the response should match OpenAPI contract for {method} {endpoint}`
Validates response matches OpenAPI contract.

#### `Given I load AsyncAPI spec from "{file_path}"`
Loads AsyncAPI specification for contract validation.

### Chaos Engineering

#### `Given I enable chaos engineering`
Enables chaos engineering features.

#### `Given I inject latency between {min_ms:f} and {max_ms:f} milliseconds`
Injects random latency into requests.

#### `Given I inject error rate of {percentage:d} percent`
Injects random errors into requests.

#### `When I send a GET request to "{endpoint}"`
Sends request with chaos engineering enabled.

#### `Then the response should complete despite injected latency`
Validates request completed despite latency injection.

#### `Then some requests may fail due to injected errors`
Validates some requests failed due to error injection.

#### `Then circuit breaker should remain in CLOSED state`
Validates circuit breaker stayed closed despite chaos.

#### `Then error rate should be less than {percentage:d} percent`
Validates actual error rate is below threshold.

### Advanced Logging

#### `Given I set logging level to "{level}"`
Sets logging level (DEBUG, INFO, WARNING, ERROR).

#### `Given I enable request logging to directory "{directory}"`
Enables request logging to specified directory.

#### `Then request and response should be logged to file`
Validates request/response were logged to file.

---

## Integration Scenarios

### Full Stack Testing

#### `Given I set performance alert for response_time threshold {threshold:d} milliseconds`
Sets performance alert threshold.

#### `Then performance metrics should be collected`
Validates performance metrics were collected.

#### `Then cache should contain {count:d} entry`
Validates cache contains specified number of entries.

### Resilience Testing

#### `Given I create circuit breaker with failure_threshold={threshold:d}`
Creates circuit breaker for resilience testing.

#### `When I send {count:d} GET requests to "{endpoint}"`
Sends multiple requests for resilience testing.

#### `Then circuit breaker should remain in CLOSED state`
Validates circuit breaker remained closed.

#### `Then error rate should be less than {percentage:d} percent`
Validates error rate stayed below threshold.

---

## Important Notes

- **Variable Interpolation**: Use `{variableName}` syntax in URLs, headers, and JSON bodies.
- **.env Files**: Steps with `from env` automatically load variables from .env files.
- **JSONPath**: Use standard JSONPath syntax like `$.field.subfield` to navigate JSON structures.
- **Data Types**: The framework automatically handles conversions between strings and numbers when appropriate.
- **Automatic Logging**: When enabled, automatically saves requests/responses with timestamps and metadata.
- **Pattern Matching**: Supports Karate-style patterns like `##string`, `##number`, `##email`, etc.
- **File Formats**: Supports JSON, YAML, and CSV files for test data.
- **Backoff Strategies**: Retry policies support linear, exponential, fibonacci, and random strategies.
- **Circuit Breaker States**: CLOSED (normal), OPEN (failing), HALF_OPEN (testing recovery).
- **Performance Metrics**: Includes avg, p95, p99 response times, error rate, and throughput.
- **Verification**: This documentation has been verified against the source code v1.5.0.

---

*Judo Framework v1.5.0 - Documentation verified against source code*