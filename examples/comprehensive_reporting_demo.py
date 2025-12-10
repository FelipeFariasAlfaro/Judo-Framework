"""
Comprehensive Reporting Demo
Demonstrates all reporting capabilities of Judo Framework
"""

from judo import Judo
from judo.reporting.reporter import JudoReporter
import json
import time


def create_comprehensive_test_report():
    """Create a comprehensive test report with all features"""
    print("🥋 Judo Framework - Comprehensive Reporting Demo")
    print("=" * 60)
    
    # Create reporter with custom title
    reporter = JudoReporter("Comprehensive API Testing Report - All Features Demo")
    
    # Create Judo instance
    judo = Judo(enable_reporting=True)
    judo.reporter = reporter
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # Add environment and configuration info
    reporter.report_data.environment.update({
        "test_environment": "demo",
        "api_base_url": judo.url,
        "test_suite": "comprehensive_demo"
    })
    
    reporter.report_data.configuration = {
        "timeout": 30,
        "retry_count": 3,
        "verify_ssl": True,
        "parallel_execution": False
    }
    
    # Feature 1: User Management
    print("\n📋 Feature 1: User Management")
    feature1 = reporter.start_feature(
        name="User Management API",
        description="Complete CRUD operations for user management with detailed validation",
        file_path="examples/comprehensive_reporting_demo.py",
        tags=["api", "users", "crud", "management"]
    )
    
    # Scenario 1.1: Get Single User
    scenario1 = reporter.start_scenario("Get single user details", ["get", "user", "details"])
    
    try:
        # Step 1: Setup test data
        step1 = reporter.start_step("Given I have a user ID for testing")
        judo.set("targetUserId", 1)
        judo.set("expectedUserName", "Leanne Graham")
        reporter.finish_step()
        
        # Step 2: Make request
        step2 = reporter.start_step("When I send a GET request to /users/{userId}")
        user_id = judo.get_var("targetUserId")
        response = judo.get(f"/users/{user_id}")
        reporter.finish_step()
        
        # Step 3: Validate status
        step3 = reporter.start_step("Then the response status should be 200")
        judo.match(response.status, 200)
        reporter.finish_step()
        
        # Step 4: Validate user data
        step4 = reporter.start_step("And the user data should be valid")
        judo.match(response.json["id"], user_id)
        judo.match(response.json["name"], "##string")
        judo.match(response.json["email"], "##email")
        judo.match(response.json["phone"], "##string")
        reporter.finish_step()
        
        # Step 5: Extract user data
        step5 = reporter.start_step("And I extract user information for later use")
        judo.set("retrievedUser", response.json)
        judo.set("userEmail", response.json["email"])
        reporter.finish_step()
        
        reporter.finish_scenario()
        print("✅ Scenario 1.1: Get single user - PASSED")
        
    except Exception as e:
        reporter.finish_scenario(error_message=str(e))
        print(f"❌ Scenario 1.1: Get single user - FAILED: {e}")
    
    # Scenario 1.2: Create New User
    scenario2 = reporter.start_scenario("Create new user", ["post", "user", "create"])
    
    try:
        # Step 1: Prepare user data
        step1 = reporter.start_step("Given I have new user data")
        new_user = {
            "name": "Test User Demo",
            "username": "testuserdemo",
            "email": "testdemo@example.com",
            "phone": "1-555-DEMO-123",
            "website": "demo.example.com",
            "address": {
                "street": "123 Demo Street",
                "city": "Demo City",
                "zipcode": "12345"
            },
            "company": {
                "name": "Demo Company",
                "catchPhrase": "Demo testing made easy"
            }
        }
        judo.set("newUserData", new_user)
        reporter.finish_step()
        
        # Step 2: Send POST request
        step2 = reporter.start_step("When I send a POST request to create the user")
        response = judo.post("/users", json=new_user)
        reporter.finish_step()
        
        # Step 3: Validate creation
        step3 = reporter.start_step("Then the user should be created successfully")
        judo.match(response.status, 201)
        judo.match(response.json["name"], new_user["name"])
        judo.match(response.json["email"], new_user["email"])
        reporter.finish_step()
        
        # Step 4: Store created user ID
        step4 = reporter.start_step("And I store the created user ID")
        created_id = response.json["id"]
        judo.set("createdUserId", created_id)
        reporter.finish_step()
        
        reporter.finish_scenario()
        print("✅ Scenario 1.2: Create new user - PASSED")
        
    except Exception as e:
        reporter.finish_scenario(error_message=str(e))
        print(f"❌ Scenario 1.2: Create new user - FAILED: {e}")
    
    # Scenario 1.3: Update User (with intentional failure)
    scenario3 = reporter.start_scenario("Update user with validation failure", ["put", "user", "update", "failure"])
    
    try:
        # Step 1: Prepare update data
        step1 = reporter.start_step("Given I have updated user data")
        update_data = {
            "name": "Updated Demo User",
            "email": "updated.demo@example.com",
            "phone": "1-555-UPDATED-123"
        }
        judo.set("updateUserData", update_data)
        reporter.finish_step()
        
        # Step 2: Send PUT request
        step2 = reporter.start_step("When I send a PUT request to update the user")
        response = judo.put("/users/1", json=update_data)
        reporter.finish_step()
        
        # Step 3: Validate update
        step3 = reporter.start_step("Then the user should be updated")
        judo.match(response.status, 200)
        reporter.finish_step()
        
        # Step 4: Intentional failure for demo
        step4 = reporter.start_step("And the response should contain a specific field (DEMO FAILURE)")
        # This will fail to demonstrate error reporting
        judo.match(response.json.get("nonexistent_field"), "expected_value")
        reporter.finish_step()
        
        reporter.finish_scenario()
        print("✅ Scenario 1.3: Update user - PASSED")
        
    except Exception as e:
        reporter.finish_scenario(error_message=str(e))
        print(f"❌ Scenario 1.3: Update user - FAILED: {e}")
    
    reporter.finish_feature()
    
    # Feature 2: Post Management
    print("\n📋 Feature 2: Post Management")
    feature2 = reporter.start_feature(
        name="Post Management API",
        description="Testing blog post operations with advanced validation",
        file_path="examples/comprehensive_reporting_demo.py",
        tags=["api", "posts", "blog", "content"]
    )
    
    # Scenario 2.1: Get All Posts
    scenario4 = reporter.start_scenario("Get all posts with filtering", ["get", "posts", "list", "filter"])
    
    try:
        # Step 1: Set query parameters
        step1 = reporter.start_step("Given I set query parameters for filtering")
        judo.param("userId", 1)
        judo.param("_limit", 5)
        reporter.finish_step()
        
        # Step 2: Make request
        step2 = reporter.start_step("When I send a GET request to /posts")
        response = judo.get("/posts")
        reporter.finish_step()
        
        # Step 3: Validate response
        step3 = reporter.start_step("Then I should get a filtered list of posts")
        judo.match(response.status, 200)
        judo.match(response.json, "##array")
        reporter.finish_step()
        
        # Step 4: Validate post structure
        step4 = reporter.start_step("And each post should have the correct structure")
        posts = response.json
        for i, post in enumerate(posts[:3]):
            judo.match(post["id"], "##number")
            judo.match(post["userId"], "##number")
            judo.match(post["title"], "##string")
            judo.match(post["body"], "##string")
        reporter.finish_step()
        
        # Step 5: Store post data
        step5 = reporter.start_step("And I store post information")
        judo.set("postCount", len(posts))
        judo.set("firstPost", posts[0] if posts else None)
        reporter.finish_step()
        
        reporter.finish_scenario()
        print("✅ Scenario 2.1: Get all posts - PASSED")
        
    except Exception as e:
        reporter.finish_scenario(error_message=str(e))
        print(f"❌ Scenario 2.1: Get all posts - FAILED: {e}")
    
    # Scenario 2.2: Create Post with File Data
    scenario5 = reporter.start_scenario("Create post using external data", ["post", "create", "file-data"])
    
    try:
        # Step 1: Load post data from variable (simulating file)
        step1 = reporter.start_step("Given I have post data from external source")
        post_data = {
            "title": "Demo Post from Comprehensive Test",
            "body": "This is a comprehensive demo post created during the reporting demonstration. It includes detailed information about the test execution.",
            "userId": 1,
            "tags": ["demo", "test", "comprehensive"],
            "metadata": {
                "created_by": "judo_framework",
                "test_run": "comprehensive_demo",
                "timestamp": time.time()
            }
        }
        judo.set("postData", post_data)
        reporter.finish_step()
        
        # Step 2: Create post
        step2 = reporter.start_step("When I create a new post")
        response = judo.post("/posts", json=post_data)
        reporter.finish_step()
        
        # Step 3: Validate creation
        step3 = reporter.start_step("Then the post should be created successfully")
        judo.match(response.status, 201)
        judo.match(response.json["title"], post_data["title"])
        judo.match(response.json["userId"], post_data["userId"])
        reporter.finish_step()
        
        reporter.finish_scenario()
        print("✅ Scenario 2.2: Create post - PASSED")
        
    except Exception as e:
        reporter.finish_scenario(error_message=str(e))
        print(f"❌ Scenario 2.2: Create post - FAILED: {e}")
    
    reporter.finish_feature()
    
    # Feature 3: Data Validation
    print("\n📋 Feature 3: Advanced Data Validation")
    feature3 = reporter.start_feature(
        name="Advanced Data Validation",
        description="Testing complex data validation scenarios with schema validation",
        file_path="examples/comprehensive_reporting_demo.py",
        tags=["validation", "schema", "data", "advanced"]
    )
    
    # Scenario 3.1: Schema Validation
    scenario6 = reporter.start_scenario("Validate response against JSON schema", ["validation", "schema", "json"])
    
    try:
        # Step 1: Define schema
        step1 = reporter.start_step("Given I have a JSON schema for user validation")
        user_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "minimum": 1},
                "name": {"type": "string", "minLength": 1},
                "username": {"type": "string", "minLength": 1},
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
            "required": ["id", "name", "username", "email"]
        }
        judo.set("userSchema", user_schema)
        reporter.finish_step()
        
        # Step 2: Get user data
        step2 = reporter.start_step("When I retrieve user data")
        response = judo.get("/users/1")
        reporter.finish_step()
        
        # Step 3: Validate against schema
        step3 = reporter.start_step("Then the user data should match the schema")
        judo.match(response.status, 200)
        judo.match(response.json, user_schema)
        reporter.finish_step()
        
        reporter.finish_scenario()
        print("✅ Scenario 3.1: Schema validation - PASSED")
        
    except Exception as e:
        reporter.finish_scenario(error_message=str(e))
        print(f"❌ Scenario 3.1: Schema validation - FAILED: {e}")
    
    reporter.finish_feature()
    
    # Generate comprehensive report
    print("\n📊 Generating Comprehensive HTML Report...")
    report_path = reporter.generate_html_report("comprehensive_demo_report.html")
    
    # Show detailed summary
    summary = reporter.get_report_data().get_summary()
    print(f"\n📈 Comprehensive Test Summary:")
    print(f"   Features: {summary['total_features']}")
    print(f"   Scenarios: {summary['total_scenarios']}")
    print(f"   Steps: {summary['total_steps']}")
    print(f"   Passed Scenarios: {summary['scenario_counts']['passed']}")
    print(f"   Failed Scenarios: {summary['scenario_counts']['failed']}")
    print(f"   Success Rate: {summary['success_rate']:.1f}%")
    
    print(f"\n✅ Comprehensive HTML Report generated: {report_path}")
    print("\n🎯 Report Features Demonstrated:")
    print("   ✅ Multiple features and scenarios")
    print("   ✅ Detailed step-by-step execution")
    print("   ✅ HTTP request/response capture")
    print("   ✅ Headers, parameters, and body data")
    print("   ✅ Variable usage and assignment")
    print("   ✅ Assertion results with expected/actual values")
    print("   ✅ Error handling and failure reporting")
    print("   ✅ Execution timing and performance data")
    print("   ✅ Interactive HTML with collapsible sections")
    print("   ✅ Environment and configuration info")
    
    return report_path


def main():
    """Run comprehensive reporting demo"""
    try:
        report_path = create_comprehensive_test_report()
        
        print("\n" + "=" * 60)
        print("🎉 COMPREHENSIVE REPORTING DEMO COMPLETED!")
        print("=" * 60)
        print(f"📊 HTML Report: {report_path}")
        print("\n📋 What's included in the report:")
        print("   • Complete test execution timeline")
        print("   • All HTTP requests and responses")
        print("   • Headers, query parameters, and request bodies")
        print("   • Response data with syntax highlighting")
        print("   • Variable assignments and usage")
        print("   • Assertion results with pass/fail status")
        print("   • Error messages and stack traces")
        print("   • Performance metrics and timing")
        print("   • Interactive collapsible sections")
        print("   • Summary statistics and success rates")
        print("\n🌐 Open the HTML file in your browser to explore the report!")
        
    except Exception as e:
        print(f"❌ Error in comprehensive demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()