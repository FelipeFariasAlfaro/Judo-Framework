<div align="center">
  <img src="assets/judo-framework-logo.png" alt="Judo Framework Logo" width="400"/>
  
  **A comprehensive API testing framework for Python, inspired by Karate Framework**
</div>

[![PyPI version](https://badge.fury.io/py/judo-framework.svg)](https://badge.fury.io/py/judo-framework)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/judo-framework)](https://pepy.tech/project/judo-framework)

[🇪🇸 Español](JUDO_STEPS_REFERENCE_EN.md) | [🇺🇸 English](JUDO_STEPS_REFERENCE_ES.md) |  [ep spanglish](JUDO_STEPS_REFERENCE_MIXED.md)

> **"As simple as Karate, as powerful as Python"**

Judo Framework brings the simplicity and elegance of Karate Framework to the Python ecosystem. Write API tests in plain English (or Spanish!), get beautiful HTML reports automatically, and enjoy the power of Python's ecosystem.

## 🎉 What's New in v1.5.9.2

### 🎨 NUEVA FUNCIONALIDAD: Reportes HTML Completamente Personalizables

Judo Framework v1.5.9.2 introduce un sistema revolucionario de personalización de reportes HTML, permitiendo a las empresas crear reportes con su identidad visual corporativa:

#### **🎨 Personalización Visual Completa**
- **Logos Personalizables** - Logo principal, secundario y de empresa con soporte Base64
- **Colores Corporativos** - Esquema completo de colores personalizables
- **Información del Proyecto** - Campos para ingeniero, equipo, producto y empresa
- **Gráficos Interactivos** - Gráficos tipo torta con Chart.js para visualización de resultados
- **Branding Empresarial** - Identidad visual completamente personalizable

#### **📊 Gráficos y Visualización**
- **Gráficos de Torta** - Distribución visual de escenarios y pasos
- **Gráficos de Barras** - Comparación de resultados (opcional)
- **Colores Personalizables** - Esquema de colores para cada estado
- **Interactividad** - Tooltips con porcentajes y detalles
- **Chart.js Integration** - Biblioteca moderna para gráficos interactivos

#### **⚙️ Sistema de Configuración**
- **Configuración JSON** - Sistema completo mediante archivos JSON
- **Múltiples Ubicaciones** - Búsqueda automática en ubicaciones estándar
- **Merge Inteligente** - Combinación de configuración por defecto con personalizada
- **Validación Robusta** - Manejo de errores y fallbacks automáticos

#### **📚 Documentación y Ejemplos**
- **CUSTOM_REPORTS_GUIDE.md** - Guía completa de uso y configuración
- **report_config_example.json** - Archivo de ejemplo con configuración completa
- **Casos de Uso Empresariales** - Ejemplos para diferentes tipos de organizaciones

### 🚀 Previous Major Features (v1.5.9.1)

#### **📋 Complete Contract Validation Suite** 🎯
- **OpenAPI/AsyncAPI Support** - Load and validate against industry-standard specifications
- **Schema Validation** - Comprehensive validation against specific schemas by name
- **Advanced Data Types** - Email, URL, UUID, ISO dates, phone numbers, credit cards
- **Nested Structures** - Recursive validation of complex object hierarchies
- **Request/Response Validation** - Complete contract compliance including headers and bodies
- **Endpoint Discovery** - Automatic validation of all contract endpoints
- **Pattern Matching** - Regex validation for custom field formats
- **Multi-Format Support** - JSON and YAML specification files

#### **📊 Framework Statistics**
- **354 @step decorators** implemented across all features
- **328 unique step functions** covering every testing scenario
- **162 English steps** with complete documentation
- **192 Spanish steps** with flexible syntax variants
- **100% verified** against actual source code
- **70+ enterprise features** fully operational

#### **🔧 Enhanced Step Distribution**
- **Basic Steps (≈40% - 140+ steps)**: Configuration, authentication, HTTP requests, basic validation
- **Advanced Validation (≈30% - 105+ steps)**: Arrays, JSONPath, schemas, data types
- **Enterprise Features (≈20% - 70+ steps)**: Circuit breakers, rate limiting, WebSocket, GraphQL
- **Contract Validation (≈10% - 35+ steps)**: OpenAPI, AsyncAPI, formats, structures

#### **📚 Updated Documentation**
- **JUDO_STEPS_REFERENCE_EN.md** - 162 unique steps documented and verified
- **JUDO_STEPS_REFERENCE_ES.md** - 166 unique steps with Spanish variants
- **Synchronization Rule** - Automatic verification that all documented steps exist in code
- **100% Accuracy** - Every documented step is guaranteed to work

### 🎯 Previous Major Features (v1.5.0)

#### **TIER 1: Robustness & Reliability** ⚡
- **Retry Policy** - Automatic retry with 4 backoff strategies (linear, exponential, fibonacci, random)
- **Circuit Breaker Pattern** - Prevent cascading failures with configurable thresholds
- **Request/Response Interceptors** - Modify requests and responses with custom logic
- **Rate Limiting & Throttling** - Token bucket rate limiter and fixed delay throttling
- **Advanced Assertions** - Response time, JSON schema, array validation, field matching

#### **TIER 2: Performance & Modern APIs** 📊
- **Data-Driven Testing** - Load test data from CSV, JSON, Excel files
- **Performance Monitoring** - Track response times (avg, p95, p99), error rates, throughput
- **Response Caching** - Automatic caching of GET requests with TTL support
- **GraphQL Support** - Execute GraphQL queries and mutations
- **WebSocket Support** - Real-time communication testing
- **OAuth2 & JWT** - Modern authentication methods with automatic token refresh

#### **TIER 3: Enterprise Features** 🏢
- **Multi-Format Reporting** - HTML, JSON, JUnit, Allure formats
- **Chaos Engineering** - Inject latency and errors for resilience testing
- **Advanced Logging** - Detailed request/response logging with configurable levels

### 📚 Complete Step References
- **English**: [JUDO_STEPS_REFERENCE_EN.md](JUDO_STEPS_REFERENCE_EN.md) - 162+ steps in English
- **Spanish**: [JUDO_STEPS_REFERENCE_ES.md](JUDO_STEPS_REFERENCE_ES.md) - 166+ pasos en español
- **Mixed Mode**: [JUDO_STEPS_REFERENCE_MIXED.md](JUDO_STEPS_REFERENCE_MIXED.md) - English keywords + Spanish steps

### 📖 Advanced Features Guide
- **Complete Guide**: [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md) - Detailed documentation of all advanced features
- **Contract Validation**: [examples/contract_validation_example.feature](examples/contract_validation_example.feature) - Complete contract testing examples

### 🎯 Showcase Examples
- **English**: [examples/showcase_advanced_features.feature](examples/showcase_advanced_features.feature)
- **Spanish**: [examples/showcase_completo_caracteristicas_avanzadas.feature](examples/showcase_completo_caracteristicas_avanzadas.feature)
- **Mixed Mode**: [examples/showcase_mixed_advanced_features.feature](examples/showcase_mixed_advanced_features.feature)
- **Contract Validation**: [examples/contract_validation_example.feature](examples/contract_validation_example.feature)

[See full changelog](CHANGELOG.md)

---

## 🌟 Why Judo Framework?

### 🏆 Most Complete API Testing Framework for Python

**354 step decorators** | **328 unique functions** | **70+ enterprise features** | **100% bilingual**

Judo Framework is officially the most comprehensive API testing framework in the Python ecosystem, offering unmatched coverage from basic HTTP testing to enterprise-grade contract validation.

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
```

### 🌎 Mixed Mode (NEW!)

Perfect for Latin American developers! Use English keywords with Spanish descriptions:

```gherkin
Feature: Pruebas de API de Usuarios

  Scenario: Crear un nuevo usuario
    Given la URL base es "https://api.example.com"
    When hago una petición POST a "/users" con el cuerpo:
      """
      {
        "name": "Juan Pérez",
        "email": "juan@example.com"
      }
      """
    Then el código de respuesta debe ser 201
    And la respuesta debe contener el campo "id"
```

**No language tag needed!** Spanish steps use `@step()` decorator, working with any keyword (Given/When/Then/And/But).

📚 [Complete Mixed Mode Guide](examples/README_mixed_mode.md) | [Mixed Mode Reference](judo-steps-reference-mixed.md)
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
# Install Judo Framework (pure API testing)
pip install judo-framework
```

> **API Testing Focused**: Judo Framework is now a pure API testing framework. If you need browser automation, install Playwright separately: `pip install playwright && playwright install chromium`

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

### 📊 Professional HTML Reports
Zero configuration, maximum insight with professional branding:

- **🏢 Official Branding**: CENTYC and Judo Framework logos in header and footer
- **🎨 Modern Design**: Beautiful gradient headers and responsive layout
- **📋 Request Details**: Method, URL, headers, body with syntax highlighting
- **📥 Response Details**: Status, headers, body, timing with color-coded status
- **✅ Assertions**: All validations with expected vs actual comparisons
- **💾 Variables**: Track variable usage and data flow across scenarios
- **📊 Statistics**: Success rate, timing, error tracking with visual indicators
- **🔗 Professional Footer**: Creator information and links to documentation
- **📱 Responsive Design**: Works perfectly on desktop and mobile devices

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

### 📖 Full Documentation by Language

**For complete step documentation, see:**

- **🇺🇸 English**: [JUDO_STEPS_REFERENCE_EN.md](JUDO_STEPS_REFERENCE_EN.md)
  - 100+ predefined steps in English
  - Configuration, Authentication, HTTP Requests, Validation, Data Extraction
  - Tier 1, 2, 3 advanced features
  - Pattern matching and utilities

- **🇪🇸 Spanish**: [JUDO_STEPS_REFERENCE_ES.md](JUDO_STEPS_REFERENCE_ES.md)
  - 100+ pasos predefinidos en español
  - Configuración, Autenticación, Peticiones HTTP, Validación, Extracción de Datos
  - Características avanzadas Tier 1, 2, 3
  - Patrones y utilidades

- **🌎 Mixed Mode**: [JUDO_STEPS_REFERENCE_MIXED.md](JUDO_STEPS_REFERENCE_MIXED.md)
  - English keywords + Spanish step descriptions
  - Perfect for Latin American teams
  - All features in mixed mode format

### 🔧 Quick Reference - Configuration Steps

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

### 🔐 Quick Reference - Authentication Steps

**English:**
- `Given I use bearer token "{token}"`
- `Given I use basic authentication with username "{user}" and password "{pass}"`
- `Given I setup OAuth2 with:` (table format)
- `Given I setup JWT with secret "{secret}" and algorithm "{algorithm}"`

**Spanish:**
- `Dado que uso el token bearer "{token}"`
- `Dado que uso autenticación básica con usuario "{usuario}" y contraseña "{password}"`
- `Dado que configuro OAuth2 con:` (formato tabla)
- `Dado que configuro JWT con secreto "{secreto}" y algoritmo "{algoritmo}"`

### 🌐 Quick Reference - HTTP Request Steps

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

### ✅ Quick Reference - Validation Steps

**English:**
- `Then the response status should be {status}`
- `Then the response should be successful`
- `Then the response should contain "{field}"`
- `Then the response field "{field}" should equal "{value}"`
- `Then the response should be an array`
- `Then the response array should have {count} items`
- `Then the response time should be less than {max_time} milliseconds`
- `Then the response should match JSON schema:`

**Spanish:**
- `Entonces el código de respuesta debe ser {status}`
- `Entonces la respuesta debe ser exitosa`
- `Entonces la respuesta debe contener el campo "{campo}"`
- `Entonces el campo "{campo}" debe ser "{valor}"`
- `Entonces la respuesta debe ser un array`
- `Entonces la respuesta debe tener {count} elementos`
- `Entonces el tiempo de respuesta debe ser menor a {max_time} milisegundos`
- `Entonces la respuesta debe coincidir con el esquema JSON:`

### 💾 Quick Reference - Data Extraction Steps

**English:**
- `When I extract "{path}" from the response as "{variable}"`
- `When I store the response as "{variable}"`

**Spanish:**
- `Cuando guardo el valor del campo "{campo}" en la variable "{variable}"`
- `Cuando guardo la respuesta completa en la variable "{variable}"`

### 🔄 Quick Reference - Variable Comparison Steps

**English:**
- `Then the variable "{var1}" should equal the variable "{var2}"`
- `Then the variable "{var1}" should not equal the variable "{var2}"`

**Spanish:**
- `Entonces la variable "{var1}" debe ser igual a la variable "{var2}"`
- `Entonces la variable "{var1}" no debe ser igual a la variable "{var2}"`

### 🚀 Advanced Features Steps (v1.5.9.1)

**Contract Validation (NEW!):**
- `Given I load OpenAPI contract from "{contract_file}"`
- `Given I load AsyncAPI contract from "{contract_file}"`
- `Then the response should match the contract schema`
- `Then the response field "{field_path}" should be of type "{expected_type}"`
- `Then the response field "{field_path}" should be a valid email`
- `Then the response field "{field_path}" should be a valid URL`
- `Then the response field "{field_path}" should be a valid UUID`
- `Then the response should have nested structure`
- `When I validate request body against contract for {method} {path}`
- `Then the response should match data contract specification`

**Retry & Circuit Breaker:**
- `Given I set retry policy with max_retries={count} and backoff_strategy="{strategy}"`
- `Given I create a circuit breaker named "{name}" with failure_threshold={threshold}`

**Rate Limiting:**
- `Given I set rate limit to {requests} requests per second`
- `Given I set throttle with delay {delay} milliseconds`

**Performance Monitoring:**
- `When I send {count} GET requests to "{endpoint}"`
- `Then I should have performance metrics:` (table format)

**Response Caching:**
- `Given I enable response caching with TTL {ttl} seconds`
- `Then the second response should come from cache`

**Data-Driven Testing:**
- `Given I load test data from file "{file_path}"`
- `When I run data-driven test for each row`

**GraphQL:**
- `When I execute GraphQL query:` (query in text)
- `When I execute GraphQL mutation:` (mutation in text)

**WebSocket:**
- `Given I connect to WebSocket "{url}"`
- `When I send WebSocket message:` (message in text)

**Chaos Engineering:**
- `Given I enable chaos engineering`
- `Given I inject latency between {min} and {max} milliseconds`
- `Given I inject error rate of {percentage} percent`

**See complete documentation in:**
- [JUDO_STEPS_REFERENCE_EN.md](JUDO_STEPS_REFERENCE_EN.md) - Full English reference (162+ steps)
- [JUDO_STEPS_REFERENCE_ES.md](JUDO_STEPS_REFERENCE_ES.md) - Full Spanish reference (166+ steps)
- [JUDO_STEPS_REFERENCE_MIXED.md](JUDO_STEPS_REFERENCE_MIXED.md) - Full Mixed mode reference

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

#### Custom Runner
```python
# Runner/runner.py
from judo.runner.base_runner import BaseRunner
import os

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

#### Installation Issues
```bash
# Clear pip cache and reinstall
pip cache purge
pip install --upgrade judo-framework
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

# Check all dependencies
pip list | grep -E "judo|behave|requests"
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
| **Contract Validation** | ✅ Basic | ✅ **Advanced** |
| **Step Count** | ~50 steps | **354 steps** |
| **Enterprise Features** | ✅ Some | ✅ **70+ features** |
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
- **Version**: 1.5.9.1
- **Steps**: 354 @step decorators / 328 unique functions
- **Features**: 70+ enterprise-grade capabilities
- **Languages**: English + Spanish (100% bilingual)
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

---

## 📈 Framework Statistics

### 🎯 By the Numbers

| Metric | Count | Description |
|--------|-------|-------------|
| **@step Decorators** | 354 | Total step implementations |
| **Unique Functions** | 328 | Distinct step functions |
| **English Steps** | 162 | Steps with English syntax |
| **Spanish Steps** | 192 | Steps with Spanish variants |
| **Enterprise Features** | 70+ | Advanced capabilities |
| **Test Categories** | 4 | Basic, Advanced, Enterprise, Contracts |
| **Validation Tests** | 18/18 | All validation tests passing |
| **Documentation Coverage** | 100% | Every step documented and verified |

### 📊 Step Distribution

- **🔧 Basic Steps (40%)**: Configuration, authentication, HTTP requests, basic validation
- **📊 Advanced Validation (30%)**: Arrays, JSONPath, schemas, data types  
- **🚀 Enterprise Features (20%)**: Circuit breakers, rate limiting, WebSocket, GraphQL
- **📋 Contract Validation (10%)**: OpenAPI, AsyncAPI, formats, structures

### 🏆 Industry Leadership

**Judo Framework is officially the most comprehensive API testing framework in the Python ecosystem**, offering more steps, features, and capabilities than any other solution.
