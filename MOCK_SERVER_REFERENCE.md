# 🎭 Judo Mock Server - Complete Reference

**Version**: 1.3.42  
**Language**: Python 3.8+  
**Type**: Built-in HTTP Mock Server

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [HTTP Methods](#http-methods)
- [Response Configuration](#response-configuration)
- [Advanced Features](#advanced-features)
- [Behave Integration](#behave-integration)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Best Practices](#best-practices)

---

## Quick Start

```python
from judo import Judo

judo = Judo()
mock = judo.start_mock(port=8080)

mock.get("/users/1", {
    "status": 200,
    "body": {"id": 1, "name": "John Doe"}
})

judo.url = "http://localhost:8080"
response = judo.get("/users/1")
print(response.json)  # {"id": 1, "name": "John Doe"}

judo.stop_mock()
```

---

## Installation

Mock Server is included with Judo Framework:

```bash
pip install judo-framework
```

No additional dependencies required.

---

## Basic Usage

### Starting the Server

```python
from judo import Judo

judo = Judo()

# Start mock server on port 8080 (default)
mock = judo.start_mock()

# Or specify custom port
mock = judo.start_mock(port=9000)

# Server URL
print(mock.get_url())  # http://localhost:8080
```

### Stopping the Server

```python
# Stop the mock server
judo.stop_mock()

# Or directly
mock.stop()
```

### Checking Server Status

```python
if mock.is_running():
    print("Server is running")
```

---

## HTTP Methods

### GET Requests

```python
# Simple GET
mock.get("/users", {
    "status": 200,
    "body": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
})

# GET with specific ID
mock.get("/users/1", {
    "status": 200,
    "body": {"id": 1, "name": "Alice", "email": "alice@example.com"}
})
```

### POST Requests

```python
# Create resource
mock.post("/users", {
    "status": 201,
    "body": {"id": 3, "name": "Charlie", "created": True}
})

# POST with validation error
mock.post("/users/invalid", {
    "status": 400,
    "body": {"error": "Name is required"}
})
```

### PUT Requests

```python
# Update resource
mock.put("/users/1", {
    "status": 200,
    "body": {"id": 1, "name": "Alice Updated"}
})
```

### PATCH Requests

```python
# Partial update
mock.add_route("PATCH", "/users/1", {
    "status": 200,
    "body": {"id": 1, "name": "Alice Patched"}
})
```

### DELETE Requests

```python
# Delete resource
mock.delete("/users/1", {
    "status": 204,
    "body": None
})

# Delete with confirmation
mock.delete("/users/2", {
    "status": 200,
    "body": {"message": "User deleted successfully"}
})
```

---

## Response Configuration

### Status Codes

```python
# Success responses
mock.get("/ok", {"status": 200, "body": {"message": "OK"}})
mock.post("/created", {"status": 201, "body": {"id": 1}})
mock.delete("/deleted", {"status": 204, "body": None})

# Client errors
mock.get("/bad-request", {"status": 400, "body": {"error": "Bad Request"}})
mock.get("/unauthorized", {"status": 401, "body": {"error": "Unauthorized"}})
mock.get("/forbidden", {"status": 403, "body": {"error": "Forbidden"}})
mock.get("/not-found", {"status": 404, "body": {"error": "Not Found"}})

# Server errors
mock.get("/server-error", {"status": 500, "body": {"error": "Internal Server Error"}})
mock.get("/unavailable", {"status": 503, "body": {"error": "Service Unavailable"}})
```

### Custom Headers

```python
mock.get("/with-headers", {
    "status": 200,
    "headers": {
        "Content-Type": "application/json",
        "X-Custom-Header": "custom-value",
        "Cache-Control": "no-cache, no-store",
        "X-Rate-Limit": "100",
        "X-Rate-Remaining": "99"
    },
    "body": {"data": "value"}
})
```

### Response Body Types

```python
# JSON object
mock.get("/object", {
    "status": 200,
    "body": {"key": "value"}
})

# JSON array
mock.get("/array", {
    "status": 200,
    "body": [1, 2, 3, 4, 5]
})

# String
mock.get("/text", {
    "status": 200,
    "body": "Plain text response"
})

# Empty body
mock.delete("/no-content", {
    "status": 204,
    "body": None
})
```

---

## Advanced Features

### Wildcards

```python
# Match any user ID
mock.get("/users/*", {
    "status": 200,
    "body": {"id": "any", "name": "Any User"}
})

# Match any path under /api/
mock.get("/api/*", {
    "status": 200,
    "body": {"message": "API response"}
})

# Usage
judo.get("/users/123")  # Matches
judo.get("/users/abc")  # Matches
judo.get("/api/v1/data")  # Matches
```

### Conditional Responses

```python
# Check for authorization header
def check_auth(request):
    return "Authorization" in request["headers"]

mock.get("/protected", {
    "status": 200,
    "body": {"data": "protected"}
}, condition=check_auth)

# Without auth header -> 404
# With auth header -> 200
```

### Query Parameter Conditions

```python
def check_admin(request):
    query = request.get("query", {})
    return "admin" in query.get("role", [])

mock.get("/admin/users", {
    "status": 200,
    "body": {"users": ["admin1", "admin2"]}
}, condition=check_admin)

# GET /admin/users?role=admin -> 200
# GET /admin/users -> 404
```

### Request Body Conditions

```python
def check_valid_email(request):
    import json
    try:
        body = json.loads(request["body"])
        return "@" in body.get("email", "")
    except:
        return False

mock.post("/register", {
    "status": 201,
    "body": {"message": "User registered"}
}, condition=check_valid_email)
```

### Multiple Routes for Same Path

```python
# Different responses based on conditions
def has_token(request):
    return "token" in request["headers"].get("Authorization", "")

def no_token(request):
    return "token" not in request["headers"].get("Authorization", "")

# With token
mock.get("/data", {
    "status": 200,
    "body": {"data": "secret"}
}, condition=has_token)

# Without token
mock.get("/data", {
    "status": 401,
    "body": {"error": "Unauthorized"}
}, condition=no_token)
```

### Clear Routes

```python
# Clear all configured routes
mock.clear_routes()

# Reconfigure
mock.get("/new-route", {"status": 200, "body": {}})
```

---

## Behave Integration

### Option 1: Using Fixture

```python
# features/environment.py
from judo.behave import *

before_all = before_all_judo
before_scenario = before_scenario_judo
after_scenario = after_scenario_judo
after_all = after_all_judo
```

```gherkin
# features/mock.feature
@fixture.mock_server
Feature: Mock Server Testing

  Scenario: Test with mock
    Given the base URL is "http://localhost:8080"
    When I send a GET request to "/users"
    Then the response status should be 200
```

### Option 2: Custom Hooks

```python
# features/environment.py
from judo.behave import *

def before_all(context):
    before_all_judo(context)
    
    # Start mock server
    context.mock = context.judo_context.judo.start_mock(port=8080)
    
    # Configure routes
    context.mock.get("/api/status", {
        "status": 200,
        "body": {"status": "ok"}
    })

def after_all(context):
    context.judo_context.judo.stop_mock()
    after_all_judo(context)

before_scenario = before_scenario_judo
after_scenario = after_scenario_judo
```

### Option 3: Custom Steps

```python
# features/steps/mock_steps.py
from behave import given
import json

@given('the mock responds to {method} "{path}" with')
def mock_response(context, method, path):
    body = json.loads(context.text) if context.text else {}
    
    response = {"status": 200, "body": body}
    
    if method == "GET":
        context.mock.get(path, response)
    elif method == "POST":
        context.mock.post(path, response)

@given('the mock responds to {method} "{path}" with status {status:d}')
def mock_response_status(context, method, path, status):
    body = json.loads(context.text) if context.text else {}
    
    response = {"status": status, "body": body}
    
    if method == "GET":
        context.mock.get(path, response)
```

**Usage**:

```gherkin
Feature: API Testing

  Scenario: Get users
    Given the mock responds to GET "/users" with:
      """
      [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
      ]
      """
    When I send a GET request to "http://localhost:8080/users"
    Then the response status should be 200
```

---

## API Reference

### MockServer Class

```python
class MockServer:
    """HTTP Mock Server for testing"""
    
    def __init__(self, port: int = 8080):
        """
        Initialize mock server
        
        Args:
            port: Port number (default: 8080)
        """
    
    def start(self) -> None:
        """Start the mock server"""
    
    def stop(self) -> None:
        """Stop the mock server"""
    
    def get(self, path: str, response: Dict, condition: Callable = None) -> None:
        """
        Add GET route
        
        Args:
            path: URL path (supports wildcards)
            response: Response configuration
            condition: Optional condition function
        """
    
    def post(self, path: str, response: Dict, condition: Callable = None) -> None:
        """Add POST route"""
    
    def put(self, path: str, response: Dict, condition: Callable = None) -> None:
        """Add PUT route"""
    
    def delete(self, path: str, response: Dict, condition: Callable = None) -> None:
        """Add DELETE route"""
    
    def add_route(self, method: str, path: str, response: Dict, 
                  condition: Callable = None) -> None:
        """
        Add custom route
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            path: URL path
            response: Response configuration
            condition: Optional condition function
        """
    
    def clear_routes(self) -> None:
        """Clear all configured routes"""
    
    def get_url(self) -> str:
        """Get server URL"""
    
    def is_running(self) -> bool:
        """Check if server is running"""
```

### Response Format

```python
response = {
    "status": 200,          # Required: HTTP status code
    "headers": {},          # Optional: Response headers
    "body": {}              # Optional: Response body (dict, list, str, or None)
}
```

### Condition Function

```python
def condition(request: Dict) -> bool:
    """
    Condition function to determine if response should be used
    
    Args:
        request: Request data dictionary
            {
                "method": "GET",
                "path": "/api/users",
                "query": {"page": ["1"], "limit": ["10"]},
                "body": '{"key": "value"}',
                "headers": {
                    "Authorization": "Bearer token",
                    "Content-Type": "application/json"
                }
            }
    
    Returns:
        True if response should be used, False otherwise
    """
    return True
```

---

## Examples

### Example 1: Complete CRUD

```python
from judo import Judo

judo = Judo()
mock = judo.start_mock(port=8080)
judo.url = "http://localhost:8080"

# List users
mock.get("/users", {
    "status": 200,
    "body": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
})

# Get single user
mock.get("/users/1", {
    "status": 200,
    "body": {"id": 1, "name": "Alice", "email": "alice@example.com"}
})

# Create user
mock.post("/users", {
    "status": 201,
    "body": {"id": 3, "name": "Charlie", "created": True}
})

# Update user
mock.put("/users/1", {
    "status": 200,
    "body": {"id": 1, "name": "Alice Updated"}
})

# Delete user
mock.delete("/users/1", {
    "status": 204,
    "body": None
})

# Run tests
response = judo.get("/users")
assert response.status == 200
assert len(response.json) == 2

response = judo.post("/users", json={"name": "Charlie"})
assert response.status == 201

judo.stop_mock()
```

### Example 2: Error Simulation

```python
mock = judo.start_mock(port=8080)
judo.url = "http://localhost:8080"

# 400 Bad Request
mock.post("/users", {
    "status": 400,
    "body": {
        "error": "Bad Request",
        "message": "Name is required",
        "field": "name"
    }
})

# 401 Unauthorized
mock.get("/protected", {
    "status": 401,
    "body": {
        "error": "Unauthorized",
        "message": "Invalid or missing token"
    }
})

# 404 Not Found
mock.get("/users/999", {
    "status": 404,
    "body": {
        "error": "Not Found",
        "message": "User with ID 999 not found"
    }
})

# 500 Internal Server Error
mock.get("/error", {
    "status": 500,
    "body": {
        "error": "Internal Server Error",
        "message": "Something went wrong"
    }
})

# Test error handling
response = judo.post("/users", json={})
assert response.status == 400
assert "error" in response.json

judo.stop_mock()
```

### Example 3: Authentication Flow

```python
mock = judo.start_mock(port=8080)
judo.url = "http://localhost:8080"

# Login endpoint
mock.post("/auth/login", {
    "status": 200,
    "body": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 1,
            "email": "user@example.com",
            "name": "John Doe"
        },
        "expires_in": 3600
    }
})

# Protected endpoint (requires token)
def check_auth_token(request):
    auth = request["headers"].get("Authorization", "")
    return auth.startswith("Bearer ")

mock.get("/api/profile", {
    "status": 200,
    "body": {
        "id": 1,
        "name": "John Doe",
        "email": "user@example.com"
    }
}, condition=check_auth_token)

# Unauthorized access
mock.get("/api/profile", {
    "status": 401,
    "body": {"error": "Unauthorized"}
}, condition=lambda r: not check_auth_token(r))

# Test flow
# 1. Login
response = judo.post("/auth/login", json={
    "email": "user@example.com",
    "password": "password123"
})
assert response.status == 200
token = response.json["token"]

# 2. Access protected endpoint
judo.bearer_token(token)
response = judo.get("/api/profile")
assert response.status == 200
assert response.json["email"] == "user@example.com"

judo.stop_mock()
```

### Example 4: Pagination

```python
mock = judo.start_mock(port=8080)

# Page 1
def is_page_1(request):
    query = request.get("query", {})
    return query.get("page", ["1"])[0] == "1"

mock.get("/users", {
    "status": 200,
    "body": {
        "data": [
            {"id": 1, "name": "User 1"},
            {"id": 2, "name": "User 2"}
        ],
        "page": 1,
        "total_pages": 3,
        "total_items": 6
    }
}, condition=is_page_1)

# Page 2
def is_page_2(request):
    query = request.get("query", {})
    return query.get("page", ["1"])[0] == "2"

mock.get("/users", {
    "status": 200,
    "body": {
        "data": [
            {"id": 3, "name": "User 3"},
            {"id": 4, "name": "User 4"}
        ],
        "page": 2,
        "total_pages": 3,
        "total_items": 6
    }
}, condition=is_page_2)

# Test pagination
judo.url = "http://localhost:8080"

response = judo.get("/users?page=1")
assert response.json["page"] == 1
assert len(response.json["data"]) == 2

response = judo.get("/users?page=2")
assert response.json["page"] == 2

judo.stop_mock()
```

### Example 5: Multiple Servers

```python
from judo.mock import MockServer

# API Server
api_mock = MockServer(port=8080)
api_mock.start()
api_mock.get("/api/data", {
    "status": 200,
    "body": {"data": "from api"}
})

# Auth Server
auth_mock = MockServer(port=8081)
auth_mock.start()
auth_mock.post("/auth/login", {
    "status": 200,
    "body": {"token": "abc123"}
})

# Payment Server
payment_mock = MockServer(port=8082)
payment_mock.start()
payment_mock.post("/payments", {
    "status": 201,
    "body": {"payment_id": "pay_123", "status": "success"}
})

# Use in tests
judo = Judo()

judo.url = "http://localhost:8080"
response1 = judo.get("/api/data")

judo.url = "http://localhost:8081"
response2 = judo.post("/auth/login", json={"user": "test"})

judo.url = "http://localhost:8082"
response3 = judo.post("/payments", json={"amount": 100})

# Cleanup
api_mock.stop()
auth_mock.stop()
payment_mock.stop()
```

---

## Best Practices

### 1. Use Descriptive Paths

```python
# Good
mock.get("/api/v1/users", {...})
mock.get("/api/v1/users/123", {...})

# Avoid
mock.get("/u", {...})
mock.get("/data", {...})
```

### 2. Return Realistic Data

```python
# Good - realistic structure
mock.get("/users/1", {
    "status": 200,
    "body": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
})

# Avoid - minimal data
mock.get("/users/1", {
    "status": 200,
    "body": {"id": 1}
})
```

### 3. Test Error Cases

```python
# Always test error scenarios
mock.get("/users/invalid", {"status": 404, "body": {"error": "Not Found"}})
mock.post("/users", {"status": 400, "body": {"error": "Validation failed"}})
mock.get("/error", {"status": 500, "body": {"error": "Server error"}})
```

### 4. Use Conditions for Complex Logic

```python
# Good - use conditions
def check_valid_request(request):
    # Complex validation logic
    return True

mock.post("/api/data", {...}, condition=check_valid_request)

# Avoid - multiple similar routes
mock.post("/api/data/valid", {...})
mock.post("/api/data/invalid", {...})
```

### 5. Clean Up After Tests

```python
# Always stop the server
try:
    mock = judo.start_mock()
    # ... tests ...
finally:
    judo.stop_mock()

# Or use context manager (if implemented)
with MockServer(port=8080) as mock:
    # ... tests ...
    pass  # Server stops automatically
```

### 6. Use Appropriate Status Codes

```python
# GET - 200 OK, 404 Not Found
mock.get("/users/1", {"status": 200, "body": {...}})
mock.get("/users/999", {"status": 404, "body": {"error": "Not Found"}})

# POST - 201 Created, 400 Bad Request
mock.post("/users", {"status": 201, "body": {...}})
mock.post("/users/invalid", {"status": 400, "body": {"error": "Bad Request"}})

# PUT - 200 OK, 404 Not Found
mock.put("/users/1", {"status": 200, "body": {...}})

# DELETE - 204 No Content, 404 Not Found
mock.delete("/users/1", {"status": 204, "body": None})
```

### 7. Document Your Mocks

```python
# Good - documented
# Mock for user authentication endpoint
# Returns JWT token on successful login
mock.post("/auth/login", {
    "status": 200,
    "body": {
        "token": "eyJ...",  # JWT token
        "expires_in": 3600  # 1 hour
    }
})

# Avoid - no documentation
mock.post("/auth/login", {"status": 200, "body": {"token": "x"}})
```

---

## Troubleshooting

### Server Won't Start

```python
# Check if port is already in use
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if is_port_in_use(8080):
    print("Port 8080 is already in use")
    mock = judo.start_mock(port=8081)  # Use different port
```

### Routes Not Matching

```python
# Check exact path
mock.get("/users", {...})  # Matches /users
# Does NOT match /users/ or /users/1

# Use wildcards for flexible matching
mock.get("/users/*", {...})  # Matches /users/1, /users/abc, etc.
```

### Condition Not Working

```python
# Debug condition function
def debug_condition(request):
    print(f"Method: {request['method']}")
    print(f"Path: {request['path']}")
    print(f"Headers: {request['headers']}")
    print(f"Body: {request['body']}")
    return True

mock.get("/debug", {...}, condition=debug_condition)
```

### Server Not Stopping

```python
# Force stop
if mock.is_running():
    mock.stop()

# Or restart
mock.stop()
mock.start()
```

---

## Limitations

1. **No HTTPS Support**: Only HTTP protocol
2. **No State Persistence**: Routes don't persist between restarts
3. **No Request History**: Can't query past requests
4. **No Proxy Mode**: Can't intercept real requests
5. **No WebSocket Support**: HTTP only
6. **Single-threaded Handler**: One request at a time per route

---

## Future Enhancements

Potential features for future versions:

- ✨ HTTPS support
- ✨ Request history and logging
- ✨ State persistence (save/load routes)
- ✨ Proxy mode
- ✨ WebSocket support
- ✨ Web UI for configuration
- ✨ Request matching by body content
- ✨ Response delays (simulate latency)
- ✨ Random failures (chaos testing)

---

## Comparison with Alternatives

| Feature | Judo Mock | WireMock | json-server | responses |
|---------|-----------|----------|-------------|-----------|
| Language | Python | Java | Node.js | Python |
| Real HTTP | ✅ | ✅ | ✅ | ❌ |
| Setup Complexity | Low | High | Low | Low |
| Wildcards | ✅ | ✅ | ❌ | ✅ |
| Conditions | ✅ | ✅ | ❌ | ❌ |
| UI | ❌ | ✅ | ❌ | ❌ |
| State Persistence | ❌ | ✅ | ✅ | ❌ |
| BDD Integration | ✅ | ❌ | ❌ | ❌ |

---

## Support

- **Documentation**: [Judo Framework Docs](http://centyc.cl/judo-framework/)
- **GitHub**: [Judo Framework Repository](https://github.com/FelipeFariasAlfaro/Judo-Framework)
- **PyPI**: [judo-framework](https://pypi.org/project/judo-framework/)
- **Issues**: [GitHub Issues](https://github.com/FelipeFariasAlfaro/Judo-Framework/issues)

---

**Author**: Felipe Farias - CENTYC  
**Version**: 1.3.42  
**Last Updated**: December 14, 2024  
**License**: MIT
