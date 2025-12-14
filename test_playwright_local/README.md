# Playwright Integration Test Suite

This directory contains comprehensive tests for the Playwright integration with Judo Framework.

## 🎯 Purpose

Test the complete Playwright integration to ensure:
- ✅ Backward compatibility with existing API tests
- ✅ New UI testing capabilities work correctly
- ✅ Hybrid API + UI scenarios function properly
- ✅ Bilingual support (English + Spanish) works
- ✅ Reporting integration captures both API and UI data
- ✅ Screenshots and visual testing work
- ✅ Multi-page management functions correctly

## 📁 Test Structure

```
test_playwright_local/
├── features/
│   ├── environment.py              # Test environment setup
│   ├── test_api_only.feature       # API-only tests (backward compatibility)
│   ├── test_ui_only.feature        # UI-only tests (Playwright features)
│   ├── test_hybrid.feature         # Hybrid API + UI tests
│   └── test_spanish.feature        # Spanish language tests
├── .env                            # Environment configuration
├── run_tests.py                    # Comprehensive test runner
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Judo Framework with browser support
pip install 'judo-framework[browser]'

# Install Playwright browsers
playwright install
```

### 2. Run All Tests

```bash
cd test_playwright_local
python run_tests.py
```

### 3. Run Specific Test Suites

```bash
# API-only tests (should always work)
behave features/test_api_only.feature

# UI-only tests (requires Playwright)
behave features/test_ui_only.feature

# Hybrid tests (requires Playwright)
behave features/test_hybrid.feature

# Spanish tests
behave features/test_spanish.feature
```

### 4. Run by Tags

```bash
# Smoke tests only
behave --tags=@smoke

# API tests only
behave --tags=@api

# UI tests only
behave --tags=@ui

# Hybrid tests only
behave --tags=@hybrid

# Spanish tests only
behave --tags=@español
```

## 🧪 Test Categories

### 1. API-Only Tests (`test_api_only.feature`)
**Purpose**: Ensure backward compatibility

- ✅ Basic GET/POST requests
- ✅ Variable extraction and usage
- ✅ Custom headers
- ✅ Bearer token authentication
- ✅ Response validation with patterns

### 2. UI-Only Tests (`test_ui_only.feature`)
**Purpose**: Test pure Playwright functionality

- ✅ Browser startup and navigation
- ✅ Form interaction (fill, click, select)
- ✅ Element validation (visibility, text, attributes)
- ✅ JavaScript execution and storage
- ✅ Multi-page management
- ✅ Advanced waiting and timing
- ✅ Screenshot testing

### 3. Hybrid Tests (`test_hybrid.feature`)
**Purpose**: Test API + UI integration

- ✅ API data used in UI forms
- ✅ UI data captured for API use
- ✅ Complex workflows with validation
- ✅ Multi-step forms with API validation

### 4. Spanish Tests (`test_spanish.feature`)
**Purpose**: Test bilingual support

- ✅ API tests in Spanish
- ✅ UI tests in Spanish
- ✅ Hybrid tests in Spanish
- ✅ JavaScript execution in Spanish
- ✅ Multi-page management in Spanish

## 🔧 Configuration

### Environment Variables (`.env`)

```bash
# Browser testing
JUDO_USE_BROWSER=true
JUDO_BROWSER=chromium
JUDO_HEADLESS=true

# Screenshots
JUDO_SCREENSHOTS=true
JUDO_SCREENSHOT_ON_FAILURE=true

# Output directories
JUDO_OUTPUT_DIRECTORY=test_reports
JUDO_SCREENSHOT_DIR=test_screenshots
```

### Test Environment (`features/environment.py`)

- Automatically detects Playwright availability
- Sets up both API and browser contexts
- Handles screenshot capture on failures
- Provides detailed logging

## 📊 Expected Outputs

### Generated Files

```
test_playwright_local/
├── test_reports/
│   ├── test_report.html            # HTML test report
│   └── scenario_name/              # Request/response logs per scenario
│       ├── 01_GET_request.json
│       └── 01_GET_response.json
└── test_screenshots/
    ├── httpbin_homepage.png
    ├── form_filled.png
    ├── form_submitted.png
    └── workflow_completed.png
```

### Console Output

The test runner provides detailed output:
- ✅ Prerequisites check
- 📋 Test suite execution
- 📸 Screenshot generation
- 📊 Report generation
- 🎯 Final summary

## 🎭 Test Scenarios

### Smoke Tests (`@smoke`)
Quick validation of core functionality:
- Basic API request
- Basic browser startup
- Simple form interaction

### API Tests (`@api`)
Comprehensive API testing:
- All HTTP methods
- Authentication
- Variable management
- Response validation

### UI Tests (`@ui`)
Complete browser automation:
- Navigation and interaction
- Form handling
- JavaScript execution
- Multi-page management
- Screenshot capture

### Hybrid Tests (`@hybrid`)
API + UI integration:
- Data flow between domains
- Complex workflows
- Validation across both domains

## 🔍 Debugging

### Enable Debug Mode

```bash
# In .env file
JUDO_DEBUG_STEPS=true
JUDO_LOG_CONSOLE=true
JUDO_SCREENSHOT_BEFORE_STEP=true
JUDO_SCREENSHOT_AFTER_STEP=true
```

### Run Individual Scenarios

```bash
# Run specific scenario
behave features/test_hybrid.feature:15  # Line number

# Run with verbose output
behave features/test_ui_only.feature --no-capture --format=pretty

# Run in headed mode (visible browser)
JUDO_HEADLESS=false behave features/test_ui_only.feature
```

## ✅ Success Criteria

The integration is considered successful if:

1. **All API tests pass** - Backward compatibility maintained
2. **UI tests pass** (if Playwright installed) - New functionality works
3. **Hybrid tests pass** - Integration between domains works
4. **Spanish tests pass** - Bilingual support works
5. **Screenshots generated** - Visual testing works
6. **Reports generated** - Reporting integration works
7. **No errors in console** - Clean execution

## 🚨 Troubleshooting

### Common Issues

1. **Playwright not installed**
   ```bash
   pip install 'judo-framework[browser]'
   playwright install
   ```

2. **Browser not found**
   ```bash
   playwright install chromium
   ```

3. **Network issues**
   - Ensure internet connectivity
   - Check if httpbin.org is accessible

4. **Permission issues**
   - Ensure write permissions for output directories
   - Check if browser can be launched

### Expected Behavior

- **Without Playwright**: Only API tests run, UI tests are skipped
- **With Playwright**: All tests run, including browser automation
- **Headless mode**: Tests run faster, no visible browser
- **Headed mode**: Browser windows visible, useful for debugging

## 📈 Performance Expectations

- **API tests**: ~10-30 seconds
- **UI tests**: ~60-120 seconds (browser startup overhead)
- **Hybrid tests**: ~90-150 seconds
- **Spanish tests**: ~60-120 seconds
- **Total suite**: ~5-10 minutes

## 🎯 Next Steps

After successful testing:

1. **Review generated reports** in `test_reports/`
2. **Check screenshots** in `test_screenshots/`
3. **Validate console output** for any warnings
4. **Test with different browsers** (Firefox, WebKit)
5. **Test in different environments** (CI/CD, different OS)

---

**Happy Testing! 🎭🚀**