"""
Steps en Español para Judo Framework
Spanish step definitions for Behave integration
"""

from behave import given, when, then, step
import json
import yaml


# ============================================================
# STEPS DE CONFIGURACIÓN
# ============================================================

@step('que la URL base es "{base_url}"')
def step_url_base_es(context, base_url):
    """Establecer la URL base para las peticiones"""
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    context.judo_context.set_base_url(base_url)


@step('que tengo un cliente Judo API')
def step_setup_judo_es(context):
    """Inicializar contexto Judo"""
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)


@step('que establezco la variable "{nombre}" a "{valor}"')
def step_set_variable_es(context, nombre, valor):
    """Establecer una variable"""
    context.judo_context.set_variable(nombre, valor)


@step('que establezco la variable "{nombre}" a {valor:d}')
def step_set_variable_int_es(context, nombre, valor):
    """Establecer una variable numérica"""
    context.judo_context.set_variable(nombre, valor)


# ============================================================
# STEPS DE AUTENTICACIÓN
# ============================================================

@step('que uso el token bearer "{token}"')
def step_bearer_token_es(context, token):
    """Establecer token bearer"""
    token = context.judo_context.interpolate_string(token)
    context.judo_context.set_auth_header('bearer', token)


@step('que uso autenticación básica con usuario "{usuario}" y contraseña "{password}"')
def step_basic_auth_es(context, usuario, password):
    """Establecer autenticación básica"""
    context.judo_context.set_basic_auth(usuario, password)


@step('que establezco el header "{nombre}" a "{valor}"')
def step_set_header_es(context, nombre, valor):
    """Establecer un header"""
    valor = context.judo_context.interpolate_string(valor)
    context.judo_context.set_header(nombre, valor)


@step('que establezco el parámetro "{nombre}" a "{valor}"')
def step_set_param_es(context, nombre, valor):
    """Establecer un parámetro de query"""
    valor = context.judo_context.interpolate_string(valor)
    context.judo_context.set_query_param(nombre, valor)


# ============================================================
# STEPS DE PETICIONES HTTP
# ============================================================

@step('hago una petición GET a "{endpoint}"')
def step_get_request_es(context, endpoint):
    """Hacer petición GET"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    context.judo_context.make_request('GET', endpoint)


@step('hago una petición POST a "{endpoint}"')
def step_post_request_es(context, endpoint):
    """Hacer petición POST sin cuerpo"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    context.judo_context.make_request('POST', endpoint)


@step('hago una petición POST a "{endpoint}" con el cuerpo')
@step('hago una petición POST a "{endpoint}" con el cuerpo:')
def step_post_request_with_body_es(context, endpoint):
    """Hacer petición POST con cuerpo JSON"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    
    # Interpolar variables en el texto JSON antes de parsear
    json_text = context.text
    for key, value in context.judo_context.variables.items():
        json_text = json_text.replace(f"{{{key}}}", str(value))
    
    body = json.loads(json_text)
    context.judo_context.make_request('POST', endpoint, json=body)


@step('hago una petición PUT a "{endpoint}" con el cuerpo')
@step('hago una petición PUT a "{endpoint}" con el cuerpo:')
def step_put_request_with_body_es(context, endpoint):
    """Hacer petición PUT con cuerpo JSON"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    
    # Interpolar variables en el texto JSON antes de parsear
    json_text = context.text
    for key, value in context.judo_context.variables.items():
        json_text = json_text.replace(f"{{{key}}}", str(value))
    
    body = json.loads(json_text)
    context.judo_context.make_request('PUT', endpoint, json=body)


@step('hago una petición PATCH a "{endpoint}" con el cuerpo')
@step('hago una petición PATCH a "{endpoint}" con el cuerpo:')
def step_patch_request_with_body_es(context, endpoint):
    """Hacer petición PATCH con cuerpo JSON"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    
    # Interpolar variables en el texto JSON antes de parsear
    json_text = context.text
    for key, value in context.judo_context.variables.items():
        json_text = json_text.replace(f"{{{key}}}", str(value))
    
    body = json.loads(json_text)
    context.judo_context.make_request('PATCH', endpoint, json=body)


@step('hago una petición DELETE a "{endpoint}"')
def step_delete_request_es(context, endpoint):
    """Hacer petición DELETE"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    context.judo_context.make_request('DELETE', endpoint)


# ============================================================
# STEPS DE VALIDACIÓN DE RESPUESTA
# ============================================================

@step('el código de respuesta debe ser {status:d}')
def step_validate_status_es(context, status):
    """Validar código de respuesta"""
    context.judo_context.validate_status(status)


