"""
Import all Judo Framework step definitions for Behave
This file makes all Judo steps available to your feature files
"""

# Import all step definitions from Judo Framework
from judo.behave.steps import *

# You can add custom step definitions here if needed
from behave import given, when, then, step


# Example of custom step definition
@given('I have custom test setup')
def step_custom_setup(context):
    """Custom setup step"""
    context.judo_context.log("Custom setup completed")


@then('I should see the custom result')
def step_custom_validation(context):
    """Custom validation step"""
    # Add your custom validation logic here
    pass