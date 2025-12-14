# language: es
Característica: Uso de Variables de Entorno desde archivo .env

  Antecedentes:
    Dado que tengo un cliente Judo API
    Y que la URL base es "https://jsonplaceholder.typicode.com"

  @env @headers
  Escenario: Establecer headers desde variables de entorno
    # Esto demuestra cómo cargar headers desde archivo .env
    # Crea un archivo .env con: API_TOKEN=Bearer test123
    Dado que agrego el header "Authorization" desde env "API_TOKEN"
    Y que agrego el header "X-API-Key" desde env "API_KEY"
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener el campo "id"

  @env @multiple-headers
  Escenario: Múltiples headers desde entorno
    # Cargar múltiples headers desde .env
    Dado que establezco el header "Authorization" desde env "API_TOKEN"
    Y que establezco el header "X-API-Key" desde env "API_KEY"
    Y que establezco el header "X-Custom-Header" desde env "CUSTOM_HEADER_1"
    Cuando hago una petición GET a "/posts/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener el campo "title"

  @env @api-real
  Escenario: Autenticación con API real usando .env
    # Ejemplo práctico con API que requiere autenticación
    # En tu .env: API_TOKEN=tu_token_real
    Dado que la URL base es "https://api.github.com"
    Y que agrego el header "Authorization" desde env "GITHUB_TOKEN"
    Y que agrego el header "Accept" desde env "GITHUB_ACCEPT"
    Cuando hago una petición GET a "/user"
    Entonces el código de respuesta debe ser 200
