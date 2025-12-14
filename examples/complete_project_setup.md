# 🥋 Complete Project Setup Guide

This guide shows a **real production setup** for Judo Framework with API and UI testing, based on actual implementations.

## 📁 Project Structure

```
my-judo-project/
├── features/
│   ├── api/
│   │   ├── users.feature
│   │   ├── products.feature
│   │   └── orders.feature
│   ├── ui/
│   │   ├── login.feature
│   │   ├── dashboard.feature
│   │   └── checkout.feature
│   ├── mixed/
│   │   └── e2e_flow.feature
│   ├── environment.py              # ⭐ Main configuration
│   └── steps/
│       └── custom_steps.py         # Optional custom steps
├── Runner/
│   ├── runner.py                   # Custom runner
│   └── judo_reports/               # Generated reports (gitignored)
│       ├── test_execution_report.html
│       ├── screenshots/
│       ├── api_logs/
│       └── cucumber-json/
├── test_data/
│   ├── users/
│   │   ├── create_user.json
│   │   └── update_user.json
│   ├── products/
│   │   └── product_data.json
│   └── schemas/
│       ├── user_schema.json
│       └── product_schema.json
├── .env                            # Environment variables
├── .env.example                    # Template for .env
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔧 Configuration Files

### 1. environment.py (Complete Setup)

```python
"""
Environment setup for Judo Framework with Playwright
Includes automatic screenshot integration in HTML reports
"""

from judo.behave import *
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

PLAYWRIGHT_ENABLED = False

try:
    from judo.playwright import PLAYWRIGHT_AVAILABLE
    from judo.playwright.browser_context import JudoBrowserContext
    
    if PLAYWRIGHT_AVAILABLE and os.getenv('JUDO_USE_BROWSER', 'false').lower() == 'true':
        PLAYWRIGHT_ENABLED = True
except ImportError:
    PLAYWRIGHT_ENABLED = False

def before_all(context):
    """Initialize Judo Framework"""
    before_all_judo(context)
    print("🥋 Judo Framework initialized")

def before_scenario(context, scenario):
    """Setup before each scenario"""
    before_scenario_judo(context, scenario)
    
    # Initialize Playwright for UI tests (tagged with @test-front or @front)
    if PLAYWRIGHT_ENABLED and any(tag in scenario.tags for tag in ['test-front', 'front', 'ui']):
        try:
            from playwright.sync_api import sync_playwright
            from judo.playwright.browser_context import JudoBrowserContext
            
            if not hasattr(context.judo_context, 'page'):
                # Save old context
                old_context = context.judo_context
                
                # Create browser context
                context.judo_context = JudoBrowserContext(context)
                
                # Copy variables from old context
                if hasattr(old_context, 'variables'):
                    context.judo_context.variables = old_context.variables
                if hasattr(old_context, 'base_url'):
                    context.judo_context.base_url = old_context.base_url
                
                # Start Playwright
                if not hasattr(context.judo_context, 'playwright') or not context.judo_context.playwright:
                    context.judo_context.playwright = sync_playwright().start()
                
                # Browser configuration (full screen)
                browser_options = {
                    'headless': os.getenv('JUDO_HEADLESS', 'false').lower() == 'true',
                    'args': ['--start-maximized']
                }
                
                context.judo_context.browser = context.judo_context.playwright.chromium.launch(**browser_options)
                
                # Create context without viewport (full screen)
                context.judo_context.browser_context = context.judo_context.browser.new_context(
                    no_viewport=True
                )
                
                # Create page
                context.judo_context.page = context.judo_context.browser_context.new_page()
                print("✅ Playwright configured in full screen mode")
                
        except ImportError:
            raise Exception("❌ Playwright not installed. Run: pip install playwright && playwright install chromium")
        except Exception as e:
            print(f"❌ Error configuring Playwright: {e}")
            raise

def after_step(context, step):
    """Take screenshot after EVERY step (pass or fail)"""
    
    # 📸 Screenshot ALWAYS (if Playwright is active)
    if hasattr(context.judo_context, 'page') and context.judo_context.page:
        try:
            # Clean step name for filename
            step_name_clean = step.name.replace(' ', '_').replace('"', '').replace("'", '')
            screenshot_name = f"{step.status}_{step_name_clean}"
            
            screenshot_path = context.judo_context.take_screenshot(screenshot_name)
            print(f"📸 Screenshot saved: {screenshot_path}")
            
            # ✅ Attach to HTML report
            try:
                from judo.reporting.reporter import get_reporter
                reporter = get_reporter()
                if reporter and reporter.current_step:
                    reporter.attach_screenshot(screenshot_path)
                    print(f"✅ Screenshot attached to HTML report")
            except Exception as e:
                print(f"⚠️ Could not attach screenshot to report: {e}")
                
        except Exception as e:
            print(f"⚠️ Could not take screenshot: {e}")
    
    # Additional debug on failures
    if step.status == 'failed':
        print(f"❌ Step failed: {step.name}")
        if hasattr(step, 'exception'):
            print(f"   Error: {step.exception}")
    
    after_step_judo(context, step)

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    # Close page at end of scenario
    if hasattr(context.judo_context, 'page') and context.judo_context.page:
        try:
            context.judo_context.page.close()
            context.judo_context.page = None
            print("✅ Page closed at end of scenario")
        except Exception as e:
            print(f"⚠️ Error closing page: {e}")
    
    # Call Judo hook
    after_scenario_judo(context, scenario)

