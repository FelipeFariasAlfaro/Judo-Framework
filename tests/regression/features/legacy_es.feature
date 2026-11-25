# language: es
@regression
Característica: Los pasos legacy en español siguen funcionando

  Antecedentes:
    Dado que tengo un cliente Judo API
    Y la URL base es "__BASE__"

  Escenario: GET y validaciones
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe ser exitosa
    Y la respuesta "$.name" debe ser "Ana"
    Y la respuesta "$.id" debe ser 1
    Y la respuesta debe contener el campo "email"
    Y la respuesta "$.active" debe ser un booleano
    Y la respuesta "$.age" debe ser un número
    Y la respuesta "$.name" debe ser una cadena
    Y la respuesta "$.tags" debe ser un array
    Y la respuesta "$.address" debe ser un objeto
    Y la respuesta "$.nickname" debe ser null
    Y la respuesta "$.email" debe ser un email válido

  Escenario: Arrays
    Cuando hago una petición GET a "/users"
    Entonces la respuesta debe ser un array
    Y la respuesta debe tener 2 elementos

  Escenario: Variables, headers y parámetros
    Dado que establezco la variable "quien" a "Ana"
    Y que establezco el header "X-Custom" a "abc"
    Y que establezco el parámetro "q" a "busca"
    Y que uso el token bearer "tok123"
    Cuando hago una petición GET a "/echo?name={quien}"
    Entonces la respuesta "$.query.name" debe ser "Ana"
    Y la respuesta "$.query.q" debe ser "busca"
    Y la respuesta "$.headers.x-custom" debe ser "abc"
    Y la respuesta "$.headers.authorization" debe ser "Bearer tok123"

  Escenario: POST con cuerpo y guardado de campo
    Cuando hago una petición POST a "/users" con el cuerpo
      """
      {"name": "Nuevo"}
      """
    Entonces el código de respuesta debe ser 201
    Cuando guardo el valor del campo "id" en la variable "nuevoId"
    Y establezco la variable "esperado" a 99
    Entonces la variable "nuevoId" debe ser igual a la variable "esperado"

  Escenario: Espera y tiempo
    Cuando hago una petición GET a "/health"
    Entonces el tiempo de respuesta debe ser menor a 5.0 segundos
    Cuando espero 0.1 segundos

  Escenario: Validadores de campo
    Cuando hago una petición GET a "/users/1"
    Entonces el campo de respuesta "age" debe ser de tipo "integer"
    Y el campo de respuesta "email" debe ser un email válido
    Y el campo de respuesta "uuid" debe ser un UUID válido
    Y el campo de respuesta "created" debe ser una fecha ISO válida
