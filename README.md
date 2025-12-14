<div align="center">
  <img src="assets/judo-framework-logo.png" alt="Judo Framework Logo" width="400"/>
  
  **A comprehensive API testing framework for Python, inspired by Karate Framework**
</div>

[![PyPI version](https://badge.fury.io/py/judo-framework.svg)](https://badge.fury.io/py/judo-framework)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/judo-framework)](https://pepy.tech/project/judo-framework)

[🇪🇸 Español](docs/README_ES.md) | [🇺🇸 English](README.md)

> **"As simple as Karate, as powerful as Python"**

Judo Framework brings the simplicity and elegance of Karate Framework to the Python ecosystem. Write API tests in plain English (or Spanish!), get beautiful HTML reports automatically, and enjoy the power of Python's ecosystem.

## 🎉 What's New in v1.3.39

### 📸 Screenshot Integration in HTML Reports (NEW!)
- **Automatic Screenshot Embedding** - Playwright screenshots automatically appear in HTML reports
- **Base64 Encoding** - Self-contained reports with no external file dependencies
- **Fullscreen View** - Click any screenshot to view it fullscreen
- **Failure Capture** - Automatic screenshots on test failures
- **Manual Control** - Take screenshots programmatically when needed

### 🎭 Playwright Browser Testing
- **Hybrid Testing** - Combine API and UI testing in the same scenario
- **50+ Browser Steps** - Complete browser automation in English and Spanish
- **Multi-page Support** - Handle multiple browser tabs and windows
- **Visual Testing** - Screenshot comparison and visual validation
- **100% Backward Compatible** - Existing API tests work unchanged

### 📊 Enhanced HTML Reports
- Professional reports with official CENTYC and Judo Framework logos
- Beautiful gradient headers, responsive layout, and professional footer
- Request/Response logging with complete headers
- Organized by scenario with numbered files

[See full changelog](CHANGELOG.md)

---

## 🌟 Why Judo Framework?

### ✅ Simple Setup (Just 10 Lines!)

```python
# features/environment.py
from judo.behave import *

before_all = before_all_judo
before_feature = before_feature_judo
after_feature = after_feature_judo
before_scenario = before_scenario_judo
after_scenario = after_scenario_judo
before_step = before_step_judo
after_step = after_step_judo
after_all = after_all_judo
```

**That's it!** Automatic HTML reports, full test tracking, and detailed statistics included.

### 🚀 Write Tests in Plain Language

```gherkin
# language: en
Feature: User API Testing

  Scenario: Create a new user
    Given the base URL is "https://api.example.com"
    When I send a POST request to "/users" with JSON:
      """
      {
        "name": "John Doe",
        "email": "john@example.com"
      }
      """
    Then the response status should be 201
    And the response should contain "id"
    And the response field "name" should equal "John Doe"
```

### 🇪🇸 Full Spanish Support

```gherkin
# language: es
Característica: Pruebas de API de Usuarios

  Escenario: Crear un nuevo usuario
    Dado que la URL base es "https://api.example.com"
    Cuando hago una petición POST a "/users" con el cuerpo:
      """
      {
        "name": "Juan Pérez",
        "email": "juan@example.com"
      }
      """
    Entonces el código de respuesta debe ser 201
    Y la respuesta debe contener el campo "id"
    Y el campo "name" debe ser "Juan Pérez"
```

### 📊 Beautiful HTML Reports (Automatic!)

Every test run generates a comprehensive HTML report with:
- ✅ Complete request/response details
- 📋 All scenarios and steps with status
- ⏱️ Execution times and performance metrics
- 🔍 Error messages with full stack traces
- 📈 Success rate and statistics
- 🎨 Clean, modern UI

**No configuration needed** - reports are generated automatically in `judo_reports/`

---

## 🚀 Quick Start

### Installation

```bash
# Install Judo Framework (includes browser testing capabilities)
pip install judo-framework

# Install browser engines (one-time setup for UI testing)
playwright install
```

> **🎭 Browser Testing Included**: Playwright comes pre-installed! No need for `[browser]` extras.

### 1. Create Your First Test

**features/api_test.feature:**
```gherkin
Feature: JSONPlaceholder API Testing

  Scenario: Get user information
    Given the base URL is "https://jsonplaceholder.typicode.com"
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "name"
    And the response should contain "email"
```

### 2. Setup Environment (One Time Only)

**features/environment.py:**
```python
from judo.behave import *

before_all = before_all_judo
before_feature = before_feature_judo
after_feature = after_feature_judo
before_scenario = before_scenario_judo
after_scenario = after_scenario_judo
before_step = before_step_judo
after_step = after_step_judo
after_all = after_all_judo
```

### 3. Run Tests

```bash
behave features/
```

**Output:**
```
🥋 Judo Framework - Captura automática de reportes activada

📋 Feature: JSONPlaceholder API Testing
  📝 Scenario: Get user information
    ✅ Given the base URL is "https://jsonplaceholder.typicode.com"
    ✅ When I send a GET request to "/users/1"
    ✅ Then the response status should be 200
    ✅ And the response should contain "name"
    ✅ And the response should contain "email"
  ✅ Scenario completado: Get user information

✅ Feature completado: JSONPlaceholder API Testing

📊 Reporte HTML generado: judo_reports/test_report_20251210_120000.html

============================================================
📈 RESUMEN DE EJECUCIÓN
============================================================
Features:  1
Scenarios: 1 (✅ 1 | ❌ 0 | ⏭️ 0)
Steps:     5 (✅ 5 | ❌ 0 | ⏭️ 0)
Tasa de éxito: 100.0%
============================================================
```

---

## 🎯 Key Features

### 🥋 Karate-like DSL
Familiar syntax for Karate Framework users with Python's power:

```python
from judo import Judo

judo = Judo()
response = judo.get("https://api.example.com/users/1")

# Karate-style matching
judo.match(response.status, 200)
judo.match(response.json["name"], "##string")
judo.match(response.json["email"], "##email")
judo.match(response.json["age"], "##number")
```

### 🥒 BDD Integration (Behave/Gherkin)
Full Behave support with 100+ predefined steps in English and Spanish:

**English Steps:**
- `Given the base URL is "{url}"`
- `When I send a GET request to "{endpoint}"`
- `Then the response status should be {status}`
- `And the response should contain "{field}"`
- `And I extract "{path}" from the response as "{variable}"`

**Spanish Steps:**
- `Dado que la URL base es "{url}"`
- `Cuando hago una petición GET a "{endpoint}"`
- `Entonces el código de respuesta debe ser {status}`
- `Y la respuesta debe contener el campo "{campo}"`
- `Y guardo el valor del campo "{campo}" en la variable "{variable}"`

### 🌐 Complete HTTP Testing
All HTTP methods with full control:

```gherkin
Scenario: Complete CRUD operations
  Given the base URL is "https://api.example.com"
  
  # CREATE
  When I send a POST request to "/users" with JSON:
    """
    {"name": "John", "email": "john@example.com"}
    """
  Then the response status should be 201
  And I extract "id" from the response as "userId"
  
  # READ
  When I send a GET request to "/users/{userId}"
  Then the response status should be 200
  
  # UPDATE
  When I send a PUT request to "/users/{userId}" with JSON:
    """
    {"name": "John Updated"}
    """
  Then the response status should be 200
  
  # DELETE
  When I send a DELETE request to "/users/{userId}"
  Then the response status should be 204
```

### 📄 File Support (Like Karate's `read()`)
Load test data from JSON, YAML, or CSV files:

```python
# Load test data
user_data = judo.read("test_data/users/create_user.json")
response = judo.post("/users", json=user_data)

# Load YAML
config = judo.read_yaml("config/api_config.yaml")

# Load CSV for data-driven tests
users = judo.read_csv("test_data/users.csv")
```

**In Gherkin:**
```gherkin
Scenario: Create user from file
  Given I load test data "user" from file "test_data/users/john.json"
  When I POST to "/users" with JSON file "test_data/users/john.json"
  Then the response status should be 201
```

### 📊 Professional HTML Reports with Screenshots
Zero configuration, maximum insight with professional branding:

- **🏢 Official Branding**: CENTYC and Judo Framework logos in header and footer
- **🎨 Modern Design**: Beautiful gradient headers and responsive layout
- **📸 Screenshot Integration**: Playwright screenshots embedded directly in reports (v1.3.39+)
- **🖼️ Fullscreen View**: Click any screenshot to view it fullscreen
- **📋 Request Details**: Method, URL, headers, body with syntax highlighting
- **📥 Response Details**: Status, headers, body, timing with color-coded status
- **✅ Assertions**: All validations with expected vs actual comparisons
- **💾 Variables**: Track variable usage and data flow across scenarios
- **📊 Statistics**: Success rate, timing, error tracking with visual indicators
- **🔗 Professional Footer**: Creator information and links to documentation
- **📱 Responsive Design**: Works perfectly on desktop and mobile devices

#### 📸 Screenshot Features (v1.3.39+)

**Automatic Screenshots:**
```python
# In environment.py - screenshots on failures
import os
os.environ['JUDO_SCREENSHOT_ON_STEP_FAILURE'] = 'true'
```

**Manual Screenshots:**
```python
# In your step definitions
@when('I verify the dashboard')
def step_impl(context):
    context.judo_context.take_screenshot("dashboard_view")
    # Screenshot automatically appears in HTML report!
```

**In Gherkin:**
```gherkin
Scenario: Visual verification
  Given I navigate to "https://example.com"
  When I take a screenshot named "homepage"
  Then I should see "Welcome"
```

Screenshots are:
- ✅ Embedded as base64 (no external files needed)
- ✅ Clickable for fullscreen view
- ✅ Automatically attached to steps
- ✅ Captured on failures by default

### 💾 Advanced Request/Response Logging
Automatically save all HTTP interactions to JSON files with complete details:

```gherkin
Feature: API Testing with Enhanced Logging

  Background:
    Given I have a Judo API client
    And the base URL is "https://api.example.com"
    # Enable automatic request/response logging
    And I enable request/response logging to directory "api_logs"

  Scenario: User operations with detailed logging
    When I send a GET request to "/users/1"
    Then the response status should be 200
    # Files automatically saved with complete details:
    # api_logs/User_operations_with_detailed_logging/01_GET_143052_request.json
    # api_logs/User_operations_with_detailed_logging/01_GET_143052_response.json
```

**Enhanced Features:**
- 📁 **Organized by scenario** - Each scenario gets its own directory
- 🔢 **Sequential numbering** - Requests numbered in execution order
- ⏰ **Timestamped files** - Easy to track when requests were made
- 📝 **Complete headers** - All request and response headers captured
- 🔍 **Query parameters** - Separate tracking of URL parameters
- 📊 **Response metadata** - Content type, size, and timing information
- 🛡️ **Error handling** - Graceful handling of malformed responses
- 🔧 **Configurable** - Enable/disable per scenario or globally
- 🌐 **Bilingual support** - English and Spanish steps available

### ⚡ Parallel Execution with Tag Support
Run tests faster with parallel execution and advanced tag filtering:

```python
from judo.runner import ParallelRunner

runner = ParallelRunner(
    features_dir="features",
    max_workers=8,
    save_requests_responses=True,
    requests_responses_dir="./api_logs"
)

# Support for Jira-style tags with hyphens
results = runner.run(tags=["@PROJ-123", "@API-456", "@end-to-end"])
print(f"Passed: {results['passed']}/{results['total']}")
```

**Tag Features:**
- 🏷️ **Hyphen Support** - Full support for tags like `@PROJ-123`, `@API-456`
- 🎯 **Jira Integration** - Perfect for Jira ticket references
- 🔍 **Advanced Filtering** - Combine multiple tags for precise test selection
- ⚡ **Parallel Safe** - Tag filtering works seamlessly with parallel execution

### 🎭 Built-in Mock Server
Test without external dependencies:

```python
from judo import Judo

judo = Judo()

# Start mock server
mock = judo.start_mock(port=8080)

# Configure mock responses
mock.when("GET", "/users/1").then(
    status=200,
    json={"id": 1, "name": "Mock User"}
)

# Test against mock
response = judo.get("http://localhost:8080/users/1")
judo.match(response.json["name"], "Mock User")

# Stop mock
judo.stop_mock()
```

### ✅ Schema Validation
Validate responses against JSON schemas:

```gherkin
Scenario: Validate user schema
  When I send a GET request to "/users/1"
  Then the response should match schema file "schemas/user_schema.json"
```

```python
# In Python
schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["id", "name", "email"]
}

judo.match(response.json, schema)
```

### 🔐 Authentication Support
JWT, OAuth, Basic Auth, and custom headers:

```gherkin
Scenario: Authenticated requests
  Given I use bearer token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  When I send a GET request to "/protected/resource"
  Then the response status should be 200

Scenario: Basic authentication
  Given I use basic authentication with username "admin" and password "secret"
  When I send a GET request to "/admin/users"
  Then the response status should be 200
```

---

## 📚 Complete Step Reference

### 🔧 Configuration Steps

**English:**
- `Given I have a Judo API client`
- `Given the base URL is "{url}"`
- `Given I set the variable "{name}" to "{value}"`
- `Given I set the header "{name}" to "{value}"`
- `Given I set the query parameter "{name}" to "{value}"`
- `Given I enable request/response logging`
- `Given I enable request/response logging to directory "{directory}"`
- `Given I disable request/response logging`

**Spanish:**
- `Dado que tengo un cliente API Judo`
- `Dado que la URL base es "{url}"`
- `Dado que establezco la variable "{nombre}" a "{valor}"`
- `Dado que establezco el header "{nombre}" a "{valor}"`
- `Dado que establezco el parámetro "{nombre}" a "{valor}"`
- `Dado que habilito el guardado de peticiones y respuestas`
- `Dado que habilito el guardado de peticiones y respuestas en el directorio "{directorio}"`
- `Dado que deshabilito el guardado de peticiones y respuestas`

### 🔐 Authentication Steps

**English:**
- `Given I use bearer token "{token}"`
- `Given I use basic authentication with username "{user}" and password "{pass}"`

**Spanish:**
- `Dado que uso el token bearer "{token}"`
- `Dado que uso autenticación básica con usuario "{usuario}" y contraseña "{password}"`

### 🌐 HTTP Request Steps

**English:**
- `When I send a GET request to "{endpoint}"`
- `When I send a POST request to "{endpoint}" with JSON:`
- `When I send a PUT request to "{endpoint}" with JSON:`
- `When I send a PATCH request to "{endpoint}" with JSON:`
- `When I send a DELETE request to "{endpoint}"`

**Spanish:**
- `Cuando hago una petición GET a "{endpoint}"`
- `Cuando hago una petición POST a "{endpoint}" con el cuerpo:`
- `Cuando hago una petición PUT a "{endpoint}" con el cuerpo:`
- `Cuando hago una petición PATCH a "{endpoint}" con el cuerpo:`
- `Cuando hago una petición DELETE a "{endpoint}"`

### ✅ Validation Steps

**English:**
- `Then the response status should be {status}`
- `Then the response should be successful`
- `Then the response should contain "{field}"`
- `Then the response field "{field}" should equal "{value}"`
- `Then the response should be an array`
- `Then the response array should have {count} items`

**Spanish:**
- `Entonces el código de respuesta debe ser {status}`
- `Entonces la respuesta debe ser exitosa`
- `Entonces la respuesta debe contener el campo "{campo}"`
- `Entonces el campo "{campo}" debe ser "{valor}"`
- `Entonces la respuesta debe ser un array`
- `Entonces la respuesta debe tener {count} elementos`

### 💾 Data Extraction Steps

**English:**
- `When I extract "{path}" from the response as "{variable}"`
- `When I store the response as "{variable}"`

**Spanish:**
- `Cuando guardo el valor del campo "{campo}" en la variable "{variable}"`
- `Cuando guardo la respuesta completa en la variable "{variable}"`

### 🔄 Variable Comparison Steps

**English:**
- `Then the variable "{var1}" should equal the variable "{var2}"`

**Spanish:**
- `Entonces la variable "{var1}" debe ser igual a la variable "{var2}"`
- `Entonces la variable "{var1}" no debe ser igual a la variable "{var2}"`

---

## 🎯 Real-World Examples

### Complete Project Setup

Here's a real production setup combining API and UI testing:

#### Project Structure
```
my-project/
├── features/
│   ├── api_tests.feature          # API tests
│   ├── ui_tests.feature           # Browser tests
│   ├── environment.py             # Configuration
│   └── steps/                     # Custom steps
├── Runner/
│   ├── runner.py                  # Custom runner
│   └── judo_reports/              # Generated reports
├── base_requests/                 # JSON test data
├── .env                           # Environment variables
└── requirements.txt
```

#### Environment Configuration with Screenshots
```python
# features/environment.py
from judo.behave import *
from dotenv import load_dotenv
import os

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
    before_all_judo(context)

def before_scenario(context, scenario):
    before_scenario_judo(context, scenario)
    
    # Initialize Playwright for @test-front tagged scenarios
    if PLAYWRIGHT_ENABLED and any(tag in scenario.tags for tag in ['test-front', 'front']):
        from playwright.sync_api import sync_playwright
        from judo.playwright.browser_context import JudoBrowserContext
        
        if not hasattr(context.judo_context, 'page'):
            old_context = context.judo_context
            context.judo_context = JudoBrowserContext(context)
            
            # Copy variables
            if hasattr(old_context, 'variables'):
                context.judo_context.variables = old_context.variables
            
            # Start Playwright
            context.judo_context.playwright = sync_playwright().start()
            
            # Full screen browser
            browser_options = {
                'headless': False,
                'args': ['--start-maximized']
            }
            context.judo_context.browser = context.judo_context.playwright.chromium.launch(**browser_options)
            context.judo_context.browser_context = context.judo_context.browser.new_context(no_viewport=True)
            context.judo_context.page = context.judo_context.browser_context.new_page()

def after_step(context, step):
    """Take screenshot after EVERY step (pass or fail)"""
    if hasattr(context.judo_context, 'page') and context.judo_context.page:
        try:
            step_name_clean = step.name.replace(' ', '_').replace('"', '').replace("'", '')
            screenshot_name = f"{step.status}_{step_name_clean}"
            
            screenshot_path = context.judo_context.take_screenshot(screenshot_name)
            
            # Attach to HTML report
            from judo.reporting.reporter import get_reporter
            reporter = get_reporter()
            if reporter and reporter.current_step:
                reporter.attach_screenshot(screenshot_path)
        except Exception as e:
            print(f"⚠️ Screenshot failed: {e}")
    
    after_step_judo(context, step)

def after_scenario(context, scenario):
    if hasattr(context.judo_context, 'page') and context.judo_context.page:
        try:
            context.judo_context.page.close()
            context.judo_context.page = None
        except:
            pass
    after_scenario_judo(context, scenario)

def after_all(context):
    if hasattr(context.judo_context, 'browser') and context.judo_context.browser:
        try:
            if hasattr(context.judo_context, 'browser_context'):
                context.judo_context.browser_context.close()
            context.judo_context.browser.close()
            if hasattr(context.judo_context, 'playwright'):
                context.judo_context.playwright.stop()
        except:
            pass
    after_all_judo(context)

before_feature = before_feature_judo
after_feature = after_feature_judo
before_step = before_step_judo
```

#### Environment Variables (.env)
```bash
# API Configuration
API_BASE_URL=https://api.example.com
API_TOKEN=Bearer your-token-here
TIMEOUT_SECONDS=30

# Playwright Configuration
JUDO_USE_BROWSER=true
JUDO_BROWSER=chromium
JUDO_HEADLESS=false
JUDO_SCREENSHOT_DIR=screenshots

# Debug
JUDO_DEBUG_REPORTER=false
```

#### Custom Runner
```python
# Runner/runner.py
from judo.runner.base_runner import BaseRunner
import os

os.environ['JUDO_DEBUG_REPORTER'] = 'false'

class MyRunner(BaseRunner):
    basedir = "./judo_reports"
    
    def __init__(self):
        super().__init__(
            features_dir="../features",
            output_dir=self.basedir,
            generate_cucumber_json=True,
            cucumber_json_dir=f"{self.basedir}/cucumber-json",
            parallel=False,
            save_requests_responses=True,
            requests_responses_dir=f"{self.basedir}/api_logs"
        )
    
    def run_tests(self):
        return self.run(tags=["@smoke"])

if __name__ == "__main__":
    runner = MyRunner()
    results = runner.run_tests()
    print(f"✅ Tests completed: {results['passed']}/{results['total']} passed")
```

### Mixed API + UI Testing

```gherkin
Feature: E-commerce Complete Flow

  @mix
  Scenario: Create product via API and verify in UI
    # API: Create product
    Given the base URL is "https://api.shop.com"
    And I use bearer token "{API_TOKEN}"
    When I send a POST request to "/products" with JSON:
      """
      {
        "name": "Laptop Pro",
        "price": 1299.99,
        "category": "electronics"
      }
      """
    Then the response status should be 201
    And I extract "$.id" from the response as "productId"
    
    # UI: Verify product appears
    Given I navigate to "https://shop.com/products/{productId}"
    Then I should see "Laptop Pro"
    And I should see "$1,299.99"
    When I take a screenshot named "product_page"
    
    # UI: Add to cart
    When I click "#add-to-cart"
    Then I should see "Added to cart"
    When I take a screenshot named "cart_confirmation"
```

### Frontend Testing with Full Screenshots

```gherkin
@test-front
Feature: Website Navigation

  Scenario: Homepage verification with screenshots
    Given I navigate to "https://www.centyc.cl"
    # Screenshot automatically captured after each step
    When I click "a[href='/services']"
    Then I should see "Our Services"
    # All screenshots embedded in HTML report
```

### Complete CRUD Workflow

```gherkin
Feature: User Management

  Background:
    Given the base URL is "https://api.example.com"
    And I use bearer token "{API_TOKEN}"

  Scenario: Complete user lifecycle
    # CREATE
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
    And I extract "$.email" from the response as "userEmail"
    
    # READ
    When I send a GET request to "/users/{userId}"
    Then the response status should be 200
    And the response field "name" should equal "John Doe"
    And the response field "email" should equal "{userEmail}"
    
    # UPDATE
    When I send a PUT request to "/users/{userId}" with JSON:
      """
      {
        "name": "John Doe Updated",
        "email": "john.updated@example.com",
        "role": "user"
      }
      """
    Then the response status should be 200
    And the response field "name" should equal "John Doe Updated"
    
    # VERIFY UPDATE
    When I send a GET request to "/users/{userId}"
    Then the response field "role" should equal "user"
    
    # DELETE
    When I send a DELETE request to "/users/{userId}"
    Then the response status should be 204
    
    # VERIFY DELETION
    When I send a GET request to "/users/{userId}"
    Then the response status should be 404
```

### Using External JSON Files

```gherkin
Feature: Data-Driven Testing

  Scenario: Create multiple posts from files
    Given the base URL is "https://api.example.com"
    
    # Load from file
    When I POST to "/posts" with JSON file "test_data/posts/post1.json"
    Then the response status should be 201
    And I save the response to file "responses/post1_response.json"
    
    # Validate against schema
    When I POST to "/posts" with JSON file "test_data/posts/post2.json"
    Then the response should match schema file "schemas/post_schema.json"
```

**test_data/posts/post1.json:**
```json
{
  "title": "Judo Framework Test",
  "body": "Testing with external files",
  "userId": 1
}
```

**schemas/post_schema.json:**
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "number"},
    "title": {"type": "string"},
    "body": {"type": "string"},
    "userId": {"type": "number"}
  },
  "required": ["id", "title", "body", "userId"]
}
```

---

## 🎓 Advanced Examples

### Example 1: Data-Driven Testing

```gherkin
Feature: User Registration

  Scenario Outline: Register multiple users
    Given the base URL is "https://api.example.com"
    When I send a POST request to "/users" with JSON:
      """
      {
        "name": "<name>",
        "email": "<email>",
        "age": <age>
      }
      """
    Then the response status should be 201
    And the response field "name" should equal "<name>"
    
    Examples:
      | name        | email              | age |
      | John Doe    | john@example.com   | 30  |
      | Jane Smith  | jane@example.com   | 25  |
      | Bob Johnson | bob@example.com    | 35  |
