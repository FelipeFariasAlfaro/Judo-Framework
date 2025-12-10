Feature: Data-Driven API Testing
  As a QA engineer
  I want to run the same test with different data sets
  So that I can validate API behavior with various inputs

  Background:
    Given I have a Judo API client
    And the base URL is "https://jsonplaceholder.typicode.com"

  Scenario Outline: Validate different users
    When I send a GET request to "/users/<user_id>"
    Then the response status should be 200
    And the response "$.id" should be <user_id>
    And the response "$.name" should be a string
    And the response "$.email" should be a valid email
    And the response "$.username" should be "<expected_username>"

    Examples:
      | user_id | expected_username |
      | 1       | Bret             |
      | 2       | Antonette        |
      | 3       | Samantha         |

  Scenario Outline: Create posts with different data
    When I send a POST request to "/posts" with JSON:
      """
      {
        "title": "<title>",
        "body": "<body>",
        "userId": <user_id>
      }
      """
    Then the response status should be 201
    And the response "$.title" should be "<title>"
    And the response "$.userId" should be <user_id>

    Examples:
      | title           | body                    | user_id |
      | First Post      | This is my first post   | 1       |
      | Second Post     | This is my second post  | 2       |
      | Technical Post  | Technical content here  | 3       |

  Scenario: Test with complex test data
    Given I load test data "users" from JSON:
      """
      [
        {
          "name": "John Doe",
          "email": "john@example.com",
          "username": "johndoe"
        },
        {
          "name": "Jane Smith", 
          "email": "jane@example.com",
          "username": "janesmith"
        }
      ]
      """
    When I send a POST request to "/users" with the variable "users"
    Then the response status should be 201