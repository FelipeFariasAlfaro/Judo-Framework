"""
Pasos para servicios que no (solo) usan JSON (Español):
XML/SOAP, formularios, texto plano, CSV, descargas binarias, Server-Sent Events y GraphQL.
Reutiliza la lógica de ``steps_protocols``.
"""
from behave import step

from .steps_protocols import (
    _assert_valid_xml, _xml_exists, _xml_contains, _xml_matches, _xml_xsd, _soap_no_fault,
    _soap_fault_code, _soap_fault_message, _soap12, _soap_from_file, _xml_post,
    _form_post, _form_set, _form_submit, _text_contains, _text_matches, _text_equals,
    _content_type, _size_less, _csv_count, _csv_column, _bytes_equal_file, _download,
    _download_name, _save_text, _sse_open, _sse_event, _sse_data_contains, _sse_count,
    _sse_last, _sse_close, _gql_vars, _gql_send, _gql_no_errors, _gql_error_contains,
    _gql_data_equals, _gql_data_exists, _gql_data_count, _gql_save, _gql_introspect, _gql_type,
)


# --- XML / SOAP -------------------------------------------------------------
@step('la respuesta debe ser XML válido')
def step_valid_xml_es(context):
    """Valida que el cuerpo de la respuesta sea XML bien formado"""
    _assert_valid_xml(context)


@step('el XML de la respuesta "{xpath}" debe existir')
def step_xml_exists_es(context, xpath):
    """Valida que un XPath seleccione al menos un nodo"""
    _xml_exists(context, xpath, True)


@step('el XML de la respuesta "{xpath}" no debe existir')
def step_xml_not_exists_es(context, xpath):
    """Valida que un XPath no seleccione nada"""
    _xml_exists(context, xpath, False)


@step('el XML de la respuesta "{xpath}" debe contener "{texto}"')
def step_xml_contains_es(context, xpath, texto):
    """Valida que un nodo seleccionado por XPath contenga un texto"""
    _xml_contains(context, xpath, texto)


@step('el XML de la respuesta "{xpath}" debe coincidir con "{patron}"')
def step_xml_matches_es(context, xpath, patron):
    """Valida que el primer nodo seleccionado por XPath cumpla una expresión regular"""
    _xml_matches(context, xpath, patron)


@step('el XML de la respuesta debe cumplir con el XSD "{ruta}"')
def step_xml_xsd_es(context, ruta):
    """Valida el XML de la respuesta contra un esquema XSD (requiere lxml)"""
    _xml_xsd(context, ruta)


@step('la respuesta SOAP no debe ser un fallo')
def step_soap_no_fault_es(context):
    """Valida que la respuesta SOAP no sea un fault"""
    _soap_no_fault(context)


@step('el código del fallo SOAP debe ser "{codigo}"')
def step_soap_fault_code_es(context, codigo):
    """Valida el código del fault SOAP"""
    _soap_fault_code(context, codigo)


@step('el mensaje del fallo SOAP debe contener "{texto}"')
def step_soap_fault_message_es(context, texto):
    """Valida que el mensaje del fault SOAP contenga un texto"""
    _soap_fault_message(context, texto)


@step('envío una petición SOAP 1.2 a "{endpoint}" con la acción "{accion}"')
def step_soap12_es(context, endpoint, accion):
    """Envía el XML del texto del paso como petición SOAP 1.2"""
    _soap12(context, endpoint, accion, context.text)


@step('envío el archivo de sobre SOAP "{ruta}" a "{endpoint}" con la acción "{accion}"')
def step_soap_file_es(context, ruta, endpoint, accion):
    """Envía una petición SOAP 1.1 cuyo envelope se lee de un archivo"""
    _soap_from_file(context, endpoint, accion, ruta)


@step('envío un POST XML a "{endpoint}"')
def step_xml_post_es(context, endpoint):
    """Envía por POST el XML del texto del paso con Content-Type application/xml"""
    _xml_post(context, endpoint, context.text)


# --- Formularios, texto, CSV, binario ---------------------------------------
@step('envío un POST de formulario a "{endpoint}"')
def step_form_post_es(context, endpoint):
    """Envía application/x-www-form-urlencoded usando una tabla con columnas field | value"""
    _form_post(context, endpoint, context.table)


@step('establezco el campo de formulario "{nombre}" a "{valor}"')
def step_form_set_es(context, nombre, valor):
    """Prepara un campo de formulario para el próximo 'envío el formulario'"""
    _form_set(context, nombre, valor)


@step('envío el formulario a "{endpoint}"')
def step_form_submit_es(context, endpoint):
    """Envía por POST los campos de formulario preparados"""
    _form_submit(context, endpoint)


@step('el texto de la respuesta debe contener "{texto}"')
def step_text_contains_es(context, texto):
    """Valida que el texto de la respuesta contenga una cadena"""
    _text_contains(context, texto)


@step('el texto de la respuesta no debe contener "{texto}"')
def step_text_not_contains_es(context, texto):
    """Valida que el texto de la respuesta no contenga una cadena"""
    _text_contains(context, texto, negate=True)


@step('el texto de la respuesta debe coincidir con "{patron}"')
def step_text_matches_es(context, patron):
    """Valida que el texto de la respuesta cumpla una expresión regular"""
    _text_matches(context, patron)


@step('el texto de la respuesta debe ser igual a "{texto}"')
def step_text_equals_es(context, texto):
    """Valida el texto completo de la respuesta (sin espacios en los extremos)"""
    _text_equals(context, texto)


