Feature: Contract Validation Examples
  Como desarrollador de API
  Quiero validar contratos de servicios
  Para asegurar que las APIs cumplan con las especificaciones

  Background:
    Given que tengo un cliente Judo API
    And la URL base es "https://jsonplaceholder.typicode.com"

  @contract @openapi
  Scenario: Validar respuesta contra contrato OpenAPI
    Given cargo el contrato OpenAPI desde "specs/jsonplaceholder-openapi.yaml"
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And la respuesta debe coincidir con el esquema del contrato

  @contract @schema
  Scenario: Validar tipos de datos específicos
    When hago una petición GET a "/users/1"
    Then el código de respuesta debe ser 200
    And el campo de respuesta "id" debe ser de tipo "entero"
    And el campo de respuesta "name" debe ser de tipo "cadena"
    And el campo de respuesta "email" debe ser un email válido
    And el campo de respuesta "website" debe ser una URL válida

  @contract @structure
  Scenario: Validar estructura de datos con tabla
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And la respuesta debe tener los campos requeridos
      | campo  | tipo   | requerido |
      | id     | entero | true      |
      | userId | entero | true      |
      | title  | cadena | true      |
      | body   | cadena | true      |

  @contract @array
  Scenario: Validar estructura de array
    When hago una petición GET a "/posts"
    Then el código de respuesta debe ser 200
    And la respuesta debe ser un array
    And el array de respuesta debe contener objetos con estructura
      | campo  | tipo   | requerido |
      | id     | entero | true      |
      | userId | entero | true      |
      | title  | cadena | true      |
      | body   | cadena | true      |
    And la respuesta debe tener tipos de datos consistentes en elementos del array

  @contract @json-schema
  Scenario: Validar contra esquema JSON específico
    When hago una petición GET a "/users/1"
    Then el código de respuesta debe ser 200
    And la respuesta debe cumplir con el esquema JSON
      """
      {
        "type": "object",
        "required": ["id", "name", "email"],
        "properties": {
          "id": {"type": "integer"},
          "name": {"type": "string"},
          "email": {"type": "string", "format": "email"},
          "address": {
            "type": "object",
            "properties": {
              "street": {"type": "string"},
              "city": {"type": "string"}
            }
          }
        }
      }
      """

  @contract @pattern
  Scenario: Validar patrones de datos
    When hago una petición GET a "/users/1"
    Then el código de respuesta debe ser 200
    And el campo de respuesta "email" debe coincidir con el patrón "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    And el campo de respuesta "phone" debe coincidir con el patrón "^\d{1}-\d{3}-\d{3}-\d{4}$"

  @contract @nested
  Scenario: Validar estructura anidada compleja
    When hago una petición GET a "/users/1"
    Then el código de respuesta debe ser 200
    And la respuesta debe tener estructura anidada
      """
      {
        "id": "integer",
        "name": "string",
        "email": "string",
        "address": {
          "street": "string",
          "suite": "string",
          "city": "string",
          "zipcode": "string",
          "geo": {
            "lat": "string",
            "lng": "string"
          }
        },
        "company": {
          "name": "string",
          "catchPhrase": "string",
          "bs": "string"
        }
      }
      """

  @contract @comprehensive
  Scenario: Validación comprensiva de contrato
    Given cargo el contrato OpenAPI desde "specs/jsonplaceholder-openapi.yaml"
    When hago una petición GET a "/posts/1"
    Then el código de respuesta debe ser 200
    And la respuesta debe coincidir con especificación completa del contrato de datos
    And valido los headers de respuesta contra contrato