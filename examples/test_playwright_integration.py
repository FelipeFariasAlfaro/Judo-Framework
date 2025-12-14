#!/usr/bin/env python3
"""
Test script to verify Playwright integration with Judo Framework
Run this script to test the integration without running full feature files
"""

import os
import sys

def test_playwright_availability():
    """Test if Playwright integration is available"""
    print("🧪 Testing Playwright Integration Availability...")
    
    try:
        from judo import PLAYWRIGHT_AVAILABLE
        print(f"   Playwright Available: {PLAYWRIGHT_AVAILABLE}")
        
        if PLAYWRIGHT_AVAILABLE:
            from judo.playwright.browser_context import JudoBrowserContext
            from judo.playwright.page_manager import PageManager
            print("   ✅ Playwright integration classes imported successfully")
            return True
        else:
            print("   ❌ Playwright not available")
            return False
            
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False


def test_browser_context_creation():
    """Test creating a JudoBrowserContext"""
    print("\n🧪 Testing JudoBrowserContext Creation...")
    
    try:
        from judo.playwright.browser_context import JudoBrowserContext
        
        # Create context
        context = JudoBrowserContext()
        print("   ✅ JudoBrowserContext created successfully")
        
        # Test basic properties
        assert hasattr(context, 'start_browser'), "Missing start_browser method"
        assert hasattr(context, 'navigate_to'), "Missing navigate_to method"
        assert hasattr(context, 'click_element'), "Missing click_element method"
        print("   ✅ Required methods available")
        
        # Test variable system compatibility
        context.set_variable('test_var', 'test_value')
        assert context.get_variable('test_var') == 'test_value', "Variable system not working"
        print("   ✅ Variable system compatible")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_step_imports():
    """Test importing Playwright steps"""
    print("\n🧪 Testing Step Imports...")
    
    try:
        # Test English steps
        from judo.playwright import steps
        print("   ✅ English steps imported")
        
        # Test Spanish steps
        from judo.playwright import steps_es
        print("   ✅ Spanish steps imported")
        
        # Test hooks
        from judo.playwright.hooks import integrate_playwright_hooks
        print("   ✅ Hooks imported")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error importing steps: {e}")
        return False


def test_browser_startup():
    """Test actual browser startup (if Playwright is installed)"""
    print("\n🧪 Testing Browser Startup...")
    
    try:
        from judo.playwright.browser_context import JudoBrowserContext
        from judo.playwright import check_playwright_availability
        
        # Check if browsers are installed
        check_playwright_availability()
        print("   ✅ Playwright browsers are installed")
        
        # Create context and start browser
        context = JudoBrowserContext()
        context.start_browser(headless=True)  # Use headless for testing
        print("   ✅ Browser started successfully")
        
        # Create a page
        page = context.new_page()
        print("   ✅ Page created successfully")
        
        # Navigate to a simple page
        context.navigate_to("data:text/html,<html><body><h1>Test Page</h1></body></html>")
        print("   ✅ Navigation successful")
        
        # Test element interaction
        title = context.get_element_text("h1")
        assert "Test Page" in title, f"Expected 'Test Page', got '{title}'"
        print("   ✅ Element interaction working")
        
        # Clean up
        context.close_browser()
        print("   ✅ Browser closed successfully")
        
        return True
        
    except ImportError:
        print("   ⚠️ Playwright not installed - skipping browser test")
        return True  # Not a failure, just not installed
    except Exception as e:
        print(f"   ❌ Browser test failed: {e}")
        return False


def test_hybrid_functionality():
    """Test hybrid API + UI functionality"""
    print("\n🧪 Testing Hybrid API + UI Functionality...")
    
    try:
        from judo.playwright.browser_context import JudoBrowserContext
        
        # Create browser context
        context = JudoBrowserContext()
        
        # Test API functionality (inherited from JudoContext)
        context.set_base_url("https://httpbin.org")
        print("   ✅ API base URL set")
        
        # Test variable sharing
        context.set_variable("test_data", "shared_value")
        assert context.get_variable("test_data") == "shared_value"
        print("   ✅ Variable sharing works")
        
        # Test string interpolation
        interpolated = context.interpolate_string("Hello {test_data}")
        assert interpolated == "Hello shared_value"
        print("   ✅ String interpolation works")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Hybrid functionality test failed: {e}")
        return False


def test_configuration():
    """Test configuration system"""
    print("\n🧪 Testing Configuration System...")
    
    try:
        from judo.playwright.hooks import configure_playwright_from_env
        
        # Test configuration loading
        config = configure_playwright_from_env()
        print("   ✅ Configuration loaded from environment")
        
        # Test default values
        assert 'use_browser' in config
        assert 'browser_type' in config
        assert 'headless' in config
        print("   ✅ Default configuration values present")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🎭 Judo Framework - Playwright Integration Test Suite")
    print("=" * 60)
    
    tests = [
        test_playwright_availability,
        test_browser_context_creation,
        test_step_imports,
        test_hybrid_functionality,
        test_configuration,
        test_browser_startup,  # This one last as it requires full Playwright setup
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   💥 Test crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Playwright integration is working correctly.")
        
        print("\n🚀 Next Steps:")
        print("1. Set environment variables:")
        print("   export JUDO_USE_BROWSER=true")
        print("   export JUDO_HEADLESS=false")
        print("2. Run example features:")
        print("   behave examples/playwright_integration.feature")
        print("3. Check the documentation:")
        print("   cat examples/README_playwright.md")
        
        return 0
    else:
        print("❌ Some tests failed. Check the output above for details.")
        
        print("\n🔧 Troubleshooting:")
        print("1. Install Playwright support:")
        print("   pip install 'judo-framework[browser]'")
        print("2. Install browsers:")
        print("   playwright install")
        print("3. Check Python version (requires 3.8+)")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())