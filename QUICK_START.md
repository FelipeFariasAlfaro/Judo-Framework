# 🚀 Judo Framework - Quick Start Guide

Get started with Judo Framework in less than 5 minutes!

---

## 📦 Step 1: Install (30 seconds)

```bash
pip install judo-framework
```

---

## 📝 Step 2: Create Your First Test (2 minutes)

### Create Feature File

**features/my_first_test.feature:**
```gherkin
Feature: My First API Test

  Scenario: Get user information
    Given the base URL is "https://jsonplaceholder.typicode.com"
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "name"
    And the response should contain "email"
```

### Create Environment File

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

---

## 🏃 Step 3: Run Your Test (30 seconds)

```bash
behave features/
```

**You'll see:**
```
🥋 Judo Framework - Captura automática de reportes activada

📋 Feature: My First API Test
  📝 Scenario: Get user information
    ✅ Given the base URL is "https://jsonplaceholder.typicode.com"
    ✅ When I send a GET request to "/users/1"
    ✅ Then the response status should be 200
    ✅ And the response should contain "name"
    ✅ And the response should contain "email"
  ✅ Scenario completado: Get user information

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

## 🎉 That's It!

You now have:
- ✅ A working API test
- ✅ Automatic HTML report in `judo_reports/`
- ✅ Complete test execution tracking
- ✅ Beautiful console output

---

## 🇪🇸 En Español

### Crear Feature en Español

**features/mi_primer_test.feature:**
```gherkin
# language: es
Característica: Mi Primera Prueba de API

  Escenario: Obtener información de usuario
    Dado que la URL base es "https://jsonplaceholder.typicode.com"
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener el campo "name"
    Y la respuesta debe contener el campo "email"
```

### Mismo environment.py

No changes needed! The same `environment.py` works for both English and Spanish.

---

## 📚 Next Steps

### Learn More Steps

**Common Steps:**
```gherkin
# Configuration
Given the base URL is "{url}"
Given I set the header "{name}" to "{value}"
Given I use bearer token "{token}"

# HTTP Requests
When I send a GET request to "{endpoint}"
When I send a POST request to "{endpoint}" with JSON:
  """
  {"key": "value"}
  """
When I send a PUT request to "{endpoint}" with JSON:
When I send a DELETE request to "{endpoint}"

# Validations
Then the response status should be {status}
Then the response should contain "{field}"
Then the response field "{field}" should equal "{value}"
Then the response should be an array

# Data Extraction
When I extract "{field}" from the response as "{variable}"
When I store the response as "{variable}"
```

### Spanish Steps

```gherkin
# Configuración
Dado que la URL base es "{url}"
Dado que establezco el header "{nombre}" a "{valor}"
Dado que uso el token bearer "{token}"

# Peticiones HTTP
Cuando hago una petición GET a "{endpoint}"
Cuando hago una petición POST a "{endpoint}" con el cuerpo:
  """
  {"clave": "valor"}
  """
Cuando hago una petición PUT a "{endpoint}" con el cuerpo:
Cuando hago una petición DELETE a "{endpoint}"

# Validaciones
Entonces el código de respuesta debe ser {status}
Entonces la respuesta debe contener el campo "{campo}"
Entonces el campo "{campo}" debe ser "{valor}"
Entonces la respuesta debe ser un array

# Extracción de Datos
Cuando guardo el valor del campo "{campo}" en la variable "{variable}"
Cuando guardo la respuesta completa en la variable "{variable}"
```

---

## 🎯 Common Use Cases

### POST Request

```gherkin
Scenario: Create a new user
  Given the base URL is "https://api.example.com"
  When I send a POST request to "/users" with JSON:
    """
    {
      "name": "John Doe",
      "email": "john@example.com",
      "age": 30
    }
    """
  Then the response status should be 201
  And the response should contain "id"
  And I extract "id" from the response as "userId"
