"""
Environment setup for local Playwright integration testing
"""

import os
import sys

# Add the project root to Python path so we can import judo
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Import all Judo functionality including steps
from judo.behave import *

# Try to import Playwright integration
try:
    import playwright
    from judo.playwright.hooks import integrate_playwright_hooks, configure_playwright_from_env
    # Import Playwright steps to register them
    from judo.playwright import steps, steps_es
    PLAYWRIGHT_AVAILABLE = True
    print("🎭 Playwright integration available")
except ImportError as e:
    PLAYWRIGHT_AVAILABLE = False
    print(f"⚠️ Playwright not available: {e}")

# Configure Playwright from environment
if PLAYWRIGHT_AVAILABLE:
    playwright_config = configure_playwright_from_env()
else:
    playwright_config = {}

def before_all(context):
    """Setup before all tests"""
    print("🚀 Starting Judo Framework Test Suite")
    
    # Call the original Judo before_all hook
    before_all_judo(context)
    print("✅ Judo context initialized")
    
    print(f"📊 Test Configuration:")
    print(f"   - API Testing: ✅ Enabled")
    print(f"   - Browser Testing: {'✅ Enabled' if PLAYWRIGHT_AVAILABLE else '❌ Disabled'}")

def before_scenario(context, scenario):
    """Setup before each scenario"""
    # Call the original Judo before_scenario hook
    before_scenario_judo(context, scenario)
    
    # Log scenario type
    scenario_tags = set(scenario.tags)
    if 'ui' in scenario_tags or 'browser' in scenario_tags:
        print(f"🎭 UI Scenario: {scenario.name}")
    elif 'api' in scenario_tags:
        print(f"🌐 API Scenario: {scenario.name}")
    elif 'hybrid' in scenario_tags:
        print(f"🔄 Hybrid Scenario: {scenario.name}")
    else:
        print(f"📝 Scenario: {scenario.name}")

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    # Call the original Judo after_scenario hook
    after_scenario_judo(context, scenario)
    
    # Log scenario result
    if scenario.status == 'passed':
        print(f"✅ Scenario passed: {scenario.name}")
    elif scenario.status == 'failed':
        print(f"❌ Scenario failed: {scenario.name}")
    else:
        print(f"⚠️ Scenario {scenario.status}: {scenario.name}")

def after_all(context):
    """Cleanup after all tests"""
    # Call the original Judo after_all hook
    after_all_judo(context)
    
    print("🏁 All tests completed")

# Optional: Enable step-level debugging
def before_step(context, step):
    """Before each step (for debugging)"""
    if os.getenv('JUDO_DEBUG_STEPS', 'false').lower() == 'true':
        print(f"🔍 Step: {step.name}")
        if PLAYWRIGHT_AVAILABLE:
            integrate_playwright_hooks(context, 'before_step', step)

def after_step(context, step):
    """After each step (for debugging)"""
    if step.status == 'failed':
        print(f"❌ Step failed: {step.name}")
        if hasattr(step, 'exception'):
            print(f"   Error: {step.exception}")
    
    if PLAYWRIGHT_AVAILABLE:
        integrate_playwright_hooks(context, 'after_step', step)