# Playwright Integration Examples

This directory contains examples demonstrating the Playwright integration with Judo Framework, enabling hybrid API + UI testing.

## 🎯 What is Playwright Integration?

The Playwright integration allows you to:
- **Combine API and UI testing** in the same scenario
- **Share data** between API responses and UI elements
- **Use the same reporting system** for both API and browser actions
- **Maintain full compatibility** with existing API-only tests

## 📁 Files in this Directory

### Feature Files
- `playwright_integration.feature` - English examples of hybrid API + UI testing
- `playwright_integration_es.feature` - Spanish examples (same functionality)

### Configuration
- `environment_playwright.py` - Example environment.py setup for Playwright integration
- `.env.playwright` - Example environment variables for browser configuration

## 🚀 Quick Start

### 1. Install Playwright Support

```bash
# Install Judo Framework with browser support
pip install 'judo-framework[browser]'

# Install Playwright browsers
playwright install
```

### 2. Set Environment Variables

```bash
# Enable browser testing
export JUDO_USE_BROWSER=true

# Browser configuration (optional)
export JUDO_BROWSER=chromium
export JUDO_HEADLESS=false
export JUDO_SCREENSHOTS=true
```

### 3. Update Your environment.py

```python
from judo.behave import setup_judo_context
from judo.playwright.hooks import integrate_playwright_hooks

def before_all(context):
    setup_judo_context(context)
    integrate_playwright_hooks(context, 'before_all')

def before_scenario(context, scenario):
    integrate_playwright_hooks(context, 'before_scenario', scenario)

def after_scenario(context, scenario):
    integrate_playwright_hooks(context, 'after_scenario', scenario)

def after_all(context):
    integrate_playwright_hooks(context, 'after_all')
```

### 4. Run Examples

```bash
# Run all examples
behave examples/playwright_integration.feature

# Run specific scenarios
behave examples/playwright_integration.feature --tags=@hybrid
behave examples/playwright_integration.feature --tags=@ui

# Run with specific browser
JUDO_BROWSER=firefox behave examples/playwright_integration.feature

# Run in headed mode (visible browser)
JUDO_HEADLESS=false behave examples/playwright_integration.feature
```

## 📝 Example Scenarios

### 1. Hybrid API + UI Testing

```gherkin
@hybrid
Scenario: Create user via API and verify in UI
  # API Testing - Create a user
  When I send a POST request to "/users" with JSON:
    """
    {"name": "John Doe", "email": "john@example.com"}
    """
  Then the response status should be 201
  And I extract "$.name" from the API response and store it as "userName"
  
  # UI Testing - Use API data in browser
  Given I start a browser
  When I navigate to "https://example.com/form"
  And I fill "#name" with "{userName}"
  And I click on "#submit"
  Then the element "#success" should be visible
```

### 2. Pure UI Testing

```gherkin
@ui
Scenario: Form validation testing
  Given I start a browser
  When I navigate to "https://example.com/form"
  And I click on "#submit"
  Then the element "#name:invalid" should be visible
  
  When I fill "#name" with "Test User"
  And I fill "#email" with "test@example.com"
  And I click on "#submit"
  Then the element "#success" should be visible
```

### 3. Multi-Page Testing

```gherkin
@ui @multi-page
Scenario: Multi-page workflow
  Given I start a browser
  And I create a new page named "login_page"
  And I create a new page named "dashboard_page"
  
  When I switch to page "login_page"
  And I navigate to "https://example.com/login"
  And I fill "#username" with "testuser"
  And I fill "#password" with "testpass"
  And I click on "#login"
  
  When I switch to page "dashboard_page"
  And I navigate to "https://example.com/dashboard"
  Then the element "#welcome" should be visible
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `JUDO_USE_BROWSER` | `false` | Enable browser testing |
| `JUDO_BROWSER` | `chromium` | Browser type (chromium/firefox/webkit) |
| `JUDO_HEADLESS` | `true` | Headless mode |
| `JUDO_SCREENSHOTS` | `false` | Enable screenshots |
| `JUDO_SCREENSHOT_ON_FAILURE` | `true` | Screenshot on test failure |
| `JUDO_AUTO_START_BROWSER` | `true` | Auto-start browser for UI scenarios |
| `JUDO_VIEWPORT_WIDTH` | `1280` | Browser viewport width |
| `JUDO_VIEWPORT_HEIGHT` | `720` | Browser viewport height |

### Browser-Specific Configuration

```bash
# Chromium with custom arguments
export JUDO_BROWSER=chromium
export JUDO_BROWSER_ARGS="--disable-web-security,--disable-features=VizDisplayCompositor"

# Firefox with custom profile
export JUDO_BROWSER=firefox
export JUDO_HEADLESS=false

# WebKit (Safari engine)
export JUDO_BROWSER=webkit
export JUDO_VIEWPORT_WIDTH=1920
export JUDO_VIEWPORT_HEIGHT=1080
```

## 📊 Available Steps

### Browser Lifecycle

```gherkin
# English
Given I start a browser
Given I start a "chromium" browser
Given I start a headless browser
Given I create a new page
Given I create a new page named "login_page"
Given I close the browser

# Spanish
Dado que inicio un navegador
Dado que inicio un navegador "chromium"
Dado que inicio un navegador sin cabeza
Dado que creo una nueva página
Dado que creo una nueva página llamada "pagina_login"
Dado que cierro el navegador
```

### Navigation

```gherkin
# English
When I navigate to "https://example.com"
When I reload the page
When I go back
When I go forward

