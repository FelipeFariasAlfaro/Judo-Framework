"""
Pasos condicionales y de control de flujo (Español).

El bloque de pasos va en un docstring y se ejecuta con ``context.execute_steps``::

    Cuando hago una petición GET a "/users/1"
    Y si el estado de la respuesta es 404 entonces ejecuto
      \"\"\"
      Cuando hago una petición POST a "/users" con el cuerpo
        '''
        {"name": "Ana"}
        '''
      \"\"\"
    Y en caso contrario ejecuto
      \"\"\"
      Entonces la respuesta "$.active" debe ser "True"
      \"\"\"

Dentro de un bloque usa ``'''`` para un docstring anidado. Reutiliza la lógica de ``steps_flow``.
"""
from behave import step

from .steps_flow import (
    _if, _otherwise, _status_is, _json_equals, _json_exists, _json_contains, _json_number,
    _var_equals, _var_defined, _var_empty, _env_is, _envvar_set, _has_tag, _file_exists,
    _header_exists, _body_contains, _time_over, _skip, _fail, _assert_defined, _assert_empty,
    _assert_env, _repeat, _repeat_until, _for_each, _retry, _soft,
)


@step('si el estado de la respuesta es {estado:d} entonces ejecuto')
def step_if_status_es(context, estado):
    """Ejecuta el bloque cuando el estado de la respuesta coincide"""
    _if(context, _status_is(context, estado), context.text)


@step('si el estado de la respuesta no es {estado:d} entonces ejecuto')
def step_if_status_not_es(context, estado):
    """Ejecuta el bloque cuando el estado de la respuesta es distinto"""
    _if(context, not _status_is(context, estado), context.text)


@step('si la respuesta "{ruta}" es igual a "{esperado}" entonces ejecuto')
def step_if_json_equals_es(context, ruta, esperado):
    """Ejecuta el bloque cuando un JSONPath es igual a un valor"""
    _if(context, _json_equals(context, ruta, esperado), context.text)


@step('si la respuesta "{ruta}" existe entonces ejecuto')
def step_if_json_exists_es(context, ruta):
    """Ejecuta el bloque cuando un JSONPath existe"""
    _if(context, _json_exists(context, ruta), context.text)


@step('si la respuesta "{ruta}" no existe entonces ejecuto')
def step_if_json_missing_es(context, ruta):
    """Ejecuta el bloque cuando un JSONPath no existe"""
    _if(context, not _json_exists(context, ruta), context.text)


@step('si la respuesta "{ruta}" contiene "{texto}" entonces ejecuto')
def step_if_json_contains_es(context, ruta, texto):
    """Ejecuta el bloque cuando un valor JSON (o elemento de array) contiene el texto"""
    _if(context, _json_contains(context, ruta, texto), context.text)


@step('si la respuesta "{ruta}" es mayor que {numero:g} entonces ejecuto')
def step_if_json_gt_es(context, ruta, numero):
    """Ejecuta el bloque cuando un valor numérico JSON es mayor que un número"""
    _if(context, _json_number(context, ruta, numero, True), context.text)


@step('si la respuesta "{ruta}" es menor que {numero:g} entonces ejecuto')
def step_if_json_lt_es(context, ruta, numero):
    """Ejecuta el bloque cuando un valor numérico JSON es menor que un número"""
    _if(context, _json_number(context, ruta, numero, False), context.text)


@step('si la variable "{nombre}" es igual a "{esperado}" entonces ejecuto')
def step_if_var_equals_es(context, nombre, esperado):
    """Ejecuta el bloque cuando una variable es igual a un valor"""
    _if(context, _var_equals(context, nombre, esperado), context.text)


@step('si la variable "{nombre}" está definida entonces ejecuto')
def step_if_var_defined_es(context, nombre):
    """Ejecuta el bloque cuando una variable está definida"""
    _if(context, _var_defined(context, nombre), context.text)


@step('si la variable "{nombre}" no está definida entonces ejecuto')
def step_if_var_undefined_es(context, nombre):
    """Ejecuta el bloque cuando una variable no está definida"""
    _if(context, not _var_defined(context, nombre), context.text)


@step('si la variable "{nombre}" está vacía entonces ejecuto')
def step_if_var_empty_es(context, nombre):
    """Ejecuta el bloque cuando una variable no existe o está vacía"""
    _if(context, _var_empty(context, nombre), context.text)


@step('si el entorno es "{entorno}" entonces ejecuto')
def step_if_env_es(context, entorno):
    """Ejecuta el bloque cuando JUDO_ENV / KARATE_ENV coincide"""
    _if(context, _env_is(entorno), context.text)


