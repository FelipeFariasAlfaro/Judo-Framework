"""
Playwright Integration Hooks for Judo Framework
Extends existing Behave hooks to support browser automation
"""

import os
from typing import Optional
from ..behave.hooks import *  # Import all existing hooks
from . import PLAYWRIGHT_AVAILABLE, check_playwright_availability

if PLAYWRIGHT_AVAILABLE:
    from .browser_context import JudoBrowserContext


def setup_playwright_context(context):
    """
    Setup Playwright context if browser testing is enabled
    This function should be called from environment.py
    """
    # Check if user wants browser testing
    use_browser = os.getenv('JUDO_USE_BROWSER', 'false').lower() == 'true'
    
    if use_browser or hasattr(context, 'config') and getattr(context.config, 'use_browser', False):
        try:
            check_playwright_availability()
            
            # Replace regular JudoContext with JudoBrowserContext
            from ..behave.context import JudoContext
            if isinstance(context.judo_context, JudoContext) and not isinstance(context.judo_context, JudoBrowserContext):
                # Preserve existing state
                old_context = context.judo_context
                
                # Create new browser context
                browser_context = JudoBrowserContext(context)
                
                # Transfer state from old context
                browser_context.variables = old_context.variables.copy()
                browser_context.test_data = old_context.test_data.copy()
                browser_context.save_requests_responses = old_context.save_requests_responses
                browser_context.output_directory = old_context.output_directory
                browser_context.current_scenario_name = old_context.current_scenario_name
                
                # Replace context
                context.judo_context = browser_context
                context.judo = browser_context.judo
                
                print("🎭 Playwright integration enabled")
                
        except ImportError as e:
            print(f"⚠️ Playwright not available: {e}")
            print("   Continuing with API-only testing")
        except Exception as e:
            print(f"⚠️ Playwright setup failed: {e}")
            print("   Continuing with API-only testing")


def before_all_playwright(context):
    """
    Enhanced before_all hook with Playwright support
    Call this from your environment.py before_all function
    """
    # Call original before_all_judo
    before_all_judo(context)
    
    # Setup Playwright if needed
    setup_playwright_context(context)


def before_scenario_playwright(context, scenario):
    """
    Enhanced before_scenario hook with Playwright support
    Call this from your environment.py before_scenario function
    """
    # Call original before_scenario_judo
    before_scenario_judo(context, scenario)
    
    # Additional Playwright setup if browser context is available
    if hasattr(context.judo_context, 'start_browser'):
        # Check if scenario has browser-related tags
        browser_tags = [tag for tag in scenario.tags if tag.startswith('browser')]
        ui_tags = [tag for tag in scenario.tags if tag in ['ui', 'frontend', 'browser', 'playwright']]
        
        if browser_tags or ui_tags:
            # Auto-start browser for UI scenarios
            auto_start = os.getenv('JUDO_AUTO_START_BROWSER', 'true').lower() == 'true'
            if auto_start:
                try:
                    if not context.judo_context.browser:
                        context.judo_context.start_browser()
                        print(f"🎭 Auto-started browser for scenario: {scenario.name}")
                except Exception as e:
                    print(f"⚠️ Failed to auto-start browser: {e}")


def after_scenario_playwright(context, scenario):
    """
    Enhanced after_scenario hook with Playwright support
    Call this from your environment.py after_scenario function
    """
    # Handle browser-specific cleanup and screenshots
    if hasattr(context.judo_context, 'browser') and context.judo_context.browser:
        try:
            # Take screenshot on failure if enabled
            if scenario.status == 'failed' and context.judo_context.screenshot_on_failure:
                try:
                    screenshot_path = context.judo_context.take_screenshot(
                        f"failure_{context.judo_context._sanitize_filename(scenario.name)}"
                    )
                    print(f"📸 Failure screenshot saved: {screenshot_path}")
                    
                    # Add screenshot info to reporter if available
                    try:
                        from ..reporting.reporter import get_reporter
                        reporter = get_reporter()
                        if reporter and reporter.current_scenario:
                            if not hasattr(reporter.current_scenario, 'screenshots'):
                                reporter.current_scenario.screenshots = []
                            reporter.current_scenario.screenshots.append({
                                'type': 'failure',
                                'path': screenshot_path,
                                'timestamp': context.judo_context._get_timestamp()
                            })
                    except Exception as e:
                        print(f"⚠️ Could not add screenshot to report: {e}")
                        
                except Exception as e:
                    print(f"⚠️ Failed to take failure screenshot: {e}")
            
            # Close pages but keep browser for next scenario (performance optimization)
            close_browser_after_scenario = os.getenv('JUDO_CLOSE_BROWSER_AFTER_SCENARIO', 'false').lower() == 'true'
            if close_browser_after_scenario:
                context.judo_context.close_browser()
            else:
                # Just close pages, keep browser context
                if hasattr(context.judo_context, 'pages'):
                    for page_name in list(context.judo_context.pages.keys()):
                        context.judo_context.close_page(page_name)
                
        except Exception as e:
            print(f"⚠️ Error in Playwright cleanup: {e}")
    
    # Call original after_scenario_judo
    after_scenario_judo(context, scenario)


