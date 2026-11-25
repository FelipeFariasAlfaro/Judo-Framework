"""
Pasos gRPC (Español). Usan reflexión del servidor, no se necesitan archivos .proto.
Instala las dependencias opcionales con: pip install "judo-framework[grpc]"
"""
from behave import step

from .steps_grpc import (
    _connect, _set_metadata, _set_timeout, _send, _send_stream, _assert_status, _assert_value,
    _assert_contains, _save, _assert_service, _assert_method, _assert_stream_count,
    _assert_stream_value, _assert_time, _close,
)


@step('me conecto al servidor gRPC "{destino}"')
def step_grpc_connect_es(context, destino):
    """Abre un canal gRPC sin TLS (host:puerto)"""
    _connect(context, destino)


@step('me conecto al servidor gRPC "{destino}" con TLS')
def step_grpc_connect_tls_es(context, destino):
    """Abre un canal gRPC con TLS usando los certificados del sistema"""
    _connect(context, destino, tls=True)


@step('establezco el metadato gRPC "{clave}" a "{valor}"')
def step_grpc_metadata_es(context, clave, valor):
    """Agrega un metadato (header) enviado en cada llamada gRPC"""
    _set_metadata(context, clave, valor)


@step('establezco el timeout gRPC a {segundos:g} segundos')
def step_grpc_timeout_es(context, segundos):
    """Define el plazo máximo de las llamadas gRPC"""
    _set_timeout(context, segundos)


@step('envío la petición gRPC "{metodo}"')
def step_grpc_send_es(context, metodo):
    """Llama a un método unario; la petición (JSON) va en el texto del paso"""
    _send(context, metodo, context.text)


@step('envío la petición gRPC de streaming "{metodo}"')
def step_grpc_send_stream_es(context, metodo):
    """Llama a un método con streaming del servidor; la petición (JSON) va en el texto del paso"""
    _send_stream(context, metodo, context.text)


@step('el estado gRPC debe ser "{estado}"')
def step_grpc_status_es(context, estado):
    """Valida el nombre del código gRPC (OK, NOT_FOUND, UNAUTHENTICATED, ...)"""
    _assert_status(context, estado)


@step('la respuesta gRPC "{ruta}" debe ser "{esperado}"')
def step_grpc_value_es(context, ruta, esperado):
    """Valida un campo de la respuesta gRPC"""
    _assert_value(context, ruta, esperado)


@step('la respuesta gRPC debe contener "{campo}"')
def step_grpc_contains_es(context, campo):
    """Valida que la respuesta gRPC tenga un campo"""
    _assert_contains(context, campo)


@step('guardo la respuesta gRPC "{ruta}" como "{variable}"')
def step_grpc_save_es(context, ruta, variable):
    """Guarda un campo de la respuesta gRPC en una variable"""
    _save(context, ruta, variable)


@step('el servidor gRPC debe exponer el servicio "{servicio}"')
def step_grpc_service_es(context, servicio):
    """Valida (por reflexión) que un servicio esté expuesto"""
    _assert_service(context, servicio)


@step('el servidor gRPC debe exponer el método "{metodo}"')
def step_grpc_method_es(context, metodo):
    """Valida (por reflexión) que un método exista"""
    _assert_method(context, metodo)


@step('el stream gRPC debe devolver {cantidad:d} mensajes')
def step_grpc_stream_count_es(context, cantidad):
    """Valida cuántos mensajes devolvió el stream del servidor"""
    _assert_stream_count(context, cantidad)


@step('el mensaje {indice:d} del stream gRPC "{ruta}" debe ser "{esperado}"')
def step_grpc_stream_value_es(context, indice, ruta, esperado):
    """Valida un campo de un mensaje del stream (índice desde 0)"""
    _assert_stream_value(context, indice, ruta, esperado)


@step('la llamada gRPC debe tardar menos de {ms:d} milisegundos')
def step_grpc_time_es(context, ms):
    """Valida la duración de la última llamada gRPC"""
    _assert_time(context, ms)


@step('cierro la conexión gRPC')
def step_grpc_close_es(context):
    """Cierra el canal gRPC"""
    _close(context)
