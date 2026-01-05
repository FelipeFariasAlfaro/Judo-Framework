# Referencia Completa de Pasos - Judo Framework (Español)

Esta es la referencia completa de todos los pasos **VERIFICADOS** disponibles en Judo Framework v1.5.0 en español.

**⚠️ IMPORTANTE**: Esta documentación ha sido verificada contra el código fuente del framework. Solo incluye pasos que realmente existen y funcionan.

**💡 Nota**: Todos los pasos usan el decorador `@step()`, lo que significa que funcionan con cualquier keyword (Given, When, Then, And, But, Dado, Cuando, Entonces, Y, Pero). Esto proporciona máxima flexibilidad al escribir tus escenarios de prueba.

## 📋 Índice

- [Configuración](#configuración)
- [Autenticación](#autenticación)
- [Peticiones HTTP](#peticiones-http)
- [Validación de Respuestas](#validación-de-respuestas)
- [Extracción de Datos](#extracción-de-datos)
- [Variables](#variables)
- [Arrays y Colecciones](#arrays-y-colecciones)
- [Utilidades](#utilidades)
- [Logging](#logging)
- [Características Avanzadas - Tier 1](#características-avanzadas---tier-1-robustez-y-confiabilidad)
- [Características Avanzadas - Tier 2](#características-avanzadas---tier-2-rendimiento-y-apis-modernas)
- [Características Avanzadas - Tier 3](#características-avanzadas---tier-3-características-empresariales)

---

## Configuración

### `Dado que tengo un cliente Judo API`
Inicializa el contexto de Judo Framework para comenzar las pruebas de API.

### `Dado que la URL base es "{url}"`
Establece la URL base que se usará para todas las peticiones HTTP subsecuentes.

### `Dado que establezco la variable "{nombre}" a "{valor}"`
Crea o actualiza una variable de tipo string que puede ser reutilizada en otros pasos.

### `Dado que establezco la variable "{nombre}" a {valor:d}`
Crea o actualiza una variable de tipo numérico (entero).

### `obtengo el valor "{nombre_var_env}" desde env y lo almaceno en "{nombre_variable}"`
Obtiene el valor de una variable de entorno (.env) y lo almacena en una variable para uso posterior. Útil para configuraciones dinámicas como URLs base, tokens, etc.

---

## Autenticación

### `Dado que uso el token bearer "{token}"`
Configura autenticación Bearer Token (JWT) para todas las peticiones subsecuentes.

### `Dado que uso autenticación básica con usuario "{usuario}" y contraseña "{password}"`
Configura autenticación HTTP Basic con usuario y contraseña.

### `Dado que establezco el header "{nombre}" a "{valor}"`
Agrega un header HTTP personalizado a todas las peticiones subsecuentes.

### `Dado que establezco el header "{nombre_header}" desde env "{nombre_var_env}"`
### `Dado que agrego el header "{nombre_header}" desde env "{nombre_var_env}"`
Establece un header HTTP usando el valor de una variable de entorno o archivo .env.

### `Dado que establezco el parámetro "{nombre}" a "{valor}"`
Agrega un parámetro de query string a la siguiente petición HTTP.

---

## Peticiones HTTP

### `Cuando hago una petición GET a "{endpoint}"`
Envía una petición HTTP GET para recuperar datos del servidor.

### `Cuando hago una petición POST a "{endpoint}"`
Envía una petición HTTP POST sin cuerpo de datos.

### `Cuando hago una petición POST a "{endpoint}" con el cuerpo`
### `Cuando hago una petición POST a "{endpoint}" con el cuerpo:`
Envía una petición HTTP POST con datos JSON en el cuerpo usando el texto del paso.

### `Cuando hago una petición PUT a "{endpoint}" con el cuerpo`
### `Cuando hago una petición PUT a "{endpoint}" con el cuerpo:`
Envía una petición HTTP PUT con datos JSON para reemplazar completamente un recurso.

### `Cuando hago una petición PATCH a "{endpoint}" con el cuerpo`
### `Cuando hago una petición PATCH a "{endpoint}" con el cuerpo:`
Envía una petición HTTP PATCH con datos JSON para actualizar parcialmente un recurso.

### `Cuando hago una petición DELETE a "{endpoint}"`
Envía una petición HTTP DELETE para eliminar un recurso del servidor.

---

## Validación de Respuestas

### `Entonces el código de respuesta debe ser {status:d}`
Valida que el código de estado HTTP de la respuesta sea el esperado.

### `Entonces la respuesta debe ser exitosa`
Valida que la respuesta tenga un código de estado exitoso (2xx).

### `Entonces la respuesta debe contener el campo "{campo}"`
Verifica que la respuesta JSON contenga un campo específico.

### `Entonces el campo "{campo}" debe ser "{valor}"`
Valida que un campo específico tenga exactamente el valor string esperado.

### `Entonces el campo "{campo}" debe ser {valor:d}`
Valida que un campo específico tenga exactamente el valor numérico esperado.

### `Entonces el campo "{campo}" debe ser igual a la variable "{variable}"`
Compara el valor de un campo con el valor almacenado en una variable.

### `Entonces la respuesta debe tener la siguiente estructura`
### `Entonces la respuesta debe tener la siguiente estructura:`
Valida la estructura de la respuesta contra un esquema JSON definido en el texto del paso.

### `Entonces el tiempo de respuesta debe ser menor a {max_time:f} segundos`
Valida que el tiempo de respuesta de la petición HTTP sea menor al límite especificado.

---

## Extracción de Datos

### `Cuando guardo el valor del campo "{campo}" en la variable "{variable}"`
Extrae el valor de un campo de la respuesta y lo almacena en una variable para uso posterior.

### `Cuando guardo la respuesta completa en la variable "{variable}"`
Almacena toda la respuesta JSON en una variable.

---

## Variables

### `Entonces la variable "{variable1}" debe ser igual a la variable "{variable2}"`
Compara que dos variables tengan exactamente el mismo valor.

### `Entonces la variable "{variable1}" no debe ser igual a la variable "{variable2}"`
Verifica que dos variables tengan valores diferentes.

---

## Arrays y Colecciones

### `Entonces la respuesta debe ser un array`
### `Entonces la respuesta debe ser una lista`
Valida que la respuesta sea un array JSON (lista).

### `Entonces la respuesta debe tener {count:d} elementos`
Verifica que el array de respuesta tenga exactamente el número de elementos especificado.

### `Entonces cada elemento debe tener el campo "{campo}"`
Valida que todos los elementos del array tengan un campo específico.

### `Entonces el array "{ruta_array}" debe contener un elemento con "{campo}" igual a "{valor}"`
Busca en un array (anidado o de nivel raíz) un elemento que tenga un campo con un valor específico.



---

## Utilidades

### `Cuando espero {segundos:f} segundos`
Pausa la ejecución del test por el número de segundos especificado.

### `Cuando imprimo la respuesta`
Imprime la respuesta completa en la consola para propósitos de debugging.

---

## Logging

### `Cuando habilito el guardado de peticiones y respuestas`
Activa el guardado automático de todas las interacciones HTTP en archivos JSON.

### `Cuando deshabilito el guardado de peticiones y respuestas`
Desactiva el guardado automático de interacciones HTTP.

### `Cuando habilito el guardado de peticiones y respuestas en el directorio "{directorio}"`
Activa el logging de HTTP con un directorio personalizado para los archivos.

### `Cuando establezco el directorio de salida a "{directorio}"`
Configura el directorio donde se guardarán los logs de peticiones y respuestas.

---

## Variables Avanzadas

### `Dado que establezco la variable "{nombre}" al JSON`
Almacena un objeto JSON completo en una variable usando el texto del paso.

---

## Peticiones con Variables

### `Cuando hago una petición {método} a "{endpoint}" con la variable "{nombre_var}"`
Envía una petición HTTP de cualquier método usando datos JSON almacenados en una variable.

---

## Validación JSONPath

### `Entonces la respuesta "{ruta_json}" debe ser "{valor_esperado}"`
Valida el valor de una ruta JSONPath específica contra un valor esperado.

### `Entonces la respuesta "{ruta_json}" debe ser {valor_esperado:d}`
Valida el valor numérico de una ruta JSONPath específica.

---

## Archivos

### `Cuando hago POST a "{endpoint}" con archivo JSON "{ruta_archivo}"`
Envía una petición POST usando datos JSON cargados desde un archivo externo.

### `Cuando hago PUT a "{endpoint}" con archivo JSON "{ruta_archivo}"`
Envía una petición PUT usando datos JSON cargados desde un archivo externo.

### `Cuando hago PATCH a "{endpoint}" con archivo JSON "{ruta_archivo}"`
Envía una petición PATCH usando datos JSON cargados desde un archivo externo.

### `Cuando guardo la respuesta en el archivo "{ruta_archivo}"`
Guarda la respuesta completa en un archivo para análisis posterior o debugging.

### `Cuando guardo la variable "{nombre_var}" en el archivo "{ruta_archivo}"`
Guarda el contenido de una variable en un archivo externo.

---

## Validación de Esquemas

### `Entonces la respuesta debe coincidir con el esquema`
Valida la respuesta contra un esquema JSON definido en el texto del paso.

### `Entonces la respuesta debe coincidir con el archivo de esquema "{ruta_archivo}"`
Valida la respuesta contra un esquema JSON almacenado en un archivo externo.

---

## Validación de Tipos

### `Entonces la respuesta "{ruta_json}" debe ser una cadena`
Valida que el valor en la ruta JSONPath especificada sea de tipo string.

### `Entonces la respuesta "{ruta_json}" debe ser un número`
Valida que el valor en la ruta JSONPath especificada sea de tipo numérico.

### `Entonces la respuesta "{ruta_json}" debe ser un booleano`
Valida que el valor en la ruta JSONPath especificada sea de tipo boolean.

### `Entonces la respuesta "{ruta_json}" debe ser un array`
Valida que el valor en la ruta JSONPath especificada sea de tipo array.

### `Entonces la respuesta "{ruta_json}" debe ser un objeto`
Valida que el valor en la ruta JSONPath especificada sea de tipo object.

### `Entonces la respuesta "{ruta_json}" debe ser null`
Valida que el valor en la ruta JSONPath especificada sea null.

### `Entonces la respuesta "{ruta_json}" no debe ser null`
Valida que el valor en la ruta JSONPath especificada no sea null.

### `Entonces la respuesta "{ruta_json}" debe ser un email válido`
Valida que el valor en la ruta JSONPath especificada tenga formato de email válido.

### `Entonces la respuesta "{ruta_json}" debe ser una URL válida`
Valida que el valor en la ruta JSONPath especificada tenga formato de URL válido.

### `Entonces la respuesta "{ruta_json}" debe ser un UUID válido`
Valida que el valor en la ruta JSONPath especificada tenga formato de UUID válido.

---

## Notas Importantes

- **Interpolación de Variables**: Usa la sintaxis `{nombreVariable}` en URLs, headers y cuerpos JSON.
- **Archivos .env**: Los pasos `desde env` cargan automáticamente variables desde archivos .env.
- **JSONPath**: Usa sintaxis JSONPath estándar como `$.campo.subcampo` para navegar estructuras JSON.
- **Tipos de Datos**: El framework maneja automáticamente conversiones entre strings y números cuando es apropiado.
- **Logging Automático**: Cuando está habilitado, guarda automáticamente requests/responses con timestamps y metadata.
- **Archivos**: Soporta carga y guardado de datos JSON desde/hacia archivos externos.
- **Validación de Esquemas**: Permite validar respuestas contra esquemas JSON para verificar estructura.
- **Validación de Tipos**: Incluye validadores para tipos específicos como email, URL, UUID, etc.

---

## Características Avanzadas - Tier 1: Robustez y Confiabilidad

### Política de Reintentos

#### `Dado que establezco la política de reintentos con max_retries={count:d} y backoff_strategy="{estrategia}"`
Configura la política automática de reintentos para peticiones fallidas con estrategia de backoff especificada.

**Estrategias Soportadas:**
- `lineal` - El retraso aumenta linealmente
- `exponencial` - El retraso aumenta exponencialmente (por defecto)
- `fibonacci` - El retraso sigue la secuencia de Fibonacci
- `aleatorio` - Retraso aleatorio entre mín y máx

#### `Dado que establezco la política de reintentos con max_retries={count:d}, initial_delay={delay:f}, y max_delay={max_delay:f}`
Configura la política de reintentos con parámetros de retraso personalizados.

### Circuit Breaker

#### `Dado que creo un circuit breaker llamado "{nombre}" con failure_threshold={threshold:d}`
Crea un circuit breaker para prevenir fallos en cascada.

#### `Dado que creo un circuit breaker llamado "{nombre}" con failure_threshold={threshold:d}, success_threshold={success:d}, y timeout={timeout:d}`
Crea un circuit breaker con umbral de éxito y timeout personalizados.

#### `Entonces el circuit breaker "{nombre}" debe estar en estado {estado}`
Valida el estado actual de un circuit breaker (CLOSED, OPEN, HALF_OPEN).

### Interceptores de Solicitud

#### `Dado que agrego un interceptor de timestamp con nombre de encabezado "{nombre_encabezado}"`
Agrega un timestamp a todas las solicitudes con el nombre de encabezado especificado.

#### `Dado que agrego un interceptor de autorización con token "{token}"`
Agrega autorización Bearer token a todas las solicitudes.

#### `Dado que agrego un interceptor de autorización con token "{token}" y esquema "{esquema}"`
Agrega esquema de autorización personalizado a todas las solicitudes.

#### `Dado que agrego un interceptor de registro`
Habilita el registro de todas las solicitudes.

#### `Dado que agrego un interceptor de registro de respuestas`
Habilita el registro de todas las respuestas.

### Limitador de Velocidad y Acelerador

#### `Dado que establezco el límite de velocidad a {solicitudes:d} solicitudes por segundo`
Configura el limitador de velocidad con token bucket.

#### `Dado que establezco el acelerador con retraso {retraso:d} milisegundos`
Configura el acelerador de retraso fijo entre solicitudes.

#### `Dado que establezco el límite de velocidad adaptativo con inicial {rps:d} solicitudes por segundo`
Configura limitación de velocidad adaptativa que respeta encabezados de API.

#### `Entonces el limitador de velocidad debe tener {restantes:d} solicitudes restantes`
Valida las solicitudes restantes en el limitador de velocidad.

### Aserciones Avanzadas

#### `Entonces el tiempo de respuesta debe ser menor a {max_time:d} milisegundos`
Valida que el tiempo de respuesta esté por debajo del umbral en milisegundos.

#### `Entonces la respuesta debe coincidir con el esquema JSON`
Valida la respuesta contra esquema JSON definido en el texto del paso.

#### `Entonces el array de respuesta debe tener más de {count:d} elementos`
Valida que el array tenga más elementos que los especificados.

#### `Entonces el array de respuesta debe tener menos de {count:d} elementos`
Valida que el array tenga menos elementos que los especificados.

#### `Entonces la respuesta debe contener todos los campos: {campos}`
Valida que la respuesta contenga todos los campos especificados.

#### `Entonces el campo de respuesta "{campo}" debe ser de tipo "{tipo}"`
Valida que el campo sea del tipo especificado (string, number, boolean, array, object).

#### `Entonces el campo de respuesta "{campo}" debe coincidir con patrón "{patrón}"`
Valida que el campo coincida con patrón regex.

#### `Entonces el campo de respuesta "{campo}" debe estar en rango {min:d} a {max:d}`
Valida que el campo numérico esté dentro del rango.

---

## Características Avanzadas - Tier 2: Rendimiento y APIs Modernas

### Pruebas Dirigidas por Datos

#### `Dado que cargo datos de prueba del archivo "{ruta_archivo}"`
Carga datos de prueba desde archivo CSV, JSON o Excel.

#### `Cuando ejecuto prueba dirigida por datos para cada fila`
Ejecuta escenario de prueba para cada fila en datos cargados.

#### `Entonces todas las pruebas deben completarse exitosamente`
Valida que todas las pruebas dirigidas por datos se completaron sin errores.

### Monitoreo de Rendimiento

#### `Cuando envío {count:d} solicitudes GET a "{endpoint}"`
Envía múltiples solicitudes GET para pruebas de rendimiento.

#### `Entonces debo tener métricas de rendimiento`
Valida que métricas de rendimiento fueron recopiladas (usado con tabla).

#### `Entonces el tiempo promedio de respuesta debe ser menor a {max_time:d} milisegundos`
Valida el tiempo promedio de respuesta entre solicitudes.

#### `Entonces el tiempo de respuesta p95 debe ser menor a {max_time:d} milisegundos`
Valida el percentil 95 del tiempo de respuesta.

#### `Entonces la tasa de error debe ser menor al {porcentaje:d} por ciento`
Valida que la tasa de error esté por debajo del umbral.

### Caché de Respuestas

#### `Dado que habilito el caché de respuestas con TTL de {ttl:d} segundos`
Habilita el almacenamiento automático en caché de respuestas GET con tiempo de vida.

#### `Cuando envío la misma solicitud GET a "{endpoint}" nuevamente`
Envía solicitud GET idéntica (usado para probar caché).

#### `Entonces la segunda respuesta debe provenir del caché`
Valida que la respuesta fue servida desde caché.

#### `Entonces el caché debe contener {count:d} entradas`
Valida el número de entradas en caché.

### GraphQL

#### `Dado que establezco la URL base a "{url}"`
Establece la URL base para endpoint GraphQL.

#### `Cuando ejecuto consulta GraphQL`
Ejecuta consulta GraphQL definida en el texto del paso.

#### `Cuando ejecuto mutación GraphQL`
Ejecuta mutación GraphQL definida en el texto del paso.

#### `Entonces la respuesta debe contener "{campo}"`
Valida que la respuesta GraphQL contenga campo.

### WebSocket

#### `Dado que me conecto a WebSocket "{url}"`
Establece conexión WebSocket.

#### `Cuando envío mensaje WebSocket`
Envía mensaje a través de WebSocket (mensaje en texto del paso).

#### `Entonces debo recibir un mensaje WebSocket dentro de {segundos:d} segundos`
Valida que mensaje WebSocket fue recibido dentro del timeout.

#### `Cuando me desconecto de WebSocket`
Cierra conexión WebSocket.

### Autenticación OAuth2

#### `Dado que configuro OAuth2 con`
Configura autenticación OAuth2 (usado con tabla de client_id, client_secret, token_url).

#### `Entonces la solicitud debe incluir encabezado Authorization`
Valida que encabezado Authorization está presente en solicitud.

#### `Entonces el token OAuth2 debe ser válido`
Valida que token OAuth2 es válido.

### Autenticación JWT

#### `Dado que configuro JWT con secreto "{secreto}" y algoritmo "{algoritmo}"`
Configura JWT con secreto y algoritmo (HS256, RS256, etc.).

#### `Cuando creo token JWT con payload`
Crea token JWT con payload del texto del paso.

#### `Entonces el token debe ser válido`
Valida que token JWT es válido y está correctamente firmado.

#### `Entonces el token debe contener claim "{claim}" con valor "{valor}"`
Valida que token JWT contiene claim específico.

---

## Características Avanzadas - Tier 3: Características Empresariales

### Reportes

#### `Cuando ejecuto suite de pruebas`
Ejecuta suite de pruebas completa para reportes.

#### `Entonces debo generar reportes en formatos`
Genera reportes en formatos especificados (usado con tabla).

#### `Entonces el reporte debe ser generado en formato "{formato}"`
Valida que reporte fue generado en formato especificado (html, json, junit, allure).

### Validación de Contrato

#### `Dado que cargo especificación OpenAPI desde "{ruta_archivo}"`
Carga especificación OpenAPI para validación de contrato.

#### `Entonces la respuesta debe coincidir con contrato OpenAPI para {método} {endpoint}`
Valida que respuesta coincide con contrato OpenAPI.

#### `Dado que cargo especificación AsyncAPI desde "{ruta_archivo}"`
Carga especificación AsyncAPI para validación de contrato.

### Ingeniería del Caos

#### `Dado que habilito ingeniería del caos`
Habilita características de ingeniería del caos.

#### `Dado que inyecto latencia entre {min:d} y {max:d} milisegundos`
Inyecta latencia aleatoria en solicitudes.

#### `Dado que inyecto tasa de error del {porcentaje:d} por ciento`
Inyecta errores aleatorios en solicitudes.

#### `Cuando envío una solicitud GET a "{endpoint}"`
Envía solicitud con ingeniería del caos habilitada.

#### `Entonces la respuesta debe completarse a pesar de la latencia inyectada`
Valida que solicitud se completó a pesar de inyección de latencia.

#### `Entonces algunas solicitudes pueden fallar debido a errores inyectados`
Valida que algunas solicitudes fallaron debido a inyección de errores.

#### `Entonces circuit breaker debe permanecer en estado CLOSED`
Valida que circuit breaker permaneció cerrado a pesar del caos.

#### `Entonces tasa de error debe ser menor al {porcentaje:d} por ciento`
Valida que tasa de error real está por debajo del umbral.

### Registro Avanzado

#### `Dado que establezco nivel de registro a "{nivel}"`
Establece nivel de registro (DEBUG, INFO, WARNING, ERROR).

#### `Dado que habilito registro de solicitud al directorio "{directorio}"`
Habilita registro de solicitud al directorio especificado.

#### `Entonces solicitud y respuesta deben registrarse en archivo`
Valida que solicitud/respuesta fueron registradas en archivo.

---

## Escenarios de Integración

### Pruebas de Pila Completa

#### `Dado que establezco alerta de rendimiento para umbral de response_time de {umbral:d} milisegundos`
Establece umbral de alerta de rendimiento.

#### `Entonces métricas de rendimiento deben ser recopiladas`
Valida que métricas de rendimiento fueron recopiladas.

#### `Entonces caché debe contener {count:d} entrada`
Valida que caché contiene número especificado de entradas.

### Pruebas de Resiliencia

#### `Dado que creo circuit breaker con failure_threshold={threshold:d}`
Crea circuit breaker para pruebas de resiliencia.

#### `Cuando envío {count:d} solicitudes GET a "{endpoint}"`
Envía múltiples solicitudes para pruebas de resiliencia.

#### `Entonces circuit breaker debe permanecer en estado CLOSED`
Valida que circuit breaker permaneció cerrado.

#### `Entonces tasa de error debe ser menor al {porcentaje:d} por ciento`
Valida que tasa de error permaneció por debajo del umbral.

---

## Notas Importantes

- **Interpolación de Variables**: Usa la sintaxis `{nombreVariable}` en URLs, headers y cuerpos JSON.
- **Archivos .env**: Los pasos `desde env` cargan automáticamente variables desde archivos .env.
- **JSONPath**: Usa sintaxis JSONPath estándar como `$.campo.subcampo` para navegar estructuras JSON.
- **Tipos de Datos**: El framework maneja automáticamente conversiones entre strings y números cuando es apropiado.
- **Logging Automático**: Cuando está habilitado, guarda automáticamente requests/responses con timestamps y metadata.
- **Archivos**: Soporta carga y guardado de datos JSON desde/hacia archivos externos.
- **Validación de Esquemas**: Permite validar respuestas contra esquemas JSON para verificar estructura.
- **Validación de Tipos**: Incluye validadores para tipos específicos como email, URL, UUID, etc.
- **Estrategias de Backoff**: Las políticas de reintentos soportan estrategias lineal, exponencial, fibonacci y aleatoria.
- **Estados de Circuit Breaker**: CLOSED (normal), OPEN (fallando), HALF_OPEN (probando recuperación).
- **Métricas de Rendimiento**: Incluye tiempos de respuesta promedio, p95, p99, tasa de error y throughput.
- **Verificación**: Esta documentación ha sido verificada contra el código fuente v1.5.0.

---

*Judo Framework v1.5.0 - Documentación completa y verificada*