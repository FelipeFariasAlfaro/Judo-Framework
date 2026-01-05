# language: es
@showcase @avanzado
Característica: Demostración de Características Avanzadas - Framework Judo v1.5.0

  Antecedentes:
    Dado que tengo un cliente API Judo
    Y la URL base es "https://jsonplaceholder.typicode.com"

  # ==================== TIER 1: Robustez y Confiabilidad ====================

  @tier1 @reintentos
  Escenario: Política de Reintentos con Backoff Exponencial
    """
    Demuestra reintentos automáticos con estrategia de backoff exponencial
    para manejar fallos transitorios
    """
    Dado que establezco la política de reintentos con max_retries=3 y backoff_strategy="exponencial"
    Cuando envío una solicitud GET a "/posts/1"
    Entonces el estado de la respuesta debe ser 200
    Y la respuesta debe contener "title"

  @tier1 @circuit-breaker
  Escenario: Patrón Circuit Breaker
    """
    Demuestra circuit breaker para prevenir fallos en cascada
    """
    Dado que creo un circuit breaker llamado "api_breaker" con failure_threshold=5
    Cuando envío una solicitud GET a "/posts/1"
    Entonces el estado de la respuesta debe ser 200
    Y el circuit breaker "api_breaker" debe estar en estado CLOSED

  @tier1 @interceptores
  Escenario: Interceptores de Solicitud
    """
    Demuestra agregar encabezados personalizados mediante interceptores
    """
    Dado que agrego un interceptor de timestamp con nombre de encabezado "X-Request-Time"
    Y agrego un interceptor de autorización con token "test-token"
    Cuando envío una solicitud GET a "/posts/1"
    Entonces el estado de la respuesta debe ser 200

  @tier1 @limitador-velocidad
  Escenario: Limitador de Velocidad
    """
    Demuestra limitación de velocidad para respetar límites de API
    """
    Dado que establezco el límite de velocidad a 10 solicitudes por segundo
    Cuando envío 5 solicitudes GET a "/posts/1"
    Entonces todas las respuestas deben tener estado 200

  @tier1 @acelerador
  Escenario: Acelerador de Solicitudes
    """
    Demuestra retraso fijo entre solicitudes
    """
    Dado que establezco el acelerador con retraso de 100 milisegundos
    Cuando envío una solicitud GET a "/posts/1"
    Y envío una solicitud GET a "/posts/2"
    Entonces ambas respuestas deben tener estado 200

  @tier1 @aserciones
  Escenario: Aserciones Avanzadas - Tiempo de Respuesta
    """
    Demuestra aserciones de tiempo de respuesta
    """
    Cuando envío una solicitud GET a "/posts/1"
    Entonces el estado de la respuesta debe ser 200
    Y el tiempo de respuesta debe ser menor a 5000 milisegundos

  @tier1 @aserciones
  Escenario: Aserciones Avanzadas - Esquema JSON
    """
    Demuestra validación de esquema JSON
    """
    Cuando envío una solicitud GET a "/posts/1"
    Entonces el estado de la respuesta debe ser 200
    Y la respuesta debe coincidir con el esquema JSON:
      """
      {
        "type": "object",
        "properties": {
          "userId": {"type": "number"},
          "id": {"type": "number"},
          "title": {"type": "string"},
          "body": {"type": "string"}
        },
        "required": ["userId", "id", "title", "body"]
      }
      """

  @tier1 @aserciones
  Escenario: Aserciones Avanzadas - Validación de Array
    """
    Demuestra validación de longitud y contenido de array
    """
    Cuando envío una solicitud GET a "/posts"
    Entonces el estado de la respuesta debe ser 200
    Y el array de respuesta debe tener más de 0 elementos
    Y la respuesta debe contener todos los campos: ["userId", "id", "title", "body"]

  # ==================== TIER 2: Rendimiento y APIs Modernas ====================

  @tier2 @pruebas-dirigidas-datos
  Escenario: Pruebas Dirigidas por Datos con CSV
    """
    Demuestra ejecutar la misma prueba con múltiples conjuntos de datos desde CSV
    """
    Dado que cargo datos de prueba del archivo "examples/test_data/posts.csv"
    Cuando ejecuto prueba dirigida por datos para cada fila
    Entonces todas las pruebas deben completarse exitosamente

  @tier2 @rendimiento
  Escenario: Monitoreo de Rendimiento
    """
    Demuestra recopilación y análisis de métricas de rendimiento
    """
    Cuando envío 10 solicitudes GET a "/posts/1"
    Entonces debo tener métricas de rendimiento:
      | métrica | condición |
      | avg_response_time | menor a 5000 |
      | p95_response_time | menor a 5000 |
      | error_rate | igual a 0 |

  @tier2 @caché
  Escenario: Caché de Respuestas
    """
    Demuestra almacenamiento automático en caché de solicitudes GET
    """
    Dado que habilito el caché de respuestas con TTL de 300 segundos
    Cuando envío una solicitud GET a "/posts/1"
    Y envío la misma solicitud GET a "/posts/1" nuevamente
    Entonces ambas respuestas deben tener estado 200
    Y la segunda respuesta debe provenir del caché

  @tier2 @graphql
  Escenario: Consulta GraphQL
    """
    Demuestra ejecución de consulta GraphQL
    Nota: Requiere un endpoint GraphQL
    """
    Dado que establezco la URL base a "https://graphql-api.example.com"
    Cuando ejecuto consulta GraphQL:
      """
      query GetUser($id: ID!) {
        user(id: $id) {
          id
          name
          email
        }
      }
      """
    Entonces la respuesta debe contener "user"

  @tier2 @websocket
  Escenario: Conexión WebSocket
    """
    Demuestra comunicación en tiempo real por WebSocket
    Nota: Requiere un endpoint WebSocket
    """
    Dado que me conecto a WebSocket "wss://echo.websocket.org"
    Cuando envío mensaje WebSocket:
      """
      {"action": "subscribe", "channel": "updates"}
      """
    Entonces debo recibir un mensaje WebSocket dentro de 5 segundos

  @tier2 @oauth2
  Escenario: Autenticación OAuth2
    """
    Demuestra configuración de OAuth2 y actualización automática de token
    """
    Dado que configuro OAuth2 con:
      | client_id | test-client |
      | client_secret | test-secret |
      | token_url | https://auth.example.com/token |
    Cuando envío una solicitud GET a "/posts/1"
    Entonces la solicitud debe incluir encabezado Authorization

  @tier2 @jwt
  Escenario: Autenticación JWT
    """
    Demuestra creación y verificación de token JWT
    """
    Dado que configuro JWT con secreto "my-secret" y algoritmo "HS256"
    Cuando creo token JWT con payload:
      """
      {"user_id": 123, "username": "john"}
      """
    Entonces el token debe ser válido

  # ==================== TIER 3: Características Empresariales ====================

  @tier3 @reportes
  Escenario: Generar Múltiples Formatos de Reporte
    """
    Demuestra generación de reportes en formatos HTML, JSON, JUnit y Allure
    """
    Cuando ejecuto suite de pruebas
    Entonces debo generar reportes en formatos:
      | formato |
      | html |
      | json |
      | junit |
      | allure |

  @tier3 @contrato
  Escenario: Validación de Contrato OpenAPI
    """
    Demuestra validación de respuestas contra especificación OpenAPI
    """
    Dado que cargo especificación OpenAPI desde "examples/openapi.yaml"
    Cuando envío una solicitud GET a "/posts/1"
    Entonces la respuesta debe coincidir con contrato OpenAPI para GET /posts/{id}

  @tier3 @chaos
  Escenario: Ingeniería del Caos - Inyección de Latencia
    """
    Demuestra inyección de latencia para pruebas de resiliencia
    """
    Dado que habilito ingeniería del caos
    Y inyecto latencia entre 100 y 500 milisegundos
    Cuando envío una solicitud GET a "/posts/1"
    Entonces la respuesta debe completarse a pesar de la latencia inyectada

  @tier3 @chaos
  Escenario: Ingeniería del Caos - Inyección de Errores
    """
    Demuestra inyección de errores para pruebas de resiliencia
    """
    Dado que habilito ingeniería del caos
    Y inyecto tasa de error del 10 por ciento
    Cuando envío 10 solicitudes GET a "/posts/1"
    Entonces algunas solicitudes pueden fallar debido a errores inyectados

  @tier3 @registro
  Escenario: Registro Avanzado
    """
    Demuestra registro detallado de solicitud/respuesta
    """
    Dado que establezco nivel de registro a "DEBUG"
    Y habilito registro de solicitud al directorio "request_logs"
    Cuando envío una solicitud GET a "/posts/1"
    Entonces solicitud y respuesta deben registrarse en archivo

  # ==================== Escenarios de Integración ====================

  @integracion @pila-completa
  Escenario: Pila Completa - Reintentos + Limitador + Caché + Monitoreo
    """
    Demuestra uso de múltiples características juntas
    """
    Dado que establezco la política de reintentos con max_retries=3
    Y establezco el límite de velocidad a 10 solicitudes por segundo
    Y habilito el caché de respuestas con TTL de 300 segundos
    Y establezco alerta de rendimiento para umbral de response_time de 1000 milisegundos
    Cuando envío 5 solicitudes GET a "/posts/1"
    Entonces todas las respuestas deben tener estado 200
    Y métricas de rendimiento deben ser recopiladas
    Y caché debe contener 1 entrada

  @integracion @resiliencia
  Escenario: Prueba de Resiliencia con Caos
    """
    Demuestra prueba de resiliencia con ingeniería del caos
    """
    Dado que habilito ingeniería del caos
    Y inyecto latencia entre 100 y 300 milisegundos
    Y inyecto tasa de error del 5 por ciento
    Y creo circuit breaker con failure_threshold=10
    Cuando envío 20 solicitudes GET a "/posts/1"
    Entonces circuit breaker debe permanecer en estado CLOSED
    Y tasa de error debe ser menor al 10 por ciento
