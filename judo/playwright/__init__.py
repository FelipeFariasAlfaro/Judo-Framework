"""
Playwright Integration for Judo Framework
Optional browser automation capabilities

This module provides the infrastructure to use Playwright with Judo Framework,
but does NOT provide pre-built steps. Users should create their own custom steps
based on their specific needs.

Example usage in features/environment.py:
    from judo.behave import *
    from judo.playwright.browser_context import JudoBrowserContext
    
    def before_scenario(context, scenario):
        before_scenario_judo(context, scenario)
        
        # Initialize Playwright for UI tests
        if 'ui' in scenario.tags:
            context.judo_context = JudoBrowserContext(context)
            # Your custom browser setup here

Then create your own custom steps in features/steps/:
    from behave import given, when, then
    
    @when('navego a "{url}"')
    def step_navigate(context, url):
        context.judo_context.navigate_to(url)
    
    @when('hago clic en "{selector}"')
    def step_click(context, selector):
        context.judo_context.click_element(selector)
"""

# Check if Playwright is available
try:
    import playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

__all__ = ['PLAYWRIGHT_AVAILABLE']