# Referencia Completa de Pasos - Judo Framework (Modo Mixto)

Esta es la referencia completa de todos los pasos **VERIFICADOS** disponibles en Judo Framework v1.3.40 en **Modo Mixto** (keywords en inglés + descripciones en español).

**⚠️ IMPORTANTE**: Esta documentación ha sido verificada contra el código fuente del framework. Solo incluye pasos que realmente existen y funcionan.

**💡 Modo Mixto**: Usa keywords en inglés (Given, When, Then, And, But) con descripciones de pasos en español. Esto funciona porque los pasos españoles usan el decorador `@step()`, que acepta cualquier keyword.

## 📋 Índice

- [Configuración](#configuración)
- [Autenticación](#autenticación)
- [Peticiones HTTP](#peticiones-http)
- [Validación de Respuestas](#validación-de-respuestas)
- [Extracción de Datos](#extracción-de-datos)
- [Variables](#variables)
- [Arrays y Colecciones](#arrays-y-colecciones)
- [Operaciones con Archivos](#operaciones-con-archivos)
- [Utilidades](#utilidades)
- [Logging](#logging)
- [Validación de Esquemas](#validación-de-esquemas)
- [Validación de Tipos](#validación-de-tipos)

---

## Configuración

### `Given tengo un cliente Judo API`
Inicializa el contexto de Judo Framework para comenzar las pruebas de API.

**Ejemplo:**
```gherkin
Given tengo un cliente Judo API
```

### `Given la URL base es "{url}"`
Establece la URL base que se usará para todas las peticiones HTTP subsecuentes.

**Ejemplo:**
```gherkin
Given la URL base es "https://api.example.com"
And la URL base es "https://jsonplaceholder.typicode.com"
```

### `Given establezco la variable "{nombre}" a "{valor}"`
Crea o actualiza una variable de tipo string que puede ser reutilizada en otros pasos.

**Ejemplo:**
```gherkin
Given establezco la variable "userId" a "123"
And establezco la variable "apiVersion" a "v1"
```

### `Given establezco la variable "{nombre}" a {valor:d}`
Crea o actualiza una variable de tipo numérico (entero).

**Ejemplo:**
```gherkin
Given establezco la variable "maxRetries" a 3
And establezco la variable "timeout" a 5000
```

### `Given establezco la variable "{nombre}" al JSON`
Almacena un objeto JSON completo en una variable usando el texto del paso.

**Ejemplo:**
```gherkin
Given establezco la variable "userData" al JSON
  """
  {
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "age": 30
  }
  """
```

### `Given obtengo el valor "{nombre_var_env}" desde env y lo almaceno en "{nombre_variable}"`
Obtiene el valor de una variable de entorno (.env) y lo almacena en una variable para uso posterior.

**Ejemplo:**
```gherkin
Given obtengo el valor "API_TOKEN" desde env y lo almaceno en "token"
And obtengo el valor "BASE_URL" desde env y lo almaceno en "baseUrl"
```

---

## Autenticación

### `Given uso el token bearer "{token}"`
Configura autenticación Bearer Token (JWT) para todas las peticiones subsecuentes.

**Ejemplo:**
```gherkin
Given uso el token bearer "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
And uso el token bearer "{token}"
```

### `Given uso autenticación básica con usuario "{usuario}" y contraseña "{password}"`
Configura autenticación HTTP Basic con usuario y contraseña.

**Ejemplo:**
```gherkin
Given uso autenticación básica con usuario "admin" y contraseña "secret123"
```

### `Given establezco el header "{nombre}" a "{valor}"`
Agrega un header HTTP personalizado a todas las peticiones subsecuentes.

**Ejemplo:**
```gherkin
Given establezco el header "Content-Type" a "application/json"
And establezco el header "X-API-Version" a "v2"
And establezco el header "Accept-Language" a "es-ES"
```

### `Given establezco el header "{nombre_header}" desde env "{nombre_var_env}"`
Establece un header HTTP desde una variable de entorno (.env).

**Ejemplo:**
```gherkin
Given establezco el header "Authorization" desde env "API_TOKEN"
And establezco el header "X-API-Key" desde env "API_KEY"
```

### `Given agrego el header "{nombre_header}" desde env "{nombre_var_env}"`
Alias del paso anterior para agregar un header desde variable de entorno.

**Ejemplo:**
```gherkin
Given agrego el header "Authorization" desde env "JWT_TOKEN"
```

### `Given establezco el parámetro "{nombre}" a "{valor}"`
Agrega un parámetro de query string a las peticiones.

**Ejemplo:**
```gherkin
Given establezco el parámetro "page" a "1"
And establezco el parámetro "limit" a "10"
And establezco el parámetro "sort" a "desc"
```

---

## Peticiones HTTP

### `When hago una petición GET a "{endpoint}"`
Envía una petición HTTP GET al endpoint especificado.

**Ejemplo:**
```gherkin
When hago una petición GET a "/users"
When hago una petición GET a "/users/123"
When hago una petición GET a "/users/{userId}"
```

### `When hago una petición POST a "{endpoint}"`
Envía una petición HTTP POST sin cuerpo al endpoint especificado.

**Ejemplo:**
```gherkin
When hago una petición POST a "/users/123/activate"
```

### `When hago una petición POST a "{endpoint}" con el cuerpo`
Envía una petición HTTP POST con cuerpo JSON al endpoint especificado.

**Ejemplo:**
```gherkin
When hago una petición POST a "/users" con el cuerpo:
  """
  {
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "age": 30
  }
  """
```

### `When hago una petición PUT a "{endpoint}" con el cuerpo`
Envía una petición HTTP PUT con cuerpo JSON al endpoint especificado.

**Ejemplo:**
```gherkin
When hago una petición PUT a "/users/123" con el cuerpo:
  """
  {
    "name": "Juan Pérez Actualizado",
    "email": "juan.nuevo@example.com"
  }
  """
```

### `When hago una petición PATCH a "{endpoint}" con el cuerpo`
Envía una petición HTTP PATCH con cuerpo JSON al endpoint especificado.

**Ejemplo:**
```gherkin
When hago una petición PATCH a "/users/123" con el cuerpo:
  """
  {
    "email": "nuevo.email@example.com"
  }
  """
```

### `When hago una petición DELETE a "{endpoint}"`
Envía una petición HTTP DELETE al endpoint especificado.

**Ejemplo:**
```gherkin
When hago una petición DELETE a "/users/123"
When hago una petición DELETE a "/users/{userId}"
```

### `When hago una petición {método} a "{endpoint}" con la variable "{nombre_var}"`
Envía una petición HTTP con datos JSON desde una variable previamente almacenada.

**Ejemplo:**
```gherkin
Given establezco la variable "newUser" al JSON
  """
  {"name": "Juan", "email": "juan@example.com"}
  """
When hago una petición POST a "/users" con la variable "newUser"
```

---

## Validación de Respuestas

### `Then el código de respuesta debe ser {status:d}`
Valida que el código de estado HTTP de la respuesta sea el esperado.

**Ejemplo:**
```gherkin
Then el código de respuesta debe ser 200
Then el código de respuesta debe ser 201
Then el código de respuesta debe ser 404
```

### `Then la respuesta debe ser exitosa`
Valida que la respuesta sea exitosa (código 2xx).

**Ejemplo:**
```gherkin
Then la respuesta debe ser exitosa
```

### `Then la respuesta debe contener el campo "{campo}"`
Valida que la respuesta JSON contenga un campo específico.

**Ejemplo:**
```gherkin
Then la respuesta debe contener el campo "id"
And la respuesta debe contener el campo "name"
And la respuesta debe contener el campo "email"
```

### `Then el campo "{campo}" debe ser "{valor}"`
Valida que un campo de la respuesta tenga un valor específico (string).

**Ejemplo:**
```gherkin
Then el campo "name" debe ser "Juan Pérez"
And el campo "status" debe ser "active"
```

### `Then el campo "{campo}" debe ser {valor:d}`
Valida que un campo de la respuesta tenga un valor específico (número).

**Ejemplo:**
```gherkin
Then el campo "age" debe ser 30
And el campo "id" debe ser 123
```

### `Then el campo "{campo}" debe ser igual a la variable "{variable}"`
Valida que un campo de la respuesta sea igual al valor de una variable.

**Ejemplo:**
```gherkin
Given establezco la variable "expectedName" a "Juan Pérez"
When hago una petición GET a "/users/1"
Then el campo "name" debe ser igual a la variable "expectedName"
```

### `Then la respuesta debe tener la siguiente estructura`
Valida que la respuesta tenga una estructura JSON específica.

**Ejemplo:**
```gherkin
Then la respuesta debe tener la siguiente estructura:
  """
  {
    "id": 123,
    "name": "Juan Pérez",
    "email": "juan@example.com"
  }
  """
```

---

## Arrays y Colecciones

### `Then la respuesta debe ser un array`
Valida que la respuesta sea un array JSON.

**Ejemplo:**
```gherkin
When hago una petición GET a "/users"
Then la respuesta debe ser un array
```

### `Then la respuesta debe ser una lista`
Alias del paso anterior.

**Ejemplo:**
```gherkin
Then la respuesta debe ser una lista
```

### `Then la respuesta debe tener {count:d} elementos`
Valida que el array de respuesta tenga una cantidad específica de elementos.

**Ejemplo:**
```gherkin
Then la respuesta debe tener 10 elementos
And la respuesta debe tener 0 elementos
```

### `Then cada elemento debe tener el campo "{campo}"`
Valida que cada elemento del array tenga un campo específico.

**Ejemplo:**
```gherkin
When hago una petición GET a "/users"
Then la respuesta debe ser un array
And cada elemento debe tener el campo "id"
And cada elemento debe tener el campo "name"
And cada elemento debe tener el campo "email"
```

### `Then el array "{ruta_array}" debe contener un elemento con "{campo}" igual a "{valor}"`
Valida que un array (posiblemente anidado) contenga un elemento con un valor específico.

**Ejemplo:**
```gherkin
Then el array "users" debe contener un elemento con "name" igual a "Juan"
And el array "data.items" debe contener un elemento con "id" igual a "123"
```

---

## Extracción de Datos

### `When guardo el valor del campo "{campo}" en la variable "{variable}"`
Extrae el valor de un campo de la respuesta y lo almacena en una variable.

**Ejemplo:**
```gherkin
When hago una petición POST a "/users" con el cuerpo:
  """
  {"name": "Juan", "email": "juan@example.com"}
  """
Then el código de respuesta debe ser 201
When guardo el valor del campo "id" en la variable "userId"
```

### `When guardo la respuesta completa en la variable "{variable}"`
Almacena la respuesta JSON completa en una variable.

**Ejemplo:**
```gherkin
When hago una petición GET a "/users/1"
When guardo la respuesta completa en la variable "userData"
```

---

## Variables

### `Then la variable "{variable1}" debe ser igual a la variable "{variable2}"`
Compara que dos variables tengan el mismo valor.

**Ejemplo:**
```gherkin
Given establezco la variable "expected" a "Juan"
When guardo el valor del campo "name" en la variable "actual"
Then la variable "actual" debe ser igual a la variable "expected"
```

### `Then la variable "{variable1}" no debe ser igual a la variable "{variable2}"`
Compara que dos variables tengan valores diferentes.

**Ejemplo:**
```gherkin
Then la variable "userId1" no debe ser igual a la variable "userId2"
```

### `Then debo tener la variable "{nombre_variable}" con valor "{valor_esperado}"`
Valida que una variable tenga un valor específico.

**Ejemplo:**
```gherkin
Given establezco la variable "status" a "active"
Then debo tener la variable "status" con valor "active"
```

---

## Operaciones con Archivos

### `When hago POST a "{endpoint}" con archivo JSON "{ruta_archivo}"`
Envía una petición POST con el cuerpo JSON cargado desde un archivo.

**Ejemplo:**
```gherkin
When hago POST a "/users" con archivo JSON "test_data/new_user.json"
```

### `When hago PUT a "{endpoint}" con archivo JSON "{ruta_archivo}"`
Envía una petición PUT con el cuerpo JSON cargado desde un archivo.

**Ejemplo:**
```gherkin
When hago PUT a "/users/123" con archivo JSON "test_data/updated_user.json"
```

### `When hago PATCH a "{endpoint}" con archivo JSON "{ruta_archivo}"`
Envía una petición PATCH con el cuerpo JSON cargado desde un archivo.

**Ejemplo:**
```gherkin
When hago PATCH a "/users/123" con archivo JSON "test_data/user_patch.json"
```

### `When guardo la respuesta en el archivo "{ruta_archivo}"`
Guarda la respuesta JSON en un archivo.

**Ejemplo:**
```gherkin
When hago una petición GET a "/users/1"
When guardo la respuesta en el archivo "output/user_response.json"
```

### `When guardo la variable "{nombre_var}" en el archivo "{ruta_archivo}"`
Guarda el contenido de una variable en un archivo.

**Ejemplo:**
```gherkin
When guardo la variable "userData" en el archivo "output/user_data.json"
```

---

## Utilidades

### `When espero {segundos:f} segundos`
Pausa la ejecución por un número específico de segundos.

**Ejemplo:**
```gherkin
When espero 2 segundos
When espero 0.5 segundos
```

### `When imprimo la respuesta`
Imprime la respuesta en la consola para debugging.

**Ejemplo:**
```gherkin
When hago una petición GET a "/users/1"
When imprimo la respuesta
```

### `Then el tiempo de respuesta debe ser menor a {max_time:f} segundos`
Valida que el tiempo de respuesta sea menor al especificado.

**Ejemplo:**
```gherkin
When hago una petición GET a "/users"
Then el tiempo de respuesta debe ser menor a 2.0 segundos
```

### `Then la respuesta "{ruta_json}" debe ser "{valor_esperado}"`
Valida el resultado de una expresión JSONPath (string).

**Ejemplo:**
```gherkin
Then la respuesta "$.user.name" debe ser "Juan Pérez"
And la respuesta "$.data[0].status" debe ser "active"
```

### `Then la respuesta "{ruta_json}" debe ser {valor_esperado:d}`
Valida el resultado de una expresión JSONPath (número).

**Ejemplo:**
```gherkin
Then la respuesta "$.user.age" debe ser 30
And la respuesta "$.data.count" debe ser 10
```

---

## Logging

### `Given habilito el guardado de peticiones y respuestas`
Habilita el guardado automático de todas las peticiones y respuestas HTTP en archivos JSON.

**Ejemplo:**
```gherkin
Given habilito el guardado de peticiones y respuestas
```

### `Given deshabilito el guardado de peticiones y respuestas`
Deshabilita el guardado automático de peticiones y respuestas.

**Ejemplo:**
```gherkin
Given deshabilito el guardado de peticiones y respuestas
```

### `Given habilito el guardado de peticiones y respuestas en el directorio "{directory}"`
Habilita el guardado con un directorio personalizado.

**Ejemplo:**
```gherkin
Given habilito el guardado de peticiones y respuestas en el directorio "api_logs"
```

### `Given establezco el directorio de salida a "{directory}"`
Establece el directorio de salida para el guardado de peticiones y respuestas.

**Ejemplo:**
```gherkin
Given establezco el directorio de salida a "test_output"
```

---

## Validación de Esquemas

### `Then la respuesta debe coincidir con el esquema`
Valida la respuesta contra un esquema JSON proporcionado en el texto del paso.

**Ejemplo:**
```gherkin
Then la respuesta debe coincidir con el esquema:
  """
  {
    "type": "object",
    "properties": {
      "id": {"type": "number"},
      "name": {"type": "string"},
      "email": {"type": "string"}
    },
    "required": ["id", "name", "email"]
  }
  """
```

### `Then la respuesta debe coincidir con el archivo de esquema "{ruta_archivo}"`
Valida la respuesta contra un esquema JSON cargado desde un archivo.

**Ejemplo:**
```gherkin
Then la respuesta debe coincidir con el archivo de esquema "schemas/user_schema.json"
```

---

## Validación de Tipos

### `Then la respuesta "{ruta_json}" debe ser una cadena`
Valida que el resultado de una expresión JSONPath sea una cadena (string).

**Ejemplo:**
```gherkin
Then la respuesta "$.user.name" debe ser una cadena
```

### `Then la respuesta "{ruta_json}" debe ser un número`
Valida que el resultado de una expresión JSONPath sea un número.

**Ejemplo:**
```gherkin
Then la respuesta "$.user.age" debe ser un número
```

### `Then la respuesta "{ruta_json}" debe ser un booleano`
Valida que el resultado de una expresión JSONPath sea un booleano.

**Ejemplo:**
```gherkin
Then la respuesta "$.user.active" debe ser un booleano
```

### `Then la respuesta "{ruta_json}" debe ser un array`
Valida que el resultado de una expresión JSONPath sea un array.

**Ejemplo:**
```gherkin
Then la respuesta "$.users" debe ser un array
```

### `Then la respuesta "{ruta_json}" debe ser un objeto`
Valida que el resultado de una expresión JSONPath sea un objeto.

**Ejemplo:**
```gherkin
Then la respuesta "$.user.address" debe ser un objeto
```

### `Then la respuesta "{ruta_json}" debe ser null`
Valida que el resultado de una expresión JSONPath sea null.

**Ejemplo:**
```gherkin
Then la respuesta "$.user.deletedAt" debe ser null
```

### `Then la respuesta "{ruta_json}" no debe ser null`
Valida que el resultado de una expresión JSONPath NO sea null.

**Ejemplo:**
```gherkin
Then la respuesta "$.user.id" no debe ser null
```

### `Then la respuesta "{ruta_json}" debe ser un email válido`
Valida que el resultado de una expresión JSONPath sea un email válido.

**Ejemplo:**
```gherkin
Then la respuesta "$.user.email" debe ser un email válido
```

### `Then la respuesta "{ruta_json}" debe ser una URL válida`
Valida que el resultado de una expresión JSONPath sea una URL válida.

**Ejemplo:**
```gherkin
Then la respuesta "$.user.website" debe ser una URL válida
```

### `Then la respuesta "{ruta_json}" debe ser un UUID válido`
Valida que el resultado de una expresión JSONPath sea un UUID válido.

**Ejemplo:**
```gherkin
Then la respuesta "$.user.uuid" debe ser un UUID válido
```

---

## 📝 Ejemplo Completo en Modo Mixto

```gherkin
Feature: API de Gestión de Usuarios

  Scenario: Crear, obtener y eliminar un usuario
    # Configuración inicial
    Given tengo un cliente Judo API
    And la URL base es "https://jsonplaceholder.typicode.com"
    
    # Crear usuario
    When hago una petición POST a "/users" con el cuerpo:
      """
      {
        "name": "Juan Pérez",
        "email": "juan@example.com",
        "username": "juanp"
      }
      """
    Then el código de respuesta debe ser 201
    And la respuesta debe contener el campo "id"
    And el campo "name" debe ser "Juan Pérez"
    When guardo el valor del campo "id" en la variable "userId"
    
    # Obtener usuario creado
    When hago una petición GET a "/users/{userId}"
    Then el código de respuesta debe ser 200
    And el campo "name" debe ser "Juan Pérez"
    And el campo "email" debe ser "juan@example.com"
    And el tiempo de respuesta debe ser menor a 2.0 segundos
    
    # Actualizar usuario
    When hago una petición PUT a "/users/{userId}" con el cuerpo:
      """
      {
        "name": "Juan Pérez Actualizado",
        "email": "juan.nuevo@example.com"
      }
      """
    Then el código de respuesta debe ser 200
    And el campo "name" debe ser "Juan Pérez Actualizado"
    
    # Eliminar usuario
    When hago una petición DELETE a "/users/{userId}"
    Then el código de respuesta debe ser 200
```

---

## 💡 Consejos para Modo Mixto

1. **Usa keywords en inglés**: Son más cortos y universales (Given, When, Then, And, But)
2. **Descripciones en español**: Más naturales para equipos latinoamericanos
3. **Sin tag de idioma**: No necesitas `# language: es`
4. **Mezcla libremente**: Puedes combinar con pasos en inglés puro si lo necesitas
5. **Usa And/But**: Para encadenar múltiples pasos del mismo tipo

---

## 🔗 Referencias

- **Documentación completa**: `examples/README_mixed_mode.md`
- **Ejemplo funcional**: `examples/mixed_mode_example.feature`
- **Pasos en inglés**: `judo-steps-reference-en.md`
- **Pasos en español**: `judo-steps-reference-es.md`

---

**Versión**: 1.3.40  
**Fecha**: 14 de Diciembre, 2024  
**Autor**: Felipe Farias - CENTYC
