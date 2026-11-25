"""
Pasos extra de Judo (Español): polling, SQL (SQLite) y paginación.
Reutiliza la lógica de ``steps_extra`` para garantizar paridad con inglés.
"""
from behave import step

from .steps_extra import (
    _poll_json_equals, _poll_status, _sql_connect, _sql_execute,
    _sql_save_first, _sql_assert_count, _sql_assert_value, _collect_pages,
)


@step('consulto "{endpoint}" hasta que la respuesta "{json_path}" sea igual a "{esperado}" en máximo {segundos:d} segundos')
def step_poll_json_equals_es(context, endpoint, json_path, esperado, segundos):
    """Repite GET hasta que un JSONPath sea igual al valor esperado o se agote el tiempo"""
    _poll_json_equals(context, endpoint, json_path, esperado, segundos)


@step('consulto "{endpoint}" hasta que el estado sea {estado:d} en máximo {segundos:d} segundos')
def step_poll_status_es(context, endpoint, estado, segundos):
    """Repite GET hasta que el código de estado coincida o se agote el tiempo"""
    _poll_status(context, endpoint, estado, segundos)


@step('que me conecto a la base de datos SQLite "{ruta}"')
@step('me conecto a la base de datos SQLite "{ruta}"')
def step_sql_connect_es(context, ruta):
    """Abre una base SQLite para preparar y verificar datos"""
    _sql_connect(context, ruta)


@step('que ejecuto el SQL "{sql}"')
@step('ejecuto el SQL "{sql}"')
def step_sql_execute_es(context, sql):
    """Ejecuta una sentencia SQL (INSERT, UPDATE, DELETE, DDL)"""
    _sql_execute(context, sql)


@step('guardo el primer valor de la consulta SQL "{sql}" como "{variable}"')
def step_sql_save_first_es(context, sql, variable):
    """Ejecuta una consulta SQL y guarda la primera columna de la primera fila en una variable"""
    _sql_save_first(context, sql, variable)


@step('la consulta SQL "{sql}" debe devolver {cantidad:d} filas')
def step_sql_count_es(context, sql, cantidad):
    """Valida la cantidad de filas que devuelve una consulta SQL"""
    _sql_assert_count(context, sql, cantidad)


@step('la consulta SQL "{sql}" debe devolver el valor "{esperado}"')
def step_sql_value_es(context, sql, esperado):
    """Valida el primer valor que devuelve una consulta SQL"""
    _sql_assert_value(context, sql, esperado)


@step('recopilo todas las páginas de "{endpoint}" usando el parámetro "{parametro}" hasta {max_paginas:d} páginas como "{variable}"')
def step_collect_pages_es(context, endpoint, parametro, max_paginas, variable):
    """Recorre un endpoint GET paginado y guarda todos los elementos en una variable"""
    _collect_pages(context, endpoint, parametro, max_paginas, variable)


from .steps_extra import (  # noqa: E402
    _set_timeout, _disable_ssl, _use_ca_bundle, _use_client_cert, _use_proxy, _upload,
    _assert_sha256, _assert_header_equals, _assert_header_exists, _assert_security_headers,
    _assert_xml_value, _assert_xml_count, _extract_xml, _assert_json_equals_ignoring, _soap,
)


@step('que establezco el timeout a {segundos:g} segundos')
@step('establezco el timeout a {segundos:g} segundos')
def step_set_timeout_es(context, segundos):
    """Establece el timeout de las peticiones HTTP"""
    _set_timeout(context, segundos)


@step('que deshabilito la verificación SSL')
@step('deshabilito la verificación SSL')
def step_disable_ssl_es(context):
    """Desactiva la verificación del certificado TLS (solo pruebas)"""
    _disable_ssl(context)


@step('que uso el bundle de CA "{ruta}"')
@step('uso el bundle de CA "{ruta}"')
def step_ca_bundle_es(context, ruta):
    """Verifica TLS con un archivo de CA personalizado"""
    _use_ca_bundle(context, ruta)


