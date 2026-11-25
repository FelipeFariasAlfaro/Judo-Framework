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

## Pasos nuevos en v1.7.0

### Configuración HTTP, archivos, XML/SOAP básico, headers de seguridad, polling, SQL, paginación

#### `consulto "{endpoint}" hasta que la respuesta "{json_path}" sea igual a "{esperado}" en máximo {segundos:d} segundos`
Repite GET hasta que un JSONPath sea igual al valor esperado o se agote el tiempo.
#### `consulto "{endpoint}" hasta que el estado sea {estado:d} en máximo {segundos:d} segundos`
Repite GET hasta que el código de estado coincida o se agote el tiempo.
#### `que me conecto a la base de datos SQLite "{ruta}"`
Abre una base SQLite para preparar y verificar datos.
#### `me conecto a la base de datos SQLite "{ruta}"`
Abre una base SQLite para preparar y verificar datos.
#### `que ejecuto el SQL "{sql}"`
Ejecuta una sentencia SQL (INSERT, UPDATE, DELETE, DDL).
#### `ejecuto el SQL "{sql}"`
Ejecuta una sentencia SQL (INSERT, UPDATE, DELETE, DDL).
#### `guardo el primer valor de la consulta SQL "{sql}" como "{variable}"`
Ejecuta una consulta SQL y guarda la primera columna de la primera fila en una variable.
#### `la consulta SQL "{sql}" debe devolver {cantidad:d} filas`
Valida la cantidad de filas que devuelve una consulta SQL.
#### `la consulta SQL "{sql}" debe devolver el valor "{esperado}"`
Valida el primer valor que devuelve una consulta SQL.
#### `recopilo todas las páginas de "{endpoint}" usando el parámetro "{parametro}" hasta {max_paginas:d} páginas como "{variable}"`
Recorre un endpoint GET paginado y guarda todos los elementos en una variable.
#### `que establezco el timeout a {segundos:g} segundos`
Establece el timeout de las peticiones HTTP.
#### `establezco el timeout a {segundos:g} segundos`
Establece el timeout de las peticiones HTTP.
#### `que deshabilito la verificación SSL`
Desactiva la verificación del certificado TLS (solo pruebas).
#### `deshabilito la verificación SSL`
Desactiva la verificación del certificado TLS (solo pruebas).
#### `que uso el bundle de CA "{ruta}"`
Verifica TLS con un archivo de CA personalizado.
#### `uso el bundle de CA "{ruta}"`
Verifica TLS con un archivo de CA personalizado.
#### `que uso el certificado de cliente "{cert}" con la llave "{llave}"`
Usa un certificado y llave de cliente (TLS mutuo).
#### `uso el certificado de cliente "{cert}" con la llave "{llave}"`
Usa un certificado y llave de cliente (TLS mutuo).
#### `que uso el proxy "{url}"`
Envía las peticiones a través de un proxy HTTP.
#### `uso el proxy "{url}"`
Envía las peticiones a través de un proxy HTTP.
#### `que me conecto a la base de datos "{url}"`
Conecta a SQLite, PostgreSQL o MySQL mediante una URL.
#### `me conecto a la base de datos "{url}"`
Conecta a SQLite, PostgreSQL o MySQL mediante una URL.
#### `subo el archivo "{ruta}" como "{campo}" a "{endpoint}"`
Sube un archivo como multipart/form-data con POST.
#### `el SHA-256 de la respuesta debe ser "{esperado}"`
Valida el SHA-256 del cuerpo de la respuesta.
#### `el header de respuesta "{nombre}" debe ser "{valor}"`
Valida el valor de un header de respuesta.
#### `el header de respuesta "{nombre}" debe existir`
Valida que un header de respuesta esté presente.
#### `la respuesta debe incluir headers de seguridad`
Valida HSTS, nosniff y protección contra clickjacking.
#### `el XML de la respuesta "{xpath}" debe ser "{esperado}"`
Valida el primer valor seleccionado por un XPath.
#### `el XML de la respuesta "{xpath}" debe seleccionar {cantidad:d} nodos`
Valida cuántos nodos selecciona un XPath.
#### `extraigo el XML "{xpath}" como "{variable}"`
Guarda en una variable el primer valor seleccionado por un XPath.
#### `la respuesta debe ser igual al JSON ignorando "{campos}"`
Compara la respuesta con el JSON del texto del paso, ignorando campos volátiles.
#### `envío una petición SOAP a "{endpoint}" con la acción "{accion}"`
Envía el XML del texto del paso como petición SOAP.
#### `el código de respuesta debe ser un error de cliente`
Valida que el estado sea 4xx.
#### `el código de respuesta debe ser un error de servidor`
Valida que el estado sea 5xx.
#### `el código de respuesta debe ser uno de "{codigos}"`
Valida que el estado sea uno de una lista de códigos separados por coma.

