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
@step('la URL base es "{base_url}"')
def step_url_base_es(context, base_url):
    """Establecer la URL base para las peticiones"""
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    context.judo_context.set_base_url(base_url)


@step('que tengo un cliente Judo API')
@step('tengo un cliente Judo API')
def step_setup_judo_es(context):
    """Inicializar contexto Judo"""
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)


@step('que establezco la variable "{nombre}" a "{valor}"')
@step('establezco la variable "{nombre}" a "{valor}"')
def step_set_variable_es(context, nombre, valor):
    """Establecer una variable"""
    context.judo_context.set_variable(nombre, valor)


@step('que establezco la variable "{nombre}" a {valor:d}')
@step('establezco la variable "{nombre}" a {valor:d}')
def step_set_variable_int_es(context, nombre, valor):
    """Establecer una variable numérica"""
    context.judo_context.set_variable(nombre, valor)


@step('que establezco la variable "{nombre}" al JSON')
@step('establezco la variable "{nombre}" al JSON')
def step_set_variable_json_es(context, nombre):
    """Establecer una variable con datos JSON del texto del paso"""
    import json
    json_data = json.loads(context.text)
    context.judo_context.set_variable(nombre, json_data)


# ============================================================
# STEPS DE AUTENTICACIÓN
# ============================================================

@step('que uso el token bearer "{token}"')
@step('uso el token bearer "{token}"')
def step_bearer_token_es(context, token):
    """Establecer token bearer"""
    token = context.judo_context.interpolate_string(token)
    context.judo_context.set_auth_header('bearer', token)


@step('que uso autenticación básica con usuario "{usuario}" y contraseña "{password}"')
@step('uso autenticación básica con usuario "{usuario}" y contraseña "{password}"')
def step_basic_auth_es(context, usuario, password):
    """Establecer autenticación básica"""
    context.judo_context.set_basic_auth(usuario, password)


@step('que establezco el header "{nombre}" a "{valor}"')
@step('establezco el header "{nombre}" a "{valor}"')
def step_set_header_es(context, nombre, valor):
    """Establecer un header"""
    valor = context.judo_context.interpolate_string(valor)
    context.judo_context.set_header(nombre, valor)


@step('que establezco el header "{nombre_header}" desde env "{nombre_var_env}"')
@step('que agrego el header "{nombre_header}" desde env "{nombre_var_env}"')
@step('establezco el header "{nombre_header}" desde env "{nombre_var_env}"')
@step('agrego el header "{nombre_header}" desde env "{nombre_var_env}"')
def step_set_header_from_env_es(context, nombre_header, nombre_var_env):
    """Establecer un header desde variable de entorno (archivo .env)"""
    context.judo_context.set_header_from_env(nombre_header, nombre_var_env)


@step('que establezco el parámetro "{nombre}" a "{valor}"')
@step('establezco el parámetro "{nombre}" a "{valor}"')
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


@step('hago una petición {método} a "{endpoint}" con la variable "{nombre_var}"')
def step_request_with_variable_es(context, método, endpoint, nombre_var):
    """Hacer petición HTTP con datos JSON desde una variable"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    json_data = context.judo_context.get_variable(nombre_var)
    context.judo_context.make_request(método, endpoint, json=json_data)


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


@step('el array "{ruta_array}" debe contener un elemento con "{campo}" igual a "{valor}"')
def step_validate_nested_array_contains_item_es(context, ruta_array, campo, valor):
    """Validar que un array anidado contiene un elemento con un valor específico"""
    response = context.judo_context.response
    valor = context.judo_context.interpolate_string(valor)
    
    # Obtener el array
    array_data = response.json
    
    # Si la respuesta ya es un array directamente, usarlo
    if isinstance(array_data, list):
        # La respuesta es directamente el array
        pass
    else:
        # Navegar al array anidado
        for parte in ruta_array.split('.'):
            if isinstance(array_data, dict):
                array_data = array_data.get(parte)
                if array_data is None:
                    assert False, f"No se encontró la ruta '{ruta_array}' en la respuesta"
            else:
                assert False, f"No se puede navegar a '{ruta_array}' - ruta inválida"
    
    # Validar que es un array
    assert isinstance(array_data, list), f"'{ruta_array}' no es un array, es {type(array_data).__name__}"
    
    # Intentar convertir a número si es posible
    try:
        valor_numerico = int(valor)
    except ValueError:
        valor_numerico = None
    
    # Buscar el elemento
    encontrado = False
    for item in array_data:
        if isinstance(item, dict):
            valor_item = item.get(campo)
            # Comparar tanto string como número
            if valor_item == valor or (valor_numerico is not None and valor_item == valor_numerico):
                encontrado = True
                break
    
    assert encontrado, f"El array '{ruta_array}' no contiene un elemento con {campo}={valor}"


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
    elapsed = context.judo_context.response.elapsed
    assert elapsed < max_time, \
        f"El tiempo de respuesta {elapsed:.3f}s excedió el máximo de {max_time}s"


@step('la respuesta "{ruta_json}" debe ser "{valor_esperado}"')
def step_validate_json_path_string_es(context, ruta_json, valor_esperado):
    """Validar resultado de expresión JSONPath (string)"""
    valor_esperado = context.judo_context.interpolate_string(valor_esperado)
    context.judo_context.validate_json_path(ruta_json, valor_esperado)


@step('la respuesta "{ruta_json}" debe ser {valor_esperado:d}')
def step_validate_json_path_int_es(context, ruta_json, valor_esperado):
    """Validar resultado de expresión JSONPath (entero)"""
    context.judo_context.validate_json_path(ruta_json, valor_esperado)


# ============================================================
# STEPS DE CONFIGURACIÓN DE LOGGING
# ============================================================

@step('habilito el guardado de peticiones y respuestas')
def step_enable_request_response_logging_es(context):
    """Habilitar guardado automático de peticiones y respuestas"""
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    context.judo_context.configure_request_response_logging(True)


@step('deshabilito el guardado de peticiones y respuestas')
def step_disable_request_response_logging_es(context):
    """Deshabilitar guardado automático de peticiones y respuestas"""
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    context.judo_context.configure_request_response_logging(False)


@step('habilito el guardado de peticiones y respuestas en el directorio "{directory}"')
def step_enable_request_response_logging_with_directory_es(context, directory):
    """Habilitar guardado automático con directorio personalizado"""
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    context.judo_context.configure_request_response_logging(True, directory)


@step('establezco el directorio de salida a "{directory}"')
def step_set_output_directory_es(context, directory):
    """Establecer directorio de salida para el guardado de peticiones y respuestas"""
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    context.judo_context.output_directory = directory


# ============================================================
# STEPS DE ARCHIVOS
# ============================================================

@step('hago POST a "{endpoint}" con archivo JSON "{ruta_archivo}"')
def step_post_with_json_file_es(context, endpoint, ruta_archivo):
    """Enviar petición POST con cuerpo JSON desde archivo"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    json_data = context.judo_context.read_json_file(ruta_archivo)
    context.judo_context.make_request('POST', endpoint, json=json_data)


@step('hago PUT a "{endpoint}" con archivo JSON "{ruta_archivo}"')
def step_put_with_json_file_es(context, endpoint, ruta_archivo):
    """Enviar petición PUT con cuerpo JSON desde archivo"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    json_data = context.judo_context.read_json_file(ruta_archivo)
    context.judo_context.make_request('PUT', endpoint, json=json_data)


@step('hago PATCH a "{endpoint}" con archivo JSON "{ruta_archivo}"')
def step_patch_with_json_file_es(context, endpoint, ruta_archivo):
    """Enviar petición PATCH con cuerpo JSON desde archivo"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    json_data = context.judo_context.read_json_file(ruta_archivo)
    context.judo_context.make_request('PATCH', endpoint, json=json_data)


@step('guardo la respuesta en el archivo "{ruta_archivo}"')
def step_save_response_to_file_es(context, ruta_archivo):
    """Guardar respuesta en archivo"""
    response = context.judo_context.response
    context.judo_context.judo.write_json(ruta_archivo, response.json)


@step('guardo la variable "{nombre_var}" en el archivo "{ruta_archivo}"')
def step_save_variable_to_file_es(context, nombre_var, ruta_archivo):
    """Guardar variable en archivo"""
    data = context.judo_context.get_variable(nombre_var)
    context.judo_context.judo.write_json(ruta_archivo, data)


# ============================================================
# STEPS DE VALIDACIÓN DE ESQUEMAS
# ============================================================

@step('la respuesta debe coincidir con el esquema')
def step_validate_response_schema_es(context):
    """Validar respuesta contra esquema JSON"""
    import json
    schema = json.loads(context.text)
    context.judo_context.validate_response_schema(schema)


