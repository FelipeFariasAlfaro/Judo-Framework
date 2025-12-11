@test_cucumber_json
Feature: Test Cucumber JSON Generation
  Verify that Cucumber JSON is generated correctly

  @test_json_1
  Scenario: Simple GET request
    Given the base URL is "https://jsonplaceholder.typicode.com"
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "id"
    And the response should contain "name"

  @test_json_2
  Scenario: POST request with JSON
    Given the base URL is "https://jsonplaceholder.typicode.com"
    When I send a POST request to "/posts" with JSON:
      """
      {
        "title": "Test Post",
        "body": "Test Body",
        "userId": 1
      }
      """
    Then the response status should be 201
    And the response should contain "id"
