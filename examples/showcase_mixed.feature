# language: en
@showcase @advanced @mixed
Feature: Advanced Features Showcase - Mixed Mode - Judo Framework v1.5.0

  Background:
    Given tengo un cliente Judo API
    And la URL base es "https://jsonplaceholder.typicode.com"

  # ==================== TIER 1: Core API Testing ====================

  @tier1 @basic @mixed
  Scenario: Basic GET Request
    """
    Demonstrates basic GET request with response validation
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And la respuesta debe contener el campo "title"

  @tier1 @basic @mixed
  Scenario: POST Request with JSON Body
    """
    Demonstrates POST request with JSON body
    """
    Given establezco la variable "title" a "Test Post"
    And establezco la variable "body" a "This is a test"
    When hago una petición POST a "/posts" con el cuerpo
      """
      {
        "title": "{title}",
        "body": "{body}",
        "userId": 1
      }
      """
    Then el código de respuesta debe ser 201

  @tier1 @authentication @mixed
  Scenario: Bearer Token Authentication
    """
    Demonstrates bearer token authentication
    """
    Given uso el token bearer "test-token-12345"
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200

  @tier1 @authentication @mixed
  Scenario: Basic Authentication
    """
    Demonstrates basic authentication with username and password
    """
    Given uso autenticación básica con usuario "testuser" y contraseña "testpass"
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200

  @tier1 @headers @mixed
  Scenario: Custom Headers
    """
    Demonstrates setting custom request headers
    """
    Given establezco el header "X-Custom-Header" a "CustomValue"
    And establezco el header "X-Request-ID" a "req-12345"
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200

  @tier1 @query-params @mixed
  Scenario: Query Parameters
    """
    Demonstrates setting query parameters
    """
    Given establezco el parámetro "userId" a "1"
    When hago una petición GET a "/posts"
    Then el código de respuesta debe ser 200
    And la respuesta debe ser una lista

  @tier1 @response-validation @mixed
  Scenario: Response Field Validation
    """
    Demonstrates validating specific response fields
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And el campo "userId" debe ser 1
    And el campo "id" debe ser 1

  @tier1 @response-validation @mixed
  Scenario: Response Schema Validation
    """
    Demonstrates JSON schema validation
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And la respuesta debe coincidir con el esquema
      """
      {
        "type": "object",
        "properties": {
          "userId": {"type": "number"},
          "id": {"type": "number"},
          "title": {"type": "string"},
          "body": {"type": "string"}
        },
        "required": ["userId", "id", "title", "body"]
      }
      """

  @tier1 @array-validation @mixed
  Scenario: Array Response Validation
    """
    Demonstrates array response validation
    """
    When hago una petición GET a "/posts"
    Then el código de respuesta debe ser 200
    And la respuesta debe ser una lista
    And la respuesta debe tener más de 0 elementos

  @tier1 @data-extraction @mixed
  Scenario: Extract and Store Response Data
    """
    Demonstrates extracting data from response and storing in variables
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And guardo el valor del campo "title" en la variable "post_title"
    And debo tener la variable "post_title" con valor "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"

  @tier1 @response-time @mixed
  Scenario: Response Time Validation
    """
    Demonstrates response time assertions
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And el tiempo de respuesta debe ser menor a 5.0 segundos

  # ==================== TIER 2: Advanced Features ====================

  @tier2 @variables @mixed
  Scenario: Variable Management
    """
    Demonstrates setting and using variables
    """
    Given establezco la variable "user_id" a "1"
    And establezco la variable "post_id" a "1"
    When hago una petición GET a "/posts/{post_id}"
    Then el código de respuesta debe ser 200
    And el campo "userId" debe ser 1

  @tier2 @json-path @mixed
  Scenario: JSONPath Validation
    """
    Demonstrates JSONPath expression validation
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And la respuesta "$.title" debe ser "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
    And la respuesta "$.userId" debe ser 1

  @tier2 @type-validation @mixed
  Scenario: Type Validation
    """
    Demonstrates validating data types in response
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And la respuesta "$.title" debe ser una cadena
    And la respuesta "$.userId" debe ser un número
    And la respuesta "$.id" debe ser un número

  @tier2 @array-items @mixed
  Scenario: Array Item Validation
    """
    Demonstrates validating items in array responses
    """
    When hago una petición GET a "/posts"
    Then el código de respuesta debe ser 200
    And la respuesta debe ser una lista
    And cada elemento debe tener el campo "userId"
    And cada elemento debe tener el campo "title"

  @tier2 @nested-array @mixed
  Scenario: Nested Array Validation
    """
    Demonstrates validating nested arrays
    """
    When hago una petición GET a "/posts"
    Then el código de respuesta debe ser 200
    And el array "." debe contener un elemento con "userId" igual a "1"

  @tier2 @file-operations @mixed
  Scenario: Load Test Data from File
    """
    Demonstrates loading test data from JSON file
    """
    Given cargo datos de prueba del archivo "examples/test_data/sample.json"
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200

  @tier2 @file-save @mixed
  Scenario: Save Response to File
    """
    Demonstrates saving response to file
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And guardo la respuesta en el archivo "examples/test_data/response.json"

  @tier2 @wait @mixed
  Scenario: Wait Between Requests
    """
    Demonstrates waiting between requests
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And espero 1.0 segundos
    When hago una petición GET a "/posts/2"
    Then el código de respuesta debe ser 200

  @tier2 @logging @mixed
  Scenario: Request/Response Logging
    """
    Demonstrates enabling request/response logging
    """
    Given habilito el guardado de peticiones y respuestas
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200

  @tier2 @environment-vars @mixed
  Scenario: Environment Variables
    """
    Demonstrates loading values from environment variables
    """
    Given obtengo el valor "BASE_URL" desde env y lo almaceno en "base_url"
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200

  # ==================== TIER 3: Enterprise Features ====================

  @tier3 @put-request @mixed
  Scenario: PUT Request with JSON
    """
    Demonstrates PUT request for updating resources
    """
    When hago una petición PUT a "/posts/1" con el cuerpo
      """
      {
        "id": 1,
        "title": "Updated Title",
        "body": "Updated body content",
        "userId": 1
      }
      """
    Then el código de respuesta debe ser 200

  @tier3 @patch-request @mixed
  Scenario: PATCH Request with JSON
    """
    Demonstrates PATCH request for partial updates
    """
    When hago una petición PATCH a "/posts/1" con el cuerpo
      """
      {
        "title": "Patched Title"
      }
      """
    Then el código de respuesta debe ser 200

  @tier3 @delete-request @mixed
  Scenario: DELETE Request
    """
    Demonstrates DELETE request for removing resources
    """
    When hago una petición DELETE a "/posts/1"
    Then el código de respuesta debe ser 200

  @tier3 @request-with-variable @mixed
  Scenario: Request with Variable Data
    """
    Demonstrates sending request with data from variable
    """
    Given establezco la variable "post_data" al JSON
      """
      {
        "title": "New Post",
        "body": "Post content",
        "userId": 1
      }
      """
    When hago una petición POST a "/posts" con la variable "post_data"
    Then el código de respuesta debe ser 201

  @tier3 @multiple-validations @mixed
  Scenario: Multiple Field Validations
    """
    Demonstrates validating multiple fields in response
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And el campo "userId" debe ser 1
    And el campo "id" debe ser 1
    And la respuesta debe contener el campo "title"
    And la respuesta debe contener el campo "body"

  @tier3 @success-validation @mixed
  Scenario: Success Response Validation
    """
    Demonstrates validating successful response
    """
    When hago una petición GET a "/posts/1"
    Then la respuesta debe ser exitosa

  @tier3 @json-response @mixed
  Scenario: JSON Response Validation
    """
    Demonstrates validating response is valid JSON
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And la respuesta debe ser un objeto

  @tier3 @null-validation @mixed
  Scenario: Null Value Validation
    """
    Demonstrates validating null and non-null values
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And la respuesta "$.title" no debe ser null

  @tier3 @email-validation @mixed
  Scenario: Email Format Validation
    """
    Demonstrates validating email format in response
    Note: Requires endpoint that returns email field
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200

  @tier3 @url-validation @mixed
  Scenario: URL Format Validation
    """
    Demonstrates validating URL format in response
    Note: Requires endpoint that returns URL field
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200

  @tier3 @uuid-validation @mixed
  Scenario: UUID Format Validation
    """
    Demonstrates validating UUID format in response
    Note: Requires endpoint that returns UUID field
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200

  @tier3 @variable-comparison @mixed
  Scenario: Variable Comparison
    """
    Demonstrates comparing two variables
    """
    Given establezco la variable "value1" a "test"
    And establezco la variable "value2" a "test"
    When hago una petición GET a "/posts/1"
    Then la variable "value1" debe ser igual a la variable "value2"

  @tier3 @print-response @mixed
  Scenario: Print Response for Debugging
    """
    Demonstrates printing response for debugging
    """
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And imprimo la respuesta