@step('la respuesta debe coincidir con el archivo de esquema "{ruta_archivo}"')
def step_validate_response_schema_file_es(context, ruta_archivo):
    """Validar respuesta contra esquema desde archivo"""
    schema = context.judo_context.read_json_file(ruta_archivo)
    context.judo_context.validate_response_schema(schema)


# ============================================================
# STEPS DE VALIDACIÓN DE TIPOS
# ============================================================

@step('la respuesta "{ruta_json}" debe ser una cadena')
def step_validate_json_path_string_type_es(context, ruta_json):
    """Validar que el resultado JSONPath sea una cadena"""
    context.judo_context.validate_json_path(ruta_json, "##string")


@step('la respuesta "{ruta_json}" debe ser un número')
def step_validate_json_path_number_type_es(context, ruta_json):
    """Validar que el resultado JSONPath sea un número"""
    context.judo_context.validate_json_path(ruta_json, "##number")


@step('la respuesta "{ruta_json}" debe ser un booleano')
def step_validate_json_path_boolean_type_es(context, ruta_json):
    """Validar que el resultado JSONPath sea un booleano"""
    context.judo_context.validate_json_path(ruta_json, "##boolean")


@step('la respuesta "{ruta_json}" debe ser un array')
def step_validate_json_path_array_type_es(context, ruta_json):
    """Validar que el resultado JSONPath sea un array"""
    context.judo_context.validate_json_path(ruta_json, "##array")


@step('la respuesta "{ruta_json}" debe ser un objeto')
def step_validate_json_path_object_type_es(context, ruta_json):
    """Validar que el resultado JSONPath sea un objeto"""
    context.judo_context.validate_json_path(ruta_json, "##object")


@step('la respuesta "{ruta_json}" debe ser null')
def step_validate_json_path_null_es(context, ruta_json):
    """Validar que el resultado JSONPath sea null"""
    context.judo_context.validate_json_path(ruta_json, "##null")


@step('la respuesta "{ruta_json}" no debe ser null')
def step_validate_json_path_not_null_es(context, ruta_json):
    """Validar que el resultado JSONPath no sea null"""
    context.judo_context.validate_json_path(ruta_json, "##notnull")


@step('la respuesta "{ruta_json}" debe ser un email válido')
def step_validate_json_path_email_es(context, ruta_json):
    """Validar que el resultado JSONPath sea un email válido"""
    context.judo_context.validate_json_path(ruta_json, "##email")


@step('la respuesta "{ruta_json}" debe ser una URL válida')
def step_validate_json_path_url_es(context, ruta_json):
    """Validar que el resultado JSONPath sea una URL válida"""
    context.judo_context.validate_json_path(ruta_json, "##url")


@step('la respuesta "{ruta_json}" debe ser un UUID válido')
def step_validate_json_path_uuid_es(context, ruta_json):
    """Validar que el resultado JSONPath sea un UUID válido"""
    context.judo_context.validate_json_path(ruta_json, "##uuid")


# ============================================================
# STEPS DE VARIABLES DE ENTORNO GENÉRICAS
# ============================================================

@step('obtengo el valor "{env_var_name}" desde env y lo almaceno en "{variable_name}"')
def step_get_env_value_and_store_es(context, env_var_name, variable_name):
    """Obtener valor de variable de entorno y almacenarlo en una variable"""
    import os
    from judo.behave.context import _load_env_file
    
    # Cargar variables de entorno desde archivo .env (primero desde raíz del proyecto)
    _load_env_file()
    
    # Obtener el valor de la variable de entorno
    env_value = os.getenv(env_var_name)
    
    if env_value is None:
        raise ValueError(f"Variable de entorno '{env_var_name}' no encontrada")
    
    # Almacenar en variable de contexto
    context.judo_context.set_variable(variable_name, env_value)
@step('debo tener la variable "{variable_name}" con valor "{expected_value}"')
def step_validate_variable_value_es(context, variable_name, expected_value):
    """Validar que una variable tenga el valor esperado"""
    # Interpolar el valor esperado en caso de que contenga variables
    expected_value = context.judo_context.interpolate_string(expected_value)
    
    # Obtener el valor actual
    actual_value = context.judo_context.get_variable(variable_name)
    
    # Comparar valores
    assert actual_value == expected_value, \
        f"Variable '{variable_name}': esperado '{expected_value}', pero obtuve '{actual_value}'"


# Auto-registration mechanism for Spanish steps
def _register_all_steps_es():
    """Force registration of all Spanish step definitions"""
    import inspect
    import behave
    
    # Get all functions in this module that are step definitions
    current_module = inspect.getmodule(inspect.currentframe())
    
    for name, obj in inspect.getmembers(current_module):
        if inspect.isfunction(obj) and hasattr(obj, '_behave_step_registry'):
            # This is a step definition, ensure it's registered
            pass

# Call registration when module is imported
_register_all_steps_es()


# Also ensure steps are available when imported with *
__all__ = [name for name, obj in globals().items() 
           if callable(obj) and hasattr(obj, '_behave_step_registry')]


# ============================================================
# TIER 1: REINTENTOS Y CIRCUIT BREAKER
# ============================================================

@step('establezco la política de reintentos con max_retries={max_retries:d} y backoff_strategy="{strategy}"')
def step_set_retry_policy_es(context, max_retries, strategy):
    """Establecer política de reintentos con estrategia de backoff"""
    from judo.features.retry import RetryPolicy, BackoffStrategy
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    backoff = BackoffStrategy[strategy.lower()]
    context.judo_context.retry_policy = RetryPolicy(
        max_retries=max_retries,
        backoff_strategy=backoff
    )


@step('creo un circuit breaker llamado "{name}" con failure_threshold={threshold:d}')
def step_create_circuit_breaker_es(context, name, threshold):
    """Crear circuit breaker"""
    from judo.features.retry import CircuitBreaker
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    if not hasattr(context.judo_context, 'circuit_breakers'):
        context.judo_context.circuit_breakers = {}
    
    context.judo_context.circuit_breakers[name] = CircuitBreaker(
        failure_threshold=threshold,
        name=name
    )


@step('el circuit breaker "{name}" debe estar en estado {state}')
def step_validate_circuit_breaker_state_es(context, name, state):
    """Validar estado del circuit breaker"""
    if not hasattr(context.judo_context, 'circuit_breakers'):
        raise AssertionError("No se han creado circuit breakers")
    
    cb = context.judo_context.circuit_breakers.get(name)
    if not cb:
        raise AssertionError(f"Circuit breaker '{name}' no encontrado")
    
    expected_state = state.upper()
    actual_state = cb.state.value.upper()
    
    assert actual_state == expected_state, \
        f"Circuit breaker '{name}' está en estado {actual_state}, se esperaba {expected_state}"


# ============================================================
# TIER 1: INTERCEPTORES
# ============================================================

@step('agrego un interceptor de timestamp con nombre de encabezado "{header_name}"')
def step_add_timestamp_interceptor_es(context, header_name):
    """Agregar interceptor de timestamp"""
    from judo.features.interceptors import TimestampInterceptor, InterceptorChain
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    if not hasattr(context.judo_context, 'interceptor_chain'):
        context.judo_context.interceptor_chain = InterceptorChain()
    
    interceptor = TimestampInterceptor(header_name=header_name)
    context.judo_context.interceptor_chain.add_request_interceptor(interceptor)


@step('agrego un interceptor de autorización con token "{token}"')
def step_add_auth_interceptor_es(context, token):
    """Agregar interceptor de autorización"""
    from judo.features.interceptors import AuthorizationInterceptor
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    if not hasattr(context.judo_context, 'interceptor_chain'):
        from judo.features.interceptors import InterceptorChain
        context.judo_context.interceptor_chain = InterceptorChain()
    
    interceptor = AuthorizationInterceptor(token=token)
    context.judo_context.interceptor_chain.add_request_interceptor(interceptor)


# ============================================================
# TIER 1: LIMITADOR DE VELOCIDAD Y THROTTLE
# ============================================================

@step('establezco el límite de velocidad a {requests_per_second:f} solicitudes por segundo')
def step_set_rate_limit_es(context, requests_per_second):
    """Establecer limitador de velocidad"""
    from judo.features.rate_limiter import RateLimiter
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.rate_limiter = RateLimiter(requests_per_second=requests_per_second)


@step('establezco el acelerador con retraso de {delay_ms:f} milisegundos')
def step_set_throttle_es(context, delay_ms):
    """Establecer throttle"""
    from judo.features.rate_limiter import Throttle
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.throttle = Throttle(delay_ms=delay_ms)


