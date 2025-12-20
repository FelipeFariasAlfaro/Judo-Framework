Feature: Ejemplo de Modo Mixto
  Como desarrollador latinoamericano
  Quiero usar keywords en inglés con descripciones en español
  Para escribir tests más naturales

  Scenario: Prueba de API en modo mixto
    Given tengo un cliente Judo API
    And la URL base es "https://jsonplaceholder.typicode.com"
    When hago una petición GET a "/users/1"
    Then el código de respuesta debe ser 200
    And la respuesta debe contener el campo "name"
    And la respuesta debe contener el campo "email"
    And el campo "id" debe ser 1

  Scenario: Crear y validar usuario
    Given tengo un cliente Judo API
    And la URL base es "https://jsonplaceholder.typicode.com"
    When hago una petición POST a "/users" con el cuerpo:
      """
      {
        "name": "Juan Pérez",
        "email": "juan@example.com"
      }
      """
    Then el código de respuesta debe ser 201
    And guardo el valor del campo "id" en la variable "userId"
    When hago una petición GET a "/users/{userId}"
    Then el código de respuesta debe ser 200