```

### Example 2: Complex Workflow

```gherkin
Feature: E-commerce Workflow

  Scenario: Complete purchase flow
    Given the base URL is "https://api.shop.com"
    
    # Login
    When I send a POST request to "/auth/login" with JSON:
      """
      {"email": "user@example.com", "password": "secret"}
      """
    Then the response status should be 200
    And I extract "token" from the response as "authToken"
    
    # Use token for authenticated requests
    Given I use bearer token "{authToken}"
    
    # Add item to cart
    When I send a POST request to "/cart/items" with JSON:
      """
      {"productId": 123, "quantity": 2}
      """
    Then the response status should be 201
    And I extract "cartId" from the response as "cartId"
    
    # Checkout
    When I send a POST request to "/orders" with JSON:
      """
      {"cartId": "{cartId}", "paymentMethod": "credit_card"}
      """
    Then the response status should be 201
    And the response should contain "orderId"
    And the response field "status" should equal "confirmed"
```

### Example 3: Schema Validation

```gherkin
Feature: API Contract Testing

  Scenario: Validate user response schema
    Given the base URL is "https://api.example.com"
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should match the schema:
      """
      {
        "type": "object",
        "properties": {
          "id": {"type": "number"},
          "name": {"type": "string"},
          "email": {"type": "string", "format": "email"},
          "address": {
            "type": "object",
            "properties": {
              "street": {"type": "string"},
              "city": {"type": "string"}
            }
          }
        },
        "required": ["id", "name", "email"]
      }
      """
