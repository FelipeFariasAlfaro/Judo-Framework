<div align="center">
  <img src="assets/logos/logo_judo.png" alt="Judo Framework Logo" width="200"/>

  # Judo Framework

  **Framework completo de pruebas de API para Python, inspirado en Karate Framework**

  [![PyPI version](https://badge.fury.io/py/judo-framework.svg)](https://badge.fury.io/py/judo-framework)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Downloads](https://pepy.tech/badge/judo-framework)](https://pepy.tech/project/judo-framework)

  *"As simple as Karate, as powerful as Python"*
</div>

---

## ¿Qué es Judo Framework?

Judo Framework trae la simplicidad de Karate Framework al ecosistema Python. Escribe pruebas de API en lenguaje natural (inglés o español), obtén reportes HTML automáticos y aprovecha el poder del ecosistema Python.

**199 pasos en inglés · 229 pasos en español · Evaluación de GenAI · Mock Server integrado · Reportes HTML personalizables**

---

## Instalación

```bash
pip install judo-framework
```

Para funcionalidades específicas:

```bash
pip install judo-framework[excel]      # Soporte Excel
pip install judo-framework[websocket]  # WebSocket
pip install judo-framework[graphql]    # GraphQL
pip install judo-framework[full]       # Todo incluido
```

---

## Inicio rápido

### 1. Crear el feature

```gherkin
# features/api_test.feature
Feature: Pruebas de API

  Scenario: Obtener usuario
    Given the base URL is "https://jsonplaceholder.typicode.com"
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "name"
```

### 2. Configurar environment.py

```python
# features/environment.py
from judo.behave import *

before_all      = before_all_judo
before_feature  = before_feature_judo
after_feature   = after_feature_judo
before_scenario = before_scenario_judo
after_scenario  = after_scenario_judo
before_step     = before_step_judo
after_step      = after_step_judo
after_all       = after_all_judo
```

### 3. Ejecutar

```bash
behave features/
```

Los reportes HTML se generan automáticamente en `judo_reports/`.

---

## Soporte bilingüe completo

### Inglés

```gherkin
Feature: User API

  Scenario: Create user
    Given the base URL is "https://api.example.com"
    And I use bearer token "my-token"
    When I send a POST request to "/users" with JSON:
      """
      {"name": "John Doe", "email": "john@example.com"}
      """
    Then the response status should be 201
    And the response field "name" should equal "John Doe"
    And I extract "id" from the response as "userId"
```

### Español

```gherkin
# language: es
Característica: API de Usuarios

  Escenario: Crear usuario
    Dado que la URL base es "https://api.example.com"
    Y uso el token bearer "mi-token"
    Cuando hago una petición POST a "/users" con el cuerpo:
      """
      {"name": "Juan Pérez", "email": "juan@example.com"}
      """
    Entonces el código de respuesta debe ser 201
    Y el campo "name" debe ser "Juan Pérez"
    Y guardo el valor del campo "id" en la variable "userId"
```

### Modo mixto

```gherkin
Feature: API de Usuarios

  Scenario: Crear usuario
    Given la URL base es "https://api.example.com"
    When hago una petición POST a "/users" con el cuerpo:
      """
      {"name": "Juan Pérez"}
      """
    Then el código de respuesta debe ser 201
```

---

## Evaluación de GenAI (nuevo)

Judo permite evaluar respuestas de sistemas de IA generativa. El flujo es: llamas tu API GenAI con pasos REST normales, extraes la respuesta y la evalúas con tres estrategias.

### Configuración en .env (solo para el juez LLM)

```env
JUDO_AI_PROVIDER=openai        # openai | claude | gemini
JUDO_OPENAI_API_KEY=sk-...
JUDO_AI_MODEL=gpt-4o
```

### Importar en environment.py

```python
from judo.genai.steps_genai_es import *   # español
# from judo.genai.steps_genai import *    # inglés
```

### Estrategia 1: RAG — comparar contra documentos

```gherkin
Dado que cargo el contexto RAG desde el archivo "docs/manual.pdf"
Cuando envío una petición POST a "/chat" con el cuerpo
  """
  {"pregunta": "¿Cuál es el precio del plan básico?"}
  """
Entonces el código de respuesta debe ser 200
Y uso el campo de respuesta "respuesta" como respuesta de IA
Y la respuesta de IA debe estar fundamentada en el contexto RAG con umbral 0.7
```

### Estrategia 2: Validaciones semánticas

```gherkin
Cuando envío una petición POST a "/ai/explain" con el cuerpo
  """
  {"topic": "HTTP methods"}
  """
Entonces el código de respuesta debe ser 200
Y uso el campo de respuesta "explanation" como respuesta de IA
Y la respuesta de IA no debe ser tóxica con umbral 0.9
Y la respuesta de IA debe ser relevante para "HTTP methods" con umbral 0.4
Y la respuesta de IA debe cubrir los temas requeridos con umbral 0.8
  | tema   |
  | GET    |
  | POST   |
  | DELETE |
```

### Estrategia 3: LLM como juez

```gherkin
Dado que configuro el juez de IA con proveedor "openai" y modelo "gpt-4o"
Y establezco el prompt del juez como "Explica qué es una API REST"
Cuando envío una petición POST a "/ai/explain" con el cuerpo
  """
  {"question": "Explica qué es una API REST"}
  """
Entonces el código de respuesta debe ser 200
Y uso el campo de respuesta "answer" como respuesta de IA
Y evalúo la respuesta de IA con el juez usando umbral 0.7
  """
  La respuesta debe explicar correctamente REST,
  mencionar al menos un método HTTP y ser comprensible.
  """
Y la evaluación del juez debe pasar
```

---

## Mock Server integrado

```python
from judo import Judo

judo = Judo()
mock = judo.start_mock(port=8080)

mock.get("/api/users", {
    "status": 200,
    "body": [{"id": 1, "name": "Juan"}, {"id": 2, "name": "Ana"}]
})
mock.post("/api/users", {"status": 201, "body": {"id": 3, "message": "Created"}})
mock.get("/api/users/*", {"status": 200, "body": {"id": 1, "name": "Juan"}})

# Ejecutar pruebas contra http://localhost:8080
judo.stop_mock()
```

Desde CLI:

```bash
judo mock --port 8080
```

---

## Reportes HTML personalizables

Crea un archivo `report_config.json` en `judo_reports/`:

```json
{
  "project": {
    "name": "Mi Proyecto - API Tests",
    "engineer": "Ana García",
    "team": "Equipo QA",
    "company": "Mi Empresa S.A."
  },
  "branding": {
    "primary_logo": "data:image/png;base64,TU_LOGO_AQUI",
    "primary_color": "#1e40af",
    "secondary_color": "#3b82f6"
  },
  "theme": {
    "background_color": "#f0f2f5"
  },
  "charts": {
    "enabled": true,
    "type": "doughnut",
    "animation": true
  },
  "footer": {
    "show_creator": false,
    "show_logo": true,
    "company_name": "Mi Empresa S.A.",
    "company_url": "https://www.miempresa.com"
  }
}
```

El reporte incluye gráficos donut animados, detalles de request/response, métricas de rendimiento y branding corporativo completo.

---

## Características principales

### Pruebas REST completas

```gherkin
Scenario: CRUD completo
  Given the base URL is "https://api.example.com"

  When I send a POST request to "/users" with JSON:
    """
    {"name": "John", "email": "john@example.com"}
    """
  Then the response status should be 201
  And I extract "id" from the response as "userId"

  When I send a GET request to "/users/{userId}"
  Then the response status should be 200
  And the response field "name" should equal "John"

  When I send a DELETE request to "/users/{userId}"
  Then the response status should be 204
```

### Autenticación

```gherkin
Given I use bearer token "eyJhbGci..."
Given I use basic authentication with username "admin" and password "secret"
```

### Validación de esquemas JSON

```gherkin
Then the response should match schema file "schemas/user.json"
Then the response should match JSON schema:
  """
  {
    "type": "object",
    "required": ["id", "name", "email"],
    "properties": {
      "id": {"type": "integer"},
      "name": {"type": "string"},
      "email": {"type": "string", "format": "email"}
    }
  }
  """
```

### Ejecución paralela

```python
from judo.runner.base_runner import BaseRunner

runner = BaseRunner(
    features_dir="features",
    parallel=True,
    max_workers=8,
    output_dir="judo_reports"
)
runner.run_all_features()
```

### Características avanzadas

- **Circuit Breaker** — previene fallos en cascada
- **Retry con backoff** — reintentos automáticos (linear, exponential, fibonacci)
- **Rate limiting** — respeta límites de la API
- **Caché de respuestas** — evita requests repetidos
- **WebSocket** — pruebas en tiempo real
- **GraphQL** — queries y mutations
- **Chaos Engineering** — inyección de latencia y errores
- **Data-driven testing** — desde CSV, JSON, Excel
- **Monitoreo de performance** — avg, p95, p99, error rate
- **Validación de contratos OpenAPI** — verifica cumplimiento de specs

---

## Estructura de proyecto recomendada

```
mi_proyecto/
├── .env                      # Variables de entorno
├── features/
│   ├── environment.py        # Configuración de Behave
│   ├── api_tests.feature
│   └── steps/                # Pasos personalizados (opcional)
├── test_data/
│   └── users.json
├── judo_reports/
│   └── report_config.json    # Configuración de reportes
└── runner.py                 # Runner personalizado (opcional)
```

### Runner personalizado

```python
from judo.runner.base_runner import BaseRunner

class MiRunner(BaseRunner):
    def __init__(self):
        super().__init__(
            features_dir="features",
            output_dir="judo_reports",
            parallel=True,
            max_workers=4
        )

if __name__ == "__main__":
    runner = MiRunner()
    success = runner.run_all_features()
    exit(0 if success else 1)
```

---

## Variables de entorno (.env)

```env
# Directorios
JUDO_FEATURES_DIR=features
JUDO_OUTPUT_DIR=judo_reports

# Ejecución
JUDO_PARALLEL=false
JUDO_MAX_WORKERS=4
JUDO_TIMEOUT=300
JUDO_RETRY_COUNT=0
JUDO_FAIL_FAST=false

# Reportes
JUDO_GENERATE_CUCUMBER_JSON=true
JUDO_SAVE_REQUESTS_RESPONSES=false
JUDO_REPORT_CONFIG_FILE=judo_reports/report_config.json

# GenAI (solo para evaluación con LLM como juez)
JUDO_AI_PROVIDER=openai
JUDO_OPENAI_API_KEY=sk-...
JUDO_AI_MODEL=gpt-4o
JUDO_AI_TEMPERATURE=0.0
```

---

## Integración CI/CD

### GitHub Actions

```yaml
name: API Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install judo-framework
      - run: python runner.py
      - uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: judo_reports/
```

---

## Documentación

| Recurso | Descripción |
|---|---|
| [documentacion/JUDO_STEPS_REFERENCE_ES.md](documentacion/JUDO_STEPS_REFERENCE_ES.md) | Referencia completa de pasos en español |
| [documentacion/JUDO_STEPS_REFERENCE_EN.md](documentacion/JUDO_STEPS_REFERENCE_EN.md) | Complete step reference in English |
| [documentacion/referencia_judo.md](documentacion/referencia_judo.md) | Referencia consolidada del framework |
| [documentacion/GUIA_INSTALACION_Y_CONFIGURACION.txt](documentacion/GUIA_INSTALACION_Y_CONFIGURACION.txt) | Guía de instalación y configuración |
| [documentacion/CUSTOM_REPORTS_GUIDE.txt](documentacion/CUSTOM_REPORTS_GUIDE.txt) | Guía de reportes personalizables |
| [documentacion/GUIA_LOGOS_REPORTES.txt](documentacion/GUIA_LOGOS_REPORTES.txt) | Guía de logos en reportes |
| [examples/](examples/) | Ejemplos de features y configuración |

---

## Conteo de pasos

| Archivo | Pasos |
|---|---|
| `judo/behave/steps.py` (inglés) | 162 |
| `judo/behave/steps_es.py` (español) | 192 |
| `judo/genai/steps_genai.py` (GenAI inglés) | 37 |
| `judo/genai/steps_genai_es.py` (GenAI español) | 37 |
| **Total inglés** | **199** |
| **Total español** | **229** |

---

## Soporte

- **GitHub Issues**: [github.com/FelipeFariasAlfaro/Judo-Framework/issues](https://github.com/FelipeFariasAlfaro/Judo-Framework/issues)
- **Email**: felipe.farias@centyc.cl
- **Documentación**: [centyc.cl/judo-framework](http://centyc.cl/judo-framework/)

---

## Licencia

MIT License — ver [LICENSE](LICENSE)

---

<div align="center">
  Creado por <a href="https://www.centyc.cl">CENTYC</a> · Felipe Farias
</div>