@step('el tipo de contenido de la respuesta debe ser "{tipo}"')
def step_content_type_es(context, tipo):
    """Valida que el header Content-Type comience con un valor"""
    _content_type(context, tipo)


@step('el tamaño de la respuesta debe ser menor a {tamano:d} bytes')
def step_size_less_es(context, tamano):
    """Valida el tamaño del cuerpo de la respuesta"""
    _size_less(context, tamano)


@step('la respuesta debe ser un CSV con {cantidad:d} filas')
def step_csv_count_es(context, cantidad):
    """Valida la cantidad de filas de datos del CSV (sin encabezado)"""
    _csv_count(context, cantidad)


@step('la columna CSV "{columna}" debe contener "{valor}"')
def step_csv_column_es(context, columna, valor):
    """Valida que una columna CSV tenga un valor en alguna fila"""
    _csv_column(context, columna, valor)


@step('los bytes de la respuesta deben ser iguales al archivo "{ruta}"')
def step_bytes_equal_es(context, ruta):
    """Valida que los bytes de la respuesta sean idénticos a un archivo"""
    _bytes_equal_file(context, ruta)


@step('descargo "{endpoint}" en el archivo "{ruta}"')
def step_download_es(context, endpoint, ruta):
    """Hace GET a un endpoint y guarda los bytes en un archivo"""
    _download(context, endpoint, ruta)


@step('la respuesta debe tener el nombre de descarga "{nombre}"')
def step_download_name_es(context, nombre):
    """Valida el nombre de archivo en Content-Disposition"""
    _download_name(context, nombre)


@step('guardo el texto de la respuesta como "{variable}"')
def step_save_text_es(context, variable):
    """Guarda el texto crudo de la respuesta en una variable"""
    _save_text(context, variable)


# --- SSE ----------------------------------------------------------------------
@step('abro el stream SSE "{endpoint}"')
def step_sse_open_es(context, endpoint):
    """Abre un stream de Server-Sent Events y recolecta eventos en segundo plano"""
    _sse_open(context, endpoint)


@step('debo recibir un evento SSE "{evento}" en máximo {segundos:g} segundos')
def step_sse_event_es(context, evento, segundos):
    """Espera un evento SSE por nombre"""
    _sse_event(context, evento, segundos)


@step('debo recibir un evento SSE con datos que contengan "{texto}" en máximo {segundos:g} segundos')
def step_sse_data_es(context, texto, segundos):
    """Espera un evento SSE cuyos datos contengan un texto"""
    _sse_data_contains(context, texto, segundos)


@step('debo recibir {cantidad:d} eventos SSE en máximo {segundos:g} segundos')
def step_sse_count_es(context, cantidad, segundos):
    """Espera hasta que hayan llegado al menos N eventos SSE"""
    _sse_count(context, cantidad, segundos)


@step('los datos del último evento SSE "{ruta}" deben ser "{esperado}"')
def step_sse_last_es(context, ruta, esperado):
    """Valida un campo JSON de los datos del último evento SSE"""
    _sse_last(context, ruta, esperado)


@step('cierro el stream SSE')
def step_sse_close_es(context):
    """Cierra el stream SSE"""
    _sse_close(context)


# --- GraphQL ------------------------------------------------------------------
@step('establezco las variables GraphQL')
def step_gql_vars_es(context):
    """Define las variables (JSON en el texto del paso) para la próxima petición GraphQL"""
    _gql_vars(context, context.text)


@step('envío la consulta GraphQL a "{endpoint}"')
def step_gql_query_es(context, endpoint):
    """Envía la consulta GraphQL del texto del paso"""
    _gql_send(context, endpoint, context.text)


@step('envío la mutación GraphQL a "{endpoint}"')
def step_gql_mutation_es(context, endpoint):
    """Envía la mutación GraphQL del texto del paso"""
    _gql_send(context, endpoint, context.text)


@step('la respuesta GraphQL no debe tener errores')
def step_gql_no_errors_es(context):
    """Valida que la respuesta GraphQL no tenga errores"""
    _gql_no_errors(context)


@step('la respuesta GraphQL debe tener un error que contenga "{texto}"')
def step_gql_error_es(context, texto):
    """Valida que algún mensaje de error GraphQL contenga un texto"""
    _gql_error_contains(context, texto)


@step('los datos GraphQL "{ruta}" deben ser "{esperado}"')
def step_gql_data_equals_es(context, ruta, esperado):
    """Valida un valor dentro de los datos GraphQL"""
    _gql_data_equals(context, ruta, esperado)


@step('los datos GraphQL "{ruta}" deben existir')
def step_gql_data_exists_es(context, ruta):
    """Valida que una ruta exista dentro de los datos GraphQL"""
    _gql_data_exists(context, ruta)


@step('los datos GraphQL "{ruta}" deben tener {cantidad:d} elementos')
def step_gql_data_count_es(context, ruta, cantidad):
    """Valida el tamaño de un array dentro de los datos GraphQL"""
    _gql_data_count(context, ruta, cantidad)


@step('guardo los datos GraphQL "{ruta}" como "{variable}"')
def step_gql_save_es(context, ruta, variable):
    """Guarda un valor de los datos GraphQL en una variable"""
    _gql_save(context, ruta, variable)


@step('hago introspección del esquema GraphQL en "{endpoint}"')
def step_gql_introspect_es(context, endpoint):
    """Ejecuta la consulta de introspección"""
    _gql_introspect(context, endpoint)


@step('el esquema GraphQL debe tener el tipo "{nombre}"')
def step_gql_type_es(context, nombre):
    """Valida que un tipo exista en el esquema introspectado"""
    _gql_type(context, nombre)
