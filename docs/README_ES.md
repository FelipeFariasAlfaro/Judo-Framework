# 🥋 Judo Framework

**Un framework completo de testing de APIs para Python, inspirado en Karate Framework**

[![PyPI version](https://badge.fury.io/py/judo-framework.svg)](https://badge.fury.io/py/judo-framework)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[🇪🇸 Español](README_ES.md) | [🇺🇸 English](../README.md)

## 🚀 Inicio Rápido

```bash
pip install judo-framework
```

```python
from judo import Judo

# Crear instancia de Judo
judo = Judo()

# Hacer petición HTTP
response = judo.get("https://jsonplaceholder.typicode.com/users/1")

# Validar respuesta usando DSL similar a Karate
judo.match(response.status, 200)
judo.match(response.json["name"], "##string")
judo.match(response.json["email"], "##email")

print("✅ ¡Test pasó!")
```

## 🎯 Características Principales

- **🥋 DSL como Karate** - Sintaxis familiar para usuarios de Karate Framework
- **🥒 Integración BDD** - Soporte completo de Behave (Gherkin) con steps predefinidos
- **🌐 Testing HTTP** - Capacidades completas de testing de APIs REST
- **📄 Soporte de Archivos** - Manejo de datos de test JSON/YAML como la función `read()` de Karate
- **📊 Reportes HTML** - Reportes detallados automáticos con detalles de request/response
- **⚡ Ejecución Paralela** - Ejecuta tests en paralelo para máxima velocidad
- **🎭 Mock Server** - Servidor mock integrado para testing aislado
- **✅ Validación de Schema** - Soporte de validación de schema JSON
- **🔐 Autenticación** - Soporte JWT, OAuth, Basic Auth

## 🧪 Testing BDD (¡Igual que Karate!)

**features/api_test.feature:**
```gherkin
Feature: Testing de API
  Background:
    Given I set the base URL to "https://jsonplaceholder.typicode.com"
  
  @smoke
  Scenario: Obtener datos de usuario
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain:
      | field | value    |
      | name  | ##string |
      | email | ##email  |
      | id    | 1        |
    And the response should match "$.address.city" with "##string"
```

**features/environment.py:**
```python
from judo.behave import setup_judo_context

def before_all(context):
    setup_judo_context(context)
```

**Ejecutar tests:**
```bash
behave features/                    # Ejecutar todos los tests
behave features/ --tags @smoke      # Ejecutar solo smoke tests
```

## 🏃 Runners de Test Personalizados

```python
from judo.runner import BaseRunner

class MiTestRunner(BaseRunner):
    def __init__(self):
        super().__init__(
            features_dir="features",
            parallel=True,
            max_workers=6
        )
    
    def ejecutar_smoke_tests(self):
        return self.run(tags=["@smoke"])
    
    def ejecutar_api_tests_paralelo(self):
        self.set_parallel(True, max_workers=8)
        return self.run(tags=["@api"], exclude_tags=["@manual"])

# Uso
runner = MiTestRunner()
resultados = runner.ejecutar_smoke_tests()
print(f"Tests: {resultados['passed']}/{resultados['total']} pasaron")
```

## 📊 Reportes HTML Automáticos

Hermosos reportes HTML se generan automáticamente en `judo_reports/` con:
- 📋 Detalles completos de request/response
- ✅ Resultados de assertions con valores esperados vs actuales
- ⏱️ Métricas de rendimiento y timing
- 🔍 Seguimiento de errores y stack traces
- 📈 Estadísticas de ejecución de tests

## 🔧 Opciones de Instalación

**Instalación Básica (Recomendada):**
```bash
pip install judo-framework
```

**Con Características Opcionales:**
```bash
pip install judo-framework[crypto]    # Soporte JWT, OAuth, encriptación
pip install judo-framework[xml]       # Soporte XPath, testing SOAP  
pip install judo-framework[browser]   # Integración Selenium, Playwright
pip install judo-framework[full]      # Todas las características opcionales
```

## 📚 Documentación

| Tema | English | Español |
|------|---------|---------|
| Primeros Pasos | [📖 English](getting-started.md) | [📖 Español](getting-started_ES.md) |
| Referencia DSL | [📖 English](dsl-reference.md) | [📖 Español](dsl-reference_ES.md) |
| Integración Behave | [📖 English](behave-integration.md) | [📖 Español](behave-integration_ES.md) |
| Reportes HTML | [📖 English](html-reporting.md) | [📖 Español](html-reporting_ES.md) |
| Creando Runners | [📖 English](creating-runners.md) | [📖 Español](creating-runners_ES.md) |
| Ejemplos | [📖 English](examples.md) | [📖 Español](examples_ES.md) |
| Info del Autor | [📖 English](AUTHOR.md) | [📖 Español](AUTHOR_ES.md) |

## 🆚 Migración desde Karate

Judo Framework usa los mismos conceptos y sintaxis similar a Karate:

**Karate (JavaScript):**
```javascript
* def response = call read('get-user.feature')
* match response.name == '#string'
* match response.email == '#email'
```

**Judo (Python):**
```python
response = judo.get("/users/1")
judo.match(response.json["name"], "##string")
judo.match(response.json["email"], "##email")
```

## 🤝 Contribuir

¡Damos la bienvenida a contribuciones! Así es como empezar:

```bash
git clone https://github.com/judo-framework/judo
cd judo
pip install -e .[dev]
pytest tests/
```

## 📄 Licencia

Licencia MIT - Ver [LICENSE](../LICENSE) para detalles.

## 👨‍💻 Autor

**Creado por Felipe Farias en [CENTYC](https://www.centyc.cl)**

[CENTYC](https://www.centyc.cl) - Centro Latinoamericano de Testing y Calidad del Software

## 🙏 Reconocimientos

- Inspirado por [Karate Framework](https://github.com/karatelabs/karate) de Peter Thomas
- Desarrollado en [CENTYC](https://www.centyc.cl) para la comunidad de testing latinoamericana
- Construido para la comunidad global de testing de APIs en Python
- Agradecimientos especiales a todos los contribuidores

---

**Hecho con ❤️ en [CENTYC](https://www.centyc.cl) para la excelencia en testing de APIs**