```

---

## 🐛 Troubleshooting

### Common Issues

#### Playwright Not Working
```bash
# Reinstall Playwright
pip uninstall playwright
pip install playwright
playwright install chromium

# Verify installation
playwright --version
```

#### Screenshots Not Appearing in Reports
```python
# 1. Check reporter is active
from judo.reporting.reporter import get_reporter
reporter = get_reporter()
print(f"Reporter active: {reporter is not None}")

# 2. Verify screenshot was taken
screenshot_path = context.judo_context.take_screenshot("test")
print(f"Screenshot saved: {screenshot_path}")

# 3. Check runner configuration
runner = BaseRunner(
    generate_cucumber_json=True  # ✅ Must be True
)
```

#### "WinError 123" When Saving Screenshots
```bash
# Cause: Invalid characters in filename (: / \ | ? *)
# Solution: Framework normalizes names automatically
# If persists, avoid special characters in step names
```

#### "Playwright Sync API inside asyncio loop"
```bash
# Solution: Only initialize Playwright for @test-front tagged scenarios
# The framework detects automatically and avoids conflicts with API tests
```

#### Browser Not Starting
```bash
# Check environment variables
echo $JUDO_USE_BROWSER  # Should be 'true'

# Check scenario has correct tag
@test-front  # or @front
Scenario: My browser test
```

#### Reports Not Generated
```python
# Verify runner configuration
runner = BaseRunner(
    features_dir="features",
    output_dir="judo_reports",
    generate_cucumber_json=True  # ✅ Required for reports
)
```

### Debug Mode

Enable detailed logging:

```python
# In environment.py
import os
os.environ['JUDO_DEBUG_REPORTER'] = 'true'
os.environ['JUDO_LOG_LEVEL'] = 'DEBUG'
```

### Verify Installation

```bash
# Check Judo Framework
python -c "import judo; print(f'Judo: {judo.__version__}')"