@step('que uso el certificado de cliente "{cert}" con la llave "{llave}"')
@step('uso el certificado de cliente "{cert}" con la llave "{llave}"')
def step_client_cert_es(context, cert, llave):
    """Usa un certificado y llave de cliente (TLS mutuo)"""
    _use_client_cert(context, cert, llave)


@step('que uso el proxy "{url}"')
@step('uso el proxy "{url}"')
def step_proxy_es(context, url):
    """Envía las peticiones a través de un proxy HTTP"""
    _use_proxy(context, url)


@step('que me conecto a la base de datos "{url}"')
@step('me conecto a la base de datos "{url}"')
def step_db_connect_es(context, url):
    """Conecta a SQLite, PostgreSQL o MySQL mediante una URL"""
    from .steps_extra import _sql_connect
    _sql_connect(context, url)


@step('subo el archivo "{ruta}" como "{campo}" a "{endpoint}"')
def step_upload_es(context, ruta, campo, endpoint):
    """Sube un archivo como multipart/form-data con POST"""
    _upload(context, ruta, campo, endpoint)


@step('el SHA-256 de la respuesta debe ser "{esperado}"')
def step_sha256_es(context, esperado):
    """Valida el SHA-256 del cuerpo de la respuesta"""
    _assert_sha256(context, esperado)


@step('el header de respuesta "{nombre}" debe ser "{valor}"')
def step_header_equals_es(context, nombre, valor):
    """Valida el valor de un header de respuesta"""
    _assert_header_equals(context, nombre, valor)


@step('el header de respuesta "{nombre}" debe existir')
def step_header_exists_es(context, nombre):
    """Valida que un header de respuesta esté presente"""
    _assert_header_exists(context, nombre)


@step('la respuesta debe incluir headers de seguridad')
def step_security_headers_es(context):
    """Valida HSTS, nosniff y protección contra clickjacking"""
    _assert_security_headers(context)


@step('el XML de la respuesta "{xpath}" debe ser "{esperado}"')
def step_xml_value_es(context, xpath, esperado):
    """Valida el primer valor seleccionado por un XPath"""
    _assert_xml_value(context, xpath, esperado)


@step('el XML de la respuesta "{xpath}" debe seleccionar {cantidad:d} nodos')
def step_xml_count_es(context, xpath, cantidad):
    """Valida cuántos nodos selecciona un XPath"""
    _assert_xml_count(context, xpath, cantidad)


@step('extraigo el XML "{xpath}" como "{variable}"')
def step_xml_extract_es(context, xpath, variable):
    """Guarda en una variable el primer valor seleccionado por un XPath"""
    _extract_xml(context, xpath, variable)


@step('la respuesta debe ser igual al JSON ignorando "{campos}"')
def step_json_ignoring_es(context, campos):
    """Compara la respuesta con el JSON del texto del paso, ignorando campos volátiles"""
    _assert_json_equals_ignoring(context, campos, context.text)


@step('envío una petición SOAP a "{endpoint}" con la acción "{accion}"')
def step_soap_es(context, endpoint, accion):
    """Envía el XML del texto del paso como petición SOAP"""
    _soap(context, endpoint, accion, context.text)


from .steps_extra import _assert_status_class, _assert_status_one_of  # noqa: E402


@step('el código de respuesta debe ser un error de cliente')
def step_client_error_es(context):
    """Valida que el estado sea 4xx"""
    _assert_status_class(context, 4)


@step('el código de respuesta debe ser un error de servidor')
def step_server_error_es(context):
    """Valida que el estado sea 5xx"""
    _assert_status_class(context, 5)


@step('el código de respuesta debe ser uno de "{codigos}"')
def step_status_one_of_es(context, codigos):
    """Valida que el estado sea uno de una lista de códigos separados por coma"""
    _assert_status_one_of(context, codigos)
