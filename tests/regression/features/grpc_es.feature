# language: es
@grpc
Característica: gRPC por reflexión

  Escenario: llamada unaria y streaming
    Dado me conecto al servidor gRPC "__GRPC__"
    Entonces el servidor gRPC debe exponer el servicio "judo.test.Greeter"
    Cuando envío la petición gRPC "judo.test.Greeter/SayHello"
      """
      {"name": "Luis"}
      """
    Entonces el estado gRPC debe ser "OK"
    Y la respuesta gRPC "message" debe ser "Hello Luis"
    Cuando envío la petición gRPC de streaming "judo.test.Greeter/Countdown"
      """
      {"times": 2}
      """
    Entonces el stream gRPC debe devolver 2 mensajes
    Y el mensaje 1 del stream gRPC "message" debe ser "T-1"
    Cuando cierro la conexión gRPC
