# language: en
Feature: Judo Framework Complete Showcase
  This feature demonstrates all capabilities of Judo Framework
  Each scenario showcases a specific feature or step type

  Background:
    Given I have a Judo API client
    And the base URL is "https://jsonplaceholder.typicode.com"

  # ============================================
  # BASIC HTTP METHODS
  # ============================================

  @http @get
  Scenario: GET request - Retrieve a resource
    # GET is used to retrieve/read data from the server
    # It should NOT modify any data
    # Status 200 means success
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "id"
    And the response should contain "name"
    And the response should contain "email"

  @http @post
  Scenario: POST request - Create a new resource
    # POST is used to CREATE new resources on the server
    # Send data in JSON format in the request body
    # Status 201 means "Created" - resource was successfully created
    # The response usually includes the new resource with its generated ID
    When I send a POST request to "/posts" with JSON
      """
      {
        "title": "Judo Framework Test",
        "body": "Testing POST request",
        "userId": 1
      }
      """
    Then the response status should be 201
    And the response should contain "id"
    And the response field "title" should equal "Judo Framework Test"

  @http @put
  Scenario: PUT request - Update entire resource
    # PUT is used to REPLACE/UPDATE an entire resource
    # You must send ALL fields, even if only changing one
    # Missing fields may be set to null or default values
    # Status 200 means the update was successful
    When I send a PUT request to "/posts/1" with JSON
      """
      {
        "id": 1,
        "title": "Updated Title",
        "body": "Updated Body",
        "userId": 1
      }
      """
    Then the response status should be 200
    And the response field "title" should equal "Updated Title"

  @http @patch
  Scenario: PATCH request - Partial update
    # PATCH is used for PARTIAL updates
    # Only send the fields you want to change
    # Other fields remain unchanged
    # More efficient than PUT when updating few fields
    When I send a PATCH request to "/posts/1" with JSON
      """
      {
        "title": "Patched Title"
      }
      """
    Then the response status should be 200
    And the response field "title" should equal "Patched Title"

  @http @delete
  Scenario: DELETE request - Remove a resource
    # DELETE is used to remove/delete a resource
    # Usually returns 200 (OK) or 204 (No Content)
    # After deletion, GET requests to the same resource should return 404
    When I send a DELETE request to "/posts/1"
    Then the response status should be 200

  # ============================================
  # QUERY PARAMETERS
  # ============================================

  @query-params
  Scenario: Query parameters - Filter results with string value
    # This filters posts to only show posts from userId=1
    # URL will be: /posts?userId=1
    Given I set the query parameter "userId" to "1"
    When I send a GET request to "/posts"
    Then the response status should be 200
    And the response should be an array
    And each item in the response array should have "userId"

  @query-params
  Scenario: Query parameters - Limit results with numeric value
    # This limits the response to only 5 items
    # URL will be: /posts?_limit=5
    Given I set the query parameter "_limit" to 5
    When I send a GET request to "/posts"
    Then the response status should be 200
    And the response array should have 5 items

  @query-params
  Scenario: Query parameters - Multiple parameters combined
    # Combine multiple query parameters
    # URL will be: /posts?userId=1&_limit=3
    Given I set the query parameter "userId" to 1
    And I set the query parameter "_limit" to 3
    When I send a GET request to "/posts"
    Then the response status should be 200
    And the response should be an array
    And the response array should have 3 items

  # ============================================
  # HEADERS
  # ============================================

  @headers
  Scenario: Custom headers
    # Headers provide metadata about the request
    # Common uses: authentication, content type, API versioning, tracking
    # X-Custom-Header: custom application-specific header
    # Accept: tells server what format you want in response
    Given I set the header "X-Custom-Header" to "test-value"
    And I set the header "Accept" to "application/json"
    When I send a GET request to "/users/1"
    Then the response status should be 200

  # ============================================
  # VARIABLES
  # ============================================

  @variables @string
  Scenario: Variables - String values
    # Variables allow you to reuse values across steps
    # Use {variableName} syntax to interpolate variables in URLs
    # This makes tests more maintainable and flexible
    Given I set the variable "userId" to "1"
    When I send a GET request to "/users/{userId}"
    Then the response status should be 200
    And the response field "id" should equal 1

  @variables @number
  Scenario: Variables - Numeric values
    # Variables can store numbers too
    # Useful for IDs, counts, or any numeric value
    # Can be used in URLs, JSON bodies, and validations
    Given I set the variable "postId" to 1
    When I send a GET request to "/posts/{postId}"
    Then the response status should be 200
    And the response field "id" should equal 1

  @variables @json
  Scenario: Variables - JSON objects
    # Variables can store entire JSON objects
    # Perfect for reusing complex request bodies
    # Keeps your tests DRY (Don't Repeat Yourself)
    Given I set the variable "newPost" to the JSON
      """
      {
        "title": "Variable Test",
        "body": "Testing JSON variable",
        "userId": 1
      }
      """
    When I send a POST request to "/posts" with the variable "newPost"
    Then the response status should be 201
    And the response field "title" should equal "Variable Test"

  # ============================================
  # DATA EXTRACTION
  # ============================================

  @extraction
  Scenario: Extract data from response
    # Extract specific fields from responses to use in later steps
    # Common use case: Create a resource, extract its ID, then use that ID
    # This enables testing complete workflows
    When I send a POST request to "/posts" with JSON
      """
      {
        "title": "Extract Test",
        "body": "Testing extraction",
        "userId": 1
      }
      """
    Then the response status should be 201
    # Extract the "id" field and store it as "createdPostId" variable
    And I extract "$.id" from the response as "createdPostId"
    # Now use the extracted ID to fetch the created post
    When I send a GET request to "/posts/{createdPostId}"
    Then the response status should be 200
    And the response field "title" should equal "Extract Test"

  @extraction
  Scenario: Store complete response
    # Sometimes you need to store the entire response
    # Useful for complex validations or passing data between scenarios
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And I store the response as "userResponse"

  # ============================================
  # RESPONSE VALIDATION
  # ============================================

  @validation @status
  Scenario: Validate status codes
    # Always validate the HTTP status code
    # 200 = OK, 201 = Created, 204 = No Content, 400 = Bad Request, etc.
    # "should be successful" checks for any 2xx status (200-299)
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should be successful

  @validation @fields
  Scenario: Validate response fields - String
    # Validate that specific fields have expected string values
    # Useful for checking data integrity and API contracts
    # Values must match exactly (case-sensitive)
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response field "name" should equal "Leanne Graham"
    And the response field "username" should equal "Bret"

  @validation @fields
  Scenario: Validate response fields - Number
    # Validate numeric field values
    # Judo automatically handles type checking
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response field "id" should equal 1

  @validation @contains
  Scenario: Validate response contains keys
    # Check that response has required fields
    # Doesn't validate the values, just that the keys exist
    # Perfect for API contract testing
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "id"
    And the response should contain "name"
    And the response should contain "email"
    And the response should contain "address"
    And the response should contain "company"

  @validation @json
  Scenario: Validate response is valid JSON
    # Ensure the response is properly formatted JSON
    # Catches malformed responses early
    When I send a GET request to "/users/1"
    Then the response should be valid JSON

  # ============================================
  # JSONPATH VALIDATION
  # ============================================

  @jsonpath @string
  Scenario: JSONPath validation - String values
    # Use JSONPath expressions to validate nested data
    # $.field accesses top-level fields
    # $.nested.field accesses nested fields
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response "$.name" should be "Leanne Graham"
    And the response "$.address.city" should be "Gwenborough"

  @jsonpath @number
  Scenario: JSONPath validation - Numeric values
    # JSONPath can validate numeric values too
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response "$.id" should be 1

  @jsonpath @type
  Scenario: JSONPath type validation
    # Validate that fields are of expected types
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response "$.name" should be a string
    And the response "$.id" should be a number

  # ============================================
  # ARRAY VALIDATION
  # ============================================

  @arrays @basic
  Scenario: Validate array response
    # Check that the response is an array (list)
    # Important when expecting multiple items
    When I send a GET request to "/users"
    Then the response status should be 200
    And the response should be an array

  @arrays @count
  Scenario: Validate array count
    # Validate the exact number of items in the array
    # Useful for pagination testing and data integrity checks
    Given I set the query parameter "_limit" to 5
    When I send a GET request to "/posts"
    Then the response status should be 200
    And the response array should have 5 items

  @arrays @contains
  Scenario: Validate array contains item
    # Search for specific items in an array
    # Checks if at least one item matches the criteria
    # Great for verifying data exists in collections
    When I send a GET request to "/users"
    Then the response status should be 200
    And the response array should contain an item with "id" equal to "1"
    And the response array should contain an item with "username" equal to "Bret"

  @arrays @each
  Scenario: Validate each array item has field
    # Ensure ALL items in the array have required fields
    # Validates data consistency across the collection
    # Catches missing or malformed items
    When I send a GET request to "/users"
    Then the response status should be 200
    And each item in the response array should have "id"
    And each item in the response array should have "name"
    And each item in the response array should have "email"

  # ============================================
  # WORKFLOW - COMPLETE CRUD
  # ============================================

  @workflow @crud
  Scenario: Complete CRUD workflow
    # This demonstrates a complete CRUD (Create, Read, Update, Delete) workflow
    # This is a common pattern in API testing
    
    # CREATE - Create a new resource
    When I send a POST request to "/posts" with JSON
      """
      {
        "title": "CRUD Test Post",
        "body": "Testing complete CRUD operations",
        "userId": 1
      }
      """
    Then the response status should be 201
    # Extract the ID to use in subsequent operations
    And I extract "$.id" from the response as "postId"
    
    # READ - Retrieve the created resource
    When I send a GET request to "/posts/{postId}"
    Then the response status should be 200
    And the response field "title" should equal "CRUD Test Post"
    
    # UPDATE - Replace the entire resource
    When I send a PUT request to "/posts/{postId}" with JSON
      """
      {
        "id": 1,
        "title": "Updated CRUD Post",
        "body": "Updated body",
        "userId": 1
      }
      """
    Then the response status should be 200
    And the response field "title" should equal "Updated CRUD Post"
    
    # PARTIAL UPDATE - Update only specific fields
    When I send a PATCH request to "/posts/{postId}" with JSON
      """
      {
        "title": "Patched CRUD Post"
      }
      """
    Then the response status should be 200
    
    # DELETE - Remove the resource
    When I send a DELETE request to "/posts/{postId}"
    Then the response status should be 200

  # ============================================
  # WORKFLOW - AUTHENTICATION FLOW
  # ============================================

  @workflow @auth
  Scenario: Authentication workflow with token
    # Real-world scenario: Login, get token, use token for authenticated requests
    # Step 1: Simulate getting a token (in real tests, you'd POST to /login)
    Given I set the variable "authToken" to "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    # Step 2: Set the token for all subsequent requests
    And I use bearer token "{authToken}"
    # Step 3: Make authenticated request
    When I send a GET request to "/users/1"
    Then the response status should be 200

  # ============================================
  # UTILITY FEATURES
  # ============================================

  @utility @wait
  Scenario: Wait between requests
    # Add delays between requests when needed
    # Useful for: rate limiting, async operations, timing tests
    When I send a GET request to "/users/1"
    Then the response status should be 200
    # Wait 1 second before next request
    And I wait 1.0 seconds
    When I send a GET request to "/users/2"
    Then the response status should be 200

  @utility @debug
  Scenario: Print response for debugging
    # Print the response to console for debugging
    # Helpful during test development to see actual response data
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And I print the response

  # ============================================
  # COMPLEX SCENARIOS
  # ============================================

  @complex @nested
  Scenario: Working with nested data
    # APIs often return nested objects (objects within objects)
    # Validate that nested structures exist
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "address"
    And the response should contain "company"

  @complex @multiple-requests
  Scenario: Multiple related requests
    # Real-world scenario: Chain multiple API calls together
    # Each request uses data from the previous one
    
    # Step 1: Get user information
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And I extract "$.id" from the response as "userId"
    
    # Step 2: Get all posts from that user
    Given I set the query parameter "userId" to "{userId}"
    When I send a GET request to "/posts"
    Then the response status should be 200
    And the response should be an array
    
    # Step 3: Get details of a specific post
    When I send a GET request to "/posts/1"
    Then the response status should be 200
    And I extract "$.id" from the response as "postId"
    
    # Step 4: Get all comments on that post
    When I send a GET request to "/posts/{postId}/comments"
    Then the response status should be 200
    And the response should be an array

  @complex @data-driven
  Scenario Outline: Data-driven testing with examples
    # Run the same test with different data
    # Perfect for testing multiple users, IDs, or scenarios
    # The scenario runs once for each row in the Examples table
    When I send a GET request to "/users/<userId>"
    Then the response status should be 200
    And the response field "id" should equal <userId>
    And the response should contain "name"
    And the response should contain "email"
    
    Examples:
      | userId |
      | 1      |
      | 2      |
      | 3      |

  # ============================================
  # PERFORMANCE
  # ============================================

  @performance
  Scenario: Validate response time
    # Ensure API responds within acceptable time limits
    # Important for SLA compliance and user experience
    # Adjust the time threshold based on your requirements
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response time should be less than 5.0 seconds

  # ============================================
  # ENVIRONMENT VARIABLES (.env)
  # ============================================

  @env @security
  Scenario: Use environment variables for authentication
    # Load sensitive data like API tokens from .env file
    # This keeps credentials out of version control
    # Create a .env file with: API_TOKEN=Bearer test123
    # Create a .env file with: API_KEY=your_api_key_here
    Given I set the header "Authorization" from env "API_TOKEN"
    And I set the header "X-API-Key" from env "API_KEY"
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "id"

  @env @multiple-headers
  Scenario: Multiple headers from environment variables
    # Load multiple headers from .env for complex authentication
    # Useful for APIs requiring multiple authentication headers
    # Example .env:
    #   API_TOKEN=Bearer eyJhbGc...
    #   API_KEY=sk_test_123
    #   TENANT_ID=tenant_abc
    Given I set the header "Authorization" from env "API_TOKEN"
    And I set the header "X-API-Key" from env "API_KEY"
    And I set the header "X-Tenant-ID" from env "TENANT_ID"
    When I send a GET request to "/posts/1"
    Then the response status should be 200
    And the response should contain "title"

  # ============================================
  # ERROR HANDLING
  # ============================================

  @errors @not-found
  Scenario: Handle 404 Not Found
    # Test that API properly handles requests for non-existent resources
    # Should return 404 status code
    # Important for API contract and error handling validation
    When I send a GET request to "/users/999999"
    Then the response status should be 404

  @errors @validation
  Scenario: Validate error responses
    # Test how API handles invalid or incomplete data
    # In this case, sending empty JSON to create endpoint
    # Note: JSONPlaceholder is lenient and returns 201 anyway
    # In real APIs, this might return 400 Bad Request
    When I send a POST request to "/posts" with JSON
      """
      {}
      """
    Then the response status should be 201

  # ============================================
  # FILE OPERATIONS - SIMPLE AND DIRECT
  # ============================================

  @files @post-json
  Scenario: POST request using JSON file
    # Simply specify the JSON file path - Judo loads and sends the data
    # File: examples/test_data/simple_post.json
    When I POST to "/posts" with JSON file "examples/test_data/simple_post.json"
    Then the response status should be 201
    And the response should contain "id"
    And the response field "title" should equal "Simple Post from File"

  @files @put-json
  Scenario: PUT request using JSON file
    # Update a resource using data from a JSON file
    # File: examples/test_data/update_post.json
    When I PUT to "/posts/1" with JSON file "examples/test_data/update_post.json"
    Then the response status should be 200
    And the response field "title" should equal "Updated Post Title"

  @files @patch-json
  Scenario: PATCH request using JSON file
    # Partial update using data from a JSON file
    When I PATCH to "/posts/1" with JSON file "examples/test_data/simple_post.json"
    Then the response status should be 200
    And the response field "title" should equal "Simple Post from File"

  @files @schema-validation
  Scenario: Validate response against JSON schema file
    # Validate API response structure using a JSON schema file
    # File: examples/test_data/simple_schema.json
    When I send a POST request to "/posts" with JSON
      """
      {
        "title": "Schema Test",
        "body": "Testing schema validation",
        "userId": 1
      }
      """
    Then the response status should be 201
    And the response should match schema file "examples/test_data/simple_schema.json"

  @files @save-response
  Scenario: Save response to file
    # Save API responses to files for later analysis or debugging
    When I send a GET request to "/posts/1"
    Then the response status should be 200
    And I save the response to file "examples/output/saved_response.json"

  @files @save-variable
  Scenario: Save extracted data to file
    # Extract data from response and save it to a file
    When I send a GET request to "/posts/1"
    Then the response status should be 200
    And I extract "$.title" from the response as "postTitle"
    And I save the variable "postTitle" to file "examples/output/post_title.txt"