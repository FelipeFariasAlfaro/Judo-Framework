Feature: API Test English

  Scenario: GET request with validations
    Given the base URL is "https://jsonplaceholder.typicode.com"
    When I send a GET request to "/posts/1"
    Then the response status should be 200
    And the response should contain "userId" with value 1

  Scenario: POST request with data
    Given the base URL is "https://jsonplaceholder.typicode.com"
    When I send a POST request to "/posts" with JSON:
      """
      {
        "title": "Test Post",
        "body": "Test Content",
        "userId": 1
      }
      """
    Then the response status should be 201
