# language: es
@protocols
Característica: Servicios no JSON en español

  Antecedentes:
    Dado que tengo un cliente Judo API
    Y la URL base es "__BASE__"

  Escenario: SOAP y XML
    Cuando envío una petición SOAP a "/soap" con la acción "urn:GetUser"
      """
      <Envelope><Body><GetUser id="1"/></Body></Envelope>
      """
    Entonces la respuesta SOAP no debe ser un fallo
    Y la respuesta debe ser XML válido
    Y el XML de la respuesta "//Result/Message" debe ser "ok"
    Cuando envío una petición SOAP a "/soap" con la acción "urn:f"
      """
      <Envelope><Body>FAULT</Body></Envelope>
      """
    Entonces el código del fallo SOAP debe ser "Server"
    Y el mensaje del fallo SOAP debe contener "Boom"

  Escenario: formularios, texto y CSV
    Cuando envío un POST de formulario a "/form"
      | field   | value |
      | usuario | ana   |
    Entonces la respuesta "$.fields.usuario" debe ser "ana"
    Cuando hago una petición GET a "/text"
    Entonces el texto de la respuesta debe contener "hello"
    Y el tipo de contenido de la respuesta debe ser "text/plain"
    Cuando hago una petición GET a "/csv"
    Entonces la respuesta debe ser un CSV con 2 filas
    Y la columna CSV "name" debe contener "Ana"

  Escenario: Server-Sent Events
    Cuando abro el stream SSE "/sse"
    Entonces debo recibir un evento SSE "tick" en máximo 5 segundos
    Y debo recibir 4 eventos SSE en máximo 5 segundos
    Y los datos del último evento SSE "$.n" deben ser "4"
    Y cierro el stream SSE

  Escenario: GraphQL
    Dado establezco las variables GraphQL
      """
      {"name": "Zoe"}
      """
    Cuando envío la mutación GraphQL a "/graphql"
      """
      mutation($name: String!) { createUser(name: $name) { id name } }
      """
    Entonces la respuesta GraphQL no debe tener errores
    Y los datos GraphQL "createUser.name" deben ser "Zoe"
    Cuando envío la consulta GraphQL a "/graphql"
      """
      query { users { id name } }
      """
    Entonces los datos GraphQL "users" deben tener 2 elementos
