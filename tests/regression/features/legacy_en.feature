@regression
Feature: Legacy English steps keep working

  Background:
    Given I have a Judo API client
    And the base URL is "__BASE__"

  Scenario: GET and basic validations
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should be successful
    And the response should be valid JSON
    And the response "$.name" should be "Ana"
    And the response "$.id" should be 1
    And the response should contain "email"
    And the response "$.active" should be a boolean
    And the response "$.age" should be a number
    And the response "$.name" should be a string
    And the response "$.tags" should be an array
    And the response "$.address" should be an object
    And the response "$.nickname" should be null
    And the response "$.name" should not be null
    And the response "$.email" should be a valid email
    And the response "$.uuid" should be a valid UUID
    And the response "$.website" should be a valid URL
    And the response field "name" should match pattern "^A.*"
    And the response field "age" should be in range 18 to 65

  Scenario: Arrays
    When I send a GET request to "/users"
    Then the response should be an array
    And the response array should have 2 items
    And the response array should have more than 1 items
    And the response array should contain an item with "name" equal to "Luis"
    And each item in the response array should have "email"

  Scenario: Variables and extraction (both interpolation syntaxes)
    When I send a GET request to "/users/1"
    And I extract "$.name" from the response as "userName"
    And I set the variable "who" to "Ana"
    And I set the variable "count" to 5
    Then I should have variable "userName" with value "Ana"
    When I send a GET request to "/echo?name={userName}&other=${who}"
    Then the response "$.query.name" should be "Ana"
    And the response "$.query.other" should be "Ana"

  Scenario: Headers, query params and auth
    Given I set the header "X-Custom" to "abc"
    And I set the query parameter "q" to "search"
    And I use bearer token "tok123"
    When I send a GET request to "/echo"
    Then the response "$.headers.x-custom" should be "abc"
    And the response "$.query.q" should be "search"
    And the response "$.headers.authorization" should be "Bearer tok123"

  Scenario: Basic auth
    Given I use basic authentication with username "u" and password "p"
    When I send a GET request to "/echo"
    Then the response field "headers.authorization" should match pattern "^Basic .+"

  Scenario: POST PUT PATCH DELETE
    When I send a POST request to "/users" with JSON
      """
      {"name": "Nuevo"}
      """
    Then the response status should be 201
    And the response "$.id" should be 99
    When I send a PUT request to "/users/1" with JSON
      """
      {"name": "Cambiado"}
      """
    Then the response "$.name" should be "Cambiado"
    When I send a PATCH request to "/users/1" with JSON
      """
      {"age": 31}
      """
    Then the response "$.age" should be 31
    When I send a DELETE request to "/users/1"
    Then the response should contain "deleted"

  Scenario: Time assertions and wait
    When I send a GET request to "/health"
    Then the response time should be less than 5.0 seconds
    And the response time should be less than 5000 milliseconds
    When I wait 0.1 seconds

  Scenario: Retry policy recovers from flaky endpoint
    Given I send a GET request to "/reset"
    And I set retry policy with max_retries=3 and backoff_strategy="linear"
    When I send a GET request to "/flaky"
    Then the response status should be 200

  Scenario: Response caching
    Given I enable response caching with TTL 30 seconds
    When I send a GET request to "/users"
    And I send the same GET request to "/users" again
    Then the second response should come from cache

  Scenario: Performance monitoring
    Given I enable performance monitoring
    When I send 3 GET requests to "/health"
    Then I should have performance metrics
    And the average response time should be less than 5000 milliseconds
    And the error rate should be less than 50 percent

  Scenario: Interceptors
    Given I add timestamp interceptor with header name "X-Ts"
    When I send a GET request to "/echo"
    Then the response field "headers.x-ts" should match pattern ".+"

  Scenario: Rate limit and throttle do not break requests
    Given I set rate limit to 50 requests per second
    When I send a GET request to "/health"
    Then the response status should be 200

  Scenario: JSON Schema
    When I send a GET request to "/users/1"
    Then the response should conform to JSON Schema
      """
      {"type": "object", "required": ["id", "name"], "properties": {"id": {"type": "integer"}}}
      """

  Scenario: Failure detection still fails correctly
    When I send a GET request to "/status?code=404"
    Then the response status should be 404

  Scenario: Field-level validators (rely on context.judo response helpers)
    When I send a GET request to "/users/1"
    Then the response field "age" should be of type "integer"
    And the response field "name" should be of type "string"
    And the response field "email" should be a valid email
    And the response field "website" should be a valid URL
    And the response field "uuid" should be a valid UUID
    And the response field "created" should be a valid ISO date
    And the response field "name" should match pattern "^A.*"
    And the response should have required fields
      | field | type    | required |
      | id    | integer | true     |
      | name  | string  | true     |

  Scenario: Array structure and consistency validators
    When I send a GET request to "/users"
    Then the response should have consistent data types across array items
    And the response array should contain objects with structure
      | field | type    |
      | id    | integer |
      | name  | string  |

  Scenario: Extraction through the Judo facade
    When I send a GET request to "/users/1"
    And I extract "$.address.city" from the response as "city"
    Then I should have variable "city" with value "Santiago"
