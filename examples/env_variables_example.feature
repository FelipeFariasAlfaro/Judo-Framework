# language: en
Feature: Using Environment Variables from .env file

  Background:
    Given I have a Judo API client
    And the base URL is "https://jsonplaceholder.typicode.com"

  @env @headers
  Scenario: Set headers from environment variables
    # This demonstrates loading headers from .env file
    # Create a .env file with: API_TOKEN=Bearer test123
    Given I set the header "Authorization" from env "API_TOKEN"
    And I set the header "X-API-Key" from env "API_KEY"
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "id"

  @env @multiple-headers
  Scenario: Multiple headers from environment
    # Load multiple headers from .env
    Given I set the header "Authorization" from env "API_TOKEN"
    And I set the header "X-API-Key" from env "API_KEY"
    And I set the header "X-Custom-Header" from env "CUSTOM_HEADER_1"
    When I send a GET request to "/posts/1"
    Then the response status should be 200
    And the response should contain "title"
