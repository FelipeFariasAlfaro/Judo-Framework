# Judo Framework DSL Reference

Complete reference for Judo Framework's Domain Specific Language (DSL), providing Karate-like syntax for API testing.

## Core Concepts

### Variables

#### Setting Variables
```python
# Simple values
judo.set("name", "John Doe")
judo.set("age", 30)
judo.set("active", True)

# Complex objects
judo.set("user", {
    "name": "John Doe",
    "email": "john@example.com",
    "roles": ["admin", "user"]
})

# Arrays
judo.set("ids", [1, 2, 3, 4, 5])
```

#### Getting Variables
```python
# Get with default
name = judo.get_var("name", "Unknown")

# Direct access (returns None if not found)
age = judo.get_var("age")

# Environment variables
api_key = judo.get_env("API_KEY", "default-key")
```

#### Variable Interpolation
```python
# Set base values
judo.set("baseUrl", "https://api.example.com")
judo.set("version", "v1")

# Use in strings (future feature)
url = judo.interpolate("#{baseUrl}/#{version}/users")
```

### HTTP Methods

#### GET Requests
```python
# Simple GET
response = judo.get("/users")

# With query parameters
judo.param("page", 1)
judo.param("limit", 10)
response = judo.get("/users")

# Or inline
response = judo.get("/users", params={"page": 1, "limit": 10})
```

#### POST Requests
```python
# JSON payload
user_data = {"name": "John", "email": "john@example.com"}
response = judo.post("/users", json=user_data)

# Form data
judo.form_field("name", "John")
judo.form_field("email", "john@example.com")
response = judo.post("/users")

# Multipart form
judo.multipart_field("avatar", open("avatar.jpg", "rb"), "avatar.jpg")
response = judo.post("/users")
```

#### PUT/PATCH Requests
```python
# Update user
updated_data = {"name": "John Smith"}
response = judo.put("/users/1", json=updated_data)
response = judo.patch("/users/1", json=updated_data)
```

#### DELETE Requests
```python
response = judo.delete("/users/1")
```

### Headers and Authentication

#### Headers
```python
# Single header
judo.header("Content-Type", "application/json")

# Multiple headers
judo.headers({
    "Authorization": "Bearer token",
    "X-API-Version": "1.0",
    "User-Agent": "Judo/1.0"
})
```

#### Authentication
```python
# Basic Authentication
judo.basic_auth("username", "password")

# Bearer Token
judo.bearer_token("jwt-token-here")

# OAuth2 (alias for bearer_token)
judo.oauth2("access-token")

# Custom header auth
judo.header("X-API-Key", "your-api-key")
```

### Matching and Validation

#### Basic Matching
```python
# Exact values
judo.match(response.status, 200)
judo.match(response.json.name, "John Doe")
judo.match(response.json.age, 30)
```

#### Type Matchers
```python
# Primitive types
judo.match(response.json.name, "##string")
judo.match(response.json.age, "##number")
judo.match(response.json.active, "##boolean")
judo.match(response.json.data, "##array")
judo.match(response.json.user, "##object")

# Null checks
judo.match(response.json.deleted_at, "##null")
judo.match(response.json.created_at, "##notnull")

# Presence checks
judo.match(response.json.id, "##present")
judo.match(response.json.temp_field, "##notpresent")

# Ignore matcher (always passes)
judo.match(response.json.timestamp, "##ignore")
```

#### Parameterized Matchers
```python
# String length
judo.match(response.json.name, "##string[5]")        # Exact length
judo.match(response.json.name, "##string[3,20]")     # Length range

# Number range
judo.match(response.json.age, "##number[18,65]")     # Age range

# Array size
judo.match(response.json.tags, "##array[3]")         # Exact size
judo.match(response.json.items, "##array[1,10]")     # Size range
```

#### Format Matchers
```python
# Common formats
judo.match(response.json.email, "##email")
judo.match(response.json.website, "##url")
judo.match(response.json.id, "##uuid")
judo.match(response.json.created_at, "##date")
judo.match(response.json.updated_at, "##datetime")
```

#### Regex Matching
```python
# Regex patterns
judo.match(response.json.phone, "#regex ^\\+?[1-9]\\d{1,14}$")
judo.match(response.json.code, "#regex ^[A-Z]{3}\\d{3}$")
```

