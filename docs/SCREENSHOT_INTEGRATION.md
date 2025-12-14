# 📸 Screenshot Integration in HTML Reports

> **Version**: 1.3.39+  
> **Status**: Production Ready  
> **Compatibility**: 100% backward compatible

## Overview

Judo Framework automatically embeds Playwright screenshots into HTML reports, providing visual evidence of test execution and failures. Screenshots are base64-encoded and embedded directly in the HTML, creating self-contained reports with no external dependencies.

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📸 **Automatic Embedding** | Screenshots base64-encoded in HTML (no external files) |
| 🖼️ **Fullscreen View** | Click any screenshot to view fullscreen |
| 🎯 **Step-Level Precision** | Screenshots attach to specific steps |
| ❌ **Failure Capture** | Automatic screenshots on test failures |
| 🎮 **Manual Control** | Take screenshots programmatically anytime |
| 🔄 **Zero Configuration** | Works out of the box with default settings |
| 📦 **Self-Contained** | Single HTML file with everything embedded |
| 🎨 **Professional Display** | Clean UI with hover effects and metadata |  

## Configuration

### Environment Variables

```bash
# Enable screenshots on step failure (default: true)
JUDO_SCREENSHOT_ON_STEP_FAILURE=true

# Enable screenshots after every step (default: false)
JUDO_SCREENSHOT_AFTER_STEP=false

# Enable screenshots before every step (default: false)
JUDO_SCREENSHOT_BEFORE_STEP=false

# Screenshot directory (default: judo_screenshots)
JUDO_SCREENSHOT_DIR=judo_screenshots
```

### In environment.py

```python
import os
from judo.playwright.hooks import *

# Configure screenshot behavior
os.environ['JUDO_SCREENSHOT_ON_STEP_FAILURE'] = 'true'
os.environ['JUDO_SCREENSHOT_AFTER_STEP'] = 'false'

def before_all(context):
    before_all_playwright(context)

def before_scenario(context, scenario):
    before_scenario_playwright(context, scenario)

def after_step(context, step):
    after_step_playwright(context, step)

def after_scenario(context, scenario):
    after_scenario_playwright(context, scenario)

def after_all(context):
    after_all_playwright(context)
```

## Usage Examples

### 1. Automatic Screenshots on Failure

Screenshots are automatically taken when a step fails:

```gherkin
Feature: Login Test
  Scenario: Failed login shows error
    Given I navigate to "https://example.com/login"
    When I fill "username" with "invalid@user.com"
    And I fill "password" with "wrongpassword"
    And I click "Login"
    Then I should see "Invalid credentials"  # If this fails, screenshot is taken
```

The failure screenshot will automatically appear in the HTML report under the failed step.

### 2. Manual Screenshots in Steps

Take screenshots programmatically in your step definitions:

```python
from behave import given, when, then

@when('I take a screenshot of the dashboard')
def step_impl(context):
    # Take screenshot and automatically attach to report
    context.judo_context.take_screenshot("dashboard_view")

@then('I verify the page layout')
def step_impl(context):
    # Take screenshot before verification
    context.judo_context.take_screenshot("before_verification")
    
    # Your verification logic here
    assert context.judo_context.page.locator(".header").is_visible()
    
    # Take another screenshot after verification
    context.judo_context.take_screenshot("after_verification")
```

### 3. Element Screenshots

Capture specific elements:

```python
@when('I capture the error message')
def step_impl(context):
    # This will take a screenshot of just the error element
    context.judo_context.take_element_screenshot(
        ".error-message", 
        name="error_detail"
    )
```

### 4. Screenshot Without Report Attachment

If you want to take a screenshot but NOT attach it to the report:

```python
@when('I take a debug screenshot')
def step_impl(context):
    # attach_to_report=False prevents automatic attachment
    context.judo_context.take_screenshot(
        "debug_screenshot",
        attach_to_report=False
    )
```

### 5. Screenshots in Feature Files

Use Gherkin steps directly:

```gherkin
Feature: Visual Testing
  Scenario: Capture page states
    Given I navigate to "https://example.com"
    When I take a screenshot named "homepage"
    And I click "Products"
    And I take a screenshot named "products_page"
    Then I should see "Product Catalog"
```

## HTML Report Display

### Screenshot Section

Screenshots appear in the HTML report as a dedicated section within each step:

```
📸 Screenshot
┌─────────────────────────────┐
│                             │
│     [Screenshot Image]      │
│                             │
└─────────────────────────────┘
  screenshot_name.png
  Click to view fullscreen
```

### Features

- **Hover Effect**: Screenshots scale slightly on hover
- **Click to Expand**: Click any screenshot to view fullscreen
- **Filename Display**: Shows the screenshot filename below the image
- **Responsive**: Screenshots scale to fit the report width
- **High Quality**: Full resolution preserved in base64 encoding

## Best Practices

### 1. Strategic Screenshot Placement

