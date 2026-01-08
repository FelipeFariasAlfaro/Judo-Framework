# Judo Framework - Referencia Completa de Pasos (Español)

**✅ VERIFICADO**: Todos los pasos extraídos del código fuente v1.5.9.1

## Pasos de Configuración

### `que tengo un cliente Judo API` / `tengo un cliente Judo API`
Inicializar contexto Judo para pruebas de API.

### `que la URL base es "{base_url}"` / `la URL base es "{base_url}"`
Establecer la URL base para todas las peticiones HTTP subsecuentes.

### `que establezco la variable "{nombre}" a "{valor}"` / `establezco la variable "{nombre}" a "{valor}"`
Crear o actualizar una variable de tipo string.

### `que establezco la variable "{nombre}" a {valor:d}` / `establezco la variable "{nombre}" a {valor:d}`
Crear o actualizar una variable de tipo entero.

### `que establezco la variable "{nombre}" al JSON` / `establezco la variable "{nombre}" al JSON`
Establecer una variable con datos JSON del texto del paso.

### `obtengo el valor "{env_var_name}" desde env y lo almaceno en "{variable_name}"`
Obtener valor de variable de entorno y almacenarlo en una variable.

## Pasos de Autenticación

### `que uso el token bearer "{token}"` / `uso el token bearer "{token}"`
Establecer autenticación con token bearer para todas las peticiones.

### `que uso autenticación básica con usuario "{usuario}" y contraseña "{password}"` / `uso autenticación básica con usuario "{usuario}" y contraseña "{password}"`
Establecer autenticación básica con usuario y contraseña.

### `que establezco el header "{nombre}" a "{valor}"` / `establezco el header "{nombre}" a "{valor}"`
Agregar un header HTTP personalizado a todas las peticiones.

### `que establezco el header "{nombre_header}" desde env "{nombre_var_env}"` / `que agrego el header "{nombre_header}" desde env "{nombre_var_env}"` / `establezco el header "{nombre_header}" desde env "{nombre_var_env}"` / `agrego el header "{nombre_header}" desde env "{nombre_var_env}"`
Establecer un header desde variable de entorno.

### `que establezco el parámetro "{nombre}" a "{valor}"` / `establezco el parámetro "{nombre}" a "{valor}"`
Agregar un parámetro de query (string) a la siguiente petición.

## Pasos de Peticiones HTTP

### `hago una petición GET a "{endpoint}"`
Hacer petición HTTP GET para obtener datos.

### `hago una petición POST a "{endpoint}"`
Hacer petición HTTP POST sin cuerpo.

### `hago una petición POST a "{endpoint}" con el cuerpo` / `hago una petición POST a "{endpoint}" con el cuerpo:`
Hacer petición HTTP POST con cuerpo JSON del texto del paso.

### `hago una petición PUT a "{endpoint}" con el cuerpo` / `hago una petición PUT a "{endpoint}" con el cuerpo:`
Hacer petición HTTP PUT con cuerpo JSON del texto del paso.

### `hago una petición PATCH a "{endpoint}" con el cuerpo` / `hago una petición PATCH a "{endpoint}" con el cuerpo:`
Hacer petición HTTP PATCH con cuerpo JSON del texto del paso.

### `hago una petición DELETE a "{endpoint}"`
Hacer petición HTTP DELETE.

### `hago una petición {método} a "{endpoint}" con la variable "{nombre_var}"`
Hacer petición HTTP con datos JSON desde una variable.

## Pasos de Validación de Respuesta

### `el código de respuesta debe ser {status:d}`
Validar código de estado HTTP de la respuesta.

### `la respuesta debe ser exitosa`
Validar que la respuesta tenga estado exitoso (2xx).

### `la respuesta debe contener el campo "{campo}"`
Validar que la respuesta contenga un campo específico.

### `el campo "{campo}" debe ser "{valor}"`
Validar que un campo tenga un valor string específico.

### `el campo "{campo}" debe ser {valor:d}`
Validar que un campo tenga un valor entero específico.

### `el campo "{campo}" debe ser igual a la variable "{variable}"`
Validar que un campo sea igual a una variable.

### `la respuesta debe tener la siguiente estructura` / `la respuesta debe tener la siguiente estructura:`
Validar estructura de la respuesta contra esquema JSON del texto del paso.

### `la respuesta debe ser un array` / `la respuesta debe ser una lista`
Validar que la respuesta sea un array JSON.

### `la respuesta debe tener {count:d} elementos`
Validar que el array tenga número exacto de elementos.

