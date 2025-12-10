"""
Behave Integration Example for Judo Framework
Demonstrates how to use Judo Framework with Behave for BDD testing
"""

import os
import subprocess
import sys


def run_behave_tests():
    """Run Behave tests with Judo Framework"""
    
    print("🥋 Running Judo Framework with Behave (BDD Testing)")
    print("=" * 60)
    
    # Check if behave is installed
    try:
        import behave
        print("✓ Behave is installed")
    except ImportError:
        print("❌ Behave is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "behave>=1.2.6"])
        print("✓ Behave installed successfully")
    
    # Set environment variables for testing
    os.environ['JUDO_BASE_URL'] = 'https://jsonplaceholder.typicode.com'
    os.environ['JUDO_TIMEOUT'] = '30'
    os.environ['JUDO_VERIFY_SSL'] = 'true'
    
    print("\n📋 Environment Configuration:")
    print(f"   Base URL: {os.environ.get('JUDO_BASE_URL')}")
    print(f"   Timeout: {os.environ.get('JUDO_TIMEOUT')}s")
    print(f"   SSL Verification: {os.environ.get('JUDO_VERIFY_SSL')}")
    
    # Run specific feature file
    print("\n🚀 Running API Testing Feature...")
    
    try:
        # Run behave command
        result = subprocess.run([
            sys.executable, "-m", "behave", 
            "features/api_testing.feature",
            "--format=pretty",
            "--no-capture",  # Show print statements
            "--verbose"
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n🎉 All Behave tests passed!")
        else:
            print(f"\n❌ Some tests failed (exit code: {result.returncode})")
            
    except FileNotFoundError:
        print("❌ Could not run behave. Make sure it's installed and in PATH")
    except Exception as e:
        print(f"❌ Error running behave: {e}")


def show_gherkin_examples():
    """Show examples of Gherkin syntax with Judo Framework"""
    
    print("\n📝 Gherkin Syntax Examples with Judo Framework")
    print("=" * 60)
    
    examples = [
        {
            "title": "Basic API Testing",
            "gherkin": """
Feature: User API Testing
  Scenario: Get user information
    Given I have a Judo API client
    And the base URL is "https://api.example.com"
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "name"
    And the response "$.email" should be a valid email
            """.strip()
        },
        {
            "title": "Authentication Testing",
            "gherkin": """
Feature: API Authentication
  Scenario: Bearer token authentication
    Given I have a Judo API client
    And I use bearer token "my-jwt-token"
    When I send a GET request to "/protected-resource"
    Then the response status should be 200
            """.strip()
        },
        {
            "title": "Data-Driven Testing",
            "gherkin": """
Feature: Data-Driven API Tests
  Scenario Outline: Test multiple users
    When I send a GET request to "/users/<user_id>"
    Then the response status should be 200
    And the response "$.name" should be "<expected_name>"
    
    Examples:
      | user_id | expected_name |
      | 1       | John Doe      |
      | 2       | Jane Smith    |
            """.strip()
        },
        {
            "title": "JSON Schema Validation",
            "gherkin": """
Feature: Schema Validation
  Scenario: Validate API response structure
    When I send a GET request to "/users/1"
    Then the response should match the schema:
      '''
      {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "name": {"type": "string"},
          "email": {"type": "string", "format": "email"}
        },
        "required": ["id", "name", "email"]
      }
      '''
            """.strip()
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}:")
        print("-" * 40)
        print(example['gherkin'])


def show_step_definitions():
    """Show available step definitions"""
    
    print("\n🔧 Available Step Definitions")
    print("=" * 60)
    
    steps = [
        {
            "category": "Setup Steps",
            "steps": [
                'Given I have a Judo API client',
                'Given the base URL is "{url}"',
                'Given I set the variable "{name}" to "{value}"',
                'Given I set the header "{name}" to "{value}"'
            ]
        },
        {
            "category": "Authentication Steps", 
            "steps": [
                'Given I use bearer token "{token}"',
                'Given I use basic authentication with username "{user}" and password "{pass}"'
            ]
        },
        {
            "category": "HTTP Request Steps",
            "steps": [
                'When I send a GET request to "{endpoint}"',
                'When I send a POST request to "{endpoint}" with JSON',
                'When I send a PUT request to "{endpoint}" with JSON',
                'When I send a DELETE request to "{endpoint}"'
            ]
        },
        {
            "category": "Validation Steps",
            "steps": [
                'Then the response status should be {status}',
                'Then the response should contain "{key}"',
                'Then the response "{jsonpath}" should be "{value}"',
                'Then the response should match the schema'
            ]
        },
        {
            "category": "Type Validation Steps",
            "steps": [
                'Then the response "{jsonpath}" should be a string',
                'Then the response "{jsonpath}" should be a number',
                'Then the response "{jsonpath}" should be a valid email',
                'Then the response "{jsonpath}" should be a valid UUID'
            ]
        }
    ]
    
    for category in steps:
        print(f"\n{category['category']}:")
        print("-" * 30)
        for step in category['steps']:
            print(f"  • {step}")


def main():
    """Main function to demonstrate Behave integration"""
    
    print("🥋 Judo Framework - Behave Integration Demo")
    print("Complete BDD Testing with Gherkin DSL")
    print("=" * 60)
    
    # Show examples
    show_gherkin_examples()
    show_step_definitions()
    
    # Ask user if they want to run tests
    print("\n" + "=" * 60)
    response = input("Do you want to run the Behave tests? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        run_behave_tests()
    else:
        print("\n📚 To run Behave tests manually, use:")
        print("   behave features/")
        print("   behave features/api_testing.feature")
        print("   behave --tags=@smoke")
    
    print("\n🎯 Judo Framework + Behave Integration Complete!")
    print("You now have full BDD testing capabilities with Gherkin DSL")


if __name__ == "__main__":
    main()