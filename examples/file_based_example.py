"""
File-based Testing Example
Demonstrates how to use external JSON, YAML, and CSV files for API testing
Similar to Karate's file loading capabilities
"""

from judo import Judo
import os


def test_json_file_loading():
    """Test loading JSON files for request bodies"""
    print("=== JSON File Loading Example ===")
    
    judo = Judo()
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # Load JSON data from file (Karate-style)
    user_data = judo.read("test_data/users/create_user_request.json")
    print(f"Loaded user data: {user_data['name']}")
    
    # Use loaded data in POST request
    response = judo.post("/users", json=user_data)
    judo.match(response.status, 201)
    judo.match(response.json["name"], user_data["name"])
    judo.match(response.json["email"], user_data["email"])
    
    print(f"✅ Created user: {response.json['name']}")
    return True


def test_yaml_file_loading():
    """Test loading YAML files for request bodies"""
    print("\n=== YAML File Loading Example ===")
    
    judo = Judo()
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # Load YAML data from file
    post_data = judo.read("test_data/posts/create_post_request.yaml")
    print(f"Loaded post data: {post_data['title']}")
    
    # Use loaded data in POST request
    response = judo.post("/posts", json=post_data)
    judo.match(response.status, 201)
    judo.match(response.json["title"], post_data["title"])
    judo.match(response.json["userId"], post_data["userId"])
    
    print(f"✅ Created post: {response.json['title']}")
    return True


def test_csv_file_loading():
    """Test loading CSV files for data-driven testing"""
    print("\n=== CSV File Loading Example ===")
    
    judo = Judo()
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # Load CSV data
    test_users = judo.read_csv("test_data/test_users.csv")
    print(f"Loaded {len(test_users)} test users from CSV")
    
    # Use CSV data for validation
    response = judo.get("/users")
    judo.match(response.status, 200)
    
    users = response.json
    print(f"✅ API returned {len(users)} users")
    
    # Validate that we have at least as many users as in our test data
    assert len(users) >= len(test_users), "API should return at least as many users as test data"
    
    return True


def test_schema_validation_from_file():
    """Test schema validation using external schema files"""
    print("\n=== Schema Validation from File ===")
    
    judo = Judo()
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # Load schema from file
    user_schema = judo.read_json("test_data/schemas/user_schema.json")
    print("Loaded user schema from file")
    
    # Get user data and validate against schema
    response = judo.get("/users/1")
    judo.match(response.status, 200)
    
    # Validate response against loaded schema
    judo.match(response.json, user_schema)
    
    print("✅ User response matches schema from file")
    return True


def test_response_saving():
    """Test saving responses to files"""
    print("\n=== Response Saving Example ===")
    
    judo = Judo()
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # Get user data
    response = judo.get("/users/1")
    judo.match(response.status, 200)
    
    # Save response to file
    os.makedirs("output", exist_ok=True)
    judo.write_json("output/user_1_response.json", response.json)
    print("✅ Saved user response to output/user_1_response.json")
    
    # Save specific data
    user_summary = {
        "id": response.json["id"],
        "name": response.json["name"],
        "email": response.json["email"]
    }
    judo.write_json("output/user_1_summary.json", user_summary)
    print("✅ Saved user summary to output/user_1_summary.json")
    
    # Verify files were created
    assert judo.file_exists("output/user_1_response.json"), "Response file should exist"
    assert judo.file_exists("output/user_1_summary.json"), "Summary file should exist"
    
    return True


def test_file_based_workflow():
    """Test complete workflow using files"""
    print("\n=== Complete File-based Workflow ===")
    
    judo = Judo()
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # 1. Load request data from file
    user_data = judo.read("test_data/users/create_user_request.json")
    
    # 2. Create user
    response = judo.post("/users", json=user_data)
    judo.match(response.status, 201)
    
    # 3. Save created user data
    os.makedirs("output", exist_ok=True)
    judo.write_json("output/created_user.json", response.json)
    
    # 4. Load update data from file
    update_data = judo.read("test_data/users/update_user_request.json")
    
    # 5. Update user (simulate with PUT to existing user)
    user_id = response.json["id"]
    update_response = judo.put(f"/users/{user_id}", json=update_data)
    judo.match(update_response.status, 200)
    
    # 6. Save updated user data
    judo.write_json("output/updated_user.json", update_response.json)
    
    # 7. Load schema and validate
    schema = judo.read_json("test_data/schemas/user_schema.json")
    judo.match(update_response.json, schema)
    
    print("✅ Complete file-based workflow completed successfully")
    return True


def demonstrate_karate_style_usage():
    """Demonstrate Karate-style file usage"""
    print("\n=== Karate-style File Usage ===")
    
    judo = Judo()
    
    # Karate-style: read('file.json')
    user_data = judo.read("test_data/users/create_user_request.json")
    post_data = judo.read("test_data/posts/create_post_request.yaml")
    csv_data = judo.read("test_data/test_users.csv")
    
    print("✅ Loaded JSON file:", type(user_data).__name__)
    print("✅ Loaded YAML file:", type(post_data).__name__)
    print("✅ Loaded CSV file:", type(csv_data).__name__, f"({len(csv_data)} rows)")
    
    # Show data structure
    print(f"User name: {user_data['name']}")
    print(f"Post title: {post_data['title']}")
    print(f"First CSV user: {csv_data[0]['name']}")
    
    return True


def main():
    """Run all file-based examples"""
    print("🥋 Judo Framework - File-based Testing Examples")
    print("Demonstrating Karate-like file loading capabilities")
    print("=" * 60)
    
    tests = [
        test_json_file_loading,
        test_yaml_file_loading,
        test_csv_file_loading,
        test_schema_validation_from_file,
        test_response_saving,
        test_file_based_workflow,
        demonstrate_karate_style_usage
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"🎯 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All file-based tests passed!")
        print("\n📁 Files created in output/ directory:")
        if os.path.exists("output"):
            for file in os.listdir("output"):
                print(f"  - {file}")
    else:
        print(f"⚠️ {failed} test(s) failed")
    
    return failed == 0


if __name__ == "__main__":
    main()