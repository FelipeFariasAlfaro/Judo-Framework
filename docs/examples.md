# 📚 Examples - Judo Framework

This document provides comprehensive examples of using Judo Framework for API testing.

**Created by Felipe Farias at [CENTYC](https://www.centyc.cl) - Centro Latinoamericano de Testing y Calidad del Software**

## 🚀 Basic Examples

### Simple GET Request

```python
from judo import Judo

judo = Judo()
response = judo.get("https://jsonplaceholder.typicode.com/users/1")

# Validate response
judo.match(response.status, 200)
judo.match(response.json["name"], "##string")
judo.match(response.json["email"], "##email")
```

### POST Request with JSON

```python
from judo import Judo

judo = Judo()

# Create new user
user_data = {
    "name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com"
}

response = judo.post("https://jsonplaceholder.typicode.com/users", user_data)
judo.match(response.status, 201)
judo.match(response.json["name"], "John Doe")
```

### Using Variables

```python
from judo import Judo

judo = Judo()

# Set variables
judo.set("baseUrl", "https://jsonplaceholder.typicode.com")
judo.set("userId", 1)

# Use variables in requests
response = judo.get(f"{judo.get('baseUrl')}/users/{judo.get('userId')}")
judo.match(response.status, 200)
```

## 🧪 BDD Examples with Behave

### Basic Feature File

**features/user_api.feature:**
```gherkin
Feature: User API Testing
  Background:
    Given I set the base URL to "https://jsonplaceholder.typicode.com"
  
  @smoke
  Scenario: Get user by ID
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain:
      | field    | value    |
      | id       | 1        |
      | name     | ##string |
      | username | ##string |
      | email    | ##email  |
  
  @api
  Scenario: Create new user
    When I send a POST request to "/users" with JSON:
      """
      {
        "name": "Jane Smith",
        "username": "janesmith",
        "email": "jane@example.com"
      }
      """
    Then the response status should be 201
    And the response should contain:
      | field | value      |
      | name  | Jane Smith |
      | email | jane@example.com |
```

### Environment Setup

**features/environment.py:**
```python
from judo.behave import setup_judo_context

def before_all(context):
    setup_judo_context(context)
    print("🥋 Judo Framework initialized")

def before_scenario(context, scenario):
    print(f"📝 Starting scenario: {scenario.name}")

def after_scenario(context, scenario):
    status = "✅ PASSED" if scenario.status == "passed" else "❌ FAILED"
    print(f"{status} Scenario: {scenario.name}")
```

## 🏃 Custom Runner Examples

### Basic Runner

```python
from judo.runner import BaseRunner

class APITestRunner(BaseRunner):
    def __init__(self):
        super().__init__(
            features_dir="features",
            output_dir="test_reports"
        )
    
    def run_smoke_tests(self):
        """Run smoke tests only"""
        return self.run(tags=["@smoke"])
    
    def run_api_tests(self):
        """Run all API tests"""
        return self.run(tags=["@api"])

# Usage
runner = APITestRunner()
results = runner.run_smoke_tests()
print(f"Smoke tests: {results['passed']}/{results['total']} passed")
```

### Advanced Runner with Parallel Execution

```python
from judo.runner import BaseRunner

class AdvancedTestRunner(BaseRunner):
    def __init__(self):
        super().__init__(
            features_dir="features",
            parallel=True,
            max_workers=8
        )
        
        # Configure callbacks
        self.set_callbacks(
            before_all=self.setup_test_environment,
            after_all=self.cleanup_test_environment
        )
    
    def setup_test_environment(self):
        """Setup before all tests"""
        print("🚀 Setting up test environment...")
        # Add your setup logic here
    
    def cleanup_test_environment(self, results):
        """Cleanup after all tests"""
        print("🧹 Cleaning up test environment...")
        self.print_summary()
    
    def run_regression_suite(self):
        """Run full regression test suite"""
        self.configure(
            timeout=600,      # 10 minutes per feature
            fail_fast=False,  # Don't stop on first failure
            verbose=True      # Show detailed output
        )
        return self.run(tags=["@regression"])
    
    def run_smoke_and_api_tests(self):
        """Run smoke and API tests in parallel"""
        return self.run(tags=["@smoke", "@api"], exclude_tags=["@slow"])

# Usage
runner = AdvancedTestRunner()
results = runner.run_regression_suite()
```

## 📄 File-Based Testing

### Using JSON Files

**test_data/user_data.json:**
```json
{
  "name": "Alice Johnson",
  "username": "alicej",
  "email": "alice@example.com",
  "address": {
    "street": "123 Main St",
    "city": "New York"
  }
}
```

**Python code:**
```python
from judo import Judo

judo = Judo()

# Read data from file
user_data = judo.read("test_data/user_data.json")

# Use in request
response = judo.post("https://jsonplaceholder.typicode.com/users", user_data)
judo.match(response.status, 201)
judo.match(response.json["name"], user_data["name"])
```

### Schema Validation

**schemas/user_schema.json:**
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "name": {"type": "string"},
    "username": {"type": "string"},
    "email": {"type": "string", "format": "email"}
  },
  "required": ["id", "name", "email"]
}
```

**Validation:**
```python
from judo import Judo

