# Behave Integration - BDD Testing with Gherkin

Judo Framework provides complete integration with Behave, allowing you to write API tests using Gherkin syntax for Behavior-Driven Development (BDD).

## Installation

```bash
pip install judo-framework
# Behave is automatically installed as a dependency
```

## Quick Start

### 1. Create Feature Files

Create a `features/` directory and add `.feature` files:

```gherkin
# features/api_test.feature
Feature: User API Testing
  As a developer
  I want to test the user API
  So that I can ensure it works correctly

  Background:
    Given I have a Judo API client
    And the base URL is "https://jsonplaceholder.typicode.com"

  Scenario: Get user information
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "name"
    And the response "$.email" should be a valid email
```

### 2. Setup Environment

Create `features/environment.py`:

```python
from judo.behave.hooks import before_all, before_scenario, after_scenario, after_all
```

### 3. Import Step Definitions

Create `features/steps/judo_steps.py`:

```python
from judo.behave.steps import *
```

### 4. Run Tests

```bash
behave features/
```

## Available Step Definitions

### Setup Steps

```gherkin
Given I have a Judo API client
Given the base URL is "https://api.example.com"
Given I set the variable "userId" to "123"
Given I set the variable "userId" to 123
Given I set the header "Authorization" to "Bearer token"
Given I set the query parameter "page" to "1"
Given I set the query parameter "limit" to 10
```

### Authentication Steps

```gherkin
Given I use bearer token "jwt-token-here"
Given I use basic authentication with username "user" and password "pass"
```

### HTTP Request Steps

```gherkin
When I send a GET request to "/users"
When I send a POST request to "/users" with JSON:
  """
  {
    "name": "John Doe",
    "email": "john@example.com"
  }
  """
When I send a PUT request to "/users/1" with JSON:
  """
  {
    "name": "Updated Name"
  }
  """
When I send a DELETE request to "/users/1"
When I send a POST request to "/users" with the variable "userData"
```

### Response Validation Steps

```gherkin
Then the response status should be 200
Then the response should be successful
Then the response should contain "id"
Then the response should contain "name" with value "John Doe"
Then the response should contain "age" with value 30
Then the response "$.name" should be "John Doe"
Then the response "$.age" should be 30
Then the response "$.email" should match "##email"
```

### Type Validation Steps

```gherkin
Then the response "$.name" should be a string
Then the response "$.age" should be a number
Then the response "$.active" should be a boolean
Then the response "$.tags" should be an array
Then the response "$.profile" should be an object
Then the response "$.deletedAt" should be null
Then the response "$.createdAt" should not be null
Then the response "$.email" should be a valid email
Then the response "$.website" should be a valid URL
Then the response "$.id" should be a valid UUID
```

### Array Validation Steps

```gherkin
Then the response should be an array
Then the response array should have 10 items
Then the response array should contain an item with "name" equal to "John"
Then each item in the response array should have "id"
```

### Schema Validation

```gherkin
Then the response should match the schema:
  """
  {
    "type": "object",
    "properties": {
      "id": {"type": "integer"},
      "name": {"type": "string"},
      "email": {"type": "string", "format": "email"}
    },
    "required": ["id", "name", "email"]
  }
  """
```

### Data Extraction Steps

```gherkin
When I extract "$.id" from the response as "userId"
When I store the response as "userResponse"
```

### Utility Steps

```gherkin
When I wait 2.5 seconds
When I print the response
```

## Advanced Features

### Variables and Interpolation

```gherkin
Given I set the variable "baseUrl" to "https://api.example.com"
And I set the variable "userId" to "123"
When I send a GET request to "/users/{userId}"
Then the response "$.id" should be {userId}
```

### Data-Driven Testing

```gherkin
Scenario Outline: Test multiple users
  When I send a GET request to "/users/<user_id>"
  Then the response status should be 200
  And the response "$.name" should be "<expected_name>"

  Examples:
    | user_id | expected_name |
    | 1       | John Doe      |
    | 2       | Jane Smith    |
    | 3       | Bob Johnson   |
```

### Test Data Loading

```gherkin
Given I load test data "users" from JSON:
  """
  [
    {"name": "John", "email": "john@example.com"},
    {"name": "Jane", "email": "jane@example.com"}
  ]
  """
When I send a POST request to "/users" with the variable "users"
```

### Complex Scenarios

```gherkin
Scenario: Complete user workflow
  # Create user
  When I send a POST request to "/users" with JSON:
    """
    {
      "name": "Test User",
      "email": "test@example.com"
    }
    """
  Then the response status should be 201
  And I extract "$.id" from the response as "newUserId"
  
  # Get created user
  When I send a GET request to "/users/{newUserId}"
  Then the response status should be 200
  And the response "$.name" should be "Test User"
  
  # Update user
  When I send a PUT request to "/users/{newUserId}" with JSON:
    """
    {
      "name": "Updated User",
      "email": "updated@example.com"
    }
    """
  Then the response status should be 200
  
  # Delete user
  When I send a DELETE request to "/users/{newUserId}"
  Then the response status should be 200
```

## Configuration

### Environment Variables

Set these environment variables to configure Judo Framework:

```bash
export JUDO_BASE_URL="https://api.example.com"
export JUDO_TIMEOUT="30"
export JUDO_VERIFY_SSL="true"
export JUDO_TEST_DATA_FILE="test_data.json"
```

### Behave Configuration

Create `behave.ini`:

```ini
[behave]
default_format = pretty
show_skipped = true
logging_level = INFO
paths = features
step_definitions = features/steps
```

### Custom Step Definitions

You can add custom steps in `features/steps/custom_steps.py`:

```python
from behave import given, when, then
from judo.behave.steps import *

@given('I have custom setup')
def step_custom_setup(context):
    context.judo_context.log("Custom setup completed")

@then('I should see custom validation')
def step_custom_validation(context):
    # Your custom validation logic
    response = context.judo_context.response
    assert "custom_field" in response.json
```

## Running Tests

### Basic Execution

```bash
# Run all features
behave

# Run specific feature
behave features/api_test.feature

# Run with specific format
behave --format=json --outfile=results.json

# Run with tags
behave --tags=@smoke
behave --tags=@api,@integration
```

### CI/CD Integration

```bash
# Generate JUnit XML for CI/CD
behave --junit --junit-directory=reports/

# Generate HTML report
behave --format=html --outfile=reports/report.html
```

## Best Practices

1. **Use Background**: Set up common steps in Background sections
2. **Organize Features**: Group related scenarios in feature files
3. **Use Tags**: Tag scenarios for selective execution
4. **Variable Interpolation**: Use variables for dynamic data
5. **Schema Validation**: Validate response structure with JSON schemas
6. **Data Extraction**: Extract and reuse data between steps
7. **Error Scenarios**: Test both success and failure cases

## Example Project Structure

```
project/
├── features/
│   ├── environment.py
│   ├── api_testing.feature
│   ├── authentication.feature
│   ├── data_driven.feature
│   └── steps/
│       ├── judo_steps.py
│       └── custom_steps.py
├── behave.ini
├── requirements.txt
└── test_data.json
```

This integration makes Judo Framework a complete BDD testing solution, combining the power of Karate-like DSL with the readability of Gherkin syntax.