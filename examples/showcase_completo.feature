# language: es
Característica: Demostración Completa de Judo Framework
  Esta característica demuestra todas las capacidades de Judo Framework
  Cada escenario muestra una funcionalidad o tipo de paso específico

  Antecedentes:
    Dado que tengo un cliente Judo API
    Y que la URL base es "https://jsonplaceholder.typicode.com"

  # ============================================
  # MÉTODOS HTTP BÁSICOS
  # ============================================

  @http @get
  Escenario: Petición GET - Obtener un recurso
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener el campo "id"
    Y la respuesta debe contener el campo "name"
    Y la respuesta debe contener el campo "email"

  @http @post
  Escenario: Petición POST - Crear un nuevo recurso
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "Prueba Judo Framework",
        "body": "Probando petición POST",
        "userId": 1
      }
      """
    Entonces el código de respuesta debe ser 201
    Y la respuesta debe contener el campo "id"
    Y el campo "title" debe ser "Prueba Judo Framework"

  @http @put
  Escenario: Petición PUT - Actualizar recurso completo
    Cuando hago una petición PUT a "/posts/1" con el cuerpo:
      """
      {
        "id": 1,
        "title": "Título Actualizado",
        "body": "Cuerpo Actualizado",
        "userId": 1
      }
      """
    Entonces el código de respuesta debe ser 200
    Y el campo "title" debe ser "Título Actualizado"

  @http @patch
  Escenario: Petición PATCH - Actualización parcial
    Cuando hago una petición PATCH a "/posts/1" con el cuerpo:
      """
      {
        "title": "Título Parcheado"
      }
      """
    Entonces el código de respuesta debe ser 200
    Y el campo "title" debe ser "Título Parcheado"

  @http @delete
  Escenario: Petición DELETE - Eliminar un recurso
    Cuando hago una petición DELETE a "/posts/1"
    Entonces el código de respuesta debe ser 200

  # ============================================
  # PARÁMETROS DE CONSULTA
  # ============================================

  @parametros-consulta
  Escenario: Parámetros de consulta - Filtrar resultados
    Dado que establezco el parámetro "userId" a "1"
    Cuando hago una petición GET a "/posts"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe ser un array
    Y cada elemento debe tener el campo "userId"

  # ============================================
  # HEADERS
  # ============================================

  @headers
  Escenario: Headers personalizados
    Dado que establezco el header "X-Custom-Header" a "valor-prueba"
    Y que establezco el header "Accept" a "application/json"
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200

  # ============================================
  # VARIABLES
  # ============================================

  @variables @texto
  Escenario: Variables - Valores de texto
    Dado que establezco la variable "userId" a "1"
    Cuando hago una petición GET a "/users/{userId}"
    Entonces el código de respuesta debe ser 200
    Y el campo "id" debe ser 1

  @variables @numero
  Escenario: Variables - Valores numéricos
    Dado que establezco la variable "postId" a 1
    Cuando hago una petición GET a "/posts/{postId}"
    Entonces el código de respuesta debe ser 200
    Y el campo "id" debe ser 1

  # ============================================
  # EXTRACCIÓN DE DATOS
  # ============================================

  @extraccion
  Escenario: Extraer datos de la respuesta
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "Prueba Extracción",
        "body": "Probando extracción",
        "userId": 1
      }
      """
    Entonces el código de respuesta debe ser 201
    Y guardo el valor del campo "id" en la variable "postCreado"
    Cuando hago una petición GET a "/posts/{postCreado}"
    Entonces el código de respuesta debe ser 200
    Y el campo "title" debe ser "Prueba Extracción"

  @extraccion
  Escenario: Guardar respuesta completa
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y guardo la respuesta completa en la variable "respuestaUsuario"

  # ============================================
  # VALIDACIÓN DE RESPUESTAS
  # ============================================

  @validacion @estado
  Escenario: Validar códigos de estado
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe ser exitosa

  @validacion @campos
  Escenario: Validar campos de respuesta - Texto
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y el campo "name" debe ser "Leanne Graham"
    Y el campo "username" debe ser "Bret"

  @validacion @campos
  Escenario: Validar campos de respuesta - Número
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y el campo "id" debe ser 1

  @validacion @contiene
  Escenario: Validar que la respuesta contiene campos
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener el campo "id"
    Y la respuesta debe contener el campo "name"
    Y la respuesta debe contener el campo "email"
    Y la respuesta debe contener el campo "address"
    Y la respuesta debe contener el campo "company"

  # ============================================
  # VALIDACIÓN DE ARRAYS
  # ============================================

  @arrays @basico
  Escenario: Validar respuesta de tipo array
    Cuando hago una petición GET a "/users"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe ser un array

  @arrays @contiene
  Escenario: Validar que array contiene elemento
    Cuando hago una petición GET a "/users"
    Entonces el código de respuesta debe ser 200
    Y el array "users" debe contener un elemento con "id" igual a "1"
    Y el array "users" debe contener un elemento con "username" igual a "Bret"

  @arrays @cada
  Escenario: Validar que cada elemento del array tiene un campo
    Cuando hago una petición GET a "/users"
    Entonces el código de respuesta debe ser 200
    Y cada elemento debe tener el campo "id"
    Y cada elemento debe tener el campo "name"
    Y cada elemento debe tener el campo "email"

  # ============================================
  # FLUJO DE TRABAJO - CRUD COMPLETO
  # ============================================

  @flujo @crud
  Escenario: Flujo de trabajo CRUD completo
    # CREAR
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "Post de Prueba CRUD",
        "body": "Probando operaciones CRUD completas",
        "userId": 1
      }
      """
    Entonces el código de respuesta debe ser 201
    Y guardo el valor del campo "id" en la variable "postId"
    
    # LEER
    Cuando hago una petición GET a "/posts/{postId}"
    Entonces el código de respuesta debe ser 200
    Y el campo "title" debe ser "Post de Prueba CRUD"
    
    # ACTUALIZAR
    Cuando hago una petición PUT a "/posts/{postId}" con el cuerpo:
      """
      {
        "id": 1,
        "title": "Post CRUD Actualizado",
        "body": "Cuerpo actualizado",
        "userId": 1
      }
      """
    Entonces el código de respuesta debe ser 200
    Y el campo "title" debe ser "Post CRUD Actualizado"
    
    # ACTUALIZACIÓN PARCIAL
    Cuando hago una petición PATCH a "/posts/{postId}" con el cuerpo:
      """
      {
        "title": "Post CRUD Parcheado"
      }
      """
    Entonces el código de respuesta debe ser 200
    
    # ELIMINAR
    Cuando hago una petición DELETE a "/posts/{postId}"
    Entonces el código de respuesta debe ser 200

  # ============================================
  # FLUJO DE TRABAJO - AUTENTICACIÓN
  # ============================================

  @flujo @autenticacion
  Escenario: Flujo de autenticación con token
    Dado que establezco la variable "tokenAuth" a "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    Y que uso el token bearer "{tokenAuth}"
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200

  # ============================================
  # UTILIDADES
  # ============================================

  @utilidad @espera
  Escenario: Esperar entre peticiones
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y espero 1.0 segundos
    Cuando hago una petición GET a "/users/2"
    Entonces el código de respuesta debe ser 200

  @utilidad @debug
  Escenario: Imprimir respuesta para depuración
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y imprimo la respuesta

  # ============================================
  # ESCENARIOS COMPLEJOS
  # ============================================

  @complejo @anidado
  Escenario: Trabajar con datos anidados
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener el campo "address"
    Y la respuesta debe contener el campo "company"

  @complejo @multiples-peticiones
  Escenario: Múltiples peticiones relacionadas
    # Obtener usuario
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y guardo el valor del campo "id" en la variable "userId"
    
    # Obtener posts del usuario
    Dado que establezco el parámetro "userId" a "{userId}"
    Cuando hago una petición GET a "/posts"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe ser un array
    
    # Obtener primer post
    Cuando hago una petición GET a "/posts/1"
    Entonces el código de respuesta debe ser 200
    Y guardo el valor del campo "id" en la variable "postId"
    
    # Obtener comentarios del post
    Cuando hago una petición GET a "/posts/{postId}/comments"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe ser un array

  @complejo @datos-parametrizados
  Esquema del escenario: Pruebas parametrizadas con ejemplos
    Cuando hago una petición GET a "/users/<userId>"
    Entonces el código de respuesta debe ser 200
    Y el campo "id" debe ser <userId>
    Y la respuesta debe contener el campo "name"
    Y la respuesta debe contener el campo "email"
    
    Ejemplos:
      | userId |
      | 1      |
      | 2      |
      | 3      |

  # ============================================
  # RENDIMIENTO
  # ============================================

  @rendimiento
  Escenario: Validar tiempo de respuesta
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y el tiempo de respuesta debe ser menor a 5.0 segundos

  # ============================================
  # VARIABLES DE ENTORNO (.env)
  # ============================================

  @env @seguridad
  Escenario: Usar variables de entorno para autenticación
    # Cargar datos sensibles como tokens desde archivo .env
    # Esto mantiene las credenciales fuera del control de versiones
    # Crear archivo .env con: API_TOKEN=Bearer test123
    # Crear archivo .env con: API_KEY=tu_api_key_aqui
    Dado que agrego el header "Authorization" desde env "API_TOKEN"
    Y que agrego el header "X-API-Key" desde env "API_KEY"
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener el campo "id"

  @env @multiple-headers
  Escenario: Múltiples headers desde variables de entorno
    # Cargar múltiples headers desde .env para autenticación compleja
    # Útil para APIs que requieren múltiples headers de autenticación
    # Ejemplo .env:
    #   API_TOKEN=Bearer eyJhbGc...
    #   API_KEY=sk_test_123
    #   TENANT_ID=tenant_abc
    Dado que establezco el header "Authorization" desde env "API_TOKEN"
    Y que establezco el header "X-API-Key" desde env "API_KEY"
    Y que establezco el header "X-Tenant-ID" desde env "TENANT_ID"
    Cuando hago una petición GET a "/posts/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener el campo "title"

  @env @variables-dinamicas
  Escenario: Variables dinámicas desde .env para configuración
    # Cargar configuraciones dinámicas desde .env
    # Útil para cambiar URLs base, endpoints, IDs, etc. sin modificar el código
    # Ejemplo .env:
    #   BASE_API_URL=https://api.staging.com
    #   USER_ID=12345
    #   ENDPOINT_SUFFIX=/v2/data
    Dado que obtengo el valor "BASE_API_URL" desde env y lo almaceno en "urlBase"
    Y que obtengo el valor "USER_ID" desde env y lo almaceno en "userId"
    Y que obtengo el valor "ENDPOINT_SUFFIX" desde env y lo almaceno en "endpointSuffix"
    Y que la URL base es "{urlBase}"
    Cuando hago una petición GET a "/users/{userId}{endpointSuffix}"
    Entonces el código de respuesta debe ser 200

  @env @configuracion-completa
  Escenario: Configuración completa desde variables de entorno
    # Ejemplo completo usando múltiples variables de entorno
    # para configurar toda la prueba dinámicamente
    # Ejemplo .env:
    #   TEST_API_URL=https://jsonplaceholder.typicode.com
    #   TEST_USER_ID=1
    #   TEST_POST_TITLE=Mi Post de Prueba
    #   AUTH_TOKEN=Bearer abc123
    Dado que obtengo el valor "TEST_API_URL" desde env y lo almaceno en "apiUrl"
    Y que obtengo el valor "TEST_USER_ID" desde env y lo almaceno en "testUserId"
    Y que obtengo el valor "TEST_POST_TITLE" desde env y lo almaceno en "postTitle"
    Y que obtengo el valor "AUTH_TOKEN" desde env y lo almaceno en "authToken"
    Y que la URL base es "{apiUrl}"
    Y que uso el token bearer "{authToken}"
    Cuando hago una petición GET a "/users/{testUserId}"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener el campo "name"
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "{postTitle}",
        "body": "Contenido de prueba",
        "userId": {testUserId}
      }
      """
    Entonces el código de respuesta debe ser 201
    Y el campo "title" debe ser "{postTitle}"

  # ============================================
  # MANEJO DE ERRORES
  # ============================================

  @errores @no-encontrado
  Escenario: Manejar 404 No Encontrado
    Cuando hago una petición GET a "/users/999999"
    Entonces el código de respuesta debe ser 404

  @errores @validacion
  Escenario: Validar respuestas de error
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {}
      """
    Entonces el código de respuesta debe ser 201

  # ============================================
  # VARIABLES JSON AVANZADAS
  # ============================================

  @variables @json
  Escenario: Variables con datos JSON complejos
    Dado que establezco la variable "nuevoUsuario" al JSON
      """
      {
        "name": "Usuario de Prueba",
        "email": "usuario@test.com",
        "address": {
          "city": "Madrid",
          "country": "España"
        }
      }
      """
    Cuando hago una petición POST a "/users" con la variable "nuevoUsuario"
    Entonces el código de respuesta debe ser 201
    Y el campo "name" debe ser "Usuario de Prueba"

  # ============================================
  # PETICIONES CON VARIABLES
  # ============================================

  @variables @peticiones
  Escenario: Peticiones usando variables para diferentes métodos
    Dado que establezco la variable "datosPost" al JSON
      """
      {
        "title": "Post desde Variable",
        "body": "Contenido desde variable",
        "userId": 1
      }
      """
    Cuando hago una petición POST a "/posts" con la variable "datosPost"
    Entonces el código de respuesta debe ser 201
    Y guardo el valor del campo "id" en la variable "postId"
    
    Dado que establezco la variable "datosActualizacion" al JSON
      """
      {
        "title": "Post Actualizado desde Variable",
        "body": "Contenido actualizado",
        "userId": 1
      }
      """
    Cuando hago una petición PUT a "/posts/{postId}" con la variable "datosActualizacion"
    Entonces el código de respuesta debe ser 200

  # ============================================
  # VALIDACIÓN JSONPATH
  # ============================================

  @jsonpath @validacion
  Escenario: Validación usando JSONPath
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta "$.name" debe ser "Leanne Graham"
    Y la respuesta "$.id" debe ser 1
    Y la respuesta "$.address.city" debe ser "Gwenborough"

  # ============================================
  # VALIDACIÓN DE TIPOS
  # ============================================

  @tipos @validacion
  Escenario: Validar tipos de datos en respuestas
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta "$.id" debe ser un número
    Y la respuesta "$.name" debe ser una cadena
    Y la respuesta "$.email" debe ser un email válido
    Y la respuesta "$.address" debe ser un objeto
    Y la respuesta "$.website" debe ser una URL válida

  @tipos @null
  Escenario: Validar valores null y no-null
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta "$.name" no debe ser null
    Y la respuesta "$.email" no debe ser null

  # ============================================
  # VALIDACIÓN DE ESQUEMAS
  # ============================================

  @esquemas @validacion
  Escenario: Validar estructura con esquema JSON
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe coincidir con el esquema
      """
      {
        "type": "object",
        "required": ["id", "name", "email"],
        "properties": {
          "id": {"type": "number"},
          "name": {"type": "string"},
          "email": {"type": "string", "format": "email"},
          "address": {"type": "object"},
          "company": {"type": "object"}
        }
      }
      """

  # ============================================
  # COMPARACIÓN DE VARIABLES
  # ============================================

  @variables @comparacion
  Escenario: Comparar variables entre sí
    Dado que establezco la variable "valor1" a "test"
    Y que establezco la variable "valor2" a "test"
    Y que establezco la variable "valor3" a "diferente"
    Entonces la variable "valor1" debe ser igual a la variable "valor2"
    Y la variable "valor1" no debe ser igual a la variable "valor3"

  # ============================================
  # LOGGING Y DEPURACIÓN
  # ============================================

  @logging @debug
  Escenario: Habilitar logging de peticiones y respuestas
    Cuando habilito el guardado de peticiones y respuestas
    Y hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y imprimo la respuesta
    Cuando deshabilito el guardado de peticiones y respuestas

  @logging @directorio
  Escenario: Logging con directorio personalizado
    Cuando habilito el guardado de peticiones y respuestas en el directorio "logs_personalizados"
    Y hago una petición GET a "/posts/1"
    Entonces el código de respuesta debe ser 200
    Cuando establezco el directorio de salida a "logs_finales"