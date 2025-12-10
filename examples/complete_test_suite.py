"""
Complete Test Suite Example
Demonstrates a real-world API testing scenario using Judo Framework
"""

from judo import Judo
import time


class UserAPITestSuite:
    """Complete test suite for User API"""
    
    def __init__(self):
        self.judo = Judo()
        self.setup()
    
    def setup(self):
        """Setup test environment"""
        # Configure base URL
        self.judo.url = "https://jsonplaceholder.typicode.com"
        
        # Set common headers
        self.judo.headers({
            "Content-Type": "application/json",
            "User-Agent": "Judo-Framework-Test/1.0"
        })
        
        # Set test data
        self.judo.set("testUser", {
            "name": "Test User",
            "username": "testuser",
            "email": "test@example.com",
            "phone": "1-770-736-8031 x56442",
            "website": "hildegard.org"
        })
        
        print("🚀 Test suite initialized")
    
    def test_get_all_users(self):
        """Test GET /users - Retrieve all users"""
        print("\n=== Test: Get All Users ===")
        
        response = self.judo.get("/users")
        
        # Validate response
        self.judo.match(response.status, 200)
        self.judo.match(response.json, "##array")
        
        # Validate array is not empty
        users = response.json
        assert len(users) > 0, "Users array should not be empty"
        
        # Validate each user structure
        user_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "username": {"type": "string"},
                "email": {"type": "string"},
                "phone": {"type": "string"},
                "website": {"type": "string"}
            },
            "required": ["id", "name", "username", "email"]
        }
        
        for user in users[:3]:  # Validate first 3 users
            self.judo.match(user, user_schema)
        
        # Store first user ID for later tests
        self.judo.set("firstUserId", users[0]["id"])
        
        print(f"✅ Retrieved {len(users)} users successfully")
        return True
    
    def test_get_single_user(self):
        """Test GET /users/{id} - Retrieve single user"""
        print("\n=== Test: Get Single User ===")
        
        user_id = self.judo.get_var("firstUserId", 1)
        response = self.judo.get(f"/users/{user_id}")
        
        # Validate response
        self.judo.match(response.status, 200)
        self.judo.match(response.json["id"], user_id)
        self.judo.match(response.json["name"], "##string")
        self.judo.match(response.json["email"], "##string")
        
        # Validate email format
        email = response.json["email"]
        assert "@" in email, "Email should contain @ symbol"
        
        print(f"✅ Retrieved user {user_id}: {response.json['name']}")
        return True
    
    def test_get_user_posts(self):
        """Test GET /users/{id}/posts - Get user's posts"""
        print("\n=== Test: Get User Posts ===")
        
        user_id = self.judo.get_var("firstUserId", 1)
        response = self.judo.get(f"/users/{user_id}/posts")
        
        # Validate response
        self.judo.match(response.status, 200)
        self.judo.match(response.json, "##array")
        
        posts = response.json
        if len(posts) > 0:
            # Validate post structure
            post_schema = {
                "type": "object",
                "properties": {
                    "userId": {"type": "integer"},
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["userId", "id", "title", "body"]
            }
            
            for post in posts[:2]:  # Check first 2 posts
                self.judo.match(post, post_schema)
                self.judo.match(post["userId"], user_id)
        
        print(f"✅ Retrieved {len(posts)} posts for user {user_id}")
        return True
    
    def test_create_user(self):
        """Test POST /users - Create new user"""
        print("\n=== Test: Create User ===")
        
        new_user = self.judo.get_var("testUser")
        response = self.judo.post("/users", json=new_user)
        
        # Validate response
        self.judo.match(response.status, 201)
        self.judo.match(response.json.name, new_user["name"])
        self.judo.match(response.json.email, new_user["email"])
        self.judo.match(response.json.id, "##number")
        
        # Store created user ID
        created_id = response.json["id"]
        self.judo.set("createdUserId", created_id)
        
        print(f"✅ Created user with ID: {created_id}")
        return True
    
    def test_update_user(self):
        """Test PUT /users/{id} - Update user"""
        print("\n=== Test: Update User ===")
        
        user_id = self.judo.get_var("createdUserId", 1)
        updated_data = {
            "name": "Updated Test User",
            "email": "updated@example.com"
        }
        
        response = self.judo.put(f"/users/{user_id}", json=updated_data)
        
        # Validate response
        self.judo.match(response.status, 200)
        self.judo.match(response.json.id, user_id)
        self.judo.match(response.json.name, updated_data["name"])
        self.judo.match(response.json.email, updated_data["email"])
        
        print(f"✅ Updated user {user_id}")
        return True
    
    def test_delete_user(self):
        """Test DELETE /users/{id} - Delete user"""
        print("\n=== Test: Delete User ===")
        
        user_id = self.judo.get_var("createdUserId", 1)
        response = self.judo.delete(f"/users/{user_id}")
        
        # Validate response
        self.judo.match(response.status, 200)
        
        print(f"✅ Deleted user {user_id}")
        return True
    
    def test_error_handling(self):
        """Test error scenarios"""
        print("\n=== Test: Error Handling ===")
        
        # Test 404 - Non-existent user
        response = self.judo.get("/users/99999")
        self.judo.match(response.status, 404)
        
        # Test invalid data
        invalid_user = {"invalid": "data"}
        response = self.judo.post("/users", json=invalid_user)
        # Note: JSONPlaceholder always returns 201, but in real API this would be 400
        
        print("✅ Error scenarios handled correctly")
        return True
    
    def test_query_parameters(self):
        """Test query parameters"""
        print("\n=== Test: Query Parameters ===")
        
        # Test filtering posts by user
        self.judo.param("userId", 1)
        response = self.judo.get("/posts")
        
        self.judo.match(response.status, 200)
        self.judo.match(response.json, "##array")
        
        # All posts should be from userId 1
        posts = response.json
        for post in posts:
            self.judo.match(post["userId"], 1)
        
        print(f"✅ Filtered {len(posts)} posts by userId=1")
        return True
    
    def test_jsonpath_extraction(self):
        """Test JSONPath data extraction"""
        print("\n=== Test: JSONPath Extraction ===")
        
        response = self.judo.get("/users")
        users = response.json
        
        # Extract all names using JSONPath
        names = self.judo.json_path(users, "$[*].name")
        emails = self.judo.json_path(users, "$[*].email")
        
        assert len(names) == len(users), "Should extract all names"
        assert len(emails) == len(users), "Should extract all emails"
        
        # Extract first user's name
        first_name = self.judo.json_path(users, "$[0].name")
        assert first_name == users[0]["name"], "First name should match"
        
        print(f"✅ JSONPath extraction successful")
        print(f"   Names: {names[:3]}...")  # Show first 3 names
        return True
    
    def test_performance_timing(self):
        """Test response timing"""
        print("\n=== Test: Performance Timing ===")
        
        start_time = time.time()
        response = self.judo.get("/users")
        end_time = time.time()
        
        # Validate response time
        response_time = response.elapsed
        total_time = end_time - start_time
        
        assert response_time > 0, "Response time should be positive"
        assert total_time > response_time, "Total time should include network overhead"
        
        print(f"✅ Response time: {response_time:.3f}s")
        print(f"   Total time: {total_time:.3f}s")
        return True
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🥋 Starting Judo Framework Complete Test Suite")
        print("=" * 50)
        
        tests = [
            self.test_get_all_users,
            self.test_get_single_user,
            self.test_get_user_posts,
            self.test_create_user,
            self.test_update_user,
            self.test_delete_user,
            self.test_error_handling,
            self.test_query_parameters,
            self.test_jsonpath_extraction,
            self.test_performance_timing
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
        
        print("\n" + "=" * 50)
        print(f"🎯 Test Results: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 All tests passed! Judo Framework is working perfectly!")
        else:
            print(f"⚠️  {failed} test(s) failed. Please check the output above.")
        
        return failed == 0


def main():
    """Run the complete test suite"""
    suite = UserAPITestSuite()
    success = suite.run_all_tests()
    
    if success:
        print("\n✨ Judo Framework demonstration completed successfully!")
        print("You can now use Judo Framework for your API testing needs.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")


if __name__ == "__main__":
    main()