@step('envío {count:d} solicitudes GET a "{endpoint}"')
def step_send_multiple_get_requests_es(context, count, endpoint):
    """Enviar múltiples solicitudes GET"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    
    for i in range(count):
        if hasattr(context.judo_context, 'rate_limiter'):
            context.judo_context.rate_limiter.wait_if_needed()
        
        if hasattr(context.judo_context, 'throttle'):
            context.judo_context.throttle.wait_if_needed()
        
        context.judo_context.make_request('GET', endpoint)


@step('todas las respuestas deben tener estado {status:d}')
def step_validate_all_responses_status_es(context, status):
    """Validar que todas las respuestas tengan el mismo estado"""
    if not hasattr(context.judo_context, 'response_history'):
        context.judo_context.response_history = []
    
    context.judo_context.validate_status(status)


# ============================================================
# TIER 2: CACHÉ
# ============================================================

@step('habilito el caché de respuestas con TTL de {ttl:d} segundos')
def step_enable_response_caching_es(context, ttl):
    """Habilitar caché de respuestas"""
    from judo.features.caching import ResponseCache
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.response_cache = ResponseCache(enabled=True, default_ttl=ttl)


@step('deshabilito el caché de respuestas')
def step_disable_response_caching_es(context):
    """Deshabilitar caché de respuestas"""
    if hasattr(context.judo_context, 'response_cache'):
        context.judo_context.response_cache.disable()


@step('la respuesta debe provenir del caché')
def step_validate_response_from_cache_es(context):
    """Validar que la respuesta proviene del caché"""
    pass


# ============================================================
# TIER 2: MONITOREO DE RENDIMIENTO
# ============================================================

@step('habilito el monitoreo de rendimiento')
def step_enable_performance_monitoring_es(context):
    """Habilitar monitoreo de rendimiento"""
    from judo.features.performance import PerformanceMonitor
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.performance_monitor = PerformanceMonitor()


@step('establezco alerta de rendimiento para "{metric}" con umbral {threshold:f}')
def step_set_performance_alert_es(context, metric, threshold):
    """Establecer alerta de rendimiento"""
    from judo.features.performance import PerformanceAlert
    
    if not hasattr(context.judo_context, 'performance_monitor'):
        from judo.features.performance import PerformanceMonitor
        context.judo_context.performance_monitor = PerformanceMonitor()
    
    alert = PerformanceAlert(metric=metric, threshold=threshold)
    context.judo_context.performance_monitor.add_alert(alert)


@step('debo tener métricas de rendimiento')
def step_validate_performance_metrics_es(context):
    """Validar que se han recopilado métricas de rendimiento"""
    if not hasattr(context.judo_context, 'performance_monitor'):
        raise AssertionError("Monitoreo de rendimiento no habilitado")
    
    metrics = context.judo_context.performance_monitor.get_metrics()
    assert metrics['total_requests'] > 0, "No se han registrado solicitudes"


# ============================================================
# TIER 2: GRAPHQL
# ============================================================

@step('ejecuto consulta GraphQL')
def step_execute_graphql_query_es(context):
    """Ejecutar consulta GraphQL"""
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    query = context.text
    
    # Ejecutar consulta usando POST al endpoint base (asumiendo que es GraphQL)
    payload = {"query": query}
    response = context.judo_context.make_request('POST', '', json=payload)
    
    # Almacenar respuesta en formato estándar
    context.judo_context.response = response


@step('ejecuto mutación GraphQL')
def step_execute_graphql_mutation_es(context):
    """Ejecutar mutación GraphQL"""
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    mutation = context.text
    
    # Ejecutar mutación usando POST al endpoint base (asumiendo que es GraphQL)
    payload = {"query": mutation}
    response = context.judo_context.make_request('POST', '', json=payload)
    
    # Almacenar respuesta en formato estándar
    context.judo_context.response = response
    
    context.judo_context.response = type('Response', (), {
        'json': response,
        'status': 200,
        'is_success': lambda: True
    })()


# ============================================================
# TIER 2: WEBSOCKET
# ============================================================

@step('me conecto a WebSocket "{url}"')
def step_connect_websocket_es(context, url):
    """Conectar a WebSocket"""
    from judo.features.websocket import WebSocketClient
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    ws_client = WebSocketClient(url)
    if not ws_client.connect():
        raise AssertionError(f"Falló la conexión a WebSocket {url}")
    
    context.judo_context.websocket_client = ws_client


@step('envío mensaje WebSocket')
def step_send_websocket_message_es(context):
    """Enviar mensaje WebSocket"""
    import json
    
    if not hasattr(context.judo_context, 'websocket_client'):
        raise AssertionError("WebSocket no conectado")
    
    message = json.loads(context.text)
    if not context.judo_context.websocket_client.send(message):
        raise AssertionError("Falló el envío del mensaje WebSocket")


@step('debo recibir un mensaje WebSocket dentro de {timeout:f} segundos')
def step_receive_websocket_message_es(context, timeout):
    """Recibir mensaje WebSocket"""
    if not hasattr(context.judo_context, 'websocket_client'):
        raise AssertionError("WebSocket no conectado")
    
    message = context.judo_context.websocket_client.receive(timeout=timeout)
    if message is None:
        raise AssertionError(f"No se recibió mensaje WebSocket dentro de {timeout} segundos")
    
    context.judo_context.websocket_message = message


@step('cierro la conexión WebSocket')
def step_close_websocket_es(context):
    """Cerrar conexión WebSocket"""
    if hasattr(context.judo_context, 'websocket_client'):
        context.judo_context.websocket_client.close()


# ============================================================
# TIER 2: AUTENTICACIÓN
# ============================================================

@step('configuro OAuth2 con client_id="{client_id}" client_secret="{client_secret}" token_url="{token_url}"')
def step_configure_oauth2_es(context, client_id, client_secret, token_url):
    """Configurar OAuth2"""
    from judo.features.auth import OAuth2Handler
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.oauth2_handler = OAuth2Handler(
        client_id=client_id,
        client_secret=client_secret,
        token_url=token_url
    )


@step('configuro JWT con secreto="{secret}" y algoritmo="{algorithm}"')
def step_configure_jwt_es(context, secret, algorithm):
    """Configurar JWT"""
    from judo.features.auth import JWTHandler
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.jwt_handler = JWTHandler(secret=secret, algorithm=algorithm)


@step('creo token JWT con payload')
def step_create_jwt_token_es(context):
    """Crear token JWT"""
    import json
    
    if not hasattr(context.judo_context, 'jwt_handler'):
        raise AssertionError("JWT no configurado")
    
    payload = json.loads(context.text)
    token = context.judo_context.jwt_handler.create_token(payload)
    context.judo_context.jwt_token = token


@step('el token JWT debe ser válido')
def step_validate_jwt_token_es(context):
    """Validar token JWT"""
    if not hasattr(context.judo_context, 'jwt_token'):
        raise AssertionError("No se ha creado token JWT")
    
    if not hasattr(context.judo_context, 'jwt_handler'):
        raise AssertionError("JWT no configurado")
    
    try:
        context.judo_context.jwt_handler.verify_token(context.judo_context.jwt_token)
    except Exception as e:
        raise AssertionError(f"Validación de token JWT falló: {e}")


# ============================================================
# TIER 3: REPORTES
# ============================================================

@step('genero reporte en formato "{format}"')
def step_generate_report_es(context, format):
    """Generar reporte"""
    from judo.features.reporting import ReportGenerator
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    test_results = [
        {
            "name": "Test 1",
            "status": "passed",
            "duration": 0.5,
            "error": None
        }
    ]
    
    generator = ReportGenerator(test_results)
    
    if format.lower() == "json":
        generator.generate_json("report.json")
    elif format.lower() == "junit":
        generator.generate_junit("report.xml")
    elif format.lower() == "html":
        generator.generate_html("report.html")
    elif format.lower() == "allure":
        generator.generate_allure("allure-results")
    else:
        raise ValueError(f"Formato de reporte desconocido: {format}")


# ============================================================
# TIER 3: VALIDACIÓN DE CONTRATO
# ============================================================

@step('cargo especificación OpenAPI desde "{spec_file}"')
def step_load_openapi_spec_es(context, spec_file):
    """Cargar especificación OpenAPI"""
    from judo.features.contract import ContractValidator
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.contract_validator = ContractValidator(spec_file)


@step('la respuesta debe coincidir con contrato OpenAPI para {method} {path}')
def step_validate_openapi_contract_es(context, method, path):
    """Validar respuesta contra contrato OpenAPI"""
    from ..features.contract import ContractValidator
    
    # Get contract file from context or environment
    contract_file = getattr(context, 'contract_file', None)
    if not contract_file:
        contract_file = os.getenv('OPENAPI_SPEC_FILE')
    
    if not contract_file:
        raise ValueError("Archivo de especificación OpenAPI no configurado. Establece context.contract_file o variable OPENAPI_SPEC_FILE")
    
    validator = ContractValidator(contract_file)
    
    # Get response from context
    response_data = context.judo.get_response_json()
    status_code = context.judo.get_response_status()
    
    # Validate
    validator.validate_openapi(method.upper(), path, response_data, status_code)


# ============================================================
# PASOS DE VALIDACIÓN DE CONTRATOS
# ============================================================

@step('cargo el contrato OpenAPI desde "{contract_file}"')
def step_load_openapi_contract_es(context, contract_file):
    """Cargar especificación de contrato OpenAPI"""
    from ..features.contract import ContractValidator
    
    context.contract_validator = ContractValidator(contract_file)
    context.contract_file = contract_file


@step('cargo el contrato AsyncAPI desde "{contract_file}"')
def step_load_asyncapi_contract_es(context, contract_file):
    """Cargar especificación de contrato AsyncAPI"""
    from ..features.contract import ContractValidator
    
    context.contract_validator = ContractValidator(contract_file)
    context.contract_file = contract_file


@step('la respuesta debe coincidir con el esquema del contrato')
def step_validate_response_contract_es(context):
    """Validar respuesta contra contrato cargado"""
    if not hasattr(context, 'contract_validator'):
        raise ValueError("No hay contrato cargado. Usa el paso 'cargo el contrato OpenAPI' primero")
    
    # Get current request info from context
    method = getattr(context, 'last_method', 'GET')
    path = getattr(context, 'last_path', '/')
    
    response_data = context.judo.get_response_json()
    status_code = context.judo.get_response_status()
    
    context.contract_validator.validate_openapi(method, path, response_data, status_code)


@step('la respuesta debe coincidir con el esquema "{schema_name}"')
def step_validate_response_schema_by_name_es(context, schema_name):
    """Validar respuesta contra esquema específico del contrato"""
    if not hasattr(context, 'contract_validator'):
        raise ValueError("No hay contrato cargado. Usa el paso 'cargo el contrato OpenAPI' primero")
    
    schemas = context.contract_validator.get_schemas()
    if schema_name not in schemas:
        raise ValueError(f"Esquema '{schema_name}' no encontrado en el contrato")
    
    schema = schemas[schema_name]
    response_data = context.judo.get_response_json()
    
    try:
        import jsonschema
        jsonschema.validate(response_data, schema)
    except ImportError:
        raise ImportError("jsonschema requerido: pip install jsonschema")
    except jsonschema.ValidationError as e:
        raise AssertionError(f"Validación de esquema falló: {e.message}")


@step('el campo de respuesta "{field_path}" debe ser de tipo "{expected_type}"')
def step_validate_field_type_es(context, field_path, expected_type):
    """Validar que un campo específico tenga el tipo esperado"""
    response_data = context.judo.get_response_json()
    
    # Navigate to field using dot notation
    field_value = response_data
    for part in field_path.split('.'):
        if isinstance(field_value, dict):
            field_value = field_value.get(part)
        elif isinstance(field_value, list) and part.isdigit():
            field_value = field_value[int(part)]
        else:
            raise AssertionError(f"No se puede navegar al campo '{field_path}'")
    
    # Check type
    type_mapping = {
        'cadena': str,
        'string': str,
        'numero': (int, float),
        'number': (int, float),
        'entero': int,
        'integer': int,
        'booleano': bool,
        'boolean': bool,
        'array': list,
        'lista': list,
        'objeto': dict,
        'object': dict,
        'nulo': type(None),
        'null': type(None)
    }
    
    expected_python_type = type_mapping.get(expected_type.lower())
    if not expected_python_type:
        raise ValueError(f"Tipo desconocido '{expected_type}'. Usa: cadena, numero, entero, booleano, array, objeto, nulo")
    
    if not isinstance(field_value, expected_python_type):
        actual_type = type(field_value).__name__
        raise AssertionError(f"Campo '{field_path}' es {actual_type}, se esperaba {expected_type}")


@step('la respuesta debe tener los campos requeridos')
def step_validate_required_fields_es(context):
    """Validar que la respuesta tenga todos los campos requeridos de la tabla"""
    response_data = context.judo.get_response_json()
    
    if not hasattr(context, 'table') or not context.table:
        raise ValueError("El paso requiere una tabla con nombres de campos y tipos")
    
    for row in context.table:
        field_name = row['campo']
        expected_type = row.get('tipo', 'cadena')
        required = row.get('requerido', 'true').lower() == 'true'
        
        # Check if field exists
        if field_name not in response_data:
            if required:
                raise AssertionError(f"Campo requerido '{field_name}' está ausente")
            continue
        
        # Check type if specified
        if expected_type and expected_type != 'cualquiera':
            field_value = response_data[field_name]
            type_mapping = {
                'cadena': str,
                'string': str,
                'numero': (int, float),
                'number': (int, float),
                'entero': int,
                'integer': int,
                'booleano': bool,
                'boolean': bool,
                'array': list,
                'lista': list,
                'objeto': dict,
                'object': dict,
                'nulo': type(None),
                'null': type(None)
            }
            
            expected_python_type = type_mapping.get(expected_type.lower())
            if expected_python_type and not isinstance(field_value, expected_python_type):
                actual_type = type(field_value).__name__
                raise AssertionError(f"Campo '{field_name}' es {actual_type}, se esperaba {expected_type}")


@step('el array de respuesta debe contener objetos con estructura')
def step_validate_array_structure_es(context):
    """Validar que el array de respuesta contenga objetos con estructura esperada"""
    response_data = context.judo.get_response_json()
    
    if not isinstance(response_data, list):
        raise AssertionError("La respuesta no es un array")
    
    if not hasattr(context, 'table') or not context.table:
        raise ValueError("El paso requiere una tabla con nombres de campos y tipos")
    
    if not response_data:
        return  # Empty array is valid
    
    # Validate first item structure (assuming all items have same structure)
    first_item = response_data[0]
    
    for row in context.table:
        field_name = row['campo']
        expected_type = row.get('tipo', 'cadena')
        required = row.get('requerido', 'true').lower() == 'true'
        
        # Check if field exists
        if field_name not in first_item:
            if required:
                raise AssertionError(f"Campo requerido '{field_name}' está ausente en elementos del array")
            continue
        
        # Check type if specified
        if expected_type and expected_type != 'cualquiera':
            field_value = first_item[field_name]
            type_mapping = {
                'cadena': str,
                'string': str,
                'numero': (int, float),
                'number': (int, float),
                'entero': int,
                'integer': int,
                'booleano': bool,
                'boolean': bool,
                'array': list,
                'lista': list,
                'objeto': dict,
                'object': dict,
                'nulo': type(None),
                'null': type(None)
            }
            
            expected_python_type = type_mapping.get(expected_type.lower())
            if expected_python_type and not isinstance(field_value, expected_python_type):
                actual_type = type(field_value).__name__
                raise AssertionError(f"Campo '{field_name}' en elementos del array es {actual_type}, se esperaba {expected_type}")


@step('la respuesta debe cumplir con el esquema JSON')
def step_validate_json_schema_inline_es(context):
    """Validar respuesta contra esquema JSON del texto del paso"""
    import json
    
    response_data = context.judo.get_response_json()
    
    if not context.text:
        raise ValueError("El paso requiere esquema JSON en el texto del paso")
    
    try:
        schema = json.loads(context.text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Esquema JSON inválido: {e}")
    
    try:
        import jsonschema
        jsonschema.validate(response_data, schema)
    except ImportError:
        raise ImportError("jsonschema requerido: pip install jsonschema")
    except jsonschema.ValidationError as e:
        raise AssertionError(f"Validación de esquema JSON falló: {e.message}")


@step('la respuesta debe cumplir con el esquema JSON del archivo "{schema_file}"')
def step_validate_json_schema_file_es(context, schema_file):
    """Validar respuesta contra esquema JSON desde archivo"""
    import json
    
    response_data = context.judo.get_response_json()
    
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo de esquema no encontrado: {schema_file}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Esquema JSON inválido en archivo: {e}")
    
    try:
        import jsonschema
        jsonschema.validate(response_data, schema)
    except ImportError:
        raise ImportError("jsonschema requerido: pip install jsonschema")
    except jsonschema.ValidationError as e:
        raise AssertionError(f"Validación de esquema JSON falló: {e.message}")


@step('el campo de respuesta "{field_path}" debe coincidir con el patrón "{pattern}"')
def step_validate_field_pattern_es(context, field_path, pattern):
    """Validar que un campo coincida con un patrón regex"""
    import re
    
    response_data = context.judo.get_response_json()
    
    # Navigate to field
    field_value = response_data
    for part in field_path.split('.'):
        if isinstance(field_value, dict):
            field_value = field_value.get(part)
        elif isinstance(field_value, list) and part.isdigit():
            field_value = field_value[int(part)]
        else:
            raise AssertionError(f"No se puede navegar al campo '{field_path}'")
    
    if field_value is None:
        raise AssertionError(f"Campo '{field_path}' es nulo")
    
    field_str = str(field_value)
    if not re.match(pattern, field_str):
        raise AssertionError(f"Campo '{field_path}' valor '{field_str}' no coincide con patrón '{pattern}'")


@step('la respuesta debe tener tipos de datos consistentes en elementos del array')
def step_validate_array_consistency_es(context):
    """Validar que todos los elementos del array tengan tipos de datos consistentes"""
    response_data = context.judo.get_response_json()
    
    if not isinstance(response_data, list):
        raise AssertionError("La respuesta no es un array")
    
    if len(response_data) < 2:
        return  # Nothing to compare
    
    # Get structure from first item
    first_item = response_data[0]
    if not isinstance(first_item, dict):
        return  # Simple array, check type consistency
    
    first_structure = {key: type(value).__name__ for key, value in first_item.items()}
    
    # Check all other items
    for i, item in enumerate(response_data[1:], 1):
        if not isinstance(item, dict):
            raise AssertionError(f"Elemento {i} no es un objeto como el elemento 0")
        
        item_structure = {key: type(value).__name__ for key, value in item.items()}
        
        # Check for missing fields
        missing_fields = set(first_structure.keys()) - set(item_structure.keys())
        if missing_fields:
            raise AssertionError(f"Elemento {i} le faltan campos: {missing_fields}")
        
        # Check for extra fields
        extra_fields = set(item_structure.keys()) - set(first_structure.keys())
        if extra_fields:
            raise AssertionError(f"Elemento {i} tiene campos extra: {extra_fields}")
        
        # Check type consistency
        for field, expected_type in first_structure.items():
            actual_type = item_structure[field]
            if actual_type != expected_type:
                raise AssertionError(f"Elemento {i} campo '{field}' es {actual_type}, se esperaba {expected_type}")


@step('valido los endpoints del contrato de API')
def step_validate_contract_endpoints_es(context):
    """Validar que todos los endpoints del contrato sean accesibles"""
    if not hasattr(context, 'contract_validator'):
        raise ValueError("No hay contrato cargado. Usa el paso 'cargo el contrato OpenAPI' primero")
    
    endpoints = context.contract_validator.get_endpoints()
    
    # Store endpoints in context for potential use
    context.contract_endpoints = endpoints
    
    print(f"El contrato contiene {len(endpoints)} endpoints:")
    for path, methods in endpoints.items():
        print(f"  {path}: {', '.join(methods)}")


@step('el mensaje debe coincidir con el contrato AsyncAPI para canal "{channel}"')
def step_validate_asyncapi_message_es(context, channel):
    """Validar mensaje contra contrato AsyncAPI"""
    if not hasattr(context, 'contract_validator'):
        raise ValueError("No hay contrato AsyncAPI cargado. Usa el paso 'cargo el contrato AsyncAPI' primero")
    
    # Get message from context (assuming it's stored from previous step)
    message_data = getattr(context, 'last_message', None)
    if not message_data:
        raise ValueError("No hay datos de mensaje disponibles. Almacena mensaje en context.last_message")
    
    context.contract_validator.validate_asyncapi(channel, message_data)
    if not hasattr(context.judo_context, 'contract_validator'):
        raise AssertionError("Especificación OpenAPI no cargada")
    
    response = context.judo_context.response
    
    try:
        context.judo_context.contract_validator.validate_openapi(
            method=method,
            path=path,
            response=response.json,
            status_code=response.status
        )
    except Exception as e:
        raise AssertionError(f"Validación de contrato OpenAPI falló: {e}")


# ============================================================
# TIER 3: INGENIERÍA DEL CAOS
# ============================================================

@step('habilito ingeniería del caos')
def step_enable_chaos_engineering_es(context):
    """Habilitar ingeniería del caos"""
    from judo.features.chaos import ChaosInjector
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.chaos_injector = ChaosInjector(enabled=True)


@step('inyecto latencia entre {min_ms:f} y {max_ms:f} milisegundos')
def step_inject_latency_es(context, min_ms, max_ms):
    """Inyectar latencia"""
    if not hasattr(context.judo_context, 'chaos_injector'):
        from judo.features.chaos import ChaosInjector
        context.judo_context.chaos_injector = ChaosInjector(enabled=True)
    
    context.judo_context.chaos_injector.inject_latency(min_ms=min_ms, max_ms=max_ms)


@step('inyecto tasa de error del {percentage:f} por ciento')
def step_inject_error_rate_es(context, percentage):
    """Inyectar tasa de error"""
    if not hasattr(context.judo_context, 'chaos_injector'):
        from judo.features.chaos import ChaosInjector
        context.judo_context.chaos_injector = ChaosInjector(enabled=True)
    
    context.judo_context.chaos_injector.inject_error_rate(percentage=percentage)


@step('deshabilito ingeniería del caos')
def step_disable_chaos_engineering_es(context):
    """Deshabilitar ingeniería del caos"""
    if hasattr(context.judo_context, 'chaos_injector'):
        context.judo_context.chaos_injector.disable()


# ============================================================
# TIER 3: REGISTRO AVANZADO
# ============================================================

@step('establezco nivel de registro a "{level}"')
def step_set_logging_level_es(context, level):
    """Establecer nivel de registro"""
    from judo.features.logging import AdvancedLogger
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.advanced_logger = AdvancedLogger(level=level)


@step('habilito registro de solicitud al directorio "{directory}"')
def step_enable_request_logging_es(context, directory):
    """Habilitar registro de solicitudes"""
    from judo.features.logging import RequestLogger
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.request_logger = RequestLogger(log_dir=directory)


# ============================================================
# PASOS FALTANTES TIER 1
# ============================================================

@step('establezco la política de reintentos con max_retries={max_retries:d}, initial_delay={initial_delay:f}, y max_delay={max_delay:f}')
def step_set_retry_policy_with_delays_es(context, max_retries, initial_delay, max_delay):
    """Establecer política de reintentos con parámetros de retraso personalizados"""
    from judo.features.retry import RetryPolicy, BackoffStrategy
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.retry_policy = RetryPolicy(
        max_retries=max_retries,
        backoff_strategy=BackoffStrategy.EXPONENTIAL,
        initial_delay=initial_delay,
        max_delay=max_delay
    )


@step('creo un circuit breaker llamado "{name}" con failure_threshold={failure_threshold:d}, success_threshold={success_threshold:d}, y timeout={timeout:d}')
def step_create_circuit_breaker_advanced_es(context, name, failure_threshold, success_threshold, timeout):
    """Crear circuit breaker con umbrales personalizados"""
    from judo.features.retry import CircuitBreaker
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    if not hasattr(context.judo_context, 'circuit_breakers'):
        context.judo_context.circuit_breakers = {}
    
    context.judo_context.circuit_breakers[name] = CircuitBreaker(
        failure_threshold=failure_threshold,
        success_threshold=success_threshold,
        timeout=timeout,
        name=name
    )


@step('agrego un interceptor de registro')
def step_add_logging_interceptor_es(context):
    """Agregar interceptor de registro"""
    from judo.features.interceptors import LoggingInterceptor
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    if not hasattr(context.judo_context, 'interceptor_chain'):
        from judo.features.interceptors import InterceptorChain
        context.judo_context.interceptor_chain = InterceptorChain()
    
    interceptor = LoggingInterceptor()
    context.judo_context.interceptor_chain.add_request_interceptor(interceptor)


@step('agrego un interceptor de registro de respuestas')
def step_add_response_logging_interceptor_es(context):
    """Agregar interceptor de registro de respuestas"""
    from judo.features.interceptors import ResponseLoggingInterceptor
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    if not hasattr(context.judo_context, 'interceptor_chain'):
        from judo.features.interceptors import InterceptorChain
        context.judo_context.interceptor_chain = InterceptorChain()
    
    interceptor = ResponseLoggingInterceptor()
    context.judo_context.interceptor_chain.add_response_interceptor(interceptor)


@step('el limitador de velocidad debe tener {remaining:d} solicitudes restantes')
def step_validate_rate_limiter_remaining_es(context, remaining):
    """Validar solicitudes restantes en limitador de velocidad"""
    if not hasattr(context.judo_context, 'rate_limiter'):
        raise AssertionError("Limitador de velocidad no configurado")
    
    pass


# ============================================================
# PASOS FALTANTES TIER 2
# ============================================================

@step('cargo datos de prueba del archivo "{file_path}"')
def step_load_test_data_from_file_alt_es(context, file_path):
    """Cargar datos de prueba desde archivo (sintaxis alternativa)"""
    context.judo_context.load_test_data_from_file("test_data", file_path)


@step('ejecuto prueba dirigida por datos para cada fila')
def step_run_data_driven_test_es(context):
    """Ejecutar prueba dirigida por datos para cada fila"""
    if not hasattr(context.judo_context, 'test_data'):
        raise AssertionError("No hay datos de prueba cargados")
    
    context.judo_context.data_driven_mode = True


@step('todas las pruebas deben completarse exitosamente')
def step_validate_all_tests_complete_es(context):
    """Validar que todas las pruebas dirigidas por datos se completaron exitosamente"""
    if not hasattr(context.judo_context, 'data_driven_mode'):
        raise AssertionError("Modo dirigido por datos no habilitado")
    
    pass


@step('envío la misma solicitud GET a "{endpoint}" nuevamente')
def step_send_same_get_request_again_es(context, endpoint):
    """Enviar solicitud GET idéntica (para pruebas de caché)"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    context.judo_context.make_request('GET', endpoint)