```python
# ✅ GOOD: Take screenshots at key moments
@when('I complete the checkout process')
def step_impl(context):
    context.judo_context.fill("#card-number", "4111111111111111")
    context.judo_context.take_screenshot("payment_info_entered")
    
    context.judo_context.click("#submit-payment")
    context.judo_context.wait_for_selector(".success-message")
    context.judo_context.take_screenshot("payment_success")

# ❌ BAD: Too many screenshots
@when('I type my name')
def step_impl(context):
    context.judo_context.take_screenshot("before_typing")
    context.judo_context.fill("#name", "John")
    context.judo_context.take_screenshot("after_typing")  # Unnecessary
```

### 2. Descriptive Names

```python
# ✅ GOOD: Clear, descriptive names
context.judo_context.take_screenshot("login_page_loaded")
context.judo_context.take_screenshot("error_message_displayed")
context.judo_context.take_screenshot("order_confirmation_page")

# ❌ BAD: Generic names
context.judo_context.take_screenshot("screenshot1")
context.judo_context.take_screenshot("test")
context.judo_context.take_screenshot("page")
```

### 3. Failure Investigation

```python
@then('I verify the order total is correct')
def step_impl(context):
    try:
        total = context.judo_context.get_text(".order-total")
        assert total == "$99.99", f"Expected $99.99, got {total}"
    except AssertionError:
        # Take detailed screenshot before failing
        context.judo_context.take_screenshot("order_total_mismatch")
        raise
```

### 4. Performance Considerations

```bash
# For CI/CD: Only screenshot on failure
JUDO_SCREENSHOT_ON_STEP_FAILURE=true
JUDO_SCREENSHOT_AFTER_STEP=false

# For local debugging: Screenshot everything
JUDO_SCREENSHOT_ON_STEP_FAILURE=true
JUDO_SCREENSHOT_AFTER_STEP=true
```

## Troubleshooting

### Screenshots Not Appearing in Report

**Problem**: Screenshots are taken but don't appear in HTML report

**Solutions**:

1. **Check Playwright hooks are enabled**:
```python
# environment.py
from judo.playwright.hooks import after_step_playwright

def after_step(context, step):
    after_step_playwright(context, step)  # Required!
```

2. **Verify screenshot path is valid**:
```python
# Check screenshot was actually taken
screenshot_path = context.judo_context.take_screenshot("test")
print(f"Screenshot saved to: {screenshot_path}")
```

3. **Ensure reporter is active**:
```python
# In your runner
from judo.runner.base_runner import BaseRunner

runner = BaseRunner(
    features_dir="features",
    output_dir="judo_reports",
    generate_cucumber_json=True  # Enables reporter
)
```

### Screenshot File Not Found

**Problem**: HTML report shows "Screenshot file not found"

**Solutions**:

1. **Use absolute paths or relative to report directory**
2. **Ensure screenshot directory exists before taking screenshots**
3. **Check file permissions**

### Large HTML Files

**Problem**: HTML reports are very large due to screenshots

**Solutions**:

1. **Reduce screenshot frequency**:
```bash
JUDO_SCREENSHOT_AFTER_STEP=false  # Only on failures
```

2. **Use element screenshots instead of full page**:
```python
# Smaller file size
context.judo_context.take_element_screenshot(".main-content", "content")
```

3. **Compress screenshots** (future feature)

## Technical Details

### Implementation

1. **Screenshot Capture**: Playwright's `page.screenshot()` saves PNG to disk
2. **Path Storage**: Screenshot path stored in `StepReport.screenshot_path`
3. **Report Generation**: HTML reporter reads screenshot file
4. **Base64 Encoding**: Image converted to base64 data URL
5. **HTML Embedding**: Image embedded as `<img src="data:image/png;base64,..."/>`

### Data Flow

```
Step Execution
    ↓
take_screenshot()
    ↓
Save PNG to disk
    ↓
reporter.attach_screenshot(path)
    ↓
StepReport.screenshot_path = path
    ↓
HTML Report Generation
    ↓
Read PNG file
    ↓
Convert to base64
    ↓
Embed in HTML
```

### File Structure

```
judo_reports/
├── test_execution_report.html    # Contains embedded screenshots
└── judo_screenshots/              # Original PNG files
    ├── login_page_loaded.png
    ├── step_failure_verify_total.png
    └── payment_success.png
```

## API Reference

### JudoBrowserContext.take_screenshot()

```python
def take_screenshot(
    self, 
    name: str = None, 
    attach_to_report: bool = True, 
    **options
) -> str:
    """
    Take a screenshot and optionally attach to HTML report
    
    Args:
        name: Screenshot name (auto-generated if None)
        attach_to_report: If True, attach to current step in report
        **options: Playwright screenshot options (full_page, etc.)
    
    Returns:
        str: Path to screenshot file
    """
```

### JudoReporter.attach_screenshot()

```python
def attach_screenshot(self, screenshot_path: str):
    """
    Attach screenshot to current step
    
    Args:
        screenshot_path: Path to screenshot file
    """
```

## Examples

See complete examples in:
- `examples/playwright_integration.feature`
- `examples/environment_playwright.py`
- `examples/quick_test_playwright.py`

## Support

For issues or questions:
- GitHub: https://github.com/FelipeFariasAlfaro/Judo-Framework
- Email: felipe.farias@centyc.cl
- Documentation: http://centyc.cl/judo-framework/
