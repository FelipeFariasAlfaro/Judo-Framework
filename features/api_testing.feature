Feature: API Testing with Judo Framework
  As a QA engineer
  I want to test REST APIs using Gherkin syntax
  So that I can write readable and maintainable API tests

  Background:
    Given I have a Judo API client
    And the base URL is "https://jsonplaceholder.typicode.com"

  Scenario: Get a single post
    When I send a GET request to "/posts/1"
    Then the response status should be 200
    And the response field "id" should equal 1
    And the response field "userId" should equal 1
    And the response "$.title" should be a string
    And the response "$.body" should be a string

  Scenario: Create a new post
    Given I set the header "Content-Type" to "application/json"
    When I send a POST request to "/posts" with JSON:
      """
      {
        "title": "My Test Post",
        "body": "This is a test post created by Judo Framework",
        "userId": 1
      }
      """
    Then the response status should be 201
    And the response should contain "id"
    And the response "$.id" should be a number
    And the response "$.title" should be "My Test Post"
    And the response "$.userId" should be 1

  Scenario: Update an existing post
    When I send a PUT request to "/posts/1" with JSON:
      """
      {
        "id": 1,
        "title": "Updated Post Title",
        "body": "This post has been updated",
        "userId": 1
      }
      """
    Then the response status should be 200
    And the response "$.title" should be "Updated Post Title"
    And the response "$.body" should be "This post has been updated"

  Scenario: Delete a post
    When I send a DELETE request to "/posts/1"
    Then the response status should be 200

  Scenario: Get posts with query parameters
    Given I set the query parameter "userId" to 1
    When I send a GET request to "/posts"
    Then the response status should be 200
    And the response should be an array
    And each item in the response array should have "userId"
    And the response array should contain an item with "userId" equal to "1"

  Scenario: Validate response schema
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should match the schema:
      """
      {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "name": {"type": "string"},
          "username": {"type": "string"},
          "email": {"type": "string"},
          "address": {
            "type": "object",
            "properties": {
              "street": {"type": "string"},
              "city": {"type": "string"}
            }
          }
        },
        "required": ["id", "name", "email"]
      }
      """

  Scenario: Test response time
    When I send a GET request to "/posts"
    Then the response status should be 200
    And the response time should be less than 2.0 seconds

  Scenario: Extract and reuse data
    When I send a GET request to "/users/1"
    And I extract "$.id" from the response as "userId"
    And I extract "$.name" from the response as "userName"
    When I send a GET request to "/posts?userId={userId}"
    Then the response status should be 200
    And the response should be an array