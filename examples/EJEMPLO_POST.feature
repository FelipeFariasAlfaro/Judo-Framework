# language: es
Característica: API de Creación de Usuarios
  Como desarrollador
  Quiero crear usuarios mediante POST
  Para validar que la API funciona correctamente

  Escenario: Crear un nuevo usuario exitosamente
    Dado que la URL base es "https://jsonplaceholder.typicode.com"
    Cuando hago una petición POST a "/users" con el cuerpo:
      """
      {
        "name": "Juan Pérez",
        "username": "juanperez",
        "email": "juan@example.com",
        "phone": "1-770-736-8031",
        "website": "juan.org"
      }
      """
    Entonces el código de respuesta debe ser 201
    Y la respuesta debe contener el campo "id"
    Y el campo "name" debe ser "Juan Pérez"
    Y el campo "email" debe ser "juan@example.com"

  Escenario: Crear usuario con datos mínimos
    Dado que la URL base es "https://jsonplaceholder.typicode.com"
    Cuando hago una petición POST a "/users" con el cuerpo:
      """
      {
        "name": "María García",
        "email": "maria@example.com"
      }
      """
    Entonces el código de respuesta debe ser 201
    Y la respuesta debe contener el campo "id"

  Escenario: Crear post para un usuario
    Dado que la URL base es "https://jsonplaceholder.typicode.com"
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "Mi primer post",
        "body": "Este es el contenido de mi primer post en la plataforma",
        "userId": 1
      }
      """
    Entonces el código de respuesta debe ser 201
    Y la respuesta debe contener el campo "id"
    Y el campo "title" debe ser "Mi primer post"
    Y el campo "userId" debe ser 1

  Escenario: Crear múltiples posts y validar
    Dado que la URL base es "https://jsonplaceholder.typicode.com"
    
    # Crear primer post
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "Post sobre Python",
        "body": "Python es un lenguaje increíble",
        "userId": 1
      }
      """
    Entonces el código de respuesta debe ser 201
    Y guardo el valor del campo "id" en la variable "primerPostId"
    
    # Crear segundo post
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "Post sobre Testing",
        "body": "El testing es fundamental",
        "userId": 1
      }
      """
    Entonces el código de respuesta debe ser 201
    Y guardo el valor del campo "id" en la variable "segundoPostId"
    
    # Validar que los IDs son diferentes
    Y la variable "primerPostId" no debe ser igual a la variable "segundoPostId"

  Escenario: Crear comentario en un post
    Dado que la URL base es "https://jsonplaceholder.typicode.com"
    Cuando hago una petición POST a "/comments" con el cuerpo:
      """
      {
        "postId": 1,
        "name": "Excelente artículo",
        "email": "comentarista@example.com",
        "body": "Me gustó mucho este post, muy informativo"
      }
      """
    Entonces el código de respuesta debe ser 201
    Y la respuesta debe contener el campo "id"
    Y el campo "postId" debe ser 1
    Y el campo "email" debe ser "comentarista@example.com"

  Escenario: Crear usuario y luego un post para ese usuario
    Dado que la URL base es "https://jsonplaceholder.typicode.com"
    
    # Primero crear el usuario
    Cuando hago una petición POST a "/users" con el cuerpo:
      """
      {
        "name": "Carlos Rodríguez",
        "username": "carlosr",
        "email": "carlos@example.com"
      }
      """
    Entonces el código de respuesta debe ser 201
    Y guardo el valor del campo "id" en la variable "nuevoUserId"
    
    # Luego crear un post para ese usuario
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "Mi primer post como nuevo usuario",
        "body": "Hola a todos, soy nuevo aquí",
        "userId": {nuevoUserId}
      }
      """
    Entonces el código de respuesta debe ser 201
    Y el campo "userId" debe ser igual a la variable "nuevoUserId"

  Escenario: Validar estructura completa de respuesta POST
    Dado que la URL base es "https://jsonplaceholder.typicode.com"
    Cuando hago una petición POST a "/posts" con el cuerpo:
      """
      {
        "title": "Post de prueba",
        "body": "Contenido de prueba",
        "userId": 5
      }
      """
    Entonces el código de respuesta debe ser 201
    Y la respuesta debe tener la siguiente estructura:
      """
      {
        "id": "#number",
        "title": "Post de prueba",
        "body": "Contenido de prueba",
        "userId": 5
      }
      """