# Check Playwright
python -c "from judo.playwright import PLAYWRIGHT_AVAILABLE; print(f'Playwright: {PLAYWRIGHT_AVAILABLE}')"

# Check all dependencies
pip list | grep -E "judo|behave|playwright|requests"
```

---

## 🔧 Installation Options

**Basic Installation:**
```bash
pip install judo-framework
```

**With Optional Features:**
```bash
# Cryptography support (JWT, OAuth, encryption)
pip install judo-framework[crypto]

# XML/SOAP testing support
pip install judo-framework[xml]

# Browser automation (Selenium, Playwright)
pip install judo-framework[browser]

# All features
pip install judo-framework[full]
```

---

## 🆚 Comparison with Karate

| Feature | Karate (Java) | Judo (Python) |
|---------|---------------|---------------|
| **Language** | Java/JavaScript | Python |
| **BDD Support** | ✅ Cucumber | ✅ Behave |
| **DSL Syntax** | ✅ Karate DSL | ✅ Similar DSL |
| **HTTP Testing** | ✅ Full | ✅ Full |
| **File Support** | ✅ `read()` | ✅ `read()` |
| **HTML Reports** | ✅ Built-in | ✅ Automatic |
| **Parallel Execution** | ✅ Yes | ✅ Yes |
| **Mock Server** | ✅ Yes | ✅ Yes |
| **Spanish Support** | ❌ No | ✅ Yes |
| **Setup Complexity** | Medium | **Very Simple** |
| **Python Ecosystem** | ❌ No | ✅ Full Access |

### Migration Example

**Karate:**
```javascript
Feature: User API