@step('la respuesta debe ser exitosa')
def step_validate_success_es(context):
    """Validar que la respuesta es exitosa (2xx)"""
    assert 200 <= context.judo_context.response.status < 300, \
        f"Expected successful response (2xx), but got {context.judo_context.response.status}"


@step('la respuesta debe contener el campo "{campo}"')
def step_validate_contains_field_es(context, campo):
    """Validar que la respuesta contiene un campo"""
    context.judo_context.validate_response_contains(campo)


@step('el campo "{campo}" debe ser "{valor}"')
def step_validate_field_string_es(context, campo, valor):
    """Validar que un campo tiene un valor específico (string)"""
    context.judo_context.validate_response_contains(campo, valor)


@step('el campo "{campo}" debe ser {valor:d}')
def step_validate_field_int_es(context, campo, valor):
    """Validar que un campo tiene un valor específico (número)"""
    context.judo_context.validate_response_contains(campo, valor)


@step('el campo "{campo}" debe ser igual a la variable "{variable}"')
def step_validate_field_equals_variable_es(context, campo, variable):
    """Validar que un campo es igual a una variable"""
    expected = context.judo_context.get_variable(variable)
    actual = context.judo_context.response.json.get(campo)
    assert actual == expected, \
        f"Field '{campo}' expected to be {expected}, but got {actual}"


@step('la respuesta debe tener la siguiente estructura')
@step('la respuesta debe tener la siguiente estructura:')
def step_validate_structure_es(context):
    """Validar estructura de la respuesta"""
    expected_schema = json.loads(context.text)
    context.judo_context.validate_response_schema(expected_schema)


@step('la respuesta debe ser un array')
@step('la respuesta debe ser una lista')
def step_validate_array_es(context):
    """Validar que la respuesta es un array"""
    assert isinstance(context.judo_context.response.json, list), \
        "Expected response to be an array"


@step('la respuesta debe tener {count:d} elementos')
def step_validate_array_count_es(context, count):
    """Validar cantidad de elementos en array"""
    actual_count = len(context.judo_context.response.json)
    assert actual_count == count, \
        f"Expected {count} items, but got {actual_count}"


@step('cada elemento debe tener el campo "{campo}"')
def step_validate_each_has_field_es(context, campo):
    """Validar que cada elemento tiene un campo"""
    response_data = context.judo_context.response.json
    assert isinstance(response_data, list), "Response must be an array"
    
    for i, item in enumerate(response_data):
        assert campo in item, \
            f"Item at index {i} does not have field '{campo}'"


# ============================================================
# STEPS DE EXTRACCIÓN DE DATOS
# ============================================================

@step('guardo el valor del campo "{campo}" en la variable "{variable}"')
def step_save_field_to_variable_es(context, campo, variable):
    """Guardar valor de un campo en una variable"""
    value = context.judo_context.response.json.get(campo)
    context.judo_context.set_variable(variable, value)


@step('guardo la respuesta completa en la variable "{variable}"')
def step_save_response_to_variable_es(context, variable):
    """Guardar respuesta completa en una variable"""
    context.judo_context.set_variable(variable, context.judo_context.response.json)


# ============================================================
# STEPS DE COMPARACIÓN DE VARIABLES
# ============================================================

@step('la variable "{variable1}" debe ser igual a la variable "{variable2}"')
def step_compare_variables_equal_es(context, variable1, variable2):
    """Comparar que dos variables son iguales"""
    val1 = context.judo_context.get_variable(variable1)
    val2 = context.judo_context.get_variable(variable2)
    assert val1 == val2, \
        f"Variable '{variable1}' ({val1}) is not equal to '{variable2}' ({val2})"


@step('la variable "{variable1}" no debe ser igual a la variable "{variable2}"')
def step_compare_variables_not_equal_es(context, variable1, variable2):
    """Comparar que dos variables son diferentes"""
    val1 = context.judo_context.get_variable(variable1)
    val2 = context.judo_context.get_variable(variable2)
    assert val1 != val2, \
        f"Variable '{variable1}' should not equal '{variable2}', but both are {val1}"


# ============================================================
# STEPS DE UTILIDAD
# ============================================================

@step('espero {segundos:f} segundos')
def step_wait_es(context, segundos):
    """Esperar un tiempo determinado"""
    context.judo_context.wait(segundos)


@step('imprimo la respuesta')
def step_print_response_es(context):
    """Imprimir la respuesta para debugging"""
    context.judo_context.print_response()


@step('el tiempo de respuesta debe ser menor a {max_time:f} segundos')
def step_validate_response_time_es(context, max_time):
    """Validar tiempo de respuesta"""
    elapsed = context.judo_context.response.elapsed_time
    assert elapsed < max_time, \
        f"Response time {elapsed}s exceeded maximum {max_time}s"
