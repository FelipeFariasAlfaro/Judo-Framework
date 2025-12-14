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


@step('que establezco la variable "{nombre}" al JSON')
def step_set_variable_json_es(context, nombre):
    """Establecer una variable con datos JSON del texto del paso"""
    import json
    json_data = json.loads(context.text)
    context.judo_context.set_variable(nombre, json_data)


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


@step('que establezco el header "{nombre_header}" desde env "{nombre_var_env}"')
@step('que agrego el header "{nombre_header}" desde env "{nombre_var_env}"')
def step_set_header_from_env_es(context, nombre_header, nombre_var_env):
    """Establecer un header desde variable de entorno (archivo .env)"""
    context.judo_context.set_header_from_env(nombre_header, nombre_var_env)


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
    from dotenv import load_dotenv
    
    # Cargar variables de entorno desde archivo .env si existe
    load_dotenv()
    
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