# Spanish
Cuando navego a "https://ejemplo.com"
Cuando recargo la página
Cuando voy hacia atrás
Cuando voy hacia adelante
```

### Element Interaction

```gherkin
# English
When I click on "#submit-button"
When I fill "#username" with "john_doe"
When I select "option1" from "#dropdown"
When I check the checkbox "#agree"

# Spanish
Cuando hago clic en "#submit-button"
Cuando lleno "#username" con "juan_perez"
Cuando selecciono "opcion1" de "#dropdown"
Cuando marco la casilla "#agree"
```

### Element Validation

```gherkin
# English
Then the element "#message" should be visible
Then the element "#title" should contain "Welcome"
Then the element "#link" should have attribute "href" with value "https://example.com"

# Spanish
Entonces el elemento "#message" debe ser visible
Entonces el elemento "#title" debe contener "Bienvenido"
Entonces el elemento "#link" debe tener el atributo "href" con valor "https://ejemplo.com"
```

### Waiting

```gherkin
# English
When I wait for element "#result" to be visible
When I wait for URL to contain "success"
When I wait 3 seconds

# Spanish
Cuando espero que el elemento "#result" sea visible
Cuando espero que la URL contenga "exito"
Cuando espero 3 segundos
```

### Screenshots

```gherkin
# English
When I take a screenshot
When I take a screenshot named "login_form"
When I take a screenshot of element "#form"

# Spanish
Cuando tomo una captura de pantalla
Cuando tomo una captura de pantalla llamada "formulario_login"
Cuando tomo una captura de pantalla del elemento "#form"
```

### Hybrid API + UI

```gherkin
# English
When I extract "$.id" from the API response and store it as "userId"
When I capture text from element "#username" and store it as "currentUser"

# Spanish
Cuando extraigo "$.id" de la respuesta de la API y lo guardo como "userId"
Cuando capturo el texto del elemento "#username" y lo guardo como "currentUser"
```

## 🎭 Advanced Features

### JavaScript Execution

```gherkin
When I execute JavaScript:
  """
  return {
    title: document.title,
    url: window.location.href,
    userAgent: navigator.userAgent
  };
  """
Then I should have variable "js_result"
```

### Local Storage

```gherkin
When I set localStorage "theme" to "dark"
Then localStorage "theme" should be "dark"
When I clear localStorage
```

### Cookie Management

```gherkin
When I add cookie with name "session" and value "abc123"
When I clear all cookies
```

### File Upload

```gherkin
When I upload file "test_data/sample.pdf" to "#file-input"
```

### Drag and Drop

```gherkin
When I drag "#source-element" to "#target-element"
```

## 🔍 Debugging

### Enable Debug Mode

```bash
export JUDO_DEBUG_STEPS=true
export JUDO_SCREENSHOT_BEFORE_STEP=true
export JUDO_SCREENSHOT_AFTER_STEP=true
export JUDO_LOG_CONSOLE=true
```

### Common Issues

1. **Element not found**: Use explicit waits
   ```gherkin
   When I wait for element "#dynamic-content" to be visible
   Then the element "#dynamic-content" should contain "Loaded"
   ```

2. **Timing issues**: Add appropriate waits
   ```gherkin
   When I click on "#submit"
   And I wait for URL to contain "success"
   Then the element "#confirmation" should be visible
   ```

3. **Selector issues**: Test selectors in browser dev tools
   ```javascript
   // In browser console
   document.querySelector("#your-selector")
   ```

## 📈 Performance Tips

1. **Reuse browser instances**: Set `JUDO_CLOSE_BROWSER_AFTER_SCENARIO=false`
2. **Use headless mode in CI**: Set `JUDO_HEADLESS=true`
3. **Limit screenshots**: Only enable when needed
4. **Use specific selectors**: Avoid complex CSS selectors

## 🎯 Best Practices

1. **Tag your scenarios**:
   ```gherkin
   @api          # API-only scenarios
   @ui           # UI-only scenarios
   @hybrid       # Mixed API + UI scenarios
   ```

2. **Use descriptive page names**:
   ```gherkin
   Given I create a new page named "checkout_page"
   Given I create a new page named "confirmation_page"
   ```

3. **Take screenshots at key points**:
   ```gherkin
   When I fill the form
   And I take a screenshot named "form_completed"
   And I click on "#submit"
   And I take a screenshot named "form_submitted"
   ```

4. **Share data between API and UI**:
   ```gherkin
   # Get data from API
   When I send a GET request to "/user/profile"
   And I extract "$.name" from the API response and store it as "userName"
   
   # Use in UI
   When I fill "#display-name" with "{userName}"
   ```

## 🚀 Next Steps

1. **Run the examples**: Start with the provided feature files
2. **Customize configuration**: Adjust environment variables for your needs
3. **Create your own scenarios**: Combine API and UI testing for your application
4. **Explore advanced features**: Multi-page testing, JavaScript execution, visual testing

## 📚 Additional Resources

- [Playwright Integration Documentation](../.kiro/playwright-integration.md)
- [Judo Framework Documentation](../README.md)
- [Playwright Official Documentation](https://playwright.dev/)

---

**Happy Testing! 🎭🚀**