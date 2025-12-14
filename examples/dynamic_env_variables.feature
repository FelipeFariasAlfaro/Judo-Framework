# language: en
Feature: Dynamic Environment Variables
  As a developer
  I want to load any value from .env and use it as a variable
  So I can have completely dynamic configurations

  Background:
    Given I have a Judo API client

  @env @dynamic @basic
  Scenario: Load base URL from environment variable
    # Example .env:
    # BASE_API_URL=https://jsonplaceholder.typicode.com
    Given I get the value "BASE_API_URL" from env and store it in "baseUrl"
    And the base URL is "{baseUrl}"
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "name"

  @env @dynamic @multiple
  Scenario: Complete configuration from environment variables
    # Example .env:
    # TEST_API_URL=https://jsonplaceholder.typicode.com
    # TEST_USER_ID=1
    # TEST_POST_TITLE=My Dynamic Post
    Given I get the value "TEST_API_URL" from env and store it in "apiUrl"
    And I get the value "TEST_USER_ID" from env and store it in "userId"
    And I get the value "TEST_POST_TITLE" from env and store it in "postTitle"
    And the base URL is "{apiUrl}"
    
    # Use dynamic variables in requests
    When I send a GET request to "/users/{userId}"
    Then the response status should be 200
    And the response should contain "id"
    And the response field "id" should equal {userId}
    
    # Create post with dynamic title
    When I send a POST request to "/posts" with JSON
      """
      {
        "title": "{postTitle}",
        "body": "Dynamic test content",
        "userId": {userId}
      }
      """
    Then the response status should be 201
    And the response field "title" should equal "{postTitle}"

  @env @dynamic @endpoints
  Scenario: Dynamic endpoints from environment variables
    # Example .env:
    # BASE_API_URL=https://jsonplaceholder.typicode.com
    # USER_ID=2
    # ENDPOINT_SUFFIX=/posts
    Given I get the value "BASE_API_URL" from env and store it in "baseUrl"
    And I get the value "USER_ID" from env and store it in "userId"
    And I get the value "ENDPOINT_SUFFIX" from env and store it in "endpointSuffix"
    And the base URL is "{baseUrl}"
    
    # Build endpoint dynamically
    When I send a GET request to "/users/{userId}{endpointSuffix}"
    Then the response status should be 200
    And the response should be an array

  @env @dynamic @authentication
  Scenario: Dynamic authentication from environment variables
    # Example .env:
    # TEST_API_URL=https://jsonplaceholder.typicode.com
    # AUTH_TOKEN=Bearer abc123xyz
    # TENANT_ID=tenant_test
    Given I get the value "TEST_API_URL" from env and store it in "apiUrl"
    And I get the value "AUTH_TOKEN" from env and store it in "authToken"
    And I get the value "TENANT_ID" from env and store it in "tenantId"
    And the base URL is "{apiUrl}"
    And I use bearer token "{authToken}"
    And I set the header "X-Tenant-ID" to "{tenantId}"
    
    When I send a GET request to "/users/1"
    Then the response status should be 200

  @env @dynamic @json-variables
  Scenario: Environment variables in JSON data
    # Example .env:
    # TEST_API_URL=https://jsonplaceholder.typicode.com
    # POST_TITLE=Title from ENV
    # POST_BODY=Content from environment variable
    # USER_ID=1
    Given I get the value "TEST_API_URL" from env and store it in "apiUrl"
    And I get the value "POST_TITLE" from env and store it in "postTitle"
    And I get the value "POST_BODY" from env and store it in "postBody"
    And I get the value "USER_ID" from env and store it in "userId"
    And the base URL is "{apiUrl}"
    
    # Use environment variables in JSON
    When I send a POST request to "/posts" with JSON
      """
      {
        "title": "{postTitle}",
        "body": "{postBody}",
        "userId": {userId}
      }
      """
    Then the response status should be 201
    And the response field "title" should equal "{postTitle}"
    And the response field "body" should equal "{postBody}"

  @env @dynamic @complete-flow
  Scenario: Complete flow with dynamic configuration
    # Demonstration of complete flow using only environment variables
    # Example .env:
    # BASE_API_URL=https://jsonplaceholder.typicode.com
    # TEST_USER_ID=1
    # NEW_POST_TITLE=Dynamically Created Post
    # UPDATE_TITLE=Dynamically Updated Post
    
    # Load all configurations
    Given I get the value "BASE_API_URL" from env and store it in "baseUrl"
    And I get the value "TEST_USER_ID" from env and store it in "testUserId"
    And I get the value "NEW_POST_TITLE" from env and store it in "newTitle"
    And I get the value "UPDATE_TITLE" from env and store it in "updateTitle"
    And the base URL is "{baseUrl}"
    
    # CREATE - Create post with dynamic data
    When I send a POST request to "/posts" with JSON
      """
      {
        "title": "{newTitle}",
        "body": "Dynamic test content",
        "userId": {testUserId}
      }
      """
    Then the response status should be 201
    And I extract "id" from the response as "postId"
    
    # READ - Verify created post
    When I send a GET request to "/posts/{postId}"
    Then the response status should be 200
    And the response field "title" should equal "{newTitle}"
    
    # UPDATE - Update with new dynamic title
    When I send a PUT request to "/posts/{postId}" with JSON
      """
      {
        "id": {postId},
        "title": "{updateTitle}",
        "body": "Dynamically updated content",
        "userId": {testUserId}
      }
      """
    Then the response status should be 200
    And the response field "title" should equal "{updateTitle}"
    
    # DELETE
    When I send a DELETE request to "/posts/{postId}"
    Then the response status should be 200