def after_all(context):
    """Cleanup after all tests"""
    if hasattr(context.judo_context, 'browser') and context.judo_context.browser:
        try:
            if hasattr(context.judo_context, 'browser_context') and context.judo_context.browser_context:
                context.judo_context.browser_context.close()
            context.judo_context.browser.close()
            if hasattr(context.judo_context, 'playwright') and context.judo_context.playwright:
                context.judo_context.playwright.stop()
            print("✅ Playwright resources cleaned up")
        except Exception as e:
            print(f"⚠️ Error cleaning up Playwright: {e}")
    
    after_all_judo(context)

# Judo Framework hooks
before_feature = before_feature_judo
after_feature = after_feature_judo
before_step = before_step_judo
```

### 2. .env (Environment Variables)

```bash
# ============================================
# API CONFIGURATION
# ============================================
API_BASE_URL=https://api.example.com
API_TOKEN=Bearer your-token-here
TIMEOUT_SECONDS=30
VERIFY_SSL=true

# ============================================
# PLAYWRIGHT CONFIGURATION
# ============================================
JUDO_USE_BROWSER=true
JUDO_BROWSER=chromium
JUDO_HEADLESS=false
JUDO_VIEWPORT_WIDTH=1920
JUDO_VIEWPORT_HEIGHT=1080

# ============================================
# SCREENSHOT CONFIGURATION
# ============================================
JUDO_SCREENSHOT_DIR=screenshots
JUDO_SCREENSHOT_ON_STEP_FAILURE=true

# ============================================
# DEBUG CONFIGURATION
# ============================================
JUDO_DEBUG_REPORTER=false
JUDO_LOG_LEVEL=INFO
```

### 3. Runner/runner.py (Custom Runner)

```python
#!/usr/bin/env python3
"""
🥋 Judo Framework - Custom Runner
Optimized configuration for API + UI testing with screenshots
"""

from judo.runner.base_runner import BaseRunner
import os
import sys
from pathlib import Path

# Debug configuration
os.environ['JUDO_DEBUG_REPORTER'] = 'false'

class MyRunner(BaseRunner):
    """
    Custom runner extending BaseRunner
    Configured for optimal test execution and reporting
    """
    
    basedir = "./judo_reports"
    
    def __init__(self):
        """Initialize runner with custom configuration"""
        super().__init__(
            # ============================================
            # DIRECTORY CONFIGURATION
            # ============================================
            features_dir="../features",
            output_dir=self.basedir,
            
            # ============================================
            # REPORT CONFIGURATION
            # ============================================
            generate_cucumber_json=True,
            cucumber_json_dir=f"{self.basedir}/cucumber-json",
            
            # ============================================
            # EXECUTION CONFIGURATION
            # ============================================
            parallel=False,
            max_workers=2,
            
            # ============================================
            # API LOGGING CONFIGURATION
            # ============================================
            save_requests_responses=True,
            requests_responses_dir=f"{self.basedir}/api_logs"
        )
    
    def run_smoke_tests(self):
        """Run smoke tests"""
        return self.run(tags=["@smoke"])
    
    def run_api_tests(self):
        """Run only API tests"""
        return self.run(tags=["@api"])
    
    def run_ui_tests(self):
        """Run only UI tests"""
        return self.run(tags=["@test-front"])
    
    def run_all_tests(self):
        """Run all tests"""
        return self.run()

if __name__ == "__main__":
    print("🥋 JUDO FRAMEWORK - TEST EXECUTION")
    print("=" * 50)
    
    runner = MyRunner()
    
    # Run tests based on command line argument
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        if test_type == "smoke":
            results = runner.run_smoke_tests()
        elif test_type == "api":
            results = runner.run_api_tests()
        elif test_type == "ui":
            results = runner.run_ui_tests()
        else:
            results = runner.run_all_tests()
    else:
        results = runner.run_all_tests()
    
    # Print results
    print("\n" + "=" * 50)
    print(f"✅ Tests completed: {results['passed']}/{results['total']} passed")
    print(f"📊 Success rate: {(results['passed']/results['total']*100):.1f}%")
    print("=" * 50)