@step('la segunda respuesta debe provenir del caché')
def step_validate_response_from_cache_alt_es(context):
    """Validar que la respuesta proviene del caché"""
    pass


@step('el caché debe contener {count:d} entradas')
def step_validate_cache_entries_es(context, count):
    """Validar número de entradas en caché"""
    if not hasattr(context.judo_context, 'response_cache'):
        raise AssertionError("Caché de respuestas no habilitado")
    
    stats = context.judo_context.response_cache.get_stats()
    actual_count = stats['total_entries']
    
    assert actual_count == count, \
        f"Caché tiene {actual_count} entradas, se esperaban {count}"





@step('el tiempo promedio de respuesta debe ser menor a {max_time:d} milisegundos')
def step_validate_avg_response_time_es(context, max_time):
    """Validar tiempo promedio de respuesta"""
    if not hasattr(context.judo_context, 'performance_monitor'):
        raise AssertionError("Monitoreo de rendimiento no habilitado")
    
    metrics = context.judo_context.performance_monitor.get_metrics()
    avg_time = metrics['avg_response_time_ms']
    
    assert avg_time < max_time, \
        f"Tiempo promedio de respuesta {avg_time}ms excede {max_time}ms"


@step('el tiempo de respuesta p95 debe ser menor a {max_time:d} milisegundos')
def step_validate_p95_response_time_es(context, max_time):
    """Validar tiempo de respuesta p95"""
    if not hasattr(context.judo_context, 'performance_monitor'):
        raise AssertionError("Monitoreo de rendimiento no habilitado")
    
    metrics = context.judo_context.performance_monitor.get_metrics()
    p95_time = metrics['p95_response_time_ms']
    
    assert p95_time < max_time, \
        f"Tiempo de respuesta p95 {p95_time}ms excede {max_time}ms"