judo = Judo()
response = judo.get("https://jsonplaceholder.typicode.com/users/1")

# Load and validate schema
schema = judo.read("schemas/user_schema.json")
judo.match_schema(response.json, schema)
```

## 🔐 Authentication Examples

### Bearer Token

```python
from judo import Judo

judo = Judo()

# Set bearer token
judo.set_header("Authorization", "Bearer your-jwt-token-here")

# Or use helper method
judo.bearer_token("your-jwt-token-here")

response = judo.get("https://api.example.com/protected-endpoint")
judo.match(response.status, 200)
```

### Basic Authentication

```python
from judo import Judo

judo = Judo()

# Set basic auth
judo.basic_auth("username", "password")

response = judo.get("https://api.example.com/protected-endpoint")
judo.match(response.status, 200)
```

## 🎭 Mock Server Example

```python
from judo import Judo
from judo.mock import MockServer

# Create mock server
mock = MockServer(port=8080)

# Add mock endpoints
mock.add_route("GET", "/users/1", {
    "id": 1,
    "name": "Mock User",
    "email": "mock@example.com"
})

mock.add_route("POST", "/users", {
    "id": 2,
    "name": "Created User",
    "email": "created@example.com"
}, status_code=201)

# Start mock server
mock.start()

# Test against mock
judo = Judo()
response = judo.get("http://localhost:8080/users/1")
judo.match(response.status, 200)
judo.match(response.json["name"], "Mock User")

# Stop mock server
mock.stop()
```

## 📊 Data-Driven Testing

### CSV Data

**test_data/users.csv:**
```csv
name,email,age
John Doe,john@example.com,30
Jane Smith,jane@example.com,25
Bob Johnson,bob@example.com,35
```

**Python code:**
```python
from judo import Judo
import csv

judo = Judo()

# Read CSV data
with open("test_data/users.csv", "r") as file:
    users = list(csv.DictReader(file))

# Test each user
for user in users:
    response = judo.post("https://jsonplaceholder.typicode.com/users", user)
    judo.match(response.status, 201)
    judo.match(response.json["name"], user["name"])
    judo.match(response.json["email"], user["email"])
```

## 🔍 Advanced Matching

### JSONPath Matching

```python
from judo import Judo

judo = Judo()
response = judo.get("https://jsonplaceholder.typicode.com/users")

# Match array length
judo.match("$.length", 10)

# Match all user names are strings
judo.match("$[*].name", "##array")
judo.match("$[0].name", "##string")

# Match nested properties
judo.match("$[0].address.city", "##string")
```

### Pattern Matching

```python
from judo import Judo

judo = Judo()
response = judo.get("https://jsonplaceholder.typicode.com/users/1")

# Type matching
judo.match(response.json["id"], "##number")
judo.match(response.json["name"], "##string")
judo.match(response.json["email"], "##email")
judo.match(response.json["website"], "##url")

# Custom patterns
judo.match(response.json["phone"], "##regex:^[0-9-\s\(\)\.x]+$")
```

## 🚀 Running Examples

### Command Line

```bash
# Run all tests
behave features/

# Run specific tags
behave features/ --tags @smoke
behave features/ --tags @api

# Run with custom format
behave features/ --format json --outfile results.json

# Run in parallel (if supported)
behave features/ --processes 4
```

### Python Script

```python
#!/usr/bin/env python3
"""
Example test execution script
"""

from judo.runner import BaseRunner

def main():
    runner = BaseRunner(
        features_dir="features",
        parallel=True,
        max_workers=4
    )
    
    print("🧪 Running API tests...")
    
    # Run smoke tests first
    smoke_results = runner.run(tags=["@smoke"])
    print(f"Smoke tests: {smoke_results['passed']}/{smoke_results['total']}")
    
    if smoke_results['failed'] == 0:
        # Run full test suite if smoke tests pass
        full_results = runner.run(exclude_tags=["@manual"])
        print(f"Full suite: {full_results['passed']}/{full_results['total']}")
        
        return full_results['failed'] == 0
    else:
        print("❌ Smoke tests failed, skipping full suite")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
```

---

For more examples, check the [examples/](../examples/) directory in the repository.