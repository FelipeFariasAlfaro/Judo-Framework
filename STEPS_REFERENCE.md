# 🥋 Judo Framework - Complete Steps Reference

Complete reference of all available Gherkin steps in English and Spanish.

---

## 📋 Table of Contents

1. [Configuration Steps](#configuration-steps)
2. [Authentication Steps](#authentication-steps)
3. [HTTP Request Steps](#http-request-steps)
4. [Response Validation Steps](#response-validation-steps)
5. [Data Extraction Steps](#data-extraction-steps)
6. [Variable Management Steps](#variable-management-steps)
7. [File Operations Steps](#file-operations-steps)
8. [Array/Collection Steps](#arraycollection-steps)
9. [Schema Validation Steps](#schema-validation-steps)
10. [Type Validation Steps](#type-validation-steps)
11. [Utility Steps](#utility-steps)

---

## Configuration Steps

### Set Base URL

**English:**
```gherkin
Given the base URL is "{url}"
```

**Spanish:**
```gherkin
Dado que la URL base es "{url}"
```

**Description (English):**  
Establishes the base URL that will be used for all subsequent API requests in the scenario. This URL will be prepended to all endpoint paths, allowing you to write cleaner tests without repeating the full URL.

**Descripción (Español):**  
Establece la URL base que se utilizará para todas las peticiones API subsiguientes en el escenario. Esta URL se antepondrá a todas las rutas de endpoints, permitiéndote escribir tests más limpios sin repetir la URL completa.

**Example:**
```gherkin
# English - Testing against production API
Given the base URL is "https://api.example.com"
When I send a GET request to "/users/1"
# Will call: https://api.example.com/users/1

# Spanish - Probando contra API de producción
Dado que la URL base es "https://api.ejemplo.com"
Cuando hago una petición GET a "/usuarios/1"
# Llamará a: https://api.ejemplo.com/usuarios/1
```

---

### Initialize Judo Client

**English:**
```gherkin
Given I have a Judo API client
```

**Spanish:**
```gherkin
Dado que tengo un cliente Judo API
```

**Description (English):**  
Explicitly initializes the Judo API client. This step is usually executed automatically when the test starts, but can be used explicitly if you need to ensure the client is ready before proceeding.

**Descripción (Español):**  
Inicializa explícitamente el cliente API de Judo. Este paso normalmente se ejecuta automáticamente cuando inicia el test, pero puede usarse explícitamente si necesitas asegurar que el cliente esté listo antes de continuar.

**Example:**
```gherkin
# English - Rarely needed, but available
Given I have a Judo API client
And the base URL is "https://api.example.com"

# Spanish - Raramente necesario, pero disponible
Dado que tengo un cliente Judo API
Y la URL base es "https://api.ejemplo.com"
```

---

### Set Variable (String)

**English:**
```gherkin
Given I set the variable "{name}" to "{value}"
```

**Spanish:**
```gherkin
Dado que establezco la variable "{nombre}" a "{valor}"
```

**Description (English):**  
Creates or updates a string variable that can be referenced later in the test. Variables can be used in URLs, request bodies, and validations using the `{variableName}` syntax.

**Descripción (Español):**  
Crea o actualiza una variable de texto que puede ser referenciada más adelante en el test. Las variables pueden usarse en URLs, cuerpos de peticiones y validaciones usando la sintaxis `{nombreVariable}`.

**Example:**
```gherkin
# English - Store API key for later use
Given I set the variable "apiKey" to "sk_test_abc123xyz"
And I set the header "Authorization" to "Bearer {apiKey}"
When I send a GET request to "/protected/resource"

# Spanish - Guardar clave API para uso posterior
Dado que establezco la variable "claveApi" a "sk_test_abc123xyz"
Y establezco el header "Authorization" a "Bearer {claveApi}"
Cuando hago una petición GET a "/recurso/protegido"
```

---

### Set Variable (Number)

**English:**
```gherkin
Given I set the variable "{name}" to {value:d}
```

**Spanish:**
```gherkin
Dado que establezco la variable "{nombre}" a {valor:d}
```

**Description (English):**  
Creates or updates a numeric variable. Useful for storing IDs, counts, or any numeric value that will be used in subsequent steps. The variable can be interpolated in URLs and JSON bodies.

**Descripción (Español):**  
Crea o actualiza una variable numérica. Útil para almacenar IDs, contadores o cualquier valor numérico que se usará en pasos subsiguientes. La variable puede interpolarse en URLs y cuerpos JSON.

**Example:**
```gherkin
# English - Store user ID for later operations
Given I set the variable "userId" to 42
When I send a GET request to "/users/{userId}"
# Will call: /users/42

# Spanish - Guardar ID de usuario para operaciones posteriores
Dado que establezco la variable "idUsuario" a 42
Cuando hago una petición GET a "/usuarios/{idUsuario}"
# Llamará a: /usuarios/42
```

---

### Set Variable (JSON)

**English:**
```gherkin
Given I set the variable "{name}" to the JSON
  """
  {json_content}
  """
```

**Spanish:**
```gherkin
Dado que establezco la variable "{nombre}" al JSON
  """
  {contenido_json}
  """
```

**Description (English):**  
Stores a complete JSON object in a variable. This is useful for reusing complex data structures across multiple requests or for preparing test data that will be sent in request bodies.

**Descripción (Español):**  
Almacena un objeto JSON completo en una variable. Esto es útil para reutilizar estructuras de datos complejas en múltiples peticiones o para preparar datos de prueba que se enviarán en cuerpos de peticiones.

**Example:**
```gherkin
# English - Prepare user data for multiple tests
Given I set the variable "newUser" to the JSON
  """
  {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "address": {
      "city": "New York",
      "country": "USA"
    }
  }
  """
When I send a POST request to "/users" with the variable "newUser"

# Spanish - Preparar datos de usuario para múltiples tests
Dado que establezco la variable "nuevoUsuario" al JSON
  """
  {
    "nombre": "Juan Pérez",
    "email": "juan@ejemplo.com",
    "edad": 30,
    "direccion": {
      "ciudad": "Madrid",
      "pais": "España"
    }
  }
  """
Cuando hago una petición POST a "/usuarios" con la variable "nuevoUsuario"
```

---

### Set Header

**English:**
```gherkin
Given I set the header "{name}" to "{value}"
```

**Spanish:**
```gherkin
Dado que establezco el header "{nombre}" a "{valor}"
```

**Description (English):**  
Adds a custom HTTP header that will be included in all subsequent requests. Common uses include setting content types, custom authentication headers, or API versioning headers.

**Descripción (Español):**  
Agrega un header HTTP personalizado que se incluirá en todas las peticiones subsiguientes. Usos comunes incluyen establecer tipos de contenido, headers de autenticación personalizados o headers de versionado de API.

**Example:**
```gherkin
# English - Set custom headers for API versioning and tracking
Given I set the header "X-API-Version" to "v2"
And I set the header "X-Request-ID" to "test-123"
And I set the header "Accept-Language" to "en-US"
When I send a GET request to "/users"

# Spanish - Establecer headers personalizados para versionado y seguimiento
Dado que establezco el header "X-API-Version" a "v2"
Y establezco el header "X-Request-ID" a "prueba-123"
Y establezco el header "Accept-Language" a "es-ES"
Cuando hago una petición GET a "/usuarios"
```

---

### Set Query Parameter (String)

**English:**
```gherkin
Given I set the query parameter "{name}" to "{value}"
```

**Spanish:**
```gherkin
Dado que establezco el parámetro "{nombre}" a "{valor}"
```

**Description (English):**  
Adds a query parameter (string value) to the next request. Query parameters appear in the URL after the `?` symbol and are commonly used for filtering, pagination, or search operations.

**Descripción (Español):**  
Agrega un parámetro de consulta (valor de texto) a la siguiente petición. Los parámetros de consulta aparecen en la URL después del símbolo `?` y se usan comúnmente para filtrado, paginación u operaciones de búsqueda.

**Example:**
```gherkin
# English - Paginate and filter results
Given the base URL is "https://api.example.com"
And I set the query parameter "page" to "1"
And I set the query parameter "limit" to "10"
And I set the query parameter "status" to "active"
When I send a GET request to "/users"
# Will call: /users?page=1&limit=10&status=active

# Spanish - Paginar y filtrar resultados
Dado que la URL base es "https://api.ejemplo.com"
Y establezco el parámetro "pagina" a "1"
Y establezco el parámetro "limite" a "10"
Y establezco el parámetro "estado" a "activo"
Cuando hago una petición GET a "/usuarios"
# Llamará a: /usuarios?pagina=1&limite=10&estado=activo
```

---

### Set Query Parameter (Number)

**English:**
```gherkin
Given I set the query parameter "{name}" to {value:d}
```

**Spanish:**
```gherkin
Dado que establezco el parámetro "{nombre}" a {valor:d}
```

**Description (English):**  
Adds a query parameter with a numeric value to the next request. This is useful for pagination limits, numeric filters, or any parameter that expects a number.

**Descripción (Español):**  
Agrega un parámetro de consulta con un valor numérico a la siguiente petición. Esto es útil para límites de paginación, filtros numéricos o cualquier parámetro que espere un número.

**Example:**
```gherkin
# English - Set numeric pagination parameters
Given the base URL is "https://api.example.com"
And I set the query parameter "page" to 2
And I set the query parameter "limit" to 50
And I set the query parameter "minAge" to 18
When I send a GET request to "/users"
# Will call: /users?page=2&limit=50&minAge=18

# Spanish - Establecer parámetros numéricos de paginación
Dado que la URL base es "https://api.ejemplo.com"
Y establezco el parámetro "pagina" a 2
Y establezco el parámetro "limite" a 50
Y establezco el parámetro "edadMinima" a 18
Cuando hago una petición GET a "/usuarios"
# Llamará a: /usuarios?pagina=2&limite=50&edadMinima=18
```

---

## Authentication Steps

### Bearer Token Authentication

**English:**
```gherkin
Given I use bearer token "{token}"
```

**Spanish:**
```gherkin
Dado que uso el token bearer "{token}"
```

**Description (English):**  
Configures Bearer token authentication by adding an `Authorization: Bearer {token}` header to all subsequent requests. This is the most common authentication method for modern APIs and is typically used with JWT (JSON Web Tokens).

**Descripción (Español):**  
Configura la autenticación con token Bearer agregando un header `Authorization: Bearer {token}` a todas las peticiones subsiguientes. Este es el método de autenticación más común para APIs modernas y típicamente se usa con JWT (JSON Web Tokens).

**Example:**
```gherkin
# English - Authenticate with JWT token
Given the base URL is "https://api.example.com"
And I use bearer token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
When I send a GET request to "/protected/profile"
Then the response status should be 200

# Spanish - Autenticar con token JWT
Dado que la URL base es "https://api.ejemplo.com"
Y uso el token bearer "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
Cuando hago una petición GET a "/protegido/perfil"
Entonces el código de respuesta debe ser 200

# English - Using token from variable
Given I send a POST request to "/auth/login" with JSON:
  """
  {"username": "user@example.com", "password": "secret"}
  """
And I extract "token" from the response as "authToken"
And I use bearer token "{authToken}"
When I send a GET request to "/protected/data"

# Spanish - Usando token desde variable
Dado que hago una petición POST a "/auth/login" con el cuerpo:
  """
  {"usuario": "user@ejemplo.com", "password": "secreto"}
  """
Y guardo el valor del campo "token" en la variable "tokenAuth"
Y uso el token bearer "{tokenAuth}"
Cuando hago una petición GET a "/protegido/datos"
```

---

### Basic Authentication

**English:**
```gherkin
Given I use basic authentication with username "{username}" and password "{password}"
```

**Spanish:**
```gherkin
Dado que uso autenticación básica con usuario "{usuario}" y contraseña "{password}"
```

**Description (English):**  
Configures HTTP Basic Authentication by encoding the username and password and adding them to the `Authorization` header. This method is commonly used for simple authentication scenarios or legacy APIs.

**Descripción (Español):**  
Configura la Autenticación Básica HTTP codificando el usuario y contraseña y agregándolos al header `Authorization`. Este método se usa comúnmente para escenarios de autenticación simples o APIs legacy.

**Example:**
```gherkin
# English - Access admin panel with basic auth
Given the base URL is "https://api.example.com"
And I use basic authentication with username "admin" and password "P@ssw0rd123"
When I send a GET request to "/admin/users"
Then the response status should be 200

# Spanish - Acceder a panel de administración con auth básica
Dado que la URL base es "https://api.ejemplo.com"
Y uso autenticación básica con usuario "admin" y contraseña "P@ssw0rd123"
Cuando hago una petición GET a "/admin/usuarios"
Entonces el código de respuesta debe ser 200

# English - Test unauthorized access
Given the base URL is "https://api.example.com"
And I use basic authentication with username "guest" and password "wrongpassword"
When I send a GET request to "/admin/users"
Then the response status should be 401

# Spanish - Probar acceso no autorizado
Dado que la URL base es "https://api.ejemplo.com"
Y uso autenticación básica con usuario "invitado" y contraseña "passwordincorrecto"
Cuando hago una petición GET a "/admin/usuarios"
Entonces el código de respuesta debe ser 401
```

---

## HTTP Request Steps

### GET Request

**English:**
```gherkin
When I send a GET request to "{endpoint}"
```

**Spanish:**
```gherkin
Cuando hago una petición GET a "{endpoint}"
```

**Description (English):**  
Sends an HTTP GET request to retrieve data from the specified endpoint. GET requests are used to read or retrieve resources and should not modify server data. The endpoint path is appended to the base URL.

**Descripción (Español):**  
Envía una petición HTTP GET para recuperar datos del endpoint especificado. Las peticiones GET se usan para leer o recuperar recursos y no deberían modificar datos del servidor. La ruta del endpoint se agrega a la URL base.

**Example:**
```gherkin
# English - Retrieve a single user
Given the base URL is "https://api.example.com"
When I send a GET request to "/users/1"
Then the response status should be 200
And the response should contain "id"
And the response should contain "name"

# Spanish - Recuperar un usuario individual
Dado que la URL base es "https://api.ejemplo.com"
Cuando hago una petición GET a "/usuarios/1"
Entonces el código de respuesta debe ser 200
Y la respuesta debe contener el campo "id"
Y la respuesta debe contener el campo "nombre"

# English - Get list with query parameters
Given the base URL is "https://api.example.com"
And I set the query parameter "page" to 1
And I set the query parameter "limit" to 10
When I send a GET request to "/users"
# Calls: /users?page=1&limit=10

# Spanish - Obtener lista con parámetros de consulta
Dado que la URL base es "https://api.ejemplo.com"
Y establezco el parámetro "pagina" a 1
Y establezco el parámetro "limite" a 10
Cuando hago una petición GET a "/usuarios"
# Llama a: /usuarios?pagina=1&limite=10
```

---

### POST Request (No Body)

**English:**
```gherkin
When I send a POST request to "{endpoint}"
```

**Spanish:**
```gherkin
Cuando hago una petición POST a "{endpoint}"
```

**Description (English):**  
Sends an HTTP POST request without a request body. This is useful for endpoints that trigger actions or operations that don't require input data, such as logout endpoints or simple action triggers.

**Descripción (Español):**  
Envía una petición HTTP POST sin cuerpo de petición. Esto es útil para endpoints que disparan acciones u operaciones que no requieren datos de entrada, como endpoints de cierre de sesión o disparadores de acciones simples.

**Example:**
```gherkin
# English - Logout user (no body needed)
Given the base URL is "https://api.example.com"
And I use bearer token "user-session-token"
When I send a POST request to "/auth/logout"
Then the response status should be 200

# Spanish - Cerrar sesión de usuario (sin cuerpo necesario)
Dado que la URL base es "https://api.ejemplo.com"
Y uso el token bearer "token-sesion-usuario"
Cuando hago una petición POST a "/auth/logout"
Entonces el código de respuesta debe ser 200

# English - Trigger a background job
Given the base URL is "https://api.example.com"
When I send a POST request to "/jobs/process-queue"
Then the response status should be 202

# Spanish - Disparar un trabajo en segundo plano
Dado que la URL base es "https://api.ejemplo.com"
Cuando hago una petición POST a "/trabajos/procesar-cola"
Entonces el código de respuesta debe ser 202
```

---

### POST Request (With JSON Body)

**English:**
```gherkin
When I send a POST request to "{endpoint}" with JSON
  """
  {json_body}
  """
```

**Spanish:**
```gherkin
Cuando hago una petición POST a "{endpoint}" con el cuerpo
  """
  {json_body}
  """
```

**Description (English):**  
Sends an HTTP POST request with a JSON payload in the request body. POST requests are typically used to create new resources on the server. The JSON body can include variable interpolation using `{variableName}` syntax.

**Descripción (Español):**  
Envía una petición HTTP POST con un payload JSON en el cuerpo de la petición. Las peticiones POST típicamente se usan para crear nuevos recursos en el servidor. El cuerpo JSON puede incluir interpolación de variables usando la sintaxis `{nombreVariable}`.

**Example:**
```gherkin
# English - Create a new user
Given the base URL is "https://api.example.com"
When I send a POST request to "/users" with JSON
  """
  {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "role": "developer"
  }
  """
Then the response status should be 201
And the response should contain "id"
And I extract "id" from the response as "newUserId"

# Spanish - Crear un nuevo usuario
Dado que la URL base es "https://api.ejemplo.com"
Cuando hago una petición POST a "/usuarios" con el cuerpo
  """
  {
    "nombre": "Juan Pérez",
    "email": "juan@ejemplo.com",
    "edad": 30,
    "rol": "desarrollador"
  }
  """
Entonces el código de respuesta debe ser 201
Y la respuesta debe contener el campo "id"
Y guardo el valor del campo "id" en la variable "nuevoIdUsuario"

# English - Create post with variable interpolation
Given I set the variable "userId" to 42
When I send a POST request to "/posts" with JSON
  """
  {
    "title": "My First Post",
    "body": "This is the content of my post",
    "userId": {userId}
  }
  """
Then the response status should be 201

# Spanish - Crear publicación con interpolación de variables
Dado que establezco la variable "idUsuario" a 42
Cuando hago una petición POST a "/publicaciones" con el cuerpo
  """
  {
    "titulo": "Mi Primera Publicación",
    "cuerpo": "Este es el contenido de mi publicación",
    "idUsuario": {idUsuario}
  }
  """
Entonces el código de respuesta debe ser 201
```

---

### PUT Request (With JSON Body)

**English:**
```gherkin
When I send a PUT request to "{endpoint}" with JSON
  """
  {json_body}
  """
```

**Spanish:**
```gherkin
Cuando hago una petición PUT a "{endpoint}" con el cuerpo
  """
  {json_body}
  """
```

**Description (English):**  
Sends an HTTP PUT request with a JSON payload to completely replace an existing resource. PUT requests typically require sending the full resource representation, even if only updating specific fields. Use PATCH for partial updates.

**Descripción (Español):**  
Envía una petición HTTP PUT con un payload JSON para reemplazar completamente un recurso existente. Las peticiones PUT típicamente requieren enviar la representación completa del recurso, incluso si solo se actualizan campos específicos. Usa PATCH para actualizaciones parciales.

**Example:**
```gherkin
# English - Update complete user profile
Given the base URL is "https://api.example.com"
And I use bearer token "user-auth-token"
When I send a PUT request to "/users/1" with JSON
  """
  {
    "name": "John Doe Updated",
    "email": "john.updated@example.com",
    "age": 31,
    "role": "senior-developer",
    "active": true
  }
  """
Then the response status should be 200
And the response field "name" should equal "John Doe Updated"

# Spanish - Actualizar perfil completo de usuario
Dado que la URL base es "https://api.ejemplo.com"
Y uso el token bearer "token-auth-usuario"
Cuando hago una petición PUT a "/usuarios/1" con el cuerpo
  """
  {
    "nombre": "Juan Pérez Actualizado",
    "email": "juan.actualizado@ejemplo.com",
    "edad": 31,
    "rol": "desarrollador-senior",
    "activo": true
  }
  """
Entonces el código de respuesta debe ser 200
Y el campo "nombre" debe ser "Juan Pérez Actualizado"

# English - Update with variable
Given I extract "id" from the response as "userId"
When I send a PUT request to "/users/{userId}" with JSON
  """
  {"name": "Updated Name", "email": "new@example.com"}
  """

# Spanish - Actualizar con variable
Dado que guardo el valor del campo "id" en la variable "idUsuario"
Cuando hago una petición PUT a "/usuarios/{idUsuario}" con el cuerpo
  """
  {"nombre": "Nombre Actualizado", "email": "nuevo@ejemplo.com"}
  """
```

---

### PATCH Request (With JSON Body)

**English:**
```gherkin
When I send a PATCH request to "{endpoint}" with JSON
  """
  {json_body}
  """
```

**Spanish:**
```gherkin
Cuando hago una petición PATCH a "{endpoint}" con el cuerpo
  """
  {json_body}
  """
```

**Description (English):**  
Sends an HTTP PATCH request with a JSON payload to partially update an existing resource. Unlike PUT, PATCH only requires the fields you want to update, leaving other fields unchanged. This is more efficient for updating specific attributes.

**Descripción (Español):**  
Envía una petición HTTP PATCH con un payload JSON para actualizar parcialmente un recurso existente. A diferencia de PUT, PATCH solo requiere los campos que deseas actualizar, dejando otros campos sin cambios. Esto es más eficiente para actualizar atributos específicos.

**Example:**
```gherkin
# English - Update only email address
Given the base URL is "https://api.example.com"
And I use bearer token "user-auth-token"
When I send a PATCH request to "/users/1" with JSON
  """
  {
    "email": "newemail@example.com"
  }
  """
Then the response status should be 200
And the response field "email" should equal "newemail@example.com"
# Other fields remain unchanged

# Spanish - Actualizar solo dirección de email
Dado que la URL base es "https://api.ejemplo.com"
Y uso el token bearer "token-auth-usuario"
Cuando hago una petición PATCH a "/usuarios/1" con el cuerpo
  """
  {
    "email": "nuevoemail@ejemplo.com"
  }
  """
Entonces el código de respuesta debe ser 200
Y el campo "email" debe ser "nuevoemail@ejemplo.com"
# Otros campos permanecen sin cambios

# English - Update multiple specific fields
When I send a PATCH request to "/users/1" with JSON
  """
  {
    "active": false,
    "lastLogin": "2024-12-10T10:30:00Z"
  }
  """
Then the response status should be 200

# Spanish - Actualizar múltiples campos específicos
Cuando hago una petición PATCH a "/usuarios/1" con el cuerpo
  """
  {
    "activo": false,
    "ultimoAcceso": "2024-12-10T10:30:00Z"
  }
  """
Entonces el código de respuesta debe ser 200
```

---

### DELETE Request

**English:**
```gherkin
When I send a DELETE request to "{endpoint}"
```

**Spanish:**
```gherkin
Cuando hago una petición DELETE a "{endpoint}"
```

**Description (English):**  
Sends an HTTP DELETE request to remove a resource from the server. DELETE requests typically return status 204 (No Content) on success, or 200 with a confirmation message. The resource should no longer be accessible after deletion.

**Descripción (Español):**  
Envía una petición HTTP DELETE para eliminar un recurso del servidor. Las peticiones DELETE típicamente retornan status 204 (Sin Contenido) en caso de éxito, o 200 con un mensaje de confirmación. El recurso no debería ser accesible después de la eliminación.

**Example:**
```gherkin
# English - Delete a user
Given the base URL is "https://api.example.com"
And I use bearer token "admin-token"
When I send a DELETE request to "/users/1"
Then the response status should be 204

# Verify deletion
When I send a GET request to "/users/1"
Then the response status should be 404

# Spanish - Eliminar un usuario
Dado que la URL base es "https://api.ejemplo.com"
Y uso el token bearer "token-admin"
Cuando hago una petición DELETE a "/usuarios/1"
Entonces el código de respuesta debe ser 204

# Verificar eliminación
Cuando hago una petición GET a "/usuarios/1"
Entonces el código de respuesta debe ser 404

# English - Delete with variable
Given I extract "id" from the response as "postId"
When I send a DELETE request to "/posts/{postId}"
Then the response status should be 200
And the response field "message" should equal "Post deleted successfully"

# Spanish - Eliminar con variable
Dado que guardo el valor del campo "id" en la variable "idPublicacion"
Cuando hago una petición DELETE a "/publicaciones/{idPublicacion}"
Entonces el código de respuesta debe ser 200
Y el campo "mensaje" debe ser "Publicación eliminada exitosamente"
```

---

### Request with Variable

**English:**
```gherkin
When I send a {method} request to "{endpoint}" with the variable "{var_name}"
```

**Description:** Sends a request using data from a previously stored variable.

**Example:**
```gherkin
When I send a POST request to "/users" with the variable "userData"
```

---

## Response Validation Steps

### Validate Status Code

**English:**
```gherkin
Then the response status should be {status:d}
```

**Spanish:**
```gherkin
Entonces el código de respuesta debe ser {status:d}
```

**Description (English):**  
Validates that the HTTP response status code matches the expected value. Common status codes: 200 (OK), 201 (Created), 204 (No Content), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 500 (Server Error).

**Descripción (Español):**  
Valida que el código de estado HTTP de la respuesta coincida con el valor esperado. Códigos comunes: 200 (OK), 201 (Creado), 204 (Sin Contenido), 400 (Petición Incorrecta), 401 (No Autorizado), 404 (No Encontrado), 500 (Error del Servidor).

**Example:**
```gherkin
# English - Validate successful GET
When I send a GET request to "/users/1"
Then the response status should be 200

# English - Validate successful creation
When I send a POST request to "/users" with JSON:
  """
  {"name": "John"}
  """
Then the response status should be 201

# English - Validate not found
When I send a GET request to "/users/99999"
Then the response status should be 404

# Spanish - Validar GET exitoso
Cuando hago una petición GET a "/usuarios/1"
Entonces el código de respuesta debe ser 200

# Spanish - Validar creación exitosa
Cuando hago una petición POST a "/usuarios" con el cuerpo:
  """
  {"nombre": "Juan"}
  """
Entonces el código de respuesta debe ser 201

# Spanish - Validar no encontrado
Cuando hago una petición GET a "/usuarios/99999"
Entonces el código de respuesta debe ser 404
```

---

### Validate Successful Response

**English:**
```gherkin
Then the response should be successful
```

**Spanish:**
```gherkin
Entonces la respuesta debe ser exitosa
```

**Description (English):**  
Validates that the response status code is in the 2xx range (200-299), indicating a successful request. This is useful when you don't care about the exact status code, just that the operation succeeded.

**Descripción (Español):**  
Valida que el código de estado de la respuesta esté en el rango 2xx (200-299), indicando una petición exitosa. Esto es útil cuando no te importa el código de estado exacto, solo que la operación fue exitosa.

**Example:**
```gherkin
# English - Any successful response is acceptable
When I send a POST request to "/users" with JSON:
  """
  {"name": "John"}
  """
Then the response should be successful
# Accepts 200, 201, 202, 204, etc.

# Spanish - Cualquier respuesta exitosa es aceptable
Cuando hago una petición POST a "/usuarios" con el cuerpo:
  """
  {"nombre": "Juan"}
  """
Entonces la respuesta debe ser exitosa
# Acepta 200, 201, 202, 204, etc.
```

---

### Validate Response Contains Field

**English:**
```gherkin
Then the response should contain "{key}"
```

**Spanish:**
```gherkin
Entonces la respuesta debe contener el campo "{campo}"
```

**Description (English):**  
Validates that the response JSON object contains a specific field/key, regardless of its value. This is useful for checking that required fields are present in the response structure.

**Descripción (Español):**  
Valida que el objeto JSON de la respuesta contenga un campo/clave específico, independientemente de su valor. Esto es útil para verificar que los campos requeridos estén presentes en la estructura de la respuesta.

**Example:**
```gherkin
# English - Verify user response structure
When I send a GET request to "/users/1"
Then the response status should be 200
And the response should contain "id"
And the response should contain "name"
And the response should contain "email"
And the response should contain "createdAt"

# Spanish - Verificar estructura de respuesta de usuario
Cuando hago una petición GET a "/usuarios/1"
Entonces el código de respuesta debe ser 200
Y la respuesta debe contener el campo "id"
Y la respuesta debe contener el campo "nombre"
Y la respuesta debe contener el campo "email"
Y la respuesta debe contener el campo "creadoEn"
```

---

### Validate Field Value (String)

**English:**
```gherkin
Then the response field "{key}" should equal "{value}"
```

**Spanish:**
```gherkin
Entonces el campo "{campo}" debe ser "{valor}"
```

**Description (English):**  
Validates that a specific field in the response has an exact string value match. The comparison is case-sensitive and must match exactly, including whitespace.

**Descripción (Español):**  
Valida que un campo específico en la respuesta tenga una coincidencia exacta de valor de texto. La comparación distingue mayúsculas y minúsculas y debe coincidir exactamente, incluyendo espacios en blanco.

**Example:**
```gherkin
# English - Validate exact field values
When I send a GET request to "/users/1"
Then the response status should be 200
And the response field "name" should equal "John Doe"
And the response field "email" should equal "john@example.com"
And the response field "role" should equal "admin"

# Spanish - Validar valores exactos de campos
Cuando hago una petición GET a "/usuarios/1"
Entonces el código de respuesta debe ser 200
Y el campo "nombre" debe ser "Juan Pérez"
Y el campo "email" debe ser "juan@ejemplo.com"
Y el campo "rol" debe ser "admin"

# English - Validate after creation
When I send a POST request to "/users" with JSON:
  """
  {"name": "Jane Smith", "email": "jane@example.com"}
  """
Then the response status should be 201
And the response field "name" should equal "Jane Smith"
And the response field "email" should equal "jane@example.com"

# Spanish - Validar después de creación
Cuando hago una petición POST a "/usuarios" con el cuerpo:
  """
  {"nombre": "María García", "email": "maria@ejemplo.com"}
  """
Entonces el código de respuesta debe ser 201
Y el campo "nombre" debe ser "María García"
Y el campo "email" debe ser "maria@ejemplo.com"
```

---

### Validate Field Value (Number)

**English:**
```gherkin
Then the response field "{key}" should equal {value:d}
```

**Spanish:**
```gherkin
Entonces el campo "{campo}" debe ser {valor:d}
```

**Description (English):**  
Validates that a specific field in the response has an exact numeric value. This works for integers and will perform a numeric comparison (not string comparison).

**Descripción (Español):**  
Valida que un campo específico en la respuesta tenga un valor numérico exacto. Esto funciona para enteros y realizará una comparación numérica (no comparación de texto).

**Example:**
```gherkin
# English - Validate numeric fields
When I send a GET request to "/users/1"
Then the response status should be 200
And the response field "id" should equal 1
And the response field "age" should equal 30
And the response field "loginCount" should equal 42

# Spanish - Validar campos numéricos
Cuando hago una petición GET a "/usuarios/1"
Entonces el código de respuesta debe ser 200
Y el campo "id" debe ser 1
Y el campo "edad" debe ser 30
Y el campo "contadorAccesos" debe ser 42

# English - Validate after increment
When I send a POST request to "/users/1/increment-login"
Then the response status should be 200
And the response field "loginCount" should equal 43

# Spanish - Validar después de incremento
Cuando hago una petición POST a "/usuarios/1/incrementar-acceso"
Entonces el código de respuesta debe ser 200
Y el campo "contadorAccesos" debe ser 43
```

---

### Validate Field Equals Variable

**English:**
```gherkin
Then the response field "{key}" should equal the variable "{variable}"
```

**Spanish:**
```gherkin
Entonces el campo "{campo}" debe ser igual a la variable "{variable}"
```

**Description:** Validates that a field value matches a stored variable.

**Example:**
```gherkin
Then the response field "userId" should equal the variable "expectedUserId"
Entonces el campo "userId" debe ser igual a la variable "expectedUserId"
```

---

### Validate JSONPath (String)

**English:**
```gherkin
Then the response "{json_path}" should be "{expected_value}"
```

**Description:** Validates a value using JSONPath expression (string).

**Example:**
```gherkin
Then the response "$.user.name" should be "John Doe"
```

---

### Validate JSONPath (Number)

**English:**
```gherkin
Then the response "{json_path}" should be {expected_value:d}
```

**Description:** Validates a value using JSONPath expression (number).

**Example:**
```gherkin
Then the response "$.user.age" should be 30
```

---

### Validate JSONPath Pattern

**English:**
```gherkin
Then the response "{json_path}" should match "{pattern}"
```

**Description:** Validates that a JSONPath result matches a pattern.

**Example:**
```gherkin
Then the response "$.user.email" should match "##email"
```

---

### Validate Response is Valid JSON

**English:**
```gherkin
Then the response should be valid JSON
```

**Description:** Validates that the response body is valid JSON.

**Example:**
```gherkin
Then the response should be valid JSON
```

---

### Validate Response Time

**English:**
```gherkin
Then the response time should be less than {max_time:f} seconds
```

**Spanish:**
```gherkin
Entonces el tiempo de respuesta debe ser menor a {max_time:f} segundos
```

**Description:** Validates that the response time is below a threshold.

**Example:**
```gherkin
Then the response time should be less than 2.0 seconds
Entonces el tiempo de respuesta debe ser menor a 2.0 segundos
```

---

### Validate Response Structure

**English:**
```gherkin
Then the response should have the following structure
  """
  {json_schema}
  """
```

**Spanish:**
```gherkin
Entonces la respuesta debe tener la siguiente estructura
  """
  {json_schema}
  """
```

**Description:** Validates the response against a JSON structure.

**Example:**
```gherkin
Then the response should have the following structure
  """
  {
    "id": "#number",
    "name": "#string",
    "email": "#email"
  }
  """
```

---

## Data Extraction Steps

### Extract Field to Variable

**English:**
```gherkin
When I extract "{json_path}" from the response as "{variable_name}"
```

**Spanish:**
```gherkin
Cuando guardo el valor del campo "{campo}" en la variable "{variable}"
```

**Description:** Extracts a value from the response and stores it in a variable.

**Example:**
```gherkin
When I extract "id" from the response as "userId"
Cuando guardo el valor del campo "id" en la variable "userId"
```

---

### Store Complete Response

**English:**
```gherkin
When I store the response as "{variable_name}"
```

**Spanish:**
```gherkin
Cuando guardo la respuesta completa en la variable "{variable}"
```

**Description:** Stores the entire response in a variable.

**Example:**
```gherkin
When I store the response as "userResponse"
Cuando guardo la respuesta completa en la variable "userResponse"
```

---

## Variable Management Steps

### Compare Variables (Equal)

**English:**
```gherkin
Then the variable "{var1}" should equal the variable "{var2}"
```

**Spanish:**
```gherkin
Entonces la variable "{var1}" debe ser igual a la variable "{var2}"
```

**Description:** Validates that two variables have the same value.

**Example:**
```gherkin
Then the variable "userId" should equal the variable "expectedId"
Entonces la variable "userId" debe ser igual a la variable "expectedId"
```

---

### Compare Variables (Not Equal)

**English:**
```gherkin
Then the variable "{var1}" should not equal the variable "{var2}"
```

**Spanish:**
```gherkin
Entonces la variable "{var1}" no debe ser igual a la variable "{var2}"
```

**Description:** Validates that two variables have different values.

**Example:**
```gherkin
Then the variable "firstId" should not equal the variable "secondId"
Entonces la variable "firstId" no debe ser igual a la variable "secondId"
```

---

## File Operations Steps

### Load Test Data from File

**English:**
```gherkin
Given I load test data "{data_name}" from file "{file_path}"
```

**Description:** Loads test data from an external file (JSON, YAML, CSV).

**Example:**
```gherkin
Given I load test data "users" from file "test_data/users.json"
```

---

### Load Test Data from JSON

**English:**
```gherkin
Given I load test data "{data_name}" from JSON
  """
  {json_content}
  """
```

**Description:** Loads test data from inline JSON.

**Example:**
```gherkin
Given I load test data "user" from JSON
  """
  {"name": "John", "email": "john@example.com"}
  """
```

---

### Load Test Data from YAML

**English:**
```gherkin
Given I load test data "{data_name}" from YAML
  """
  {yaml_content}
  """
```

**Description:** Loads test data from inline YAML.

**Example:**
```gherkin
Given I load test data "config" from YAML
  """
  name: John
  email: john@example.com
  """
```

---

### POST with JSON File

**English:**
```gherkin
When I POST to "{endpoint}" with JSON file "{file_path}"
```

**Description:** Sends a POST request with JSON data from a file.

**Example:**
```gherkin
When I POST to "/users" with JSON file "test_data/create_user.json"
```

---

### PUT with JSON File

**English:**
```gherkin
When I PUT to "{endpoint}" with JSON file "{file_path}"
```

**Description:** Sends a PUT request with JSON data from a file.

**Example:**
```gherkin
When I PUT to "/users/1" with JSON file "test_data/update_user.json"
```

---

### PATCH with JSON File

**English:**
```gherkin
When I PATCH to "{endpoint}" with JSON file "{file_path}"
```

**Description:** Sends a PATCH request with JSON data from a file.

**Example:**
```gherkin
When I PATCH to "/users/1" with JSON file "test_data/patch_user.json"
```

---

### Request with Data File

**English:**
```gherkin
When I {method} to "{endpoint}" with data file "{file_path}"
```

**Description:** Sends a request with data from a file (auto-detects format).

**Example:**
```gherkin
When I POST to "/users" with data file "test_data/user.json"
```

---

### Validate Response Matches JSON File

**English:**
```gherkin
Then the response should match JSON file "{file_path}"
```

**Description:** Validates that the response matches JSON from a file.

**Example:**
```gherkin
Then the response should match JSON file "expected/user_response.json"
```

---

### Validate Response Matches Schema File

**English:**
```gherkin
Then the response should match schema file "{file_path}"
```

**Description:** Validates the response against a JSON schema file.

**Example:**
```gherkin
Then the response should match schema file "schemas/user_schema.json"
```

---

### Save Response to File

**English:**
```gherkin
When I save the response to file "{file_path}"
```

**Description:** Saves the response to a file.

**Example:**
```gherkin
When I save the response to file "output/user_response.json"
```

---

### Save Variable to File

**English:**
```gherkin
When I save the variable "{var_name}" to file "{file_path}"
```

**Description:** Saves a variable's value to a file.

**Example:**
```gherkin
When I save the variable "userData" to file "output/user_data.json"
```

---

## Array/Collection Steps

### Validate Response is Array

**English:**
```gherkin
Then the response should be an array
```

**Spanish:**
```gherkin
Entonces la respuesta debe ser un array
Entonces la respuesta debe ser una lista
```

**Description:** Validates that the response is a JSON array.

**Example:**
```gherkin
Then the response should be an array
Entonces la respuesta debe ser un array
```

---

### Validate Array Count

**English:**
```gherkin
Then the response array should have {count:d} items
```

**Spanish:**
```gherkin
Entonces la respuesta debe tener {count:d} elementos
```

**Description:** Validates the number of items in the response array.

**Example:**
```gherkin
Then the response array should have 10 items
Entonces la respuesta debe tener 10 elementos
```

---

### Validate Array Contains Item

**English:**
```gherkin
Then the response array should contain an item with "{key}" equal to "{value}"
```

**Description:** Validates that the array contains an item with a specific key-value pair.

**Example:**
```gherkin
Then the response array should contain an item with "name" equal to "John Doe"
```

---

### Validate Each Item Has Field

**English:**
```gherkin
Then each item in the response array should have "{key}"
```

**Spanish:**
```gherkin
Entonces cada elemento debe tener el campo "{campo}"
```

**Description:** Validates that every item in the array has a specific field.

**Example:**
```gherkin
Then each item in the response array should have "id"
Entonces cada elemento debe tener el campo "id"
```

---

## Schema Validation Steps

### Validate Against Schema

**English:**
```gherkin
Then the response should match the schema
  """
  {json_schema}
  """
```

**Description:** Validates the response against a JSON schema.

**Example:**
```gherkin
Then the response should match the schema
  """
  {
    "type": "object",
    "properties": {
      "id": {"type": "number"},
      "name": {"type": "string"}
    },
    "required": ["id", "name"]
  }
  """
```

---

## Type Validation Steps

### Validate Field is String

**English:**
```gherkin
Then the response "{json_path}" should be a string
```

**Description:** Validates that a field is of type string.

**Example:**
```gherkin
Then the response "$.user.name" should be a string
```

---

### Validate Field is Number

**English:**
```gherkin
Then the response "{json_path}" should be a number
```

**Description:** Validates that a field is of type number.

**Example:**
```gherkin
Then the response "$.user.age" should be a number
```

---

### Validate Field is Boolean

**English:**
```gherkin
Then the response "{json_path}" should be a boolean
```

**Description:** Validates that a field is of type boolean.

**Example:**
```gherkin
Then the response "$.user.active" should be a boolean
```

---

## Utility Steps

### Wait

**English:**
```gherkin
When I wait {seconds:f} seconds
```

**Spanish:**
```gherkin
Cuando espero {segundos:f} segundos
```

**Description:** Pauses execution for the specified number of seconds.

**Example:**
```gherkin
When I wait 2.5 seconds
Cuando espero 2.5 segundos
```

---

### Print Response

**English:**
```gherkin
When I print the response
```

**Spanish:**
```gherkin
Cuando imprimo la respuesta
```

**Description:** Prints the response to the console for debugging.

**Example:**
```gherkin
When I print the response
Cuando imprimo la respuesta
```

---

## 🎯 Pattern Matching

Judo Framework supports Karate-style pattern matching:

| Pattern | Description | Example |
|---------|-------------|---------|
| `##string` | Any string | `"name": "##string"` |
| `##number` | Any number | `"age": "##number"` |
| `##boolean` | Boolean value | `"active": "##boolean"` |
| `##array` | Any array | `"items": "##array"` |
| `##object` | Any object | `"user": "##object"` |
| `##null` | Null value | `"deleted": "##null"` |
| `##notnull` | Not null | `"id": "##notnull"` |
| `##uuid` | UUID format | `"id": "##uuid"` |
| `##email` | Email format | `"email": "##email"` |
| `##url` | URL format | `"website": "##url"` |
| `##regex` | Regex pattern | `"code": "##regex [A-Z]{3}"` |

---

## 📝 Variable Interpolation

Variables can be used in endpoints and JSON bodies using `{variableName}` syntax:

**Example:**
```gherkin
Given I set the variable "userId" to 42
When I send a GET request to "/users/{userId}"
When I send a POST request to "/posts" with JSON:
  """
  {
    "userId": {userId},
    "title": "My Post"
  }
  """
```

---

## 🌍 Language Support

### English
- Complete step definitions
- Natural language syntax
- Karate-style patterns

### Spanish
- Complete step definitions
- Natural language syntax
- Same functionality as English

### Using Both Languages

You can mix English and Spanish steps in the same project:

```gherkin
# English feature
Feature: User API
  Scenario: Create user
    Given the base URL is "https://api.example.com"
    When I send a POST request to "/users" with JSON:
      """
      {"name": "John"}
      """
    Then the response status should be 201

# Spanish feature
# language: es
Característica: API de Usuarios
  Escenario: Crear usuario
    Dado que la URL base es "https://api.example.com"
    Cuando hago una petición POST a "/users" con el cuerpo:
      """
      {"name": "Juan"}
      """
    Entonces el código de respuesta debe ser 201
```

---

## 📊 Summary

### Total Steps Available

| Category | English Steps | Spanish Steps | Total |
|----------|---------------|---------------|-------|
| Configuration | 8 | 6 | 14 |
| Authentication | 2 | 2 | 4 |
| HTTP Requests | 8 | 6 | 14 |
| Response Validation | 15 | 10 | 25 |
| Data Extraction | 2 | 2 | 4 |
| Variable Management | 2 | 2 | 4 |
| File Operations | 10 | 0 | 10 |
| Array/Collection | 4 | 3 | 7 |
| Schema Validation | 1 | 0 | 1 |
| Type Validation | 3 | 0 | 3 |
| Utility | 2 | 2 | 4 |
| **TOTAL** | **57** | **33** | **90** |

---

## 🔗 Related Documentation

- [Getting Started Guide](docs/getting-started.md)
- [DSL Reference](docs/dsl-reference.md)
- [Behave Integration](docs/behave-integration.md)
- [Examples](examples/)

---

**Made with ❤️ at CENTYC for API testing excellence** 🥋