def after_all_playwright(context):
    """
    Enhanced after_all hook with Playwright support
    Call this from your environment.py after_all function
    """
    # Close browser if it's still open
    if hasattr(context.judo_context, 'browser') and context.judo_context.browser:
        try:
            context.judo_context.close_browser()
            print("🎭 Browser closed")
        except Exception as e:
            print(f"⚠️ Error closing browser: {e}")
    
    # Call original after_all_judo
    after_all_judo(context)


def before_step_playwright(context, step):
    """
    Enhanced before_step hook with Playwright support
    Optional - call this from your environment.py before_step function
    """
    # Call original before_step if it exists
    try:
        from ..behave.hooks import before_step_judo
        before_step_judo(context, step)
    except (ImportError, AttributeError):
        pass
    
    # Playwright-specific step preparation
    if hasattr(context.judo_context, 'page') and context.judo_context.page:
        # Take screenshot before step if enabled
        if os.getenv('JUDO_SCREENSHOT_BEFORE_STEP', 'false').lower() == 'true':
            try:
                step_name = context.judo_context._sanitize_filename(step.name)
                screenshot_path = context.judo_context.take_screenshot(f"before_step_{step_name}")
                print(f"📸 Before-step screenshot: {screenshot_path}")
            except Exception as e:
                print(f"⚠️ Failed to take before-step screenshot: {e}")


def after_step_playwright(context, step):
    """
    Enhanced after_step hook with Playwright support
    Optional - call this from your environment.py after_step function
    """
    # Playwright-specific step cleanup
    if hasattr(context.judo_context, 'page') and context.judo_context.page:
        # Take screenshot after step if enabled
        if os.getenv('JUDO_SCREENSHOT_AFTER_STEP', 'false').lower() == 'true':
            try:
                step_name = context.judo_context._sanitize_filename(step.name)
                screenshot_path = context.judo_context.take_screenshot(f"after_step_{step_name}")
                print(f"📸 After-step screenshot: {screenshot_path}")
            except Exception as e:
                print(f"⚠️ Failed to take after-step screenshot: {e}")
        
        # Take screenshot on step failure
        if step.status == 'failed' and os.getenv('JUDO_SCREENSHOT_ON_STEP_FAILURE', 'true').lower() == 'true':
            try:
                step_name = context.judo_context._sanitize_filename(step.name)
                screenshot_path = context.judo_context.take_screenshot(f"step_failure_{step_name}")
                print(f"📸 Step failure screenshot: {screenshot_path}")
                
                # Add to reporter if available
                try:
                    from ..reporting.reporter import get_reporter
                    reporter = get_reporter()
                    if reporter and reporter.current_step:
                        if not hasattr(reporter.current_step, 'screenshots'):
                            reporter.current_step.screenshots = []
                        reporter.current_step.screenshots.append({
                            'type': 'step_failure',
                            'path': screenshot_path,
                            'timestamp': context.judo_context._get_timestamp()
                        })
                except Exception as e:
                    print(f"⚠️ Could not add step screenshot to report: {e}")
                    
            except Exception as e:
                print(f"⚠️ Failed to take step failure screenshot: {e}")
    
    # Call original after_step if it exists
    try:
        from ..behave.hooks import after_step_judo
        after_step_judo(context, step)
    except (ImportError, AttributeError):
        pass