```

### Using Variables

```gherkin
Scenario: Create and update user
  Given the base URL is "https://api.example.com"
  
  # Create user
  When I send a POST request to "/users" with JSON:
    """
    {"name": "John", "email": "john@example.com"}
    """
  Then the response status should be 201
  And I extract "id" from the response as "userId"
  
  # Update user
  When I send a PUT request to "/users/{userId}" with JSON:
    """
    {"name": "John Updated"}
    """
  Then the response status should be 200
```

### Authentication

```gherkin
Scenario: Authenticated request
  Given the base URL is "https://api.example.com"
  And I use bearer token "your-token-here"
  When I send a GET request to "/protected/resource"
  Then the response status should be 200
```

---

## 📊 View Your Reports

After running tests, open the HTML report:

```bash
# On Windows
start judo_reports\test_report_*.html

# On macOS
open judo_reports/test_report_*.html

# On Linux
xdg-open judo_reports/test_report_*.html
```

The report includes:
- 📋 All scenarios and steps
- ✅ Pass/fail status
- ⏱️ Execution times
- 🔍 Request/response details
- 📈 Statistics

---

## 🆘 Need Help?

### Documentation
- 📖 [Full Documentation](docs/)
- 📖 [Examples](examples/)
- 📖 [DSL Reference](docs/dsl-reference.md)

### Community
- 💬 [GitHub Discussions](https://github.com/judo-framework/judo/discussions)
- 🐛 [Report Issues](https://github.com/judo-framework/judo/issues)
- 📧 Email: felipe.farias@centyc.cl

### Quick Tips
1. **Use `--tags`** to run specific tests:
   ```bash
   behave --tags @smoke
   ```

2. **Run in parallel** for faster execution:
   ```python
   from judo.runner import ParallelRunner
   runner = ParallelRunner(features_dir="features", max_workers=4)
   runner.run()
   ```

3. **Load test data from files**:
   ```gherkin
   When I POST to "/users" with JSON file "test_data/user.json"
   ```

---

## 🎓 Learn More

### Tutorials
1. [Getting Started Guide](docs/getting-started.md)
2. [Behave Integration](docs/behave-integration.md)
3. [Creating Custom Runners](docs/creating-runners.md)
4. [HTML Reporting](docs/html-reporting.md)

### Examples
- [Basic Example](examples/basic_example.py)
- [Advanced Example](examples/advanced_example.py)
- [BDD Example](examples/behave_example.py)
- [Spanish Example](examples/EJEMPLO_POST.feature)

---

## ✨ Pro Tips

### 1. Organize Your Tests

```
project/
├── features/
│   ├── environment.py
│   ├── smoke/
│   │   └── critical_apis.feature
│   ├── regression/
│   │   └── full_suite.feature
│   └── integration/
│       └── workflows.feature
└── test_data/
    ├── users/
    └── products/
```

### 2. Use Tags

```gherkin
@smoke @critical
Scenario: Critical API test
  # Your test here

@regression
Scenario: Full regression test
  # Your test here
```

Run specific tags:
```bash
behave --tags @smoke
behave --tags @critical
behave --tags @smoke,@critical  # OR
behave --tags @smoke --tags @critical  # AND
```

### 3. Data-Driven Testing

```gherkin
Scenario Outline: Test multiple users
  When I send a POST request to "/users" with JSON:
    """
    {"name": "<name>", "email": "<email>"}
    """
  Then the response status should be 201
  
  Examples:
    | name  | email           |
    | John  | john@test.com   |
    | Jane  | jane@test.com   |
    | Bob   | bob@test.com    |
```

---

## 🚀 You're Ready!

You now know enough to:
- ✅ Write API tests in English or Spanish
- ✅ Run tests and get reports
- ✅ Use variables and data extraction
- ✅ Organize your test suite
- ✅ Use advanced features

**Happy Testing!** 🥋

---

**Made with ❤️ at CENTYC for API testing excellence**