Scenario: Get user
  Given url 'https://api.example.com'
  And path 'users', 1
  When method get
  Then status 200
  And match response.name == '#string'
  And match response.email == '#email'
```

**Judo:**
```gherkin
Feature: User API

Scenario: Get user
  Given the base URL is "https://api.example.com"
  When I send a GET request to "/users/1"
  Then the response status should be 200
  And the response field "name" should be a string
  And the response field "email" should be an email
```

---

## 📚 Documentation

### 🌐 Official Documentation
**Complete documentation available at: [http://centyc.cl/judo-framework/](http://centyc.cl/judo-framework/)**

### 📖 Quick Reference
| Topic | Description |
|-------|-------------|
| **Request/Response Logging** | [📖 Read](docs/request-response-logging.md) - Automatic logging of HTTP interactions |
| **Examples** | [📖 Read](examples/README.md) - Complete examples and tutorials |
| **Test Data** | [📖 Read](examples/test_data/README.md) - Guide for using test data files |

---

## 🤝 Contributing

**⚠️ This project only accepts contributions through GitHub Issues.**

We welcome:
- 🐛 **Bug reports** - Help us identify issues
- 💡 **Feature suggestions** - Share your ideas
- 📝 **Documentation feedback** - Help improve our docs
- ❓ **Questions** - Ask in GitHub Discussions

We do NOT accept:
- ❌ **Pull Requests** - Will be closed without review
- ❌ **Code contributions** - All development is internal

**Why?** Judo Framework is professionally maintained by CENTYC to ensure consistent quality, reliability, and enterprise-grade standards.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to report bugs and suggest features.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Created by Felipe Farias at [CENTYC](https://www.centyc.cl)**

### About CENTYC

[CENTYC](https://www.centyc.cl) - **Centro Latinoamericano de Testing y Calidad del Software**  
*Latin American Center for Software Testing and Quality*

We are dedicated to advancing software quality and testing practices across Latin America through:
- 🎓 Training and certification programs
- 🔬 Research and development
- 🛠️ Open-source tools like Judo Framework
- 🤝 Community building and knowledge sharing

---

## 🙏 Acknowledgments

- **Inspired by** [Karate Framework](https://github.com/karatelabs/karate) by Peter Thomas
- **Developed at** [CENTYC](https://www.centyc.cl) for the Latin American testing community
- **Built for** the global Python API testing community
- **Special thanks** to all contributors and early adopters

---

## 📊 Project Stats

- **Language**: Python 3.8+
- **License**: MIT
- **Status**: Production Ready
- **Version**: 1.3.18
- **Downloads**: [![Downloads](https://pepy.tech/badge/judo-framework)](https://pepy.tech/project/judo-framework)

---

## 🔗 Links

- **📖 Official Documentation**: http://centyc.cl/judo-framework/
- **📦 PyPI**: https://pypi.org/project/judo-framework/
- **💻 GitHub**: https://github.com/FelipeFariasAlfaro/Judo-Framework
- **🏢 CENTYC**: https://www.centyc.cl
- **🐛 Issues**: https://github.com/FelipeFariasAlfaro/Judo-Framework/issues
- **💬 Discussions**: https://github.com/FelipeFariasAlfaro/Judo-Framework/discussions

---

## 💬 Community

Join our community:
- 💬 [GitHub Discussions](https://github.com/FelipeFariasAlfaro/Judo-Framework/discussions)
- 🐛 [Report Issues](https://github.com/FelipeFariasAlfaro/Judo-Framework/issues)
- 📧 Contact: felipe.farias@centyc.cl

---

**Made with ❤️ at [CENTYC](https://www.centyc.cl) for API testing excellence**

*"As simple as Karate, as powerful as Python"* 🥋🐍