### Pasos condicionales y de control de flujo (si / en caso contrario, bucles, reintentos, aserciones suaves, saltar). El bloque de pasos va en un docstring; usa ''' para un docstring anidado

#### `si el estado de la respuesta es {estado:d} entonces ejecuto`
Ejecuta el bloque cuando el estado de la respuesta coincide.
#### `si el estado de la respuesta no es {estado:d} entonces ejecuto`
Ejecuta el bloque cuando el estado de la respuesta es distinto.
#### `si la respuesta "{ruta}" es igual a "{esperado}" entonces ejecuto`
Ejecuta el bloque cuando un JSONPath es igual a un valor.
#### `si la respuesta "{ruta}" existe entonces ejecuto`
Ejecuta el bloque cuando un JSONPath existe.
#### `si la respuesta "{ruta}" no existe entonces ejecuto`
Ejecuta el bloque cuando un JSONPath no existe.
#### `si la respuesta "{ruta}" contiene "{texto}" entonces ejecuto`
Ejecuta el bloque cuando un valor JSON (o elemento de array) contiene el texto.
#### `si la respuesta "{ruta}" es mayor que {numero:g} entonces ejecuto`
Ejecuta el bloque cuando un valor numérico JSON es mayor que un número.
#### `si la respuesta "{ruta}" es menor que {numero:g} entonces ejecuto`
Ejecuta el bloque cuando un valor numérico JSON es menor que un número.
#### `si la variable "{nombre}" es igual a "{esperado}" entonces ejecuto`
Ejecuta el bloque cuando una variable es igual a un valor.
#### `si la variable "{nombre}" está definida entonces ejecuto`
Ejecuta el bloque cuando una variable está definida.
#### `si la variable "{nombre}" no está definida entonces ejecuto`
Ejecuta el bloque cuando una variable no está definida.
#### `si la variable "{nombre}" está vacía entonces ejecuto`
Ejecuta el bloque cuando una variable no existe o está vacía.
#### `si el entorno es "{entorno}" entonces ejecuto`
Ejecuta el bloque cuando JUDO_ENV / KARATE_ENV coincide.
#### `si la variable de entorno "{nombre}" está definida entonces ejecuto`
Ejecuta el bloque cuando una variable de entorno del sistema está definida.
#### `si el escenario tiene el tag "{tag}" entonces ejecuto`
Ejecuta el bloque cuando el escenario tiene un tag.
#### `si el archivo "{ruta}" existe entonces ejecuto`
Ejecuta el bloque cuando un archivo existe.
#### `si el header de respuesta "{nombre}" existe entonces ejecuto`
Ejecuta el bloque cuando un header de respuesta está presente.
#### `si el cuerpo de la respuesta contiene "{texto}" entonces ejecuto`
Ejecuta el bloque cuando el cuerpo crudo de la respuesta contiene el texto.
#### `si el tiempo de respuesta es mayor a {ms:d} milisegundos entonces ejecuto`
Ejecuta el bloque cuando la respuesta fue más lenta que el límite.
#### `en caso contrario ejecuto`
Ejecuta el bloque cuando el 'si' anterior fue falso.
#### `salto el escenario si la variable "{nombre}" es igual a "{esperado}"`
Salta el resto del escenario cuando una variable es igual a un valor.
#### `salto el escenario si el entorno es "{entorno}"`
Salta el resto del escenario en un entorno determinado.
#### `salto el escenario si el estado de la respuesta es {estado:d}`
Salta el resto del escenario cuando el estado de la respuesta coincide.
#### `fallo la prueba con el mensaje "{mensaje}"`
Falla el escenario con un mensaje personalizado.
#### `la variable "{nombre}" debe estar definida`
Valida que una variable esté definida.
#### `la variable "{nombre}" no debe estar definida`
Valida que una variable no esté definida.
#### `la variable "{nombre}" debe estar vacía`
Valida que una variable no exista o esté vacía.
#### `el entorno debe ser "{entorno}"`
Valida el nombre del entorno actual.
#### `repito {n:d} veces`
Ejecuta el bloque N veces (variable ${iteration} = 1..N).
#### `repito hasta que la respuesta "{ruta}" sea igual a "{esperado}" hasta {n:d} veces`
Ejecuta el bloque hasta que un JSONPath sea igual a un valor, como máximo N veces.
#### `para cada elemento en la respuesta "{ruta}" ejecuto`
Ejecuta el bloque por cada elemento de un array (variables ${item} y ${index}).
#### `reintento los siguientes pasos hasta {n:d} veces con {segundos:g} segundos de espera`
Reintenta el bloque mientras falle.
#### `verifico todo lo siguiente`
Ejecuta cada línea del bloque como un paso y reporta todos los fallos al final.

