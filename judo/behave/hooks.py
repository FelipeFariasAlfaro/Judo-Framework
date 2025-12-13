"""
Behave Hooks for Judo Framework
Provides setup and teardown functionality for BDD tests
"""

from behave import fixture
from .context import JudoContext


def before_all(context):
    """
    Hook that runs before all tests
    Initialize global Judo context and configuration
    """
    # Initialize Judo context
    context.judo_context = JudoContext(context)
    
    # Load configuration from environment or config files
    import os
    
    # Set base URL from environment
    base_url = os.getenv('JUDO_BASE_URL')
    if base_url:
        context.judo_context.set_base_url(base_url)
    
    # Set default timeout
    timeout = os.getenv('JUDO_TIMEOUT', '30')
    try:
        timeout_seconds = float(timeout)
        context.judo_context.judo.http_client.set_timeout(timeout_seconds)
    except ValueError:
        pass
    
    # Set SSL verification
    verify_ssl = os.getenv('JUDO_VERIFY_SSL', 'true').lower()
    context.judo_context.judo.http_client.set_verify_ssl(verify_ssl == 'true')
    
    # Load global test data if available
    test_data_file = os.getenv('JUDO_TEST_DATA_FILE')
    if test_data_file and os.path.exists(test_data_file):
        try:
            import json
            with open(test_data_file, 'r') as f:
                global_data = json.load(f)
                for key, value in global_data.items():
                    context.judo_context.set_variable(key, value)
        except Exception as e:
            print(f"Warning: Could not load test data file {test_data_file}: {e}")
    
    from ..utils.safe_print import safe_emoji_print
    safe_emoji_print("🥋", "Judo Framework initialized for Behave tests")


def before_scenario(context, scenario):
    """
    Hook that runs before each scenario
    Reset context and prepare for new test
    """
    # Ensure Judo context exists
    if not hasattr(context, 'judo_context'):
        context.judo_context = JudoContext(context)
    
    # Reset context for new scenario
    context.judo_context.reset()
    
    # Set current scenario for request/response logging
    context.judo_context.set_current_scenario(scenario.name)
    
    # Log scenario start
    context.judo_context.log(f"Starting scenario: {scenario.name}")
    
    # Set scenario-specific variables
    context.judo_context.set_variable('scenario_name', scenario.name)
    context.judo_context.set_variable('scenario_tags', [tag for tag in scenario.tags])


def after_scenario(context, scenario):
    """
    Hook that runs after each scenario
    Cleanup and logging
    """
    if hasattr(context, 'judo_context'):
        # Log scenario completion
        status = "PASSED" if scenario.status == "passed" else "FAILED"
        context.judo_context.log(f"Scenario {scenario.name}: {status}")
        
        # Print response if scenario failed and we have a response
        if scenario.status == "failed" and context.judo_context.response:
            print("\n--- Last Response (for debugging) ---")
            context.judo_context.print_response()
            print("--- End Response ---\n")


def after_all(context):
    """
    Hook that runs after all tests
    Final cleanup
    """
    if hasattr(context, 'judo_context'):
        # Stop any running mock servers
        try:
            context.judo_context.judo.stop_mock()
        except:
            pass
        
        print("🏁 Judo Framework tests completed")


# Fixture for mock server
@fixture
def mock_server(context, port=8080):
    """
    Fixture to start and stop mock server
    Usage in feature files: @fixture.mock_server
    """
    mock = context.judo_context.judo.start_mock(port)
    context.mock_server = mock
    
    yield mock
    
    context.judo_context.judo.stop_mock()
    delattr(context, 'mock_server')


# Fixture for test data cleanup
@fixture
def clean_test_data(context):
    """
    Fixture to clean up test data after scenario
    Usage in feature files: @fixture.clean_test_data
    """
    yield
    
    # Clean up any test data created during scenario
    if hasattr(context, 'created_resources'):
        for resource in context.created_resources:
            try:
                # Attempt to delete created resource
                context.judo_context.make_request('DELETE', resource)
            except:
                pass  # Ignore cleanup errors
        
        context.created_resources.clear()