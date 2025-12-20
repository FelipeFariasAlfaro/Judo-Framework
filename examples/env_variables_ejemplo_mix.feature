Feature: Uso de Variables de Entorno desde archivo .env (Modo Mixto)

  Background:
    Given tengo un cliente Judo API
    And la URL base es "https://jsonplaceholder.typicode.com"

  @env @headers
  Scenario: Establecer headers desde variables de entorno
    # Esto demuestra cómo cargar headers desde archivo .env
    # Crea un archivo .env con: API_TOKEN=Bearer test123
    Given agrego el header "Authorization" desde env "API_TOKEN"
    And agrego el header "X-API-Key" desde env "API_KEY"
    When hago una petición GET a "/users/1"
    Then el código de respuesta debe ser 200
    And la respuesta debe contener el campo "id"

  @env @multiple-headers
  Scenario: Múltiples headers desde entorno
    # Cargar múltiples headers desde .env
    Given establezco el header "Authorization" desde env "API_TOKEN"
    And establezco el header "X-API-Key" desde env "API_KEY"
    And establezco el header "X-Custom-Header" desde env "CUSTOM_HEADER_1"
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And la respuesta debe contener el campo "title"

  @env @api-real
  Scenario: Autenticación con API real usando .env
    # Ejemplo práctico con API que requiere autenticación
    # En tu .env: API_TOKEN=tu_token_real
    Given la URL base es "https://api.github.com"
    And agrego el header "Authorization" desde env "GITHUB_TOKEN"
    And agrego el header "Accept" desde env "GITHUB_ACCEPT"
    When hago una petición GET a "/user"
    Then el código de respuesta debe ser 200

  @env @variables
  Scenario: Cargar valores de entorno en variables
    # Cargar valores desde .env y almacenarlos en variables
    Given obtengo el valor "API_BASE_URL" desde env y lo almaceno en "baseUrl"
    And obtengo el valor "API_TOKEN" desde env y lo almaceno en "token"
    And la URL base es "{baseUrl}"
    And uso el token bearer "{token}"
    When hago una petición GET a "/users/1"
    Then el código de respuesta debe ser 200

  @env @dynamic
  Scenario: Configuración dinámica desde entorno
    # Usar variables de entorno para configuración dinámica
    Given obtengo el valor "TEST_USER_ID" desde env y lo almaceno en "userId"
    And obtengo el valor "API_VERSION" desde env y lo almaceno en "version"
    When hago una petición GET a "/users/{userId}"
    Then el código de respuesta debe ser 200
    And la respuesta debe contener el campo "id"
    And el campo "id" debe ser igual a la variable "userId"

  @env @mixed-config
  Scenario: Mezcla de configuración estática y dinámica
    # Combinar valores estáticos con valores desde .env
    Given la URL base es "https://jsonplaceholder.typicode.com"
    And obtengo el valor "API_TOKEN" desde env y lo almaceno en "token"
    And uso el token bearer "{token}"
    And establezco el header "Content-Type" a "application/json"
    And establezco el header "X-Custom-Header" desde env "CUSTOM_HEADER_1"
    When hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "Test Post",
        "body": "This is a test",
        "userId": 1
      }
      """
    Then el código de respuesta debe ser 201
    And la respuesta debe contener el campo "id"

  @env @validation
  Scenario: Validar que las variables de entorno existen
    # Verificar que las variables necesarias están configuradas
    Given obtengo el valor "API_TOKEN" desde env y lo almaceno en "token"
    And obtengo el valor "API_KEY" desde env y lo almaceno en "apiKey"
    Then debo tener la variable "token" con valor "{token}"
    And debo tener la variable "apiKey" con valor "{apiKey}"

  @env @complete-flow
  Scenario: Flujo completo con variables de entorno
    # Ejemplo completo: configuración, autenticación, petición, validación
    Given tengo un cliente Judo API
    And obtengo el valor "API_BASE_URL" desde env y lo almaceno en "baseUrl"
    And obtengo el valor "API_TOKEN" desde env y lo almaceno in "token"
    And la URL base es "{baseUrl}"
    And uso el token bearer "{token}"
    And establezco el header "Accept" a "application/json"
    And establezco el parámetro "page" a "1"
    And establezco el parámetro "limit" a "10"
    When hago una petición GET a "/users"
    Then el código de respuesta debe ser 200
    And la respuesta debe ser un array
    And el tiempo de respuesta debe ser menor a 3.0 segundos
    When guardo la respuesta completa en la variable "usersData"
    Then la variable "usersData" no debe ser igual a la variable "token"
