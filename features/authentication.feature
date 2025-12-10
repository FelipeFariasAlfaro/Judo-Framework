Feature: API Authentication Testing
  As a developer
  I want to test different authentication methods
  So that I can ensure my API security works correctly

  Background:
    Given I have a Judo API client
    And the base URL is "https://httpbin.org"

  Scenario: Basic Authentication
    Given I use basic authentication with username "user" and password "pass"
    When I send a GET request to "/basic-auth/user/pass"
    Then the response status should be 200
    And the response field "authenticated" should equal 1
    And the response "$.user" should be "user"

  Scenario: Bearer Token Authentication
    Given I set the variable "token" to "fake-jwt-token-12345"
    And I use bearer token "{token}"
    When I send a GET request to "/bearer"
    Then the response status should be 401

  Scenario: Custom Header Authentication
    Given I set the header "X-API-Key" to "secret-api-key-123"
    When I send a GET request to "/headers"
    Then the response status should be 200
    And the response "$.headers.X-Api-Key" should be "secret-api-key-123"

  Scenario: Authentication with Variables
    Given I set the variable "apiKey" to "my-secret-key"
    And I set the header "Authorization" to "ApiKey {apiKey}"
    When I send a GET request to "/headers"
    Then the response status should be 200
    And the response should contain "headers"