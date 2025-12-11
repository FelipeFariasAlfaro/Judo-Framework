# 🥋 Judo Framework

<div align="center">
  <h2>A comprehensive API testing framework for Python</h2>
  <p><em>Inspired by Karate Framework</em></p>
  
  <p>
    <a href="https://pypi.org/project/judo-framework/"><img src="https://badge.fury.io/py/judo-framework.svg" alt="PyPI version"></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
    <a href="https://pepy.tech/project/judo-framework"><img src="https://pepy.tech/badge/judo-framework" alt="Downloads"></a>
  </p>
</div>

---

## 🌟 Why Judo Framework?

> **"As simple as Karate, as powerful as Python"**

Judo Framework brings the simplicity and elegance of Karate Framework to the Python ecosystem. Write API tests in plain English (or Spanish!), get beautiful HTML reports automatically, and enjoy the power of Python's ecosystem.

### ✨ Key Features

<div class="grid cards" markdown>

-   :material-lightning-bolt:{ .lg .middle } __Simple Setup__

    ---

    Just 10 lines of code to get started. No complex configuration needed.

    [:octicons-arrow-right-24: Quick Start](getting-started/quick-start.md)

-   :material-translate:{ .lg .middle } __Bilingual Support__

    ---

    Write tests in English or Spanish. Full language support for both.

    [:octicons-arrow-right-24: Examples](reference/examples.md)

-   :material-chart-line:{ .lg .middle } __Beautiful Reports__

    ---

    Automatic HTML reports with request/response details, no configuration needed.

    [:octicons-arrow-right-24: HTML Reports](reporting/html-reports.md)

-   :material-rocket-launch:{ .lg .middle } __Parallel Execution__

    ---

    Run tests faster with built-in parallel execution support.

    [:octicons-arrow-right-24: Parallel Execution](features/parallel-execution.md)

-   :material-file-document:{ .lg .middle } __File Support__

    ---

    Load test data from JSON, YAML, or CSV files like Karate's `read()`.

    [:octicons-arrow-right-24: File Support](features/file-support.md)

-   :material-puzzle:{ .lg .middle } __Xray Integration__

    ---

    Export results to Jira Xray with automatic Cucumber JSON generation.

    [:octicons-arrow-right-24: Xray Integration](reporting/xray-integration.md)

</div>

---

## 🚀 Quick Example

=== "English"

    ```gherkin
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

=== "Spanish"

    ```gherkin
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

---

## 📦 Installation

```bash
pip install judo-framework
```

That's it! No additional dependencies or configuration needed.

---

## 🎯 What's New in v1.2.11

!!! success "Latest Release"
    
    - 🐛 **Fixed duplicate report generation** - Reports now generate only in configured `output_dir`
    - 🎨 **Cleaner console output** - New `console_format` parameter with minimalist `progress` format
    - 🥒 **Cucumber JSON export** - Automatic generation for Xray/Allure integration
    - 🔍 **Nested array search** - Search items in nested arrays with dot notation
    - 🔧 **Variable interpolation fixes** - Proper variable replacement everywhere

    [See full changelog](about/changelog.md){ .md-button }

---

## 🏃 Getting Started

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } __Install__

    ---

    ```bash
    pip install judo-framework
    ```

-   :material-file-code:{ .lg .middle } __Create Test__

    ---

    Create your first `.feature` file with test scenarios

    [:octicons-arrow-right-24: First Test](getting-started/first-test.md)

-   :material-play:{ .lg .middle } __Run Tests__

    ---

    ```bash
    behave
    ```

-   :material-chart-box:{ .lg .middle } __View Reports__

    ---

    Open `judo_reports/test_execution_report.html`

</div>

---

## 🌐 Complete HTTP Testing

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

---

## 🎭 Custom Runners

Create powerful test runners with advanced features:

```python
from judo.runner.base_runner import BaseRunner

class MyRunner(BaseRunner):
    def __init__(self):
        super().__init__(
            features_dir="features",
            output_dir="test_reports",
            console_format="progress",      # Clean output
            generate_cucumber_json=True,    # Xray integration
            parallel=True,                  # Faster execution
            max_workers=8
        )
    
    def run_smoke_tests(self):
        return self.run(tags=["@smoke"])

# Run tests
runner = MyRunner()
results = runner.run_smoke_tests()
```

[Learn more about runners](runners/creating-runners.md){ .md-button .md-button--primary }

---

## 📊 Automatic HTML Reports

Every test run generates a comprehensive HTML report with:

- ✅ Complete request/response details
- 📋 All scenarios and steps with status
- ⏱️ Execution times and performance metrics
- 🔍 Error messages with full stack traces
- 📈 Success rate and statistics
- 🎨 Clean, modern UI

**No configuration needed** - reports are generated automatically!

[See report examples](reporting/html-reports.md){ .md-button }

---

## 🤝 Contributing

We welcome contributions! Check out our [Contributing Guide](about/contributing.md) to get started.

---

## 📝 License

Judo Framework is released under the [MIT License](about/license.md).

---

## 🔗 Links

- [GitHub Repository](https://github.com/FelipeFariasAlfaro/Judo-Framework)
- [PyPI Package](https://pypi.org/project/judo-framework/)
- [Issue Tracker](https://github.com/FelipeFariasAlfaro/Judo-Framework/issues)
- [Changelog](about/changelog.md)

---

<div align="center">
  <p>Made with ❤️ by <a href="https://github.com/FelipeFariasAlfaro">Felipe Farias</a></p>
  <p><em>Inspired by the amazing <a href="https://karatelabs.github.io/karate/">Karate Framework</a></em></p>
</div>
