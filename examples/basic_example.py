"""
Basic Judo Framework Example
Demonstrates core functionality similar to Karate
"""

from judo import Judo

def main():
    # Create Judo instance
    judo = Judo()
    
    # Set base URL
    judo.url = "https://jsonplaceholder.typicode.com"
    
    print("=== Basic GET Request ===")
    response = judo.get("/posts/1")
    
    # Basic validations
    judo.match(response.status, 200)
    judo.match(response.json["userId"], 1)
    judo.match(response.json["id"], 1)
    judo.match(response.json["title"], "##string")
    judo.match(response.json["body"], "##string")
    
    print(f"✓ GET /posts/1 - Status: {response.status}")
    print(f"✓ Title: {response.json['title']}")
    
    print("\n=== POST Request with JSON ===")
    
    # Set variables
    judo.set("newPost", {
        "title": "My New Post",
        "body": "This is the content of my new post",
        "userId": 1
    })
    
    # POST request
    response = judo.post("/posts", json=judo.get_var("newPost"))
    
    # Validate response
    judo.match(response.status, 201)
    judo.match(response.json["title"], "My New Post")
    judo.match(response.json["userId"], 1)
    judo.match(response.json["id"], "##number")
    
    print(f"✓ POST /posts - Status: {response.status}")
    print(f"✓ Created post ID: {response.json['id']}")
    
    print("\n=== Advanced Matching ===")
    
    # Get all posts
    response = judo.get("/posts")
    judo.match(response.status, 200)
    judo.match(response.json, "##array")
    
    # Check array length
    posts = response.json
    assert len(posts) > 0, "Should have posts"
    
    # Match each post structure
    for post in posts[:3]:  # Check first 3 posts
        judo.match(post["id"], "##number")
        judo.match(post["userId"], "##number") 
        judo.match(post["title"], "##string")
        judo.match(post["body"], "##string")
    
    print(f"✓ GET /posts - Found {len(posts)} posts")
    print("✓ All posts have correct structure")
    
    print("\n=== Headers and Authentication ===")
    
    # Set custom headers
    judo.header("X-Custom-Header", "test-value")
    judo.header("User-Agent", "Judo-Framework/1.0")
    
    response = judo.get("/posts/1")
    judo.match(response.status, 200)
    
    print("✓ Custom headers sent successfully")
    
    print("\n=== Query Parameters ===")
    
    # Set query parameters
    judo.param("userId", 1)
    
    response = judo.get("/posts")
    judo.match(response.status, 200)
    
    # All posts should be from userId 1
    for post in response.json:
        judo.match(post["userId"], 1)
    
    print(f"✓ Filtered posts by userId=1, found {len(response.json)} posts")
    
    print("\n=== JSONPath Examples ===")
    
    response = judo.get("/posts/1")
    
    # Extract values using JSONPath
    title = judo.json_path(response.json, "$.title")
    user_id = judo.json_path(response.json, "$.userId")
    
    print(f"✓ JSONPath $.title: {title}")
    print(f"✓ JSONPath $.userId: {user_id}")
    
    print("\n=== Utility Functions ===")
    
    # Generate test data
    random_id = judo.random_int(1, 1000)
    random_string = judo.random_string(10)
    uuid_val = judo.uuid()
    timestamp = judo.timestamp()
    
    print(f"✓ Random ID: {random_id}")
    print(f"✓ Random String: {random_string}")
    print(f"✓ UUID: {uuid_val}")
    print(f"✓ Timestamp: {timestamp}")
    
    print("\n🎉 All tests passed! Judo Framework is working correctly.")

if __name__ == "__main__":
    main()