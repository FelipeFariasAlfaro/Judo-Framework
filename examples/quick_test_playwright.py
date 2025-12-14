#!/usr/bin/env python3
"""
Quick Test Script - Playwright Integration
Test the integration without modifying your existing setup
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path

def create_test_files():
    """Create temporary test files"""
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp(prefix="judo_playwright_test_"))
    
    # Create features directory
    features_dir = temp_dir / "features"
    features_dir.mkdir()
    
    # Create environment.py (same as user's current setup)
    env_content = '''"""
Test environment - same as user's current setup
"""
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from judo.behave import *

before_all = before_all_judo
before_feature = before_feature_judo
after_feature = after_feature_judo
before_scenario = before_scenario_judo
after_scenario = after_scenario_judo
before_step = before_step_judo
after_step = after_step_judo
after_all = after_all_judo
'''
    
    with open(features_dir / "environment.py", "w") as f:
        f.write(env_content)
    
    # Create API test (should work with current setup)
    api_test = '''Feature: API Test (Current Setup)

  @api
  Scenario: Variable management test
    Given I have a Judo API client
    When I set the variable "testVar" to "testValue"
    Then I should have variable "testVar" with value "testValue"
    
  @api
  Scenario: Multiple variables test
    Given I have a Judo API client
    When I set the variable "name" to "John"
    And I set the variable "age" to "25"
    Then I should have variable "name" with value "John"
    And I should have variable "age" with value "25"
'''
    
    with open(features_dir / "api_test.feature", "w") as f:
        f.write(api_test)
    
    # Create UI test (only works if Playwright is enabled)
    ui_test = '''Feature: UI Test (Playwright Integration)

  @ui
  Scenario: Simple browser test
    Given I start a browser
    When I navigate to "data:text/html,<html><body><h1>Test Page</h1><p id='message'>Hello World</p></body></html>"
    Then the element "h1" should be visible
    And the element "h1" should contain "Test Page"
    And the element "#message" should contain "Hello World"
    And I take a screenshot named "simple_test"
    And I close the browser
'''
    
    with open(features_dir / "ui_test.feature", "w") as f:
        f.write(ui_test)
    
    # Create .env file for Playwright
    env_file_content = '''# Playwright configuration for testing
JUDO_USE_BROWSER=true
JUDO_BROWSER=chromium
JUDO_HEADLESS=true
JUDO_SCREENSHOTS=true
JUDO_SCREENSHOT_ON_FAILURE=true
JUDO_SCREENSHOT_DIR=test_screenshots
JUDO_OUTPUT_DIRECTORY=test_reports
'''
    
    with open(temp_dir / ".env", "w") as f:
        f.write(env_file_content)
    
    # Create steps directory
    steps_dir = features_dir / "steps"
    steps_dir.mkdir()
    with open(steps_dir / "__init__.py", "w") as f:
        f.write("# Steps directory")
    
    return temp_dir

def run_test(test_dir, test_type="api"):
    """Run a specific test"""
    print(f"\n🧪 Running {test_type.upper()} test...")
    
    # Change to test directory
    original_dir = os.getcwd()
    os.chdir(test_dir)
    
    try:
        if test_type == "api":
            cmd = ["behave", "features/api_test.feature", "--no-capture", "--format=pretty"]
        elif test_type == "ui":
            cmd = ["behave", "features/ui_test.feature", "--no-capture", "--format=pretty"]
        else:
            cmd = ["behave", "--no-capture", "--format=pretty"]
        
        print(f"   Command: {' '.join(cmd)}")
        print(f"   Directory: {test_dir}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"   ✅ {test_type.upper()} test PASSED")
            # Show last few lines of output
            lines = result.stdout.strip().split('\n')
            for line in lines[-5:]:
                if line.strip():
                    print(f"   📄 {line}")
            return True
        else:
            print(f"   ❌ {test_type.upper()} test FAILED")
            print(f"   Error: {result.stderr.strip()}")
            # Show relevant output
            lines = result.stdout.strip().split('\n')
            for line in lines[-10:]:
                if line.strip() and ('failed' in line.lower() or 'error' in line.lower() or 'passed' in line.lower()):
                    print(f"   📄 {line}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏰ {test_type.upper()} test TIMEOUT")
        return False
    except Exception as e:
        print(f"   💥 {test_type.upper()} test ERROR: {e}")
        return False
    finally:
        os.chdir(original_dir)

def check_playwright_installation():
    """Check if Playwright is properly installed"""
    print("🔍 Checking Playwright installation...")
    
    try:
        # Check if judo can import Playwright
        import sys
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        
        from judo import PLAYWRIGHT_AVAILABLE
        print(f"   Judo Playwright integration: {'✅ Available' if PLAYWRIGHT_AVAILABLE else '❌ Not available'}")
        
        if PLAYWRIGHT_AVAILABLE:
            # Check if browsers are installed
            try:
                import playwright
                from playwright.sync_api import sync_playwright
                
                with sync_playwright() as p:
                    browsers = []
                    try:
                        p.chromium.launch(headless=True).close()
                        browsers.append("chromium")
                    except:
                        pass
                    
                    if browsers:
                        print(f"   Browsers installed: ✅ {', '.join(browsers)}")
                        return True
                    else:
                        print(f"   Browsers installed: ❌ None (run 'playwright install')")
                        return False
                        
            except Exception as e:
                print(f"   Browser check failed: ❌ {e}")
                return False
        else:
            print(f"   Install with: pip install 'judo-framework[browser]'")
            return False
            
    except Exception as e:
        print(f"   Import check failed: ❌ {e}")
        return False

def main():
    """Main test function"""
    print("🎭 Judo Framework - Playwright Integration Quick Test")
    print("=" * 60)
    
    # Check current setup
    print("📋 Checking current setup...")
    
    # Check if we can import judo
    try:
        import sys
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        
        import judo
        print(f"   Judo Framework: ✅ Version {judo.__version__}")
    except ImportError as e:
        print(f"   Judo Framework: ❌ Not found ({e})")
        print("   Make sure you're running this from the project root")
        return 1
    
    # Check Playwright
    playwright_available = check_playwright_installation()
    
    # Create test files
    print("\n📁 Creating test files...")
    test_dir = create_test_files()
    print(f"   Test directory: {test_dir}")
    
    # Run tests
    results = []
    
    # Test 1: API test (should always work)
    print("\n" + "=" * 60)
    print("TEST 1: API Testing (Current Setup)")
    print("This should work with your current environment.py")
    print("-" * 60)
    
    api_result = run_test(test_dir, "api")
    results.append(("API Test (Current Setup)", api_result))
    
    # Test 2: UI test (only if Playwright is available)
    print("\n" + "=" * 60)
    print("TEST 2: UI Testing (Playwright Integration)")
    if playwright_available:
        print("Playwright is available - testing UI functionality")
    else:
        print("Playwright not available - skipping UI test")
    print("-" * 60)
    
    if playwright_available:
        ui_result = run_test(test_dir, "ui")
        results.append(("UI Test (Playwright)", ui_result))
    else:
        results.append(("UI Test (Playwright)", "Skipped - Playwright not installed"))
    
    # Check generated files
    print("\n📊 Checking generated files...")
    
    reports_dir = test_dir / "test_reports"
    if reports_dir.exists():
        reports = list(reports_dir.glob("*.html"))
        print(f"   HTML Reports: ✅ {len(reports)} generated")
        for report in reports:
            print(f"      - {report.name}")
    else:
        print(f"   HTML Reports: ❌ None found")
    
    screenshots_dir = test_dir / "test_screenshots"
    if screenshots_dir.exists():
        screenshots = list(screenshots_dir.glob("*.png"))
        print(f"   Screenshots: ✅ {len(screenshots)} generated")
        for screenshot in screenshots[:3]:  # Show first 3
            print(f"      - {screenshot.name}")
        if len(screenshots) > 3:
            print(f"      ... and {len(screenshots) - 3} more")
    else:
        print(f"   Screenshots: ❌ None found")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_name, result in results:
        if result is True:
            status = "✅ PASSED"
            passed += 1
        elif result is False:
            status = "❌ FAILED"
            failed += 1
        else:
            status = f"⏭️ SKIPPED ({result})"
            skipped += 1
        
        print(f"{test_name:30} {status}")
    
    print(f"\nResults: {passed} passed, {failed} failed, {skipped} skipped")
    
    # Recommendations
    print("\n🎯 RECOMMENDATIONS")
    print("-" * 30)
    
    if failed == 0 and passed > 0:
        print("✅ Integration is working correctly!")
        
        if playwright_available:
            print("\n🚀 You're ready to use Playwright integration:")
            print("   1. Your current environment.py works without changes")
            print("   2. Add JUDO_USE_BROWSER=true to enable UI testing")
            print("   3. Use @ui tags for browser tests")
            print("   4. Use @hybrid tags for API + UI tests")
        else:
            print("\n🎭 To enable Playwright integration:")
            print("   1. Install: pip install 'judo-framework[browser]'")
            print("   2. Install browsers: playwright install")
            print("   3. Add JUDO_USE_BROWSER=true to .env")
            print("   4. Your current environment.py will work without changes")
    else:
        print("❌ Some tests failed. Check the output above for details.")
        
        if not playwright_available:
            print("\n🔧 To fix Playwright issues:")
            print("   1. Install: pip install 'judo-framework[browser]'")
            print("   2. Install browsers: playwright install")
        
        print("\n🔧 To fix API issues:")
        print("   1. Check that judo framework is properly installed")
        print("   2. Verify Python path and imports")
    
    print(f"\n📁 Test files created in: {test_dir}")
    print("   You can examine the generated reports and screenshots")
    
    # Cleanup option
    import time
    print(f"\n🗑️ Test files will be kept for inspection.")
    print(f"   Delete manually when done: rm -rf {test_dir}")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)