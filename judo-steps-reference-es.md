# Referencia Completa de Pasos - Judo Framework (Español)

Esta es la referencia completa de todos los pasos **VERIFICADOS** disponibles en Judo Framework v1.3.40 en español.

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

*Judo Framework v1.3.36 - Documentación completa y verificada*