### Servicios no JSON: XML/SOAP, formularios, texto, CSV, descargas binarias, Server-Sent Events, GraphQL

#### `la respuesta debe ser XML válido`
Valida que el cuerpo de la respuesta sea XML bien formado.
#### `el XML de la respuesta "{xpath}" debe existir`
Valida que un XPath seleccione al menos un nodo.
#### `el XML de la respuesta "{xpath}" no debe existir`
Valida que un XPath no seleccione nada.
#### `el XML de la respuesta "{xpath}" debe contener "{texto}"`
Valida que un nodo seleccionado por XPath contenga un texto.
#### `el XML de la respuesta "{xpath}" debe coincidir con "{patron}"`
Valida que el primer nodo seleccionado por XPath cumpla una expresión regular.
#### `el XML de la respuesta debe cumplir con el XSD "{ruta}"`
Valida el XML de la respuesta contra un esquema XSD (requiere lxml).
#### `la respuesta SOAP no debe ser un fallo`
Valida que la respuesta SOAP no sea un fault.
#### `el código del fallo SOAP debe ser "{codigo}"`
Valida el código del fault SOAP.
#### `el mensaje del fallo SOAP debe contener "{texto}"`
Valida que el mensaje del fault SOAP contenga un texto.
#### `envío una petición SOAP 1.2 a "{endpoint}" con la acción "{accion}"`
Envía el XML del texto del paso como petición SOAP 1.2.
#### `envío el archivo de sobre SOAP "{ruta}" a "{endpoint}" con la acción "{accion}"`
Envía una petición SOAP 1.1 cuyo envelope se lee de un archivo.
#### `envío un POST XML a "{endpoint}"`
Envía por POST el XML del texto del paso con Content-Type application/xml.
#### `envío un POST de formulario a "{endpoint}"`
Envía application/x-www-form-urlencoded usando una tabla con columnas field | value.
#### `establezco el campo de formulario "{nombre}" a "{valor}"`
Prepara un campo de formulario para el próximo 'envío el formulario'.
#### `envío el formulario a "{endpoint}"`
Envía por POST los campos de formulario preparados.
#### `el texto de la respuesta debe contener "{texto}"`
Valida que el texto de la respuesta contenga una cadena.
#### `el texto de la respuesta no debe contener "{texto}"`
Valida que el texto de la respuesta no contenga una cadena.
#### `el texto de la respuesta debe coincidir con "{patron}"`
Valida que el texto de la respuesta cumpla una expresión regular.
#### `el texto de la respuesta debe ser igual a "{texto}"`
Valida el texto completo de la respuesta (sin espacios en los extremos).
#### `el tipo de contenido de la respuesta debe ser "{tipo}"`
Valida que el header Content-Type comience con un valor.
#### `el tamaño de la respuesta debe ser menor a {tamano:d} bytes`
Valida el tamaño del cuerpo de la respuesta.
#### `la respuesta debe ser un CSV con {cantidad:d} filas`
Valida la cantidad de filas de datos del CSV (sin encabezado).
#### `la columna CSV "{columna}" debe contener "{valor}"`
Valida que una columna CSV tenga un valor en alguna fila.
#### `los bytes de la respuesta deben ser iguales al archivo "{ruta}"`
Valida que los bytes de la respuesta sean idénticos a un archivo.
#### `descargo "{endpoint}" en el archivo "{ruta}"`
Hace GET a un endpoint y guarda los bytes en un archivo.
#### `la respuesta debe tener el nombre de descarga "{nombre}"`
Valida el nombre de archivo en Content-Disposition.
#### `guardo el texto de la respuesta como "{variable}"`
Guarda el texto crudo de la respuesta en una variable.
#### `abro el stream SSE "{endpoint}"`
Abre un stream de Server-Sent Events y recolecta eventos en segundo plano.
#### `debo recibir un evento SSE "{evento}" en máximo {segundos:g} segundos`
Espera un evento SSE por nombre.
#### `debo recibir un evento SSE con datos que contengan "{texto}" en máximo {segundos:g} segundos`
Espera un evento SSE cuyos datos contengan un texto.
#### `debo recibir {cantidad:d} eventos SSE en máximo {segundos:g} segundos`
Espera hasta que hayan llegado al menos N eventos SSE.
#### `los datos del último evento SSE "{ruta}" deben ser "{esperado}"`
Valida un campo JSON de los datos del último evento SSE.
#### `cierro el stream SSE`
Cierra el stream SSE.
#### `establezco las variables GraphQL`
Define las variables (JSON en el texto del paso) para la próxima petición GraphQL.
#### `envío la consulta GraphQL a "{endpoint}"`
Envía la consulta GraphQL del texto del paso.
#### `envío la mutación GraphQL a "{endpoint}"`
Envía la mutación GraphQL del texto del paso.
#### `la respuesta GraphQL no debe tener errores`
Valida que la respuesta GraphQL no tenga errores.
#### `la respuesta GraphQL debe tener un error que contenga "{texto}"`
Valida que algún mensaje de error GraphQL contenga un texto.
#### `los datos GraphQL "{ruta}" deben ser "{esperado}"`
Valida un valor dentro de los datos GraphQL.
#### `los datos GraphQL "{ruta}" deben existir`
Valida que una ruta exista dentro de los datos GraphQL.
#### `los datos GraphQL "{ruta}" deben tener {cantidad:d} elementos`
Valida el tamaño de un array dentro de los datos GraphQL.
#### `guardo los datos GraphQL "{ruta}" como "{variable}"`
Guarda un valor de los datos GraphQL en una variable.
#### `hago introspección del esquema GraphQL en "{endpoint}"`
Ejecuta la consulta de introspección.
#### `el esquema GraphQL debe tener el tipo "{nombre}"`
Valida que un tipo exista en el esquema introspectado.