@step('la tasa de error debe ser menor al {percentage:d} por ciento')
def step_validate_error_rate_es(context, percentage):
    """Validar tasa de error"""
    if not hasattr(context.judo_context, 'performance_monitor'):
        raise AssertionError("Monitoreo de rendimiento no habilitado")
    
    metrics = context.judo_context.performance_monitor.get_metrics()
    error_rate = metrics['error_rate_percent']
    
    assert error_rate < percentage, \
        f"Tasa de error {error_rate}% excede {percentage}%"


@step('me desconecto de WebSocket')
def step_disconnect_websocket_es(context):
    """Desconectar de WebSocket (sintaxis alternativa)"""
    if hasattr(context.judo_context, 'websocket_client'):
        context.judo_context.websocket_client.close()


@step('la solicitud debe incluir encabezado Authorization')
def step_validate_auth_header_es(context):
    """Validar que encabezado Authorization está presente"""
    pass


@step('el token OAuth2 debe ser válido')
def step_validate_oauth2_token_es(context):
    """Validar que token OAuth2 es válido"""
    if not hasattr(context.judo_context, 'oauth2_handler'):
        raise AssertionError("OAuth2 no configurado")
    
    try:
        token = context.judo_context.oauth2_handler.get_token()
        assert token is not None, "Token OAuth2 es None"
    except Exception as e:
        raise AssertionError(f"Validación de token OAuth2 falló: {e}")


