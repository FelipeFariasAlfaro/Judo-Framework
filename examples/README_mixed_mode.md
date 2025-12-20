# 🥋 Modo Mixto - Mixed Mode

## ¿Qué es el Modo Mixto?

El **Modo Mixto** es una característica **natural** de Judo Framework que permite escribir tests usando **keywords en inglés** (Given, When, Then, And, But) con **descripciones en español**.

Esto funciona automáticamente porque los pasos en español usan el decorador `@step()` de Behave, que acepta cualquier keyword.

## ¿Por qué Modo Mixto?

En Latinoamérica es muy común escribir código mezclando inglés y español:

```python
# Esto es muy común en LATAM
def getUserData():
    nombre = "Juan"
    edad = 25
    return {"name": nombre, "age": edad}
```

De la misma forma, muchos desarrolladores prefieren usar keywords en inglés pero describir las acciones en español, porque es más natural y legible para el equipo.

## Comparación de Modos

### Modo Inglés Puro
```gherkin
# language: en
Feature: User API Testing

  Scenario: Get user information
    Given I have a Judo API client
    And the base URL is "https://api.example.com"
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "name"
```

### Modo Español Puro
```gherkin
# language: es
Característica: Pruebas de API de Usuarios

  Escenario: Obtener información de usuario
    Dado que tengo un cliente Judo API
    Y que la URL base es "https://api.example.com"
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener el campo "name"
```

### ✨ Modo Mixto (NUEVO)
```gherkin
Feature: Pruebas de API de Usuarios

  Scenario: Obtener información de usuario
    Given tengo un cliente Judo API
    And la URL base es "https://api.example.com"
    When hago una petición GET a "/users/1"
    Then el código de respuesta debe ser 200
    And la respuesta debe contener el campo "name"
```

## Ventajas del Modo Mixto

✅ **Natural para LATAM**: Refleja cómo realmente escribimos código  
✅ **Sin tag de idioma**: No necesitas `# language: es`  
✅ **Más legible**: Keywords cortos en inglés, descripciones claras en español  
✅ **Compatible**: Funciona con todas las herramientas de Behave  
✅ **Flexible**: Puedes mezclar con pasos en inglés puro si lo necesitas

## Cómo Usar Modo Mixto

### 1. No necesitas configuración especial

El modo mixto funciona **automáticamente** porque los pasos españoles usan `@step()`. Solo escribe tu feature file:

```gherkin
Feature: API de Usuarios

  Scenario: Crear un nuevo usuario
    Given tengo un cliente Judo API
    And la URL base es "https://api.example.com"
    When hago una petición POST a "/users" con el cuerpo:
      """
      {
        "name": "Juan Pérez",
        "email": "juan@example.com"
      }
      """
    Then el código de respuesta debe ser 201
    And la respuesta debe contener el campo "id"
    And guardo el valor del campo "id" en la variable "userId"
```

### 2. Ejecuta normalmente

```bash
behave features/
```

¡Eso es todo! No necesitas ninguna configuración adicional.

## Todos los Pasos Disponibles en Modo Mixto

### Configuración
```gherkin
Given tengo un cliente Judo API
Given la URL base es "https://api.example.com"
Given establezco la variable "nombre" a "valor"
Given establezco la variable "edad" a 25
```

### Autenticación
```gherkin
Given uso el token bearer "{token}"
Given uso autenticación básica con usuario "user" y contraseña "pass"
Given establezco el header "Authorization" a "Bearer abc123"
Given establezco el header "API-Key" desde env "API_KEY"
```

### Peticiones HTTP
```gherkin
When hago una petición GET a "/users"
When hago una petición POST a "/users"
When hago una petición POST a "/users" con el cuerpo:
  """
  {"name": "Juan"}
  """
When hago una petición PUT a "/users/1" con el cuerpo:
  """
  {"name": "Juan Actualizado"}
  """
When hago una petición DELETE a "/users/1"
```

### Validaciones
```gherkin
Then el código de respuesta debe ser 200
Then la respuesta debe ser exitosa
Then la respuesta debe contener el campo "name"
Then el campo "name" debe ser "Juan"
Then el campo "age" debe ser 25
Then la respuesta debe ser un array
Then la respuesta debe tener 10 elementos
```

### Variables
```gherkin
When guardo el valor del campo "id" en la variable "userId"
When guardo la respuesta completa en la variable "userData"
Then la variable "userId" debe ser igual a la variable "expectedId"
```

### Archivos
```gherkin
When hago POST a "/users" con archivo JSON "test_data/user.json"
When guardo la respuesta en el archivo "output/response.json"
```

### Utilidades
```gherkin
When espero 2 segundos
When imprimo la respuesta
Then el tiempo de respuesta debe ser menor a 1.5 segundos
```

## Ejemplo Completo

Ver el archivo `mixed_mode_example.feature` para un ejemplo funcional completo.

## Modo Mixto vs Otros Modos

| Característica | Inglés | Español | Mixto |
|---------------|--------|---------|-------|
| Keywords | Given/When/Then | Dado/Cuando/Entonces | Given/When/Then |
| Descripciones | English | Español | Español |
| Tag de idioma | No | Sí (`# language: es`) | No |
| Natural para LATAM | ❌ | ✅ | ✅✅ |
| Herramientas CI/CD | ✅ | ✅ | ✅ |

## Preguntas Frecuentes

### ¿Puedo mezclar pasos en inglés y español en el mismo escenario?

¡Sí! Puedes usar cualquier combinación:

```gherkin
Scenario: Prueba mixta
  Given I have a Judo API client  # Inglés puro
  And la URL base es "https://api.example.com"  # Mixto
  When hago una petición GET a "/users"  # Mixto
  Then the response status should be 200  # Inglés puro
```

### ¿Cómo funciona técnicamente?

Los pasos en español usan el decorador `@step()` de Behave en lugar de `@given/@when/@then`. Esto hace que el paso funcione con **cualquier keyword** (Given, When, Then, And, But).

```python
# En judo/behave/steps_es.py
@step('tengo un cliente Judo API')  # ← Funciona con cualquier keyword
def step_setup_judo_es(context):
    # ...
```

### ¿Funciona con Playwright?

Sí, si creas tus pasos de Playwright usando `@step()`. Judo Framework proporciona la infraestructura de Playwright (`JudoBrowserContext`), pero tú creas tus propios pasos personalizados según tus necesidades.

### ¿Afecta el rendimiento?

No. Los pasos mixtos son tan rápidos como los pasos en inglés o español puro.

### ¿Funciona en CI/CD?

Sí, funciona perfectamente en cualquier entorno donde funcione Behave.

## Soporte

El modo mixto está disponible desde siempre en Judo Framework (los pasos españoles siempre han usado `@step()`). La documentación oficial del modo mixto está disponible desde v1.3.40+

Para más información, visita:
- GitHub: https://github.com/FelipeFariasAlfaro/Judo-Framework
- PyPI: https://pypi.org/project/judo-framework/
