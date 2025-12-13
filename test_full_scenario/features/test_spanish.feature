# language: es
Característica: API Test Español

  Escenario: GET request con validaciones
    Dado que la URL base es "https://jsonplaceholder.typicode.com"
    Cuando hago una petición GET a "/posts/1"
    Entonces el código de respuesta debe ser 200
    Y el campo "userId" debe ser 1

  Escenario: POST request con datos
    Dado que la URL base es "https://jsonplaceholder.typicode.com"
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "Test en Español",
        "body": "Contenido de prueba",
        "userId": 1
      }
      """
    Entonces el código de respuesta debe ser 201
