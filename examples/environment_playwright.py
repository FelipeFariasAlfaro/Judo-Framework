"""
Example environment.py for Playwright Integration with Judo Framework
This shows how to set up hybrid API + UI testing
"""

import os
from judo.behave import setup_judo_context
from judo.playwright.hooks import integrate_playwright_hooks, configure_playwright_from_env

# Configure Playwright settings from environment variables
playwright_config = configure_playwright_from_env()

def before_all(context):
    """Setup before all tests"""
    print("🚀 Starting Judo Framework with Playwright Integration")
    
    # Setup basic Judo context
    setup_judo_context(context)
    
    # Enable browser testing if configured
    if playwright_config.get('use_browser', False):
        print("🎭 Browser testing enabled")
        
        # Set browser configuration on context for hooks to use
        context.config.use_browser = True
        context.config.browser_type = playwright_config.get('browser_type', 'chromium')
        context.config.headless = playwright_config.get('headless', True)
    
    # Integrate Playwright hooks
    integrate_playwright_hooks(context, 'before_all')
    
    print(f"📊 Configuration:")
    print(f"   - API Testing: ✅ Always enabled")
    print(f"   - Browser Testing: {'✅ Enabled' if playwright_config.get('use_browser') else '❌ Disabled'}")
    if playwright_config.get('use_browser'):
        print(f"   - Browser: {playwright_config.get('browser_type', 'chromium')}")
        print(f"   - Headless: {playwright_config.get('headless', True)}")
        print(f"   - Screenshots: {'✅ Enabled' if playwright_config.get('screenshots') else '❌ Disabled'}")


def before_scenario(context, scenario):
    """Setup before each scenario"""
    # Integrate Playwright hooks
    integrate_playwright_hooks(context, 'before_scenario', scenario)
    
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
    # Integrate Playwright hooks (handles screenshots on failure, etc.)
    integrate_playwright_hooks(context, 'after_scenario', scenario)
    
    # Log scenario result
    if scenario.status == 'passed':
        print(f"✅ Scenario passed: {scenario.name}")
    elif scenario.status == 'failed':
        print(f"❌ Scenario failed: {scenario.name}")
        
        # Additional failure handling for UI scenarios
        if hasattr(context.judo_context, 'browser') and context.judo_context.browser:
            print(f"🎭 Browser was active during failure")
    else:
        print(f"⚠️ Scenario {scenario.status}: {scenario.name}")


def after_all(context):
    """Cleanup after all tests"""
    # Integrate Playwright hooks (handles browser cleanup)
    integrate_playwright_hooks(context, 'after_all')
    
    print("🏁 All tests completed")


# Optional: Step-level hooks for detailed debugging
def before_step(context, step):
    """Before each step (optional)"""
    # Only enable for debugging
    if os.getenv('JUDO_DEBUG_STEPS', 'false').lower() == 'true':
        integrate_playwright_hooks(context, 'before_step', step)


def after_step(context, step):
    """After each step (optional)"""
    # Only enable for debugging or if step screenshots are enabled
    if (os.getenv('JUDO_DEBUG_STEPS', 'false').lower() == 'true' or 
        os.getenv('JUDO_SCREENSHOT_ON_STEP_FAILURE', 'false').lower() == 'true'):
        integrate_playwright_hooks(context, 'after_step', step)


# Alternative: Simple setup without hooks integration
def simple_setup_example():
    """
    Alternative simple setup example
    Use this if you want more control over the integration
    """
    def before_all_simple(context):
        # Basic setup
        setup_judo_context(context)
        
        # Enable browser if needed
        if os.getenv('JUDO_USE_BROWSER', 'false').lower() == 'true':
            try:
                from judo.playwright.browser_context import JudoBrowserContext
                
                # Replace context with browser-enabled version
                old_context = context.judo_context
                context.judo_context = JudoBrowserContext(context)
                
                # Transfer state
                context.judo_context.variables = old_context.variables
                context.judo_context.test_data = old_context.test_data
                context.judo = context.judo_context.judo
                
                print("🎭 Browser context enabled")
            except ImportError:
                print("⚠️ Playwright not available, using API-only mode")
    
    def after_all_simple(context):
        # Simple cleanup
        if hasattr(context.judo_context, 'close_browser'):
            context.judo_context.close_browser()
    
    return before_all_simple, after_all_simple


# Environment variable examples for reference:
"""
# Basic browser configuration
export JUDO_USE_BROWSER=true
export JUDO_BROWSER=chromium  # or firefox, webkit
export JUDO_HEADLESS=false    # true for headless, false for headed

# Screenshot configuration
export JUDO_SCREENSHOTS=true
export JUDO_SCREENSHOT_ON_FAILURE=true
export JUDO_SCREENSHOT_ON_STEP_FAILURE=false
export JUDO_SCREENSHOT_BEFORE_STEP=false
export JUDO_SCREENSHOT_AFTER_STEP=false

# Browser behavior
export JUDO_AUTO_START_BROWSER=true
export JUDO_CLOSE_BROWSER_AFTER_SCENARIO=false

# Viewport and display
export JUDO_VIEWPORT_WIDTH=1920
export JUDO_VIEWPORT_HEIGHT=1080
export JUDO_USER_AGENT="Custom User Agent String"

# Browser arguments (comma-separated)
export JUDO_BROWSER_ARGS="--disable-web-security,--disable-features=VizDisplayCompositor"

# Debugging
export JUDO_DEBUG_STEPS=false
export JUDO_LOG_CONSOLE=false
export JUDO_LOG_BROWSER_REQUESTS=false
export JUDO_LOG_BROWSER_RESPONSES=false

# Directories
export JUDO_SCREENSHOT_DIR=screenshots
export JUDO_OUTPUT_DIRECTORY=judo_reports
"""