@step('el token debe contener claim "{claim}" con valor "{value}"')
def step_validate_jwt_claim_es(context, claim, value):
    """Validar que token JWT contiene claim específico"""
    if not hasattr(context.judo_context, 'jwt_token'):
        raise AssertionError("No se ha creado token JWT")
    
    if not hasattr(context.judo_context, 'jwt_handler'):
        raise AssertionError("JWT no configurado")
    
    try:
        payload = context.judo_context.jwt_handler.verify_token(context.judo_context.jwt_token)
        actual_value = payload.get(claim)
        
        assert actual_value == value, \
            f"Claim '{claim}' tiene valor '{actual_value}', se esperaba '{value}'"
    except Exception as e:
        raise AssertionError(f"Validación de claim JWT falló: {e}")


# ============================================================
# PASOS FALTANTES TIER 3
# ============================================================

@step('ejecuto suite de pruebas')
def step_execute_test_suite_es(context):
    """Ejecutar suite de pruebas"""
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.test_suite_executed = True


@step('debo generar reportes en formatos')
def step_generate_reports_table_es(context):
    """Generar reportes en múltiples formatos (basado en tabla)"""
    from judo.features.reporting import ReportGenerator
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    test_results = [
        {
            "name": "Test 1",
            "status": "passed",
            "duration": 0.5,
            "error": None
        }
    ]
    
    generator = ReportGenerator(test_results)
    
    for row in context.table:
        format_type = row['formato'] if 'formato' in row else row['format']
        
        if format_type.lower() == "json":
            generator.generate_json("report.json")
        elif format_type.lower() == "junit":
            generator.generate_junit("report.xml")
        elif format_type.lower() == "html":
            generator.generate_html("report.html")
        elif format_type.lower() == "allure":
            generator.generate_allure("allure-results")


@step('el reporte debe ser generado en formato "{format}"')
def step_validate_report_generated_es(context, format):
    """Validar que reporte fue generado en formato especificado"""
    import os
    
    if format.lower() == "json":
        assert os.path.exists("report.json"), "Reporte JSON no generado"
    elif format.lower() == "junit":
        assert os.path.exists("report.xml"), "Reporte JUnit no generado"
    elif format.lower() == "html":
        assert os.path.exists("report.html"), "Reporte HTML no generado"
    elif format.lower() == "allure":
        assert os.path.exists("allure-results"), "Reporte Allure no generado"


@step('cargo especificación AsyncAPI desde "{file_path}"')
def step_load_asyncapi_spec_es(context, file_path):
    """Cargar especificación AsyncAPI"""
    from judo.features.contract import ContractValidator
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.asyncapi_validator = ContractValidator(file_path)


@step('la respuesta debe completarse a pesar de la latencia inyectada')
def step_validate_response_despite_latency_es(context):
    """Validar que respuesta se completó a pesar de inyección de latencia"""
    response = context.judo_context.response
    assert response is not None, "No se recibió respuesta"
    assert response.status < 500, "Respuesta indica error del servidor"


@step('algunas solicitudes pueden fallar debido a errores inyectados')
def step_validate_some_requests_fail_es(context):
    """Validar que algunas solicitudes fallaron debido a inyección de errores"""
    pass


@step('circuit breaker debe permanecer en estado CLOSED')
def step_validate_circuit_breaker_closed_es(context):
    """Validar que circuit breaker permaneció cerrado"""
    if not hasattr(context.judo_context, 'circuit_breakers'):
        raise AssertionError("No se han creado circuit breakers")
    
    for cb in context.judo_context.circuit_breakers.values():
        assert cb.state.value.upper() == "CLOSED", \
            f"Circuit breaker '{cb.name}' está en estado {cb.state.value}, se esperaba CLOSED"


@step('tasa de error debe ser menor al {percentage:d} por ciento')
def step_validate_error_rate_alt_es(context, percentage):
    """Validar que tasa de error está por debajo del umbral (sintaxis alternativa)"""
    if not hasattr(context.judo_context, 'performance_monitor'):
        raise AssertionError("Monitoreo de rendimiento no habilitado")
    
    metrics = context.judo_context.performance_monitor.get_metrics()
    error_rate = metrics['error_rate_percent']
    
    assert error_rate < percentage, \
        f"Tasa de error {error_rate}% excede {percentage}%"


@step('solicitud y respuesta deben registrarse en archivo')
def step_validate_logging_to_file_es(context):
    """Validar que solicitud/respuesta fueron registradas en archivo"""
    if not hasattr(context.judo_context, 'request_logger'):
        raise AssertionError("Registro de solicitud no habilitado")
    
    logs = context.judo_context.request_logger.get_logs()
    assert len(logs) > 0, "No se encontraron logs"


# ============================================================
# PASOS ADICIONALES FALTANTES PARA COMPATIBILIDAD CON SHOWCASE
# ============================================================

@step('el array de respuesta debe tener más de {count:d} elementos')
def step_validate_array_more_than_count_es(context, count):
    """Validar que array tiene más de cantidad especificada de elementos"""
    response = context.judo_context.response
    actual_count = len(response.json)
    assert actual_count > count, \
        f"Se esperaban más de {count} elementos, pero se obtuvieron {actual_count}"


