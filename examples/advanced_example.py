"""
Advanced Judo Framework Example
Demonstrates advanced features like mock server, data-driven testing, etc.
"""

from judo import Judo
import time

def test_mock_server():
    """Test with mock server"""
    print("=== Mock Server Example ===")
    
    judo = Judo()
    
    # Start mock server
    mock = judo.start_mock(port=8081)
    
    # Add mock routes
    mock.get("/api/users/1", {
        "status": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com"
        }
    })
    
    mock.post("/api/users", {
        "status": 201,
        "body": {
            "id": 2,
            "name": "Jane Smith",
            "email": "jane@example.com"
        }
    })
    
    # Wait for server to start
    time.sleep(0.5)
    
    # Test against mock server
    judo.url = "http://localhost:8081"
    
    # GET request
    response = judo.get("/api/users/1")
    judo.match(response.status, 200)
    judo.match(response.json.name, "John Doe")
    judo.match(response.json.email, "##email")
    
    print("✓ Mock GET /api/users/1 successful")
    
    # POST request
    new_user = {
        "name": "Jane Smith",
        "email": "jane@example.com"
    }
    
    response = judo.post("/api/users", json=new_user)
    judo.match(response.status, 201)
    judo.match(response.json.id, 2)
    
    print("✓ Mock POST /api/users successful")
    
    # Stop mock server
    judo.stop_mock()
    print("✓ Mock server stopped")

def test_data_driven():
    """Data-driven testing example"""
    print("\n=== Data-Driven Testing ===")
    
    judo = Judo()
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # Test data
    test_users = [
        {"id": 1, "expected_name": "##string"},
        {"id": 2, "expected_name": "##string"},
        {"id": 3, "expected_name": "##string"}
    ]
    
    for user_data in test_users:
        user_id = user_data["id"]
        response = judo.get(f"/users/{user_id}")
        
        judo.match(response.status, 200)
        judo.match(response.json.id, user_id)
        judo.match(response.json.name, user_data["expected_name"])
        judo.match(response.json.email, "##email")
        
        print(f"✓ User {user_id}: {response.json.name}")

def test_schema_validation():
    """Schema validation example"""
    print("\n=== Schema Validation ===")
    
    judo = Judo()
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # Define JSON schema
    user_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "username": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                    "zipcode": {"type": "string"}
                }
            }
        },
        "required": ["id", "name", "email"]
    }
    
    response = judo.get("/users/1")
    judo.match(response.status, 200)
    
    # Validate against schema
    judo.match(response.json, user_schema)
    
    print("✓ User data matches schema")

def test_authentication():
    """Authentication example"""
    print("\n=== Authentication Example ===")
    
    judo = Judo()
    
    # Basic Auth example (using httpbin for testing)
    judo.url = "https://httpbin.org"
    judo.basic_auth("user", "pass")
    
    response = judo.get("/basic-auth/user/pass")
    judo.match(response.status, 200)
    judo.match(response.json.authenticated, True)
    
    print("✓ Basic authentication successful")
    
    # Bearer token example
    judo.bearer_token("fake-jwt-token")
    judo.header("Authorization", "Bearer fake-jwt-token")
    
    response = judo.get("/bearer")
    # Note: httpbin returns 401 for invalid tokens, which is expected
    print(f"✓ Bearer token request sent (status: {response.status})")

def test_file_operations():
    """File operations example"""
    print("\n=== File Operations ===")
    
    judo = Judo()
    
    # Create test data
    test_data = {
        "users": [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30}
        ]
    }
    
    # Write JSON file
    judo.write_json("test_data.json", test_data)
    print("✓ JSON file written")
    
    # Read JSON file
    loaded_data = judo.read_json("test_data.json")
    judo.match(loaded_data, test_data)
    print("✓ JSON file read and validated")
    
    # Clean up
    import os
    os.remove("test_data.json")
    print("✓ Test file cleaned up")

def test_fake_data():
    """Fake data generation example"""
    print("\n=== Fake Data Generation ===")
    
    judo = Judo()
    
    # Generate fake user data
    fake_user = {
        "name": judo.variables.fake_name(),
        "email": judo.variables.fake_email(),
        "phone": judo.variables.fake_phone(),
        "company": judo.variables.fake_company()
    }
    
    print(f"✓ Generated fake user:")
    for key, value in fake_user.items():
        print(f"  {key}: {value}")

def main():
    """Run all advanced examples"""
    try:
        test_mock_server()
        test_data_driven()
        test_schema_validation()
        test_authentication()
        test_file_operations()
        test_fake_data()
        
        print("\n🎉 All advanced tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()