# Convenience function for easy integration
def integrate_playwright_hooks(context, hook_type: str, *args, **kwargs):
    """
    Convenience function to integrate Playwright hooks
    
    Usage in environment.py:
    
    from judo.playwright.hooks import integrate_playwright_hooks
    
    def before_all(context):
        integrate_playwright_hooks(context, 'before_all')
    
    def before_scenario(context, scenario):
        integrate_playwright_hooks(context, 'before_scenario', scenario)
    
    def after_scenario(context, scenario):
        integrate_playwright_hooks(context, 'after_scenario', scenario)
    
    def after_all(context):
        integrate_playwright_hooks(context, 'after_all')
    """
    hook_functions = {
        'before_all': before_all_playwright,
        'before_scenario': before_scenario_playwright,
        'after_scenario': after_scenario_playwright,
        'after_all': after_all_playwright,
        'before_step': before_step_playwright,
        'after_step': after_step_playwright,
    }
    
    if hook_type in hook_functions:
        return hook_functions[hook_type](context, *args, **kwargs)
    else:
        raise ValueError(f"Unknown hook type: {hook_type}")


# Environment variable configuration helper
def configure_playwright_from_env():
    """
    Configure Playwright settings from environment variables
    Call this at the beginning of your environment.py
    
    Environment variables:
    - JUDO_USE_BROWSER: Enable browser testing (true/false)
    - JUDO_BROWSER: Browser type (chromium/firefox/webkit)
    - JUDO_HEADLESS: Headless mode (true/false)
    - JUDO_SCREENSHOTS: Enable screenshots (true/false)
    - JUDO_SCREENSHOT_ON_FAILURE: Screenshot on failure (true/false)
    - JUDO_SCREENSHOT_ON_STEP_FAILURE: Screenshot on step failure (true/false)
    - JUDO_SCREENSHOT_BEFORE_STEP: Screenshot before each step (true/false)
    - JUDO_SCREENSHOT_AFTER_STEP: Screenshot after each step (true/false)
    - JUDO_AUTO_START_BROWSER: Auto-start browser for UI scenarios (true/false)
    - JUDO_CLOSE_BROWSER_AFTER_SCENARIO: Close browser after each scenario (true/false)
    - JUDO_VIEWPORT_WIDTH: Browser viewport width (default: 1280)
    - JUDO_VIEWPORT_HEIGHT: Browser viewport height (default: 720)
    - JUDO_BROWSER_ARGS: Additional browser arguments (comma-separated)
    - JUDO_USER_AGENT: Custom user agent string
    """
    config = {}
    
    # Browser settings
    config['use_browser'] = os.getenv('JUDO_USE_BROWSER', 'false').lower() == 'true'
    config['browser_type'] = os.getenv('JUDO_BROWSER', 'chromium').lower()
    config['headless'] = os.getenv('JUDO_HEADLESS', 'true').lower() == 'true'
    
    # Screenshot settings
    config['screenshots'] = os.getenv('JUDO_SCREENSHOTS', 'false').lower() == 'true'
    config['screenshot_on_failure'] = os.getenv('JUDO_SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
    config['screenshot_on_step_failure'] = os.getenv('JUDO_SCREENSHOT_ON_STEP_FAILURE', 'true').lower() == 'true'
    config['screenshot_before_step'] = os.getenv('JUDO_SCREENSHOT_BEFORE_STEP', 'false').lower() == 'true'
    config['screenshot_after_step'] = os.getenv('JUDO_SCREENSHOT_AFTER_STEP', 'false').lower() == 'true'
    
    # Behavior settings
    config['auto_start_browser'] = os.getenv('JUDO_AUTO_START_BROWSER', 'true').lower() == 'true'
    config['close_browser_after_scenario'] = os.getenv('JUDO_CLOSE_BROWSER_AFTER_SCENARIO', 'false').lower() == 'true'
    
    # Viewport settings
    try:
        config['viewport_width'] = int(os.getenv('JUDO_VIEWPORT_WIDTH', '1280'))
        config['viewport_height'] = int(os.getenv('JUDO_VIEWPORT_HEIGHT', '720'))
    except ValueError:
        config['viewport_width'] = 1280
        config['viewport_height'] = 720
    
    # Browser arguments
    browser_args = os.getenv('JUDO_BROWSER_ARGS', '')
    if browser_args:
        config['browser_args'] = [arg.strip() for arg in browser_args.split(',')]
    else:
        config['browser_args'] = []
    
    # User agent
    config['user_agent'] = os.getenv('JUDO_USER_AGENT', '')
    
    return config