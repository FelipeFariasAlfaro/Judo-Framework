# 📚 Ejemplos - Judo Framework

Este documento proporciona ejemplos completos de uso de Judo Framework para testing de APIs.

**Creado por Felipe Farias en [CENTYC](https://www.centyc.cl) - Centro Latinoamericano de Testing y Calidad del Software**

## 🚀 Ejemplos Básicos

### Petición GET Simple

```python
from judo import Judo

judo = Judo()
response = judo.get("https://jsonplaceholder.typicode.com/users/1")

# Validar respuesta
judo.match(response.status, 200)
judo.match(response.json["name"], "##string")
judo.match(response.json["email"], "##email")
```

### Petición POST con JSON

```python
from judo import Judo

judo = Judo()

# Crear nuevo usuario
datos_usuario = {
    "name": "Juan Pérez",
    "username": "juanperez",
    "email": "juan@example.com"
}

response = judo.post("https://jsonplaceholder.typicode.com/users", datos_usuario)
judo.match(response.status, 201)
judo.match(response.json["name"], "Juan Pérez")
```

### Usando Variables

```python
from judo import Judo

judo = Judo()

# Establecer variables
judo.set("baseUrl", "https://jsonplaceholder.typicode.com")
judo.set("userId", 1)

# Usar variables en peticiones
response = judo.get(f"{judo.get('baseUrl')}/users/{judo.get('userId')}")
judo.match(response.status, 200)
```

## 🧪 Ejemplos BDD con Behave

### Archivo Feature Básico

**features/user_api.feature:**
```gherkin
Feature: Testing de API de Usuarios
  Background:
    Given I set the base URL to "https://jsonplaceholder.typicode.com"
  
  @smoke
  Scenario: Obtener usuario por ID
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain:
      | field    | value    |
      | id       | 1        |
      | name     | ##string |
      | username | ##string |
      | email    | ##email  |
  
  @api
  Scenario: Crear nuevo usuario
    When I send a POST request to "/users" with JSON:
      """
      {
        "name": "María García",
        "username": "mariagarcia",
        "email": "maria@example.com"
      }
      """
    Then the response status should be 201
    And the response should contain:
      | field | value        |
      | name  | María García |
      | email | maria@example.com |
```

### Configuración de Environment

**features/environment.py:**
```python
from judo.behave import setup_judo_context

def before_all(context):
    setup_judo_context(context)
    print("🥋 Judo Framework inicializado")

def before_scenario(context, scenario):
    print(f"📝 Iniciando scenario: {scenario.name}")

def after_scenario(context, scenario):
    status = "✅ PASÓ" if scenario.status == "passed" else "❌ FALLÓ"
    print(f"{status} Scenario: {scenario.name}")
```

## 🏃 Ejemplos de Runners Personalizados

### Runner Básico

```python
from judo.runner import BaseRunner

class APITestRunner(BaseRunner):
    def __init__(self):
        super().__init__(
            features_dir="features",
            output_dir="reportes_test"
        )
    
    def ejecutar_smoke_tests(self):
        """Ejecutar solo smoke tests"""
        return self.run(tags=["@smoke"])
    
    def ejecutar_api_tests(self):
        """Ejecutar todos los tests de API"""
        return self.run(tags=["@api"])

# Uso
runner = APITestRunner()
resultados = runner.ejecutar_smoke_tests()
print(f"Smoke tests: {resultados['passed']}/{resultados['total']} pasaron")
```

### Runner Avanzado con Ejecución Paralela

```python
from judo.runner import BaseRunner

class RunnerAvanzado(BaseRunner):
    def __init__(self):
        super().__init__(
            features_dir="features",
            parallel=True,
            max_workers=8
        )
        
        # Configurar callbacks
        self.set_callbacks(
            before_all=self.configurar_entorno_test,
            after_all=self.limpiar_entorno_test
        )
    
    def configurar_entorno_test(self):
        """Configurar antes de todos los tests"""
        print("🚀 Configurando entorno de test...")
        # Agregar lógica de configuración aquí
    
    def limpiar_entorno_test(self, resultados):
        """Limpiar después de todos los tests"""
        print("🧹 Limpiando entorno de test...")
        self.print_summary()
    
    def ejecutar_suite_regresion(self):
        """Ejecutar suite completa de regresión"""
        self.configure(
            timeout=600,      # 10 minutos por feature
            fail_fast=False,  # No parar en el primer fallo
            verbose=True      # Mostrar salida detallada
        )
        return self.run(tags=["@regression"])
    
    def ejecutar_smoke_y_api_tests(self):
        """Ejecutar smoke y API tests en paralelo"""
        return self.run(tags=["@smoke", "@api"], exclude_tags=["@slow"])

# Uso
runner = RunnerAvanzado()
resultados = runner.ejecutar_suite_regresion()
```

## 📄 Testing Basado en Archivos

### Usando Archivos JSON

**test_data/datos_usuario.json:**
```json
{
  "name": "Alicia Rodríguez",
  "username": "aliciar",
  "email": "alicia@example.com",
  "address": {
    "street": "Calle Principal 123",
    "city": "Madrid"
  }
}
```

**Código Python:**
```python
from judo import Judo

judo = Judo()

# Leer datos desde archivo
datos_usuario = judo.read("test_data/datos_usuario.json")

# Usar en petición
response = judo.post("https://jsonplaceholder.typicode.com/users", datos_usuario)
judo.match(response.status, 201)
judo.match(response.json["name"], datos_usuario["name"])
```

### Validación de Schema

**schemas/schema_usuario.json:**
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "name": {"type": "string"},
    "username": {"type": "string"},
    "email": {"type": "string", "format": "email"}
  },
  "required": ["id", "name", "email"]
}
```

**Validación:**
```python
from judo import Judo

