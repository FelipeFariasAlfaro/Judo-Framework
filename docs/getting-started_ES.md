# 🚀 Primeros Pasos - Judo Framework

Esta guía te ayudará a empezar con Judo Framework para testing de APIs en Python.

**Creado por Felipe Farias en [CENTYC](https://www.centyc.cl) - Centro Latinoamericano de Testing y Calidad del Software**

## 📦 Instalación

### Instalación Básica

```bash
pip install judo-framework
```

### Instalación con Características Opcionales

```bash
# Para soporte de criptografía (JWT, OAuth)
pip install judo-framework[crypto]

# Para soporte XML (XPath, SOAP)
pip install judo-framework[xml]

# Para testing de navegadores (Selenium, Playwright)
pip install judo-framework[browser]

# Instalación completa
pip install judo-framework[full]
```

## 🎯 Tu Primer Test

### 1. Test Básico con DSL

Crea un archivo `mi_primer_test.py`:

```python
from judo import Judo

# Crear instancia de Judo
judo = Judo()

# Hacer petición GET
response = judo.get("https://jsonplaceholder.typicode.com/users/1")

# Validar respuesta
judo.match(response.status, 200)
judo.match(response.json["name"], "##string")
judo.match(response.json["email"], "##email")
judo.match(response.json["id"], 1)

print("✅ ¡Test pasó!")
```

Ejecutar:
```bash
python mi_primer_test.py
```

### 2. Test con BDD (Behave)

#### Paso 1: Crear estructura de proyecto

```
mi_proyecto/
├── features/
│   ├── environment.py
│   └── mi_primer_test.feature
└── requirements.txt
```

#### Paso 2: Configurar environment.py

**features/environment.py:**
```python
from judo.behave import setup_judo_context

def before_all(context):
    setup_judo_context(context)
    print("🥋 Judo Framework configurado")

def after_scenario(context, scenario):
    status = "✅" if scenario.status == "passed" else "❌"
    print(f"{status} {scenario.name}")
```

#### Paso 3: Escribir tu primer feature

**features/mi_primer_test.feature:**
```gherkin
Feature: Mi primer test con Judo
  
  Background:
    Given I set the base URL to "https://jsonplaceholder.typicode.com"
  
  @smoke
  Scenario: Obtener información de usuario
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain:
      | field | value    |
      | id    | 1        |
      | name  | ##string |
      | email | ##email  |
    And the response should match "$.address.city" with "##string"
```

#### Paso 4: Ejecutar tests

```bash
behave features/
```

## 🔧 Conceptos Básicos

### Variables

```python
from judo import Judo

judo = Judo()

# Establecer variables
judo.set("baseUrl", "https://api.example.com")
judo.set("userId", 123)
judo.set("apiKey", "mi-api-key")

# Usar variables
base_url = judo.get("baseUrl")
user_id = judo.get("userId")

response = judo.get(f"{base_url}/users/{user_id}")
```

### Matching Patterns

```python
from judo import Judo

judo = Judo()
response = judo.get("https://jsonplaceholder.typicode.com/users/1")

# Matching de tipos
judo.match(response.json["id"], "##number")
judo.match(response.json["name"], "##string")
judo.match(response.json["email"], "##email")
judo.match(response.json["website"], "##url")

# Matching de valores exactos
judo.match(response.json["id"], 1)
judo.match(response.json["name"], "Leanne Graham")

# Matching de arrays y objetos
judo.match(response.json["address"], "##object")
judo.match(response.json["address"]["geo"], "##object")
```

### Peticiones HTTP

```python
from judo import Judo

judo = Judo()

# GET
response = judo.get("https://api.example.com/users")

# POST con JSON
datos = {"name": "Juan", "email": "juan@example.com"}
response = judo.post("https://api.example.com/users", datos)

# PUT
datos_actualizados = {"name": "Juan Pérez"}
response = judo.put("https://api.example.com/users/1", datos_actualizados)

# DELETE
response = judo.delete("https://api.example.com/users/1")

# Con headers personalizados
judo.set_header("Authorization", "Bearer mi-token")
judo.set_header("Content-Type", "application/json")
response = judo.get("https://api.example.com/protected")
```

## 📊 Reportes HTML

Los reportes HTML se generan automáticamente en la carpeta `judo_reports/`:

```python
from judo import Judo

judo = Judo()

# Hacer varias peticiones
judo.get("https://jsonplaceholder.typicode.com/users/1")
judo.get("https://jsonplaceholder.typicode.com/posts/1")
judo.post("https://jsonplaceholder.typicode.com/users", {"name": "Test"})

# Los reportes se generan automáticamente
print("📊 Ver reportes en: judo_reports/test_report.html")
```

## 🏃 Runners Personalizados

```python
from judo.runner import BaseRunner

class MiRunner(BaseRunner):
    def __init__(self):
        super().__init__(
            features_dir="features",
            output_dir="mis_reportes"
        )
    
    def ejecutar_smoke_tests(self):
        """Ejecutar solo smoke tests"""
        return self.run(tags=["@smoke"])
    
    def ejecutar_todos_los_tests(self):
        """Ejecutar todos los tests"""
        return self.run()

# Usar el runner
runner = MiRunner()
resultados = runner.ejecutar_smoke_tests()
print(f"Tests: {resultados['passed']}/{resultados['total']} pasaron")
```

## 📄 Trabajando con Archivos

### Leer Datos de Archivos

**datos/usuario.json:**
```json
{
  "name": "María García",
  "email": "maria@example.com",
  "age": 28
}
```

**Código Python:**
```python
from judo import Judo

judo = Judo()

# Leer archivo JSON
datos_usuario = judo.read("datos/usuario.json")

# Usar en petición
response = judo.post("https://api.example.com/users", datos_usuario)
judo.match(response.status, 201)
```

### Validación de Schema

**schemas/usuario_schema.json:**
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "name": {"type": "string"},
    "email": {"type": "string", "format": "email"}
  },
  "required": ["id", "name", "email"]
}
```

**Validación:**
```python
from judo import Judo

