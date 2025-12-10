# Getting Started with Judo Framework

Judo Framework is a comprehensive API testing library for Python that brings all the power and simplicity of Karate Framework to the Python ecosystem.

**Created by Felipe Farias at [CENTYC](https://www.centyc.cl) - Centro Latinoamericano de Testing y Calidad del Software**

## Installation

```bash
pip install judo-framework
```

## Quick Start

### Basic Example

```python
from judo import Judo

# Create a Judo instance
judo = Judo()

# Configure base URL
judo.url = "https://jsonplaceholder.typicode.com"

# Make a GET request
response = judo.get("/posts/1")

# Validate response
judo.match(response.status, 200)
judo.match(response.json.userId, 1)
judo.match(response.json.title, "##string")
```

### Key Concepts

#### 1. Judo Instance
The main entry point for all operations:

```python
judo = Judo()
judo.url = "https://api.example.com"
```

#### 2. HTTP Methods
All standard HTTP methods are supported:

```python
response = judo.get("/users")
response = judo.post("/users", json=user_data)
response = judo.put("/users/1", json=updated_data)
response = judo.delete("/users/1")
```

#### 3. Response Object
Rich response object with convenient properties:

```python
response = judo.get("/users/1")

# Status code
print(response.status)  # 200

# JSON data
user = response.json
print(user.name)

# Headers
print(response.headers)

# Text content
print(response.text)
```

#### 4. Matching/Validation
Powerful matching system similar to Karate:

```python
# Exact matching
judo.match(response.status, 200)
judo.match(response.json.name, "John Doe")

# Type matching
judo.match(response.json.id, "##number")
judo.match(response.json.email, "##string")
judo.match(response.json.active, "##boolean")

# Pattern matching
judo.match(response.json.email, "##email")
judo.match(response.json.id, "##uuid")
```

#### 5. Variables
Store and reuse data across requests:

```python
# Set variables
judo.set("userId", 123)
judo.set("baseUrl", "https://api.example.com")

# Use variables
user_id = judo.get_var("userId")
response = judo.get(f"/users/{user_id}")

# Environment variables
api_key = judo.get_env("API_KEY")
```

### Configuration

#### Headers
```python
# Single header
judo.header("Authorization", "Bearer token")

# Multiple headers
judo.headers({
    "Content-Type": "application/json",
    "X-API-Key": "your-key"
})
```

#### Authentication
```python
# Basic Auth
judo.basic_auth("username", "password")

# Bearer Token
judo.bearer_token("your-jwt-token")

# OAuth2
judo.oauth2("access-token")
```

#### Query Parameters
```python
# Single parameter
judo.param("page", 1)

# Multiple parameters
judo.params({
    "page": 1,
    "limit": 10,
    "sort": "name"
})
```

### Advanced Features

#### JSONPath
Extract data using JSONPath expressions:

```python
response = judo.get("/users")
names = judo.json_path(response.json, "$[*].name")
first_user_email = judo.json_path(response.json, "$[0].email")
```

#### Schema Validation
Validate responses against JSON schemas:

```python
user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["id", "name", "email"]
}

judo.match(response.json, user_schema)
```

#### Mock Server
Built-in mock server for testing:

```python
# Start mock server
mock = judo.start_mock(port=8080)

# Add routes
mock.get("/api/users/1", {
    "status": 200,
    "body": {"id": 1, "name": "John Doe"}
})

# Test against mock
judo.url = "http://localhost:8080"
response = judo.get("/api/users/1")

# Stop mock server
judo.stop_mock()
```

### Best Practices

1. **Use Variables**: Store reusable data in variables
2. **Validate Everything**: Use comprehensive matching for all responses
3. **Organize Tests**: Group related tests in functions or classes
4. **Use Mock Servers**: Test edge cases with controlled responses
5. **Handle Errors**: Always validate error responses too

### Next Steps

- Check out the [DSL Reference](dsl-reference.md) for complete syntax
- See [Examples](../examples/) for more complex scenarios
- Read about [HTTP Client](http-client.md) advanced features
- Learn about [Data Validation](validation.md) techniques