### `cada elemento debe tener el campo "{campo}"`
Validar que cada elemento del array tenga un campo específico.

### `el array "{ruta_array}" debe contener un elemento con "{campo}" igual a "{valor}"`
Validar que un array anidado contenga un elemento con par clave-valor específico.

### `el tiempo de respuesta debe ser menor a {max_time:f} segundos`
Validar que el tiempo de respuesta esté por debajo del umbral.

### `la respuesta "{ruta_json}" debe ser "{valor_esperado}"`
Validar resultado de expresión JSONPath (string).

### `la respuesta "{ruta_json}" debe ser {valor_esperado:d}`
Validar resultado de expresión JSONPath (entero).

## Pasos de Extracción de Datos

### `guardo el valor del campo "{campo}" en la variable "{variable}"`
Extraer valor de un campo de la respuesta y almacenarlo en variable.

### `guardo la respuesta completa en la variable "{variable}"`
Almacenar toda la respuesta en una variable.

## Pasos de Comparación de Variables

### `la variable "{variable1}" debe ser igual a la variable "{variable2}"`
Comparar que dos variables sean iguales.

### `la variable "{variable1}" no debe ser igual a la variable "{variable2}"`
Comparar que dos variables sean diferentes.

### `debo tener la variable "{variable_name}" con valor "{expected_value}"`
Validar que una variable tenga el valor esperado.

## Pasos de Utilidad

### `espero {segundos:f} segundos`
Pausar ejecución del test por segundos especificados.

### `imprimo la respuesta`
Imprimir respuesta en consola para debugging.

## Pasos de Logging

### `habilito el guardado de peticiones y respuestas`
Habilitar guardado automático de peticiones y respuestas.

### `deshabilito el guardado de peticiones y respuestas`
Deshabilitar guardado automático de peticiones y respuestas.

### `habilito el guardado de peticiones y respuestas en el directorio "{directory}"`
Habilitar guardado con directorio personalizado.

### `establezco el directorio de salida a "{directory}"`
Establecer directorio de salida para logging.

## Pasos de Archivos

### `hago POST a "{endpoint}" con archivo JSON "{ruta_archivo}"`
Enviar petición POST con datos JSON cargados desde archivo.

### `hago PUT a "{endpoint}" con archivo JSON "{ruta_archivo}"`
Enviar petición PUT con datos JSON cargados desde archivo.

### `hago PATCH a "{endpoint}" con archivo JSON "{ruta_archivo}"`
Enviar petición PATCH con datos JSON cargados desde archivo.

### `guardo la respuesta en el archivo "{ruta_archivo}"`
Guardar respuesta en archivo.

### `guardo la variable "{nombre_var}" en el archivo "{ruta_archivo}"`
Guardar contenido de variable en archivo.

## Pasos de Validación de Esquemas

### `la respuesta debe coincidir con el esquema`
Validar respuesta contra esquema JSON del texto del paso.

### `la respuesta debe coincidir con el archivo de esquema "{ruta_archivo}"`
Validar respuesta contra esquema desde archivo.

## Pasos de Validación de Tipos

### `la respuesta "{ruta_json}" debe ser una cadena`
Validar que resultado JSONPath sea tipo string.

### `la respuesta "{ruta_json}" debe ser un número`
Validar que resultado JSONPath sea tipo numérico.

### `la respuesta "{ruta_json}" debe ser un booleano`
Validar que resultado JSONPath sea tipo boolean.

### `la respuesta "{ruta_json}" debe ser un array`
Validar que resultado JSONPath sea tipo array.

### `la respuesta "{ruta_json}" debe ser un objeto`
Validar que resultado JSONPath sea tipo object.

### `la respuesta "{ruta_json}" debe ser null`
Validar que resultado JSONPath sea null.

### `la respuesta "{ruta_json}" no debe ser null`
Validar que resultado JSONPath no sea null.

### `la respuesta "{ruta_json}" debe ser un email válido`
Validar que resultado JSONPath tenga formato de email válido.

### `la respuesta "{ruta_json}" debe ser una URL válida`
Validar que resultado JSONPath tenga formato de URL válido.

### `la respuesta "{ruta_json}" debe ser un UUID válido`
Validar que resultado JSONPath tenga formato de UUID válido.

## Características Avanzadas - Circuit Breaker

### `establezco la política de reintentos con max_retries={max_retries:d} y backoff_strategy="{strategy}"`
Establecer política de reintentos con estrategia de backoff.