```

### 4. requirements.txt

```txt
# Judo Framework (includes behave, requests, jsonpath-ng automatically)
judo-framework>=1.3.39

# Environment variables
python-dotenv>=1.0.0

# Playwright for browser testing
playwright>=1.40.0

# Optional: Terminal colors
colorama>=0.4.6

# Optional: Better JSON handling
jsonschema>=4.17.0
```

### 5. .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Judo Reports
Runner/judo_reports/
judo_reports/
screenshots/
api_logs/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## 📝 Example Feature Files

### API Test (features/api/users.feature)

```gherkin
@api
Feature: User Management API

  Background:
    Given the base URL is "{API_BASE_URL}"
    And I use bearer token "{API_TOKEN}"

  @smoke
  Scenario: Create and retrieve user
    When I send a POST request to "/users" with JSON:
      """
      {
        "name": "John Doe",
        "email": "john@example.com",
        "role": "admin"
      }
      """
    Then the response status should be 201
    And I extract "$.id" from the response as "userId"
    
    When I send a GET request to "/users/{userId}"
    Then the response status should be 200
    And the response field "name" should equal "John Doe"
```

### UI Test (features/ui/login.feature)

```gherkin
@test-front @ui
Feature: Login Page

  @smoke
  Scenario: Successful login with screenshots
    Given I navigate to "https://app.example.com/login"
    When I fill "#username" with "admin"
    And I fill "#password" with "secret123"
    And I click "#login-button"
    Then I should see "Dashboard"
    # Screenshots automatically captured after each step
```

### Mixed Test (features/mixed/e2e_flow.feature)

```gherkin
@mix
Feature: End-to-End E-commerce Flow

  Scenario: Create product via API and purchase via UI
    # API: Create product
    Given the base URL is "{API_BASE_URL}"
    And I use bearer token "{API_TOKEN}"
    When I send a POST request to "/products" with JSON:
      """
      {
        "name": "Laptop Pro",
        "price": 1299.99,
        "stock": 10
      }
      """
    Then the response status should be 201
    And I extract "$.id" from the response as "productId"
    
    # UI: Purchase product
    Given I navigate to "https://shop.example.com/products/{productId}"
    Then I should see "Laptop Pro"
    And I should see "$1,299.99"
    When I click "#add-to-cart"
    Then I should see "Added to cart"
    When I click "#checkout"
    Then I should see "Checkout"
```

## 🚀 Running Tests

```bash
# Navigate to Runner directory
cd Runner

# Run all tests
python runner.py

# Run specific test types
python runner.py smoke    # Smoke tests only
python runner.py api      # API tests only
python runner.py ui       # UI tests only

# Or use behave directly
cd ..
behave features/ --tags=@smoke
behave features/ --tags=@api
behave features/ --tags=@test-front
```

## 📊 View Reports

After running tests:

1. **HTML Report**: `Runner/judo_reports/test_execution_report.html`
   - Complete test results
   - Screenshots embedded
   - Request/Response details
   - Statistics and metrics

2. **Screenshots**: `Runner/judo_reports/screenshots/`
   - All captured screenshots
   - Named by step and status

3. **API Logs**: `Runner/judo_reports/api_logs/`
   - Complete request/response logs
   - Organized by scenario

4. **JSON Reports**: `Runner/judo_reports/cucumber-json/`
   - For CI/CD integration

## 🎯 Best Practices

1. **Tag Organization**:
   - `@api` - API tests
   - `@test-front` or `@ui` - UI tests
   - `@smoke` - Critical tests
   - `@mix` - Hybrid tests

2. **Screenshot Strategy**:
   - Automatic on every step (configured in environment.py)
   - Manual when needed: `context.judo_context.take_screenshot("name")`

3. **Environment Variables**:
   - Use `.env` for local development
   - Use CI/CD secrets for production
   - Never commit `.env` to git

4. **Test Data**:
   - Store in `test_data/` directory
   - Use JSON files for complex data
   - Use schemas for validation

5. **Custom Steps**:
   - Add to `features/steps/custom_steps.py`
   - Keep them reusable and well-documented

## 🔍 Debugging

Enable debug mode:

```python
# In environment.py or runner.py
os.environ['JUDO_DEBUG_REPORTER'] = 'true'
os.environ['JUDO_LOG_LEVEL'] = 'DEBUG'
```

Check installation:

```bash
python -c "import judo; print(judo.__version__)"
python -c "from judo.playwright import PLAYWRIGHT_AVAILABLE; print(PLAYWRIGHT_AVAILABLE)"
```

## 📚 Additional Resources

- **Judo Framework Docs**: http://centyc.cl/judo-framework/
- **Behave Docs**: https://behave.readthedocs.io/
- **Playwright Docs**: https://playwright.dev/python/

---

**This setup is production-ready and battle-tested!** 🥋