judo = Judo()
response = judo.get("https://jsonplaceholder.typicode.com/users/1")

# Cargar y validar schema
schema = judo.read("schemas/schema_usuario.json")
judo.match_schema(response.json, schema)
```

## 🔐 Ejemplos de Autenticación

### Bearer Token

```python
from judo import Judo

judo = Judo()

# Establecer bearer token
judo.set_header("Authorization", "Bearer tu-jwt-token-aqui")

# O usar método helper
judo.bearer_token("tu-jwt-token-aqui")

response = judo.get("https://api.example.com/endpoint-protegido")
judo.match(response.status, 200)
```

### Autenticación Básica

```python
from judo import Judo

judo = Judo()

# Establecer auth básica
judo.basic_auth("usuario", "contraseña")

response = judo.get("https://api.example.com/endpoint-protegido")
judo.match(response.status, 200)
```

## 🎭 Ejemplo de Mock Server

```python
from judo import Judo
from judo.mock import MockServer

# Crear mock server
mock = MockServer(port=8080)

# Agregar endpoints mock
mock.add_route("GET", "/users/1", {
    "id": 1,
    "name": "Usuario Mock",
    "email": "mock@example.com"
})

mock.add_route("POST", "/users", {
    "id": 2,
    "name": "Usuario Creado",
    "email": "creado@example.com"
}, status_code=201)

# Iniciar mock server
mock.start()

# Testear contra mock
judo = Judo()
response = judo.get("http://localhost:8080/users/1")
judo.match(response.status, 200)
judo.match(response.json["name"], "Usuario Mock")

# Detener mock server
mock.stop()
```

## 📊 Testing Dirigido por Datos

### Datos CSV

**test_data/usuarios.csv:**
```csv
name,email,age
Juan Pérez,juan@example.com,30
María García,maria@example.com,25
Carlos López,carlos@example.com,35
```

**Código Python:**
```python
from judo import Judo
import csv

judo = Judo()

# Leer datos CSV
with open("test_data/usuarios.csv", "r") as archivo:
    usuarios = list(csv.DictReader(archivo))

# Testear cada usuario
for usuario in usuarios:
    response = judo.post("https://jsonplaceholder.typicode.com/users", usuario)
    judo.match(response.status, 201)
    judo.match(response.json["name"], usuario["name"])
    judo.match(response.json["email"], usuario["email"])
```

## 🔍 Matching Avanzado

### Matching con JSONPath

```python
from judo import Judo

judo = Judo()
response = judo.get("https://jsonplaceholder.typicode.com/users")

# Hacer match de longitud de array
judo.match("$.length", 10)

# Hacer match de que todos los nombres de usuario son strings
judo.match("$[*].name", "##array")
judo.match("$[0].name", "##string")

# Hacer match de propiedades anidadas
judo.match("$[0].address.city", "##string")
```

### Matching de Patrones

```python
from judo import Judo

judo = Judo()
response = judo.get("https://jsonplaceholder.typicode.com/users/1")

# Matching de tipos
judo.match(response.json["id"], "##number")
judo.match(response.json["name"], "##string")
judo.match(response.json["email"], "##email")
judo.match(response.json["website"], "##url")

# Patrones personalizados
judo.match(response.json["phone"], "##regex:^[0-9-\s\(\)\.x]+$")
```

## 🚀 Ejecutando Ejemplos

### Línea de Comandos

```bash
# Ejecutar todos los tests
behave features/

# Ejecutar tags específicos
behave features/ --tags @smoke
behave features/ --tags @api

# Ejecutar con formato personalizado
behave features/ --format json --outfile resultados.json

# Ejecutar en paralelo (si está soportado)
behave features/ --processes 4
```

### Script Python

```python
#!/usr/bin/env python3
"""
Script de ejemplo para ejecución de tests
"""

from judo.runner import BaseRunner

def main():
    runner = BaseRunner(
        features_dir="features",
        parallel=True,
        max_workers=4
    )
    
    print("🧪 Ejecutando tests de API...")
    
    # Ejecutar smoke tests primero
    resultados_smoke = runner.run(tags=["@smoke"])
    print(f"Smoke tests: {resultados_smoke['passed']}/{resultados_smoke['total']}")
    
    if resultados_smoke['failed'] == 0:
        # Ejecutar suite completa si los smoke tests pasan
        resultados_completos = runner.run(exclude_tags=["@manual"])
        print(f"Suite completa: {resultados_completos['passed']}/{resultados_completos['total']}")
        
        return resultados_completos['failed'] == 0
    else:
        print("❌ Smoke tests fallaron, saltando suite completa")
        return False

if __name__ == "__main__":
    exito = main()
    exit(0 if exito else 1)
```

---

Para más ejemplos, revisa el directorio [examples/](../examples/) en el repositorio.