### `establezco la política de reintentos con max_retries={max_retries:d}, initial_delay={initial_delay:f}, y max_delay={max_delay:f}`
Establecer política de reintentos con parámetros de retraso personalizados.

### `creo un circuit breaker llamado "{name}" con failure_threshold={threshold:d}`
Crear circuit breaker para prevenir fallas en cascada.

### `creo un circuit breaker llamado "{name}" con failure_threshold={failure_threshold:d}, success_threshold={success_threshold:d}, y timeout={timeout:d}`
Crear circuit breaker con umbrales personalizados y timeout.

### `el circuit breaker "{name}" debe estar en estado {state}`
Validar estado del circuit breaker (CLOSED, OPEN, HALF_OPEN).

### `circuit breaker debe permanecer en estado CLOSED`
Validar que circuit breaker permanezca cerrado.

## Características Avanzadas - Limitador de Velocidad

### `establezco el límite de velocidad a {requests_per_second:f} solicitudes por segundo`
Configurar limitador de velocidad con solicitudes por segundo.

### `establezco límite de velocidad adaptativo con inicial {rps:f} peticiones por segundo`
Configurar limitador de velocidad adaptativo que se ajusta basado en tiempos de respuesta.

### `establezco el acelerador con retraso de {delay_ms:f} milisegundos`
Establecer throttle con retraso fijo entre solicitudes.

### `envío {count:d} solicitudes GET a "{endpoint}"`
Enviar múltiples solicitudes GET para pruebas de rendimiento.

### `todas las respuestas deben tener estado {status:d}`
Validar que todas las respuestas tengan el mismo código de estado.

### `el limitador de velocidad debe tener {remaining:d} solicitudes restantes`
Validar solicitudes restantes en limitador de velocidad.

## Características Avanzadas - WebSocket

### `me conecto a WebSocket "{url}"`
Conectar a servidor WebSocket en la URL especificada.

### `envío mensaje WebSocket`
Enviar mensaje WebSocket usando el texto del paso como contenido del mensaje.

### `debo recibir un mensaje WebSocket dentro de {timeout:f} segundos`
Esperar a recibir mensaje WebSocket dentro del período de timeout.

### `cierro la conexión WebSocket`
Cerrar la conexión WebSocket.

### `me desconecto de WebSocket`
Desconectar de WebSocket (sintaxis alternativa).

## Características Avanzadas - GraphQL

### `ejecuto consulta GraphQL`
Ejecutar consulta GraphQL usando el texto del paso como consulta.

### `ejecuto mutación GraphQL`
Ejecutar mutación GraphQL usando el texto del paso como mutación.

## Características Avanzadas - Interceptores

### `agrego un interceptor de timestamp con nombre de encabezado "{header_name}"`
Agregar timestamp a todas las solicitudes con encabezado especificado.

### `agrego un interceptor de autorización con token "{token}"`
Agregar token de autorización a todas las solicitudes.

### `agrego un interceptor de autorización con token "{token}" y esquema "{schema}"`
Agregar interceptor de autorización con esquema personalizado.

### `agrego un interceptor de registro`
Agregar interceptor de registro para registrar todas las solicitudes.

### `agrego un interceptor de registro de respuestas`
Agregar interceptor de registro de respuestas para registrar todas las respuestas.

## Pasos de Validación de Contratos

### `cargo especificación OpenAPI desde "{spec_file}"`
Cargar especificación OpenAPI.

### `la respuesta debe coincidir con contrato OpenAPI para {method} {path}`
Validar respuesta contra contrato OpenAPI.

### `cargo el contrato OpenAPI desde "{contract_file}"`
Cargar especificación de contrato OpenAPI para validación de contratos.

### `cargo el contrato AsyncAPI desde "{contract_file}"`
Cargar especificación de contrato AsyncAPI para validación de contratos.

### `la respuesta debe coincidir con el esquema del contrato`
Validar respuesta contra esquema del contrato OpenAPI cargado.

### `la respuesta debe coincidir con el esquema "{schema_name}"`
Validar respuesta contra esquema específico del contrato.

### `el campo de respuesta "{field_path}" debe ser de tipo "{expected_type}"`
Validar que un campo específico tenga el tipo de datos esperado.

### `la respuesta debe tener los campos requeridos`
Validar que la respuesta tenga todos los campos requeridos de la tabla del paso.

### `el array de respuesta debe contener objetos con estructura`
Validar que el array contenga objetos con estructura esperada de la tabla.

### `la respuesta debe cumplir con el esquema JSON`
Validar respuesta contra esquema JSON del texto del paso.

