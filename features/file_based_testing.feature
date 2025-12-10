Feature: File-based API Testing
  As a QA engineer
  I want to use external files for request bodies and response validation
  So that I can manage test data separately from test logic

  Background:
    Given I have a Judo API client
    And the base URL is "https://jsonplaceholder.typicode.com"

  Scenario: Create user with JSON from file
    When I POST to "/users" with JSON file "test_data/users/create_user_request.json"
    Then the response status should be 201
    And the response should contain "id"
    And the response "$.name" should be "John Doe"
    And the response "$.email" should be "john.doe@example.com"

  Scenario: Update user with JSON from file
    When I PUT to "/users/1" with JSON file "test_data/users/update_user_request.json"
    Then the response status should be 200
    And the response "$.name" should be "John Doe Updated"
    And the response "$.email" should be "john.doe.updated@example.com"

  Scenario: Create post with YAML from file
    When I POST to "/posts" with data file "test_data/posts/create_post_request.yaml"
    Then the response status should be 201
    And the response "$.title" should be "My Amazing Post"
    And the response "$.userId" should be 1

  Scenario: Validate user response against schema from file
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should match schema file "test_data/schemas/user_schema.json"

  Scenario: Load test data from CSV file
    Given I load test data "users" from file "test_data/test_users.csv"
    When I send a GET request to "/users"
    Then the response status should be 200
    And the response should be an array

  Scenario: Save response to file for later use
    When I send a GET request to "/users/1"
    Then the response status should be 200
    When I save the response to file "output/user_response.json"
    And I extract "$.id" from the response as "userId"
    When I save the variable "userId" to file "output/user_id.json"

  Scenario: Data-driven testing with external file
    Given I load test data "testUsers" from file "test_data/test_users.csv"
    # Note: In a real scenario, you would iterate through the CSV data
    When I send a GET request to "/users"
    Then the response status should be 200
    And the response should be an array