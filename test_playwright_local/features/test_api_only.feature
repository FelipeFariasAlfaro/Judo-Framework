# Test API-only functionality to ensure backward compatibility

Feature: API Testing (Backward Compatibility)

  Background:
    Given I have a Judo API client
    And the base URL is "https://httpbin.org"

  @api @smoke
  Scenario: Basic GET request
    When I send a GET request to "/get"
    Then the response status should be 200
    And the response should contain "url"
    And the response should contain "headers"

  @api @smoke
  Scenario: POST request with JSON
    When I send a POST request to "/post" with JSON:
      """
      {
        "name": "Test User",
        "email": "test@example.com",
        "age": 30
      }
      """
    Then the response status should be 200
    And the response should contain "json"
    And the response "$.json.name" should be "Test User"
    And the response "$.json.email" should be "test@example.com"

  @api @variables
  Scenario: Variable extraction and usage
    When I send a GET request to "/uuid"
    Then the response status should be 200
    And the response should contain "uuid"
    And I extract "$.uuid" from the response as "testUuid"
    
    When I send a POST request to "/post" with JSON:
      """
      {
        "uuid": "{testUuid}",
        "message": "Using extracted UUID"
      }
      """
    Then the response status should be 200
    And the response "$.json.uuid" should be "{testUuid}"

  @api @headers
  Scenario: Custom headers
    Given I set the header "X-Test-Header" to "test-value"
    And I set the header "X-Custom-ID" to "12345"
    When I send a GET request to "/headers"
    Then the response status should be 200
    And the response should contain "X-Test-Header"
    And the response should contain "X-Custom-ID"

  @api @auth
  Scenario: Bearer token authentication
    Given I use the bearer token "test-token-123"
    When I send a GET request to "/bearer"
    Then the response status should be 200
    And the response should contain "authenticated"
    And the response should contain "token"

  @api @validation
  Scenario: Response validation with patterns
    When I send a GET request to "/json"
    Then the response status should be 200
    And the response should match:
      """
      {
        "slideshow": {
          "author": "##string",
          "date": "##string",
          "slides": "##array",
          "title": "##string"
        }
      }
      """