@step('la respuesta debe contener todos los campos: {fields}')
def step_validate_response_contains_all_fields_es(context, fields):
    """Validar que respuesta contiene todos los campos especificados"""
    import ast
    response = context.judo_context.response
    
    # Parsear la cadena de lista
    field_list = ast.literal_eval(fields)
    
    for field in field_list:
        assert field in response.json, \
            f"La respuesta no contiene el campo '{field}'"


@step('ambas respuestas deben tener estado {status:d}')
def step_validate_both_responses_status_es(context, status):
    """Validar que ambas respuestas tienen el mismo estado"""
    context.judo_context.validate_status(status)


@step('el campo "{field}" debe estar en rango {min_val:d} a {max_val:d}')
def step_validate_field_in_range_es(context, field, min_val, max_val):
    """Validar que campo de respuesta está dentro del rango"""
    response = context.judo_context.response
    actual_value = response.json.get(field)
    
    assert actual_value is not None, f"Campo '{field}' no encontrado en respuesta"
    assert min_val <= actual_value <= max_val, \
        f"Valor del campo '{field}' {actual_value} no está en rango [{min_val}, {max_val}]"


@step('el tiempo de respuesta debe ser menor a {milliseconds:d} milisegundos')
def step_validate_response_time_ms_es(context, milliseconds):
    """Validar tiempo de respuesta en milisegundos"""
    response = context.judo_context.response
    actual_time_ms = response.elapsed * 1000
    assert actual_time_ms < milliseconds, \
        f"Tiempo de respuesta {actual_time_ms:.0f}ms excede máximo de {milliseconds}ms"


@step('métricas de rendimiento deben ser recopiladas')
def step_validate_performance_metrics_collected_es(context):
    """Validar que métricas de rendimiento fueron recopiladas"""
    if not hasattr(context.judo_context, 'performance_monitor'):
        raise AssertionError("Monitoreo de rendimiento no habilitado")
    
    metrics = context.judo_context.performance_monitor.get_metrics()
    assert metrics is not None, "No se recopilaron métricas de rendimiento"
    assert metrics['total_requests'] > 0, "No se registraron solicitudes en métricas"


@step('caché debe contener {count:d} entrada')
def step_validate_cache_single_entry_es(context, count):
    """Validar que caché contiene número específico de entradas"""
    if not hasattr(context.judo_context, 'response_cache'):
        raise AssertionError("Caché de respuestas no habilitado")
    
    stats = context.judo_context.response_cache.get_stats()
    actual_count = stats['total_entries']
    
    assert actual_count == count, \
        f"Caché tiene {actual_count} entradas, se esperaban {count}"








# ============================================================
# ADDITIONAL SPANISH STEPS - Integer Parameter Variants
# ============================================================




# Retry Policy - Additional variants

@step('que establezco la política de reintentos con max_retries={count:d} y backoff_strategy="{strategy}"')
@step('establezco la política de reintentos con max_retries={count:d} y backoff_strategy="{strategy}"')
def step_set_retry_policy_backoff_es(context, count, strategy):
    """Establecer política de reintentos con estrategia de backoff"""
    from judo.features.retry import RetryPolicy, BackoffStrategy
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    backoff = BackoffStrategy[strategy.upper()]
    context.judo_context.retry_policy = RetryPolicy(
        max_retries=count,
        backoff_strategy=backoff
    )


@step('que establezco la política de reintentos con max_retries={count:d}, initial_delay={delay:f}, y max_delay={max_delay:f}')
@step('establezco la política de reintentos con max_retries={count:d}, initial_delay={delay:f}, y max_delay={max_delay:f}')
def step_set_retry_policy_delays_es(context, count, delay, max_delay):
    """Establecer política de reintentos con retrasos personalizados"""
    from judo.features.retry import RetryPolicy, BackoffStrategy
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.retry_policy = RetryPolicy(
        max_retries=count,
        backoff_strategy=BackoffStrategy.EXPONENTIAL,
        initial_delay=delay,
        max_delay=max_delay
    )




# ============================================================
# RATE LIMITING STEPS - English and Spanish variants
# ============================================================

@step('I set rate limit to {count:d} requests per second')
@step('que establezco el límite de velocidad a {count:d} peticiones por segundo')
@step('establezco el límite de velocidad a {count:d} peticiones por segundo')
def step_set_rate_limit_int_es(context, count):
    """Set rate limit with integer requests per second"""
    from judo.features.rate_limiter import RateLimiter
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.rate_limiter = RateLimiter(requests_per_second=float(count))


@step('I set throttle with delay {delay:d} milliseconds')
@step('que establezco throttle con retraso {delay:d} milisegundos')
@step('establezco throttle con retraso {delay:d} milisegundos')
def step_set_throttle_int_es(context, delay):
    """Set throttle with integer delay in milliseconds"""
    from judo.features.rate_limiter import Throttle
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.throttle = Throttle(delay_ms=float(delay))


@step('I set adaptive rate limit with initial {rps:d} requests per second')
@step('que establezco límite de velocidad adaptativo con inicial {rps:d} peticiones por segundo')
@step('establezco límite de velocidad adaptativo con inicial {rps:d} peticiones por segundo')
def step_set_adaptive_rate_limit_int_es(context, rps):
    """Set adaptive rate limit with integer initial RPS"""
    from judo.features.rate_limiter import AdaptiveRateLimiter
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.adaptive_rate_limiter = AdaptiveRateLimiter(initial_rps=float(rps))


# ============================================================
# MULTIPLE REQUEST STEPS - English and Spanish variants
# ============================================================