judo = Judo()
response = judo.get("https://api.example.com/users/1")

# Cargar y validar schema
schema = judo.read("schemas/usuario_schema.json")
judo.match_schema(response.json, schema)
```

## 🔐 Autenticación

### Bearer Token (JWT)

```python
from judo import Judo

judo = Judo()

# Establecer token
judo.bearer_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")

# O usando header directamente
judo.set_header("Authorization", "Bearer tu-token-aqui")

response = judo.get("https://api.example.com/protected")
```

### Autenticación Básica

```python
from judo import Judo

judo = Judo()

# Establecer credenciales básicas
judo.basic_auth("usuario", "contraseña")

response = judo.get("https://api.example.com/protected")
```

## 🎭 Mock Server

```python
from judo import Judo
from judo.mock import MockServer

# Crear y configurar mock server
mock = MockServer(port=8080)
mock.add_route("GET", "/users/1", {
    "id": 1,
    "name": "Usuario Mock",
    "email": "mock@example.com"
})

# Iniciar mock
mock.start()

# Testear contra mock
judo = Judo()
response = judo.get("http://localhost:8080/users/1")
judo.match(response.status, 200)
judo.match(response.json["name"], "Usuario Mock")

# Detener mock
mock.stop()
```

## 🚀 Próximos Pasos

1. **Explora más ejemplos:** [Ejemplos](examples_ES.md)
2. **Aprende el DSL completo:** [Referencia DSL](dsl-reference_ES.md)
3. **Integración avanzada con Behave:** [Integración Behave](behave-integration_ES.md)
4. **Crea runners personalizados:** [Creando Runners](creating-runners_ES.md)
5. **Configura reportes HTML:** [Reportes HTML](html-reporting_ES.md)

## 💡 Consejos

- **Empieza simple:** Comienza con tests básicos usando el DSL
- **Usa BDD gradualmente:** Introduce Behave cuando tengas múltiples tests
- **Organiza tus datos:** Usa archivos JSON/YAML para datos de test
- **Aprovecha los reportes:** Los reportes HTML te ayudan a debuggear
- **Usa runners para organizar:** Crea runners personalizados para diferentes suites

¡Feliz testing con Judo Framework! 🥋