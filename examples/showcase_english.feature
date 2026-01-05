# language: en
@showcase @advanced
Feature: Advanced Features Showcase - Judo Framework v1.5.0

  Background:
    Given I have a Judo API client
    And the base URL is "https://jsonplaceholder.typicode.com"

  # ==================== TIER 1: Robustness & Reliability ====================

  @tier1 @retry
  Scenario: Retry Policy with Exponential Backoff
    """
    Demonstrates automatic retry with exponential backoff strategy
    for handling transient failures
    """
    Given I set retry policy with max_retries=3 and backoff_strategy="exponential"
    When I send a GET request to "/posts/1"
    Then the response status should be 200
    And the response should contain "title"

  @tier1 @circuit-breaker
  Scenario: Circuit Breaker Pattern
    """
    Demonstrates circuit breaker to prevent cascading failures
    """
    Given I create a circuit breaker named "api_breaker" with failure_threshold=5
    When I send a GET request to "/posts/1"
    Then the response status should be 200
    And the circuit breaker "api_breaker" should be in CLOSED state

  @tier1 @interceptors
  Scenario: Request Interceptors
    """
    Demonstrates adding custom headers via interceptors
    """
    Given I add a timestamp interceptor with header name "X-Request-Time"
    And I add an authorization interceptor with token "test-token"
    When I send a GET request to "/posts/1"
    Then the response status should be 200

  @tier1 @rate-limiting
  Scenario: Rate Limiting
    """
    Demonstrates rate limiting to respect API limits
    """
    Given I set rate limit to 10 requests per second
    When I send 5 GET requests to "/posts/1"
    Then all responses should have status 200

  @tier1 @throttle
  Scenario: Request Throttling
    """
    Demonstrates fixed delay throttling between requests
    """
    Given I set throttle with delay 100 milliseconds
    When I send a GET request to "/posts/1"
    And I send a GET request to "/posts/2"
    Then both responses should have status 200

  @tier1 @assertions
  Scenario: Advanced Assertions - Response Time
    """
    Demonstrates response time assertions
    """
    When I send a GET request to "/posts/1"
    Then the response status should be 200
    And the response time should be less than 5000 milliseconds

  @tier1 @assertions
  Scenario: Advanced Assertions - JSON Schema
    """
    Demonstrates JSON schema validation
    """
    When I send a GET request to "/posts/1"
    Then the response status should be 200
    And the response should match JSON schema:
      """
      {
        "type": "object",
        "properties": {
          "userId": {"type": "number"},
          "id": {"type": "number"},
          "title": {"type": "string"},
          "body": {"type": "string"}
        },
        "required": ["userId", "id", "title", "body"]
      }
      """

  @tier1 @assertions
  Scenario: Advanced Assertions - Array Validation
    """
    Demonstrates array length and content validation
    """
    When I send a GET request to "/posts"
    Then the response status should be 200
    And the response array should have more than 0 items
    And the response should contain all fields: ["userId", "id", "title", "body"]

  # ==================== TIER 2: Performance & Modern APIs ====================

  @tier2 @data-driven
  Scenario: Data-Driven Testing with CSV
    """
    Demonstrates running same test with multiple data sets from CSV
    """
    Given I load test data from file "examples/test_data/posts.csv"
    When I run data-driven test for each row
    Then all tests should complete successfully

  @tier2 @performance
  Scenario: Performance Monitoring
    """
    Demonstrates collecting and analyzing performance metrics
    """
    When I send 10 GET requests to "/posts/1"
    Then I should have performance metrics:
      | metric | condition |
      | avg_response_time | less than 5000 |
      | p95_response_time | less than 5000 |
      | error_rate | equals 0 |

  @tier2 @caching
  Scenario: Response Caching
    """
    Demonstrates automatic caching of GET requests
    """
    Given I enable response caching with TTL 300 seconds
    When I send a GET request to "/posts/1"
    And I send the same GET request to "/posts/1" again
    Then both responses should have status 200
    And the second response should come from cache

  @tier2 @graphql
  Scenario: GraphQL Query
    """
    Demonstrates GraphQL query execution
    Note: This requires a GraphQL endpoint
    """
    Given I set the base URL to "https://graphql-api.example.com"
    When I execute GraphQL query:
      """
      query GetUser($id: ID!) {
        user(id: $id) {
          id
          name
          email
        }
      }
      """
    Then the response should contain "user"

  @tier2 @websocket
  Scenario: WebSocket Connection
    """
    Demonstrates WebSocket real-time communication
    Note: This requires a WebSocket endpoint
    """
    Given I connect to WebSocket "wss://echo.websocket.org"
    When I send WebSocket message:
      """
      {"action": "subscribe", "channel": "updates"}
      """
    Then I should receive a WebSocket message within 5 seconds

  @tier2 @oauth2
  Scenario: OAuth2 Authentication
    """
    Demonstrates OAuth2 setup and automatic token refresh
    """
    Given I setup OAuth2 with:
      | client_id | test-client |
      | client_secret | test-secret |
      | token_url | https://auth.example.com/token |
    When I send a GET request to "/posts/1"
    Then the request should include Authorization header

  @tier2 @jwt
  Scenario: JWT Authentication
    """
    Demonstrates JWT token creation and verification
    """
    Given I setup JWT with secret "my-secret" and algorithm "HS256"
    When I create JWT token with payload:
      """
      {"user_id": 123, "username": "john"}
      """
    Then the token should be valid

  # ==================== TIER 3: Enterprise Features ====================

  @tier3 @reporting
  Scenario: Generate Multiple Report Formats
    """
    Demonstrates generating reports in HTML, JSON, JUnit, and Allure formats
    """
    When I execute test suite
    Then I should generate reports in formats:
      | format |
      | html |
      | json |
      | junit |
      | allure |

  @tier3 @contract
  Scenario: OpenAPI Contract Validation
    """
    Demonstrates validating responses against OpenAPI spec
    """
    Given I load OpenAPI spec from "examples/openapi.yaml"
    When I send a GET request to "/posts/1"
    Then the response should match OpenAPI contract for GET /posts/{id}

  @tier3 @chaos
  Scenario: Chaos Engineering - Latency Injection
    """
    Demonstrates injecting latency for resilience testing
    """
    Given I enable chaos engineering
    And I inject latency between 100 and 500 milliseconds
    When I send a GET request to "/posts/1"
    Then the response should complete despite injected latency

  @tier3 @chaos
  Scenario: Chaos Engineering - Error Injection
    """
    Demonstrates injecting errors for resilience testing
    """
    Given I enable chaos engineering
    And I inject error rate of 10 percent
    When I send 10 GET requests to "/posts/1"
    Then some requests may fail due to injected errors

  @tier3 @logging
  Scenario: Advanced Logging
    """
    Demonstrates detailed request/response logging
    """
    Given I set logging level to "DEBUG"
    And I enable request logging to directory "request_logs"
    When I send a GET request to "/posts/1"
    Then request and response should be logged to file

  # ==================== Integration Scenarios ====================

  @integration @full-stack
  Scenario: Full Stack - Retry + Rate Limit + Caching + Monitoring
    """
    Demonstrates using multiple features together
    """
    Given I set retry policy with max_retries=3
    And I set rate limit to 10 requests per second
    And I enable response caching with TTL 300 seconds
    And I set performance alert for response_time threshold 1000 milliseconds
    When I send 5 GET requests to "/posts/1"
    Then all responses should have status 200
    And performance metrics should be collected
    And cache should contain 1 entry

  @integration @resilience
  Scenario: Resilience Testing with Chaos
    """
    Demonstrates testing resilience with chaos engineering
    """
    Given I enable chaos engineering
    And I inject latency between 100 and 300 milliseconds
    And I inject error rate of 5 percent
    And I create circuit breaker with failure_threshold=10
    When I send 20 GET requests to "/posts/1"
    Then circuit breaker should remain in CLOSED state
    And error rate should be less than 10 percent