#### Collection Matching
```python
# Array contains
judo.match_contains(response.json.tags, "python")
judo.match_contains(response.json.users, {"name": "John"})

# Array contains only (order doesn't matter)
expected_tags = ["python", "api", "testing"]
judo.match_contains_only(response.json.tags, expected_tags)

# Array contains any
possible_tags = ["python", "java", "javascript"]
judo.match_contains_any(response.json.tags, possible_tags)

# Each item matches pattern
judo.match_each(response.json.users, {"id": "##number", "name": "##string"})
```

#### Schema Validation
```python
# JSON Schema
user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer", "minimum": 1},
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "roles": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["id", "name", "email"]
}

judo.match(response.json, user_schema)
```

### JSONPath and XPath

#### JSONPath
```python
# Extract single value
user_name = judo.json_path(response.json, "$.user.name")
first_tag = judo.json_path(response.json, "$.tags[0]")

# Extract multiple values
all_names = judo.json_path(response.json, "$..name")
user_emails = judo.json_path(response.json, "$.users[*].email")

# Complex expressions
active_users = judo.json_path(response.json, "$.users[?(@.active == true)]")
```

#### XPath (for XML responses)
```python
# Extract from XML
title = judo.xml_path(response.text, "//book/title/text()")
prices = judo.xml_path(response.text, "//book/@price")
```

### Utility Functions

#### Random Data Generation
```python
# Basic random data
random_id = judo.random_int(1, 1000)
random_name = judo.random_string(10)
unique_id = judo.uuid()

# Timestamps
current_time = judo.timestamp()
formatted_date = judo.format_date("%Y-%m-%d")
```

#### Fake Data (using Faker)
```python
from judo.utils import *

# Generate realistic fake data
fake_user = {
    "name": fake_name(),
    "email": fake_email(),
    "phone": fake_phone(),
    "address": fake_address(),
    "company": fake_company()
}
```

#### Data Manipulation
```python
# JSON operations
json_str = to_json(data, pretty=True)
data = from_json(json_str)

# Base64 encoding
encoded = encode_base64("Hello World")
decoded = decode_base64(encoded)

# Hashing
md5_hash = hash_md5("password")
sha256_hash = hash_sha256("sensitive-data")
```

### File Operations

#### Reading Files
```python
# Text files
content = judo.read_file("data.txt")

# JSON files
data = judo.read_json("config.json")
```

#### Writing Files
```python
# Text files
judo.write_file("output.txt", "Hello World")

# JSON files
judo.write_json("result.json", {"status": "success"})
```

### Mock Server

#### Starting Mock Server
```python
# Start on default port (8080)
mock = judo.start_mock()

# Start on custom port
mock = judo.start_mock(port=9000)
```

#### Adding Routes
```python
# Simple GET route
mock.get("/api/users/1", {
    "status": 200,
    "body": {"id": 1, "name": "John Doe"}
})

# POST route with custom headers
mock.post("/api/users", {
    "status": 201,
    "headers": {"Location": "/api/users/123"},
    "body": {"id": 123, "name": "New User"}
})

# Conditional routes
def check_auth(request):
    return "Authorization" in request["headers"]

mock.get("/api/protected", {
    "status": 200,
    "body": {"data": "secret"}
}, condition=check_auth)
```

#### Stopping Mock Server
```python
judo.stop_mock()
```

### Configuration

#### Global Configuration
```python
# Set configuration values
judo.configure("timeout", 30)
judo.configure("retries", 3)
judo.configure("verify_ssl", False)

# Get configuration
timeout = judo.get_config("timeout", 10)
```

#### HTTP Client Configuration
```python
# Timeouts
judo.http_client.set_timeout(30)

# SSL verification
judo.http_client.set_verify_ssl(False)

# Proxies
judo.http_client.set_proxy("http://proxy.example.com:8080")
```

### Error Handling

#### Response Validation
```python
# Check status codes
if response.is_success():
    print("Request successful")
elif response.is_client_error():
    print("Client error (4xx)")
elif response.is_server_error():
    print("Server error (5xx)")

# Specific status checks
judo.match(response.status, 200)  # Will raise assertion if not 200
```

#### Exception Handling
```python
try:
    response = judo.get("/api/users")
    judo.match(response.status, 200)
except Exception as e:
    judo.log(f"Request failed: {e}", "ERROR")
```

### Debugging

#### Logging
```python
# Log messages
judo.log("Starting test", "INFO")
judo.log("Error occurred", "ERROR")

# Print for debugging
judo.print("Debug info:", response.json)
```

#### Response Inspection
```python
# Pretty print response
print(response.pretty_print())

# Check response properties
print(f"Status: {response.status}")
print(f"Headers: {response.headers}")
print(f"Time: {response.elapsed}s")
```