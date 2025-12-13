# language: es
Característica: Test Simple

  Escenario: GET simple
    Dado que la URL base es "https://jsonplaceholder.typicode.com"
    Cuando hago una petición GET a "/posts/1"
    Entonces el código de respuesta debe ser 200