### `la respuesta debe cumplir con el esquema JSON del archivo "{schema_file}"`
Validar respuesta contra esquema JSON desde archivo.

### `el campo de respuesta "{field_path}" debe coincidir con el patrón "{pattern}"`
Validar que un campo coincida con patrón regex.

### `la respuesta debe tener tipos de datos consistentes en elementos del array`
Validar que todos los elementos del array tengan tipos de datos consistentes.

### `valido los endpoints del contrato de API`
Validar que todos los endpoints del contrato sean accesibles.

### `el mensaje debe coincidir con el contrato AsyncAPI para canal "{channel}"`
Validar mensaje contra contrato AsyncAPI para canal específico.

### `cargo especificación AsyncAPI desde "{file_path}"`
Cargar especificación AsyncAPI.

## Pasos de Validación Avanzada de Formatos de Datos

### `el campo de respuesta "{field_path}" debe ser un email válido`
Validar que el campo contenga formato de dirección de email válido.

### `el campo de respuesta "{field_path}" debe ser una URL válida`
Validar que el campo contenga formato de URL válido.

### `el campo de respuesta "{field_path}" debe ser un UUID válido`
Validar que el campo contenga formato de UUID válido.

### `el campo de respuesta "{field_path}" debe ser una fecha ISO válida`
Validar que el campo contenga formato de fecha ISO válido.

### `la respuesta debe tener estructura anidada`
Validar que la respuesta tenga estructura anidada esperada del texto del paso.

### `valido el cuerpo de petición contra contrato para {method} {path}`
Validar cuerpo de petición contra especificación del contrato OpenAPI.

### `valido los headers de respuesta contra contrato`
Validar headers de respuesta contra contrato OpenAPI.

### `la respuesta debe coincidir con especificación completa del contrato de datos`
Validación comprensiva contra contrato cargado incluyendo headers y cuerpo.

## Pasos Adicionales de Validación

### `cargo datos de prueba del archivo "{file_path}"`
Cargar datos de prueba desde archivo (sintaxis alternativa).

### `ejecuto prueba dirigida por datos para cada fila`
Ejecutar prueba dirigida por datos para cada fila.

### `todas las pruebas deben completarse exitosamente`
Validar que todas las pruebas dirigidas por datos se completaron exitosamente.

### `envío la misma solicitud GET a "{endpoint}" nuevamente`
Enviar solicitud GET idéntica (para pruebas de caché).

### `la segunda respuesta debe provenir del caché`
Validar que la respuesta proviene del caché.

### `el caché debe contener {count:d} entradas`
Validar número de entradas en caché.

### `el tiempo promedio de respuesta debe ser menor a {max_time:d} milisegundos`
Validar tiempo promedio de respuesta.

### `el tiempo de respuesta p95 debe ser menor a {max_time:d} milisegundos`
Validar tiempo de respuesta p95.

### `la tasa de error debe ser menor al {percentage:d} por ciento`
Validar tasa de error.

### `me desconecto de WebSocket`
Desconectar de WebSocket (sintaxis alternativa).

### `la solicitud debe incluir encabezado Authorization`
Validar que encabezado Authorization está presente.

### `el token OAuth2 debe ser válido`
Validar que token OAuth2 es válido.

### `el token debe contener claim "{claim}" con valor "{value}"`
Validar que token JWT contiene claim específico.

### `ejecuto suite de pruebas`
Ejecutar suite de pruebas.

### `debo generar reportes en formatos`
Generar reportes en múltiples formatos (basado en tabla).

### `el reporte debe ser generado en formato "{format}"`
Validar que reporte fue generado en formato especificado.

### `la respuesta debe completarse a pesar de la latencia inyectada`
Validar que respuesta se completó a pesar de inyección de latencia.

### `algunas solicitudes pueden fallar debido a errores inyectados`
Validar que algunas solicitudes fallaron debido a inyección de errores.

### `solicitud y respuesta deben registrarse en archivo`
Validar que solicitud/respuesta fueron registradas en archivo.

### `el tiempo de respuesta debe ser menor a {milliseconds:d} milisegundos`
Validar tiempo de respuesta en milisegundos.

---

**Notas:**
- Todos los pasos funcionan con cualquier palabra clave de Gherkin (Dado, Cuando, Entonces, Y, Pero)
- La interpolación de variables usa sintaxis `{nombreVariable}`
- Los pasos con `desde env` cargan variables desde archivos .env
- JSONPath usa sintaxis estándar como `$.campo.subcampo`

*Judo Framework v1.5.9.1 - Todos los pasos verificados contra código fuente*