### gRPC por reflexión (requiere `pip install "judo-framework[grpc]"`)

#### `me conecto al servidor gRPC "{destino}"`
Abre un canal gRPC sin TLS (host:puerto).
#### `me conecto al servidor gRPC "{destino}" con TLS`
Abre un canal gRPC con TLS usando los certificados del sistema.
#### `establezco el metadato gRPC "{clave}" a "{valor}"`
Agrega un metadato (header) enviado en cada llamada gRPC.
#### `establezco el timeout gRPC a {segundos:g} segundos`
Define el plazo máximo de las llamadas gRPC.
#### `envío la petición gRPC "{metodo}"`
Llama a un método unario; la petición (JSON) va en el texto del paso.
#### `envío la petición gRPC de streaming "{metodo}"`
Llama a un método con streaming del servidor; la petición (JSON) va en el texto del paso.
#### `el estado gRPC debe ser "{estado}"`
Valida el nombre del código gRPC (OK, NOT_FOUND, UNAUTHENTICATED, ...).
#### `la respuesta gRPC "{ruta}" debe ser "{esperado}"`
Valida un campo de la respuesta gRPC.
#### `la respuesta gRPC debe contener "{campo}"`
Valida que la respuesta gRPC tenga un campo.
#### `guardo la respuesta gRPC "{ruta}" como "{variable}"`
Guarda un campo de la respuesta gRPC en una variable.
#### `el servidor gRPC debe exponer el servicio "{servicio}"`
Valida (por reflexión) que un servicio esté expuesto.
#### `el servidor gRPC debe exponer el método "{metodo}"`
Valida (por reflexión) que un método exista.
#### `el stream gRPC debe devolver {cantidad:d} mensajes`
Valida cuántos mensajes devolvió el stream del servidor.
#### `el mensaje {indice:d} del stream gRPC "{ruta}" debe ser "{esperado}"`
Valida un campo de un mensaje del stream (índice desde 0).
#### `la llamada gRPC debe tardar menos de {ms:d} milisegundos`
Valida la duración de la última llamada gRPC.
#### `cierro la conexión gRPC`
Cierra el canal gRPC.
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