@step('si la variable de entorno "{nombre}" está definida entonces ejecuto')
def step_if_envvar_es(context, nombre):
    """Ejecuta el bloque cuando una variable de entorno del sistema está definida"""
    _if(context, _envvar_set(nombre), context.text)


@step('si el escenario tiene el tag "{tag}" entonces ejecuto')
def step_if_tag_es(context, tag):
    """Ejecuta el bloque cuando el escenario tiene un tag"""
    _if(context, _has_tag(context, tag), context.text)


@step('si el archivo "{ruta}" existe entonces ejecuto')
def step_if_file_es(context, ruta):
    """Ejecuta el bloque cuando un archivo existe"""
    _if(context, _file_exists(context, ruta), context.text)


@step('si el header de respuesta "{nombre}" existe entonces ejecuto')
def step_if_header_es(context, nombre):
    """Ejecuta el bloque cuando un header de respuesta está presente"""
    _if(context, _header_exists(context, nombre), context.text)


@step('si el cuerpo de la respuesta contiene "{texto}" entonces ejecuto')
def step_if_body_es(context, texto):
    """Ejecuta el bloque cuando el cuerpo crudo de la respuesta contiene el texto"""
    _if(context, _body_contains(context, texto), context.text)


@step('si el tiempo de respuesta es mayor a {ms:d} milisegundos entonces ejecuto')
def step_if_slow_es(context, ms):
    """Ejecuta el bloque cuando la respuesta fue más lenta que el límite"""
    _if(context, _time_over(context, ms), context.text)


@step('en caso contrario ejecuto')
def step_otherwise_es(context):
    """Ejecuta el bloque cuando el 'si' anterior fue falso"""
    _otherwise(context, context.text)


@step('salto el escenario si la variable "{nombre}" es igual a "{esperado}"')
def step_skip_var_es(context, nombre, esperado):
    """Salta el resto del escenario cuando una variable es igual a un valor"""
    if _var_equals(context, nombre, esperado):
        _skip(context, f'variable "{nombre}" es igual a "{esperado}"')


@step('salto el escenario si el entorno es "{entorno}"')
def step_skip_env_es(context, entorno):
    """Salta el resto del escenario en un entorno determinado"""
    if _env_is(entorno):
        _skip(context, f'el entorno es "{entorno}"')


@step('salto el escenario si el estado de la respuesta es {estado:d}')
def step_skip_status_es(context, estado):
    """Salta el resto del escenario cuando el estado de la respuesta coincide"""
    if _status_is(context, estado):
        _skip(context, f"el estado de la respuesta es {estado}")


@step('fallo la prueba con el mensaje "{mensaje}"')
def step_fail_es(context, mensaje):
    """Falla el escenario con un mensaje personalizado"""
    _fail(context, mensaje)


@step('la variable "{nombre}" debe estar definida')
def step_var_defined_es(context, nombre):
    """Valida que una variable esté definida"""
    _assert_defined(context, nombre, True)


@step('la variable "{nombre}" no debe estar definida')
def step_var_not_defined_es(context, nombre):
    """Valida que una variable no esté definida"""
    _assert_defined(context, nombre, False)


@step('la variable "{nombre}" debe estar vacía')
def step_var_empty_es(context, nombre):
    """Valida que una variable no exista o esté vacía"""
    _assert_empty(context, nombre)


@step('el entorno debe ser "{entorno}"')
def step_env_should_es(context, entorno):
    """Valida el nombre del entorno actual"""
    _assert_env(entorno)


@step('repito {n:d} veces')
def step_repeat_es(context, n):
    """Ejecuta el bloque N veces (variable ${iteration} = 1..N)"""
    _repeat(context, n, context.text)


@step('repito hasta que la respuesta "{ruta}" sea igual a "{esperado}" hasta {n:d} veces')
def step_repeat_until_es(context, ruta, esperado, n):
    """Ejecuta el bloque hasta que un JSONPath sea igual a un valor, como máximo N veces"""
    _repeat_until(context, ruta, esperado, n, context.text)


@step('para cada elemento en la respuesta "{ruta}" ejecuto')
def step_for_each_es(context, ruta):
    """Ejecuta el bloque por cada elemento de un array (variables ${item} y ${index})"""
    _for_each(context, ruta, context.text)


@step('reintento los siguientes pasos hasta {n:d} veces con {segundos:g} segundos de espera')
def step_retry_es(context, n, segundos):
    """Reintenta el bloque mientras falle"""
    _retry(context, n, segundos, context.text)


@step('verifico todo lo siguiente')
def step_soft_es(context):
    """Ejecuta cada línea del bloque como un paso y reporta todos los fallos al final"""
    _soft(context, context.text)
