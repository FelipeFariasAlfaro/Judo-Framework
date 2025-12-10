"""
Reporting Example - Demonstrates HTML report generation
"""

from judo import Judo
from judo.reporting.reporter import JudoReporter
import time


def test_with_detailed_reporting():
    """Test with detailed HTML reporting"""
    print("🥋 Judo Framework - HTML Reporting Example")
    print("=" * 50)
    
    # Create reporter
    reporter = JudoReporter("API Testing with Detailed Reports")
    
    # Create Judo instance with reporting enabled
    judo = Judo(enable_reporting=True)
    judo.reporter = reporter
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # Start feature
    feature = reporter.start_feature(
        name="User Management API",
        description="Testing user CRUD operations with detailed reporting",
        file_path="examples/reporting_example.py",
        tags=["api", "users", "crud"]
    )
    
    try:
        # Scenario 1: Get User
        print("\n📋 Scenario 1: Get User Details")
        scenario1 = reporter.start_scenario("Get user details", ["get", "user"])
        
        try:
            # Step 1: Make GET request
            step1 = reporter.start_step("When I send a GET request to /users/1")
            response = judo.get("/users/1")
            reporter.finish_step()
            
            # Step 2: Validate status
            step2 = reporter.start_step("Then the response status should be 200")
            judo.match(response.status, 200)
            reporter.finish_step()
            
            # Step 3: Validate user data
            step3 = reporter.start_step("And the response should contain user data")
            judo.match(response.json["id"], 1)
            judo.match(response.json["name"], "##string")
            judo.match(response.json["email"], "##email")
            reporter.finish_step()
            
            reporter.finish_scenario()
            print("✅ Scenario 1 passed")
            
        except Exception as e:
            reporter.finish_scenario(error_message=str(e))
            print(f"❌ Scenario 1 failed: {e}")
        
        # Scenario 2: Create User
        print("\n📋 Scenario 2: Create New User")
        scenario2 = reporter.start_scenario("Create new user", ["post", "user", "create"])
        
        try:
            # Step 1: Set user data
            step1 = reporter.start_step("Given I have user data")
            user_data = {
                "name": "Test User",
                "username": "testuser",
                "email": "test@example.com",
                "phone": "123-456-7890"
            }
            judo.set("userData", user_data)
            reporter.finish_step()
            
            # Step 2: Make POST request
            step2 = reporter.start_step("When I send a POST request to /users")
            response = judo.post("/users", json=user_data)
            reporter.finish_step()
            
            # Step 3: Validate creation
            step3 = reporter.start_step("Then the user should be created successfully")
            judo.match(response.status, 201)
            judo.match(response.json["name"], user_data["name"])
            judo.match(response.json["email"], user_data["email"])
            reporter.finish_step()
            
            # Step 4: Extract user ID
            step4 = reporter.start_step("And I extract the user ID")
            user_id = response.json["id"]
            judo.set("createdUserId", user_id)
            reporter.finish_step()
            
            reporter.finish_scenario()
            print("✅ Scenario 2 passed")
            
        except Exception as e:
            reporter.finish_scenario(error_message=str(e))
            print(f"❌ Scenario 2 failed: {e}")
        
        # Scenario 3: Update User (with intentional failure for demo)
        print("\n📋 Scenario 3: Update User (Demo Failure)")
        scenario3 = reporter.start_scenario("Update user details", ["put", "user", "update"])
        
        try:
            # Step 1: Prepare update data
            step1 = reporter.start_step("Given I have updated user data")
            update_data = {
                "name": "Updated Test User",
                "email": "updated@example.com"
            }
            judo.set("updateData", update_data)
            reporter.finish_step()
            
            # Step 2: Make PUT request
            step2 = reporter.start_step("When I send a PUT request to /users/1")
            response = judo.put("/users/1", json=update_data)
            reporter.finish_step()
            
            # Step 3: Validate update (this will pass)
            step3 = reporter.start_step("Then the user should be updated")
            judo.match(response.status, 200)
            reporter.finish_step()
            
            # Step 4: Intentional failure for demo
            step4 = reporter.start_step("And the response should have specific field")
            # This will fail intentionally to show error reporting
            judo.match(response.json.get("nonexistent_field"), "expected_value")
            reporter.finish_step()
            
            reporter.finish_scenario()
            print("✅ Scenario 3 passed")
            
        except Exception as e:
            reporter.finish_scenario(error_message=str(e))
            print(f"❌ Scenario 3 failed: {e}")
        
        # Scenario 4: Get All Users
        print("\n📋 Scenario 4: Get All Users")
        scenario4 = reporter.start_scenario("Get all users list", ["get", "users", "list"])
        
        try:
            # Step 1: Make GET request
            step1 = reporter.start_step("When I send a GET request to /users")
            response = judo.get("/users")
            reporter.finish_step()
            
            # Step 2: Validate response
            step2 = reporter.start_step("Then I should get a list of users")
            judo.match(response.status, 200)
            judo.match(response.json, "##array")
            reporter.finish_step()
            
            # Step 3: Validate array content
            step3 = reporter.start_step("And each user should have required fields")
            users = response.json
            for i, user in enumerate(users[:3]):  # Check first 3 users
                judo.match(user["id"], "##number")
                judo.match(user["name"], "##string")
                judo.match(user["email"], "##email")
            reporter.finish_step()
            
            # Step 4: Store user count
            step4 = reporter.start_step("And I store the user count")
            judo.set("userCount", len(users))
            reporter.finish_step()
            
            reporter.finish_scenario()
            print("✅ Scenario 4 passed")
            
        except Exception as e:
            reporter.finish_scenario(error_message=str(e))
            print(f"❌ Scenario 4 failed: {e}")
        
    finally:
        # Finish feature
        reporter.finish_feature()
    
    # Generate HTML report
    print("\n📊 Generating HTML Report...")
    report_path = reporter.generate_html_report("detailed_api_test_report.html")
    print(f"✅ HTML Report generated: {report_path}")
    
    # Show summary
    summary = reporter.get_report_data().get_summary()
    print(f"\n📈 Test Summary:")
    print(f"   Features: {summary['total_features']}")
    print(f"   Scenarios: {summary['total_scenarios']}")
    print(f"   Steps: {summary['total_steps']}")
    print(f"   Success Rate: {summary['success_rate']:.1f}%")
    
    return report_path


def test_simple_reporting():
    """Simple test with automatic reporting"""
    print("\n🔧 Simple Automatic Reporting Test")
    print("-" * 40)
    
    # Create Judo instance (reporting enabled by default)
    judo = Judo()
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # Start a simple scenario
    judo.start_scenario("Simple API Test")
    
    # Test steps with automatic reporting
    judo.start_step("Get post data")
    response = judo.get("/posts/1")
    judo.finish_step(response.status == 200)
    
    judo.start_step("Validate post data")
    judo.match(response.status, 200)
    judo.match(response.json["userId"], 1)
    judo.finish_step(True)
    
    judo.finish_scenario(True)
    
    # Generate report
    report_path = judo.generate_html_report("simple_test_report.html")
    print(f"✅ Simple report generated: {report_path}")
    
    return report_path


def main():
    """Run reporting examples"""
    try:
        # Detailed reporting example
        detailed_report = test_with_detailed_reporting()
        
        # Simple reporting example
        simple_report = test_simple_reporting()
        
        print("\n🎉 Reporting Examples Completed!")
        print(f"📊 Detailed Report: {detailed_report}")
        print(f"📋 Simple Report: {simple_report}")
        print("\nOpen these HTML files in your browser to view the reports.")
        
    except Exception as e:
        print(f"❌ Error in reporting examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()