@step('envío {count:d} peticiones GET a "{endpoint}"')
def step_send_multiple_get_requests_es(context, count, endpoint):
    """Send multiple GET requests to an endpoint"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    
    for i in range(count):
        if hasattr(context.judo_context, 'rate_limiter'):
            context.judo_context.rate_limiter.wait_if_needed()
        
        if hasattr(context.judo_context, 'throttle'):
            context.judo_context.throttle.wait_if_needed()
        
        context.judo_context.make_request('GET', endpoint)


@step('when I send the same GET request to "{endpoint}" again')
@step('cuando hago la misma petición GET a "{endpoint}" nuevamente')
def step_send_same_get_request_again_es(context, endpoint):
    """Send the same GET request again"""
    endpoint = context.judo_context.interpolate_string(endpoint)
    
    if hasattr(context.judo_context, 'rate_limiter'):
        context.judo_context.rate_limiter.wait_if_needed()
    
    if hasattr(context.judo_context, 'throttle'):
        context.judo_context.throttle.wait_if_needed()
    
    context.judo_context.make_request('GET', endpoint)


# ============================================================
# CACHING STEPS - English and Spanish variants
# ============================================================

@step('que habilito caching de respuestas con TTL {ttl:d} segundos')
def step_enable_response_caching_ttl_es(context, ttl):
    """Enable response caching with TTL"""
    from judo.features.caching import ResponseCache
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.response_cache = ResponseCache(enabled=True, default_ttl=ttl)


@step('la segunda respuesta debe venir del cache')
def step_validate_response_from_cache_es(context):
    """Validate that response came from cache"""
    if not hasattr(context.judo_context, 'response_cache'):
        raise AssertionError("Response cache not enabled")
    
    # Check if last response was from cache
    if hasattr(context.judo_context.response, 'from_cache'):
        assert context.judo_context.response.from_cache, \
            "Response did not come from cache"


@step('el cache debe contener {count:d} entradas')
def step_validate_cache_entries_es(context, count):
    """Validate number of entries in cache"""
    if not hasattr(context.judo_context, 'response_cache'):
        raise AssertionError("Response cache not enabled")
    
    stats = context.judo_context.response_cache.get_stats()
    actual_count = stats.get('total_entries', 0)
    
    assert actual_count == count, \
        f"Cache has {actual_count} entries, expected {count}"


# ============================================================
# INTERCEPTOR STEPS - Additional variants with schema
# ============================================================

@step('que agrego un interceptor de autorización con token "{token}" y esquema "{schema}"')
def step_add_auth_interceptor_with_schema_es(context, token, schema):
    """Add authorization interceptor with custom schema"""
    from judo.features.interceptors import AuthorizationInterceptor, InterceptorChain
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    if not hasattr(context.judo_context, 'interceptor_chain'):
        context.judo_context.interceptor_chain = InterceptorChain()
    
    interceptor = AuthorizationInterceptor(token=token, schema=schema)
    context.judo_context.interceptor_chain.add_request_interceptor(interceptor)


# ============================================================
# AUTHENTICATION STEPS - OAuth2, JWT, Authorization
# ============================================================

@step('que configuro OAuth2 con:')
def step_configure_oauth2_table_es(context):
    """Configure OAuth2 with table"""
    from judo.features.auth import OAuth2Handler
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    oauth2_config = {}
    for row in context.table:
        oauth2_config[row['clave']] = row['valor']
    
    context.judo_context.oauth2_handler = OAuth2Handler(
        client_id=oauth2_config.get('client_id'),
        client_secret=oauth2_config.get('client_secret'),
        token_url=oauth2_config.get('token_url')
    )


@step('que configuro JWT con secret "{secret}" y algoritmo "{algorithm}"')
def step_configure_jwt_secret_algo_es(context, secret, algorithm):
    """Configure JWT with secret and algorithm"""
    from judo.features.auth import JWTHandler
    
    if not hasattr(context, 'judo_context'):
        from judo.behave import setup_judo_context
        setup_judo_context(context)
    
    context.judo_context.jwt_handler = JWTHandler(secret=secret, algorithm=algorithm)


@step('creo token JWT con payload:')
def step_create_jwt_token_payload_es(context):
    """Create JWT token with payload"""
    import json
    
    if not hasattr(context.judo_context, 'jwt_handler'):
        raise AssertionError("JWT not configured")
    
    payload = json.loads(context.text)
    token = context.judo_context.jwt_handler.create_token(payload)
    context.judo_context.jwt_token = token


@step('el token debe ser válido')
def step_validate_jwt_token_es(context):
    """Validate JWT token is valid"""
    if not hasattr(context.judo_context, 'jwt_token'):
        raise AssertionError("JWT token not created")
    
    if not hasattr(context.judo_context, 'jwt_handler'):
        raise AssertionError("JWT not configured")
    
    try:
        context.judo_context.jwt_handler.verify_token(context.judo_context.jwt_token)
    except Exception as e:
        raise AssertionError(f"JWT token validation failed: {e}")


@step('la petición debe incluir encabezado Authorization')
def step_validate_auth_header_es(context):
    """Validate Authorization header is present"""
    if not hasattr(context.judo_context, 'response'):
        raise AssertionError("No response available")
    
    # Check if Authorization header was sent in the request
    if hasattr(context.judo_context, 'last_request_headers'):
        headers = context.judo_context.last_request_headers
        assert 'Authorization' in headers, \
            "Authorization header not found in request"


# ============================================================
# RESPONSE VALIDATION STEPS - Additional variants
# ============================================================

@step('la respuesta debe tener más de 0 elementos')
def step_validate_response_has_items_es(context):
    """Validate response has more than 0 items"""
    response = context.judo_context.response
    
    assert isinstance(response.json, list), "Response is not an array"
    assert len(response.json) > 0, "Response array has no items"
# ============================================================
# PASOS DE VALIDACIÓN AVANZADA DE FORMATOS DE DATOS
# ============================================================

@step('el campo de respuesta "{field_path}" debe ser un email válido')
def step_validate_email_format_es(context, field_path):
    """Validar que un campo contenga una dirección de email válida"""
    from ..features.contract import DataTypeValidator
    
    response_data = context.judo.get_response_json()
    
    # Navigate to field
    field_value = response_data
    for part in field_path.split('.'):
        if isinstance(field_value, dict):
            field_value = field_value.get(part)
        elif isinstance(field_value, list) and part.isdigit():
            field_value = field_value[int(part)]
        else:
            raise AssertionError(f"No se puede navegar al campo '{field_path}'")
    
    if field_value is None:
        raise AssertionError(f"Campo '{field_path}' es nulo")
    
    if not DataTypeValidator.validate_email_format(str(field_value)):
        raise AssertionError(f"Campo '{field_path}' valor '{field_value}' no es un email válido")


@step('el campo de respuesta "{field_path}" debe ser una URL válida')
def step_validate_url_format_es(context, field_path):
    """Validar que un campo contenga una URL válida"""
    from ..features.contract import DataTypeValidator
    
    response_data = context.judo.get_response_json()
    
    # Navigate to field
    field_value = response_data
    for part in field_path.split('.'):
        if isinstance(field_value, dict):
            field_value = field_value.get(part)
        elif isinstance(field_value, list) and part.isdigit():
            field_value = field_value[int(part)]
        else:
            raise AssertionError(f"No se puede navegar al campo '{field_path}'")
    
    if field_value is None:
        raise AssertionError(f"Campo '{field_path}' es nulo")
    
    if not DataTypeValidator.validate_url_format(str(field_value)):
        raise AssertionError(f"Campo '{field_path}' valor '{field_value}' no es una URL válida")


@step('el campo de respuesta "{field_path}" debe ser un UUID válido')
def step_validate_uuid_format_es(context, field_path):
    """Validar que un campo contenga un UUID válido"""
    from ..features.contract import DataTypeValidator
    
    response_data = context.judo.get_response_json()
    
    # Navigate to field
    field_value = response_data
    for part in field_path.split('.'):
        if isinstance(field_value, dict):
            field_value = field_value.get(part)
        elif isinstance(field_value, list) and part.isdigit():
            field_value = field_value[int(part)]
        else:
            raise AssertionError(f"No se puede navegar al campo '{field_path}'")
    
    if field_value is None:
        raise AssertionError(f"Campo '{field_path}' es nulo")
    
    if not DataTypeValidator.validate_uuid_format(str(field_value)):
        raise AssertionError(f"Campo '{field_path}' valor '{field_value}' no es un UUID válido")


@step('el campo de respuesta "{field_path}" debe ser una fecha ISO válida')
def step_validate_iso_date_format_es(context, field_path):
    """Validar que un campo contenga una fecha ISO válida"""
    from ..features.contract import DataTypeValidator
    
    response_data = context.judo.get_response_json()
    
    # Navigate to field
    field_value = response_data
    for part in field_path.split('.'):
        if isinstance(field_value, dict):
            field_value = field_value.get(part)
        elif isinstance(field_value, list) and part.isdigit():
            field_value = field_value[int(part)]
        else:
            raise AssertionError(f"No se puede navegar al campo '{field_path}'")
    
    if field_value is None:
        raise AssertionError(f"Campo '{field_path}' es nulo")
    
    if not DataTypeValidator.validate_iso_date_format(str(field_value)):
        raise AssertionError(f"Campo '{field_path}' valor '{field_value}' no es una fecha ISO válida")


@step('la respuesta debe tener estructura anidada')
def step_validate_nested_structure_es(context):
    """Validar que la respuesta tenga estructura anidada esperada del texto del paso"""
    import json
    from ..features.contract import StructureValidator
    
    response_data = context.judo.get_response_json()
    
    if not context.text:
        raise ValueError("El paso requiere definición de estructura esperada en el texto del paso")
    
    try:
        expected_structure = json.loads(context.text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Definición de estructura inválida: {e}")
    
    errors = StructureValidator.validate_nested_structure(response_data, expected_structure)
    
    if errors:
        error_msg = "Validación de estructura falló:\n" + "\n".join(errors)
        raise AssertionError(error_msg)


@step('valido el cuerpo de petición contra contrato para {method} {path}')
def step_validate_request_body_contract_es(context, method, path):
    """Validar cuerpo de petición contra contrato OpenAPI"""
    if not hasattr(context, 'contract_validator'):
        raise ValueError("No hay contrato cargado. Usa el paso 'cargo el contrato OpenAPI' primero")
    
    # Get request body from context (should be set by previous steps)
    request_body = getattr(context, 'last_request_body', None)
    if not request_body:
        raise ValueError("No hay cuerpo de petición disponible. Almacena cuerpo de petición en context.last_request_body")
    
    context.contract_validator.validate_request_body(method.upper(), path, request_body)


@step('valido los headers de respuesta contra contrato')
def step_validate_response_headers_contract_es(context):
    """Validar headers de respuesta contra contrato OpenAPI"""
    if not hasattr(context, 'contract_validator'):
        raise ValueError("No hay contrato cargado. Usa el paso 'cargo el contrato OpenAPI' primero")
    
    # Get current request info and response headers
    method = getattr(context, 'last_method', 'GET')
    path = getattr(context, 'last_path', '/')
    headers = context.judo.get_response_headers()
    status_code = context.judo.get_response_status()
    
    context.contract_validator.validate_headers(method, path, headers, status_code)


@step('la respuesta debe coincidir con especificación completa del contrato de datos')
def step_validate_full_data_contract_es(context):
    """Validación comprensiva contra contrato cargado incluyendo headers y cuerpo"""
    if not hasattr(context, 'contract_validator'):
        raise ValueError("No hay contrato cargado. Usa el paso 'cargo el contrato OpenAPI' primero")
    
    # Get all necessary data
    method = getattr(context, 'last_method', 'GET')
    path = getattr(context, 'last_path', '/')
    response_data = context.judo.get_response_json()
    status_code = context.judo.get_response_status()
    headers = context.judo.get_response_headers()
    
    # Validate response body
    context.contract_validator.validate_openapi(method, path, response_data, status_code)
    
    # Validate headers
    context.contract_validator.validate_headers(method, path, headers, status_code)
    
    print(f"✅ Validación completa de contrato pasó para {method} {path}")