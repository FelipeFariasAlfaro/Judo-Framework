# language: es
Característica: Variables de Entorno Dinámicas
  Como desarrollador
  Quiero poder cargar cualquier valor desde .env y usarlo como variable
  Para tener configuraciones completamente dinámicas

  Antecedentes:
    Dado que tengo un cliente Judo API

  @env @dinamico @basico
  Escenario: Cargar URL base desde variable de entorno
    # Ejemplo .env:
    # BASE_API_URL=https://jsonplaceholder.typicode.com
    Dado que obtengo el valor "BASE_API_URL" desde env y lo almaceno en "urlBase"
    Y que la URL base es "{urlBase}"
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener el campo "name"

  @env @dinamico @multiple
  Escenario: Configuración completa desde variables de entorno
    # Ejemplo .env:
    # TEST_API_URL=https://jsonplaceholder.typicode.com
    # TEST_USER_ID=1
    # TEST_POST_TITLE=Mi Post Dinámico
    Dado que obtengo el valor "TEST_API_URL" desde env y lo almaceno en "apiUrl"
    Y que obtengo el valor "TEST_USER_ID" desde env y lo almaceno en "userId"
    Y que obtengo el valor "TEST_POST_TITLE" desde env y lo almaceno en "postTitle"
    Y que la URL base es "{apiUrl}"
    
    # Usar variables dinámicas en peticiones
    Cuando hago una petición GET a "/users/{userId}"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener el campo "id"
    Y el campo "id" debe ser {userId}
    
    # Crear post con título dinámico
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "{postTitle}",
        "body": "Contenido de prueba dinámico",
        "userId": {userId}
      }
      """
    Entonces el código de respuesta debe ser 201
    Y el campo "title" debe ser "{postTitle}"

  @env @dinamico @endpoints
  Escenario: Endpoints dinámicos desde variables de entorno
    # Ejemplo .env:
    # BASE_API_URL=https://jsonplaceholder.typicode.com
    # USER_ID=2
    # ENDPOINT_SUFFIX=/posts
    Dado que obtengo el valor "BASE_API_URL" desde env y lo almaceno en "baseUrl"
    Y que obtengo el valor "USER_ID" desde env y lo almaceno en "userId"
    Y que obtengo el valor "ENDPOINT_SUFFIX" desde env y lo almaceno en "endpointSuffix"
    Y que la URL base es "{baseUrl}"
    
    # Construir endpoint dinámicamente
    Cuando hago una petición GET a "/users/{userId}{endpointSuffix}"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe ser un array

  @env @dinamico @autenticacion
  Escenario: Autenticación dinámica desde variables de entorno
    # Ejemplo .env:
    # TEST_API_URL=https://jsonplaceholder.typicode.com
    # AUTH_TOKEN=Bearer abc123xyz
    # TENANT_ID=tenant_test
    Dado que obtengo el valor "TEST_API_URL" desde env y lo almaceno en "apiUrl"
    Y que obtengo el valor "AUTH_TOKEN" desde env y lo almaceno en "authToken"
    Y que obtengo el valor "TENANT_ID" desde env y lo almaceno in "tenantId"
    Y que la URL base es "{apiUrl}"
    Y que uso el token bearer "{authToken}"
    Y que establezco el header "X-Tenant-ID" a "{tenantId}"
    
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200

  @env @dinamico @json-variables
  Escenario: Variables de entorno en datos JSON
    # Ejemplo .env:
    # TEST_API_URL=https://jsonplaceholder.typicode.com
    # POST_TITLE=Título desde ENV
    # POST_BODY=Contenido desde variable de entorno
    # USER_ID=1
    Dado que obtengo el valor "TEST_API_URL" desde env y lo almaceno en "apiUrl"
    Y que obtengo el valor "POST_TITLE" desde env y lo almaceno en "tituloPost"
    Y que obtengo el valor "POST_BODY" desde env y lo almaceno en "cuerpoPost"
    Y que obtengo el valor "USER_ID" desde env y lo almaceno en "userId"
    Y que la URL base es "{apiUrl}"
    
    # Usar variables de entorno en JSON
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "{tituloPost}",
        "body": "{cuerpoPost}",
        "userId": {userId}
      }
      """
    Entonces el código de respuesta debe ser 201
    Y el campo "title" debe ser "{tituloPost}"
    Y el campo "body" debe ser "{cuerpoPost}"

  @env @dinamico @flujo-completo
  Escenario: Flujo completo con configuración dinámica
    # Demostración de un flujo completo usando solo variables de entorno
    # Ejemplo .env:
    # BASE_API_URL=https://jsonplaceholder.typicode.com
    # TEST_USER_ID=1
    # NEW_POST_TITLE=Post Creado Dinámicamente
    # UPDATE_TITLE=Post Actualizado Dinámicamente
    
    # Cargar todas las configuraciones
    Dado que obtengo el valor "BASE_API_URL" desde env y lo almaceno en "baseUrl"
    Y que obtengo el valor "TEST_USER_ID" desde env y lo almaceno en "testUserId"
    Y que obtengo el valor "NEW_POST_TITLE" desde env y lo almaceno en "nuevoTitulo"
    Y que obtengo el valor "UPDATE_TITLE" desde env y lo almaceno en "tituloActualizado"
    Y que la URL base es "{baseUrl}"
    
    # CREAR - Crear post con datos dinámicos
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "{nuevoTitulo}",
        "body": "Contenido dinámico de prueba",
        "userId": {testUserId}
      }
      """
    Entonces el código de respuesta debe ser 201
    Y guardo el valor del campo "id" en la variable "postId"
    
    # LEER - Verificar post creado
    Cuando hago una petición GET a "/posts/{postId}"
    Entonces el código de respuesta debe ser 200
    Y el campo "title" debe ser "{nuevoTitulo}"
    
    # ACTUALIZAR - Actualizar con nuevo título dinámico
    Cuando hago una petición PUT a "/posts/{postId}" con el cuerpo:
      """
      {
        "id": {postId},
        "title": "{tituloActualizado}",
        "body": "Contenido actualizado dinámicamente",
        "userId": {testUserId}
      }
      """
    Entonces el código de respuesta debe ser 200
    Y el campo "title" debe ser "{tituloActualizado}"
    
    # ELIMINAR
    Cuando hago una petición DELETE a "/posts/{postId}"
    Entonces el código de respuesta debe ser 200