"""
Playwright Steps for Judo Framework (Spanish)
Pasos de automatización de navegador que se integran perfectamente con pruebas de API
"""

from behave import step
from . import PLAYWRIGHT_AVAILABLE

if not PLAYWRIGHT_AVAILABLE:
    # Si Playwright no está disponible, crear pasos dummy que muestren errores útiles
    def _playwright_not_available(*args, **kwargs):
        raise ImportError(
            "Playwright no está instalado. Instálalo con:\n"
            "pip install 'judo-framework[browser]' o pip install playwright\n"
            "Luego ejecuta: playwright install"
        )
    
    # Crear pasos dummy
    step = lambda pattern: lambda func: _playwright_not_available

# Pasos de Ciclo de Vida del Navegador
@step('inicio un navegador "{browser_type}"')
def step_start_browser_es(context, browser_type):
    """Iniciar un tipo específico de navegador"""
    if not hasattr(context, 'judo_context') or not hasattr(context.judo_context, 'start_browser'):
        raise RuntimeError("Contexto de navegador no disponible. Usa JudoBrowserContext en environment.py")
    
    context.judo_context.start_browser(browser_type=browser_type.lower())

@step('inicio un navegador')
def step_start_default_browser_es(context):
    """Iniciar navegador por defecto (chromium)"""
    if not hasattr(context, 'judo_context') or not hasattr(context.judo_context, 'start_browser'):
        raise RuntimeError("Contexto de navegador no disponible. Usa JudoBrowserContext en environment.py")
    
    context.judo_context.start_browser()

@step('inicio un navegador sin cabeza')
def step_start_headless_browser_es(context):
    """Iniciar navegador en modo sin cabeza"""
    if not hasattr(context, 'judo_context') or not hasattr(context.judo_context, 'start_browser'):
        raise RuntimeError("Contexto de navegador no disponible. Usa JudoBrowserContext en environment.py")
    
    context.judo_context.start_browser(headless=True)

@step('inicio un navegador con cabeza')
def step_start_headed_browser_es(context):
    """Iniciar navegador en modo con cabeza (visible)"""
    if not hasattr(context, 'judo_context') or not hasattr(context.judo_context, 'start_browser'):
        raise RuntimeError("Contexto de navegador no disponible. Usa JudoBrowserContext en environment.py")
    
    context.judo_context.start_browser(headless=False)

@step('creo una nueva página')
def step_create_new_page_es(context):
    """Crear una nueva página"""
    if not hasattr(context, 'judo_context') or not hasattr(context.judo_context, 'new_page'):
        raise RuntimeError("Contexto de navegador no disponible. Usa JudoBrowserContext en environment.py")
    
    context.judo_context.new_page()

@step('creo una nueva página llamada "{page_name}"')
def step_create_named_page_es(context, page_name):
    """Crear una nueva página con un nombre específico"""
    if not hasattr(context, 'judo_context') or not hasattr(context.judo_context, 'new_page'):
        raise RuntimeError("Contexto de navegador no disponible. Usa JudoBrowserContext en environment.py")
    
    context.judo_context.new_page(name=page_name)

@step('cambio a la página "{page_name}"')
def step_switch_to_page_es(context, page_name):
    """Cambiar a una página nombrada"""
    context.judo_context.switch_to_page(page_name)

@step('cierro la página actual')
def step_close_current_page_es(context):
    """Cerrar la página actual"""
    context.judo_context.close_page()

@step('cierro la página "{page_name}"')
def step_close_named_page_es(context, page_name):
    """Cerrar una página nombrada"""
    context.judo_context.close_page(page_name)

@step('cierro el navegador')
def step_close_browser_es(context):
    """Cerrar el navegador"""
    context.judo_context.close_browser()

# Pasos de Navegación
@step('navego a "{url}"')
def step_navigate_to_url_es(context, url):
    """Navegar a una URL"""
    context.judo_context.navigate_to(url)

@step('voy a "{url}"')
def step_go_to_url_es(context, url):
    """Navegar a una URL (alias)"""
    context.judo_context.navigate_to(url)

@step('recargo la página')
def step_reload_page_es(context):
    """Recargar la página actual"""
    context.judo_context.reload_page()

@step('voy hacia atrás')
def step_go_back_es(context):
    """Ir hacia atrás en el historial del navegador"""
    context.judo_context.go_back()

@step('voy hacia adelante')
def step_go_forward_es(context):
    """Ir hacia adelante en el historial del navegador"""
    context.judo_context.go_forward()

# Pasos de Interacción con Elementos
@step('hago clic en "{selector}"')
def step_click_element_es(context, selector):
    """Hacer clic en un elemento"""
    context.judo_context.click_element(selector)

@step('hago clic en el elemento "{selector}"')
def step_click_element_alt_es(context, selector):
    """Hacer clic en un elemento (frase alternativa)"""
    context.judo_context.click_element(selector)

@step('lleno "{selector}" con "{value}"')
def step_fill_input_es(context, selector, value):
    """Llenar un campo de entrada con un valor"""
    context.judo_context.fill_input(selector, value)

@step('escribo "{text}" en "{selector}"')
def step_type_text_es(context, selector, text):
    """Escribir texto en un elemento"""
    context.judo_context.type_text(selector, text)

@step('selecciono "{value}" de "{selector}"')
def step_select_option_es(context, selector, value):
    """Seleccionar una opción de un elemento select"""
    context.judo_context.select_option(selector, value)

@step('marco la casilla "{selector}"')
def step_check_checkbox_es(context, selector):
    """Marcar una casilla de verificación"""
    context.judo_context.check_checkbox(selector)

@step('desmarco la casilla "{selector}"')
def step_uncheck_checkbox_es(context, selector):
    """Desmarcar una casilla de verificación"""
    context.judo_context.uncheck_checkbox(selector)

# Pasos de Validación de Elementos
@step('el elemento "{selector}" debe ser visible')
def step_element_should_be_visible_es(context, selector):
    """Verificar que un elemento sea visible"""
    assert context.judo_context.is_element_visible(selector), f"El elemento '{selector}' no es visible"

@step('el elemento "{selector}" no debe ser visible')
def step_element_should_not_be_visible_es(context, selector):
    """Verificar que un elemento no sea visible"""
    assert not context.judo_context.is_element_visible(selector), f"El elemento '{selector}' es visible"

@step('el elemento "{selector}" debe estar habilitado')
def step_element_should_be_enabled_es(context, selector):
    """Verificar que un elemento esté habilitado"""
    assert context.judo_context.is_element_enabled(selector), f"El elemento '{selector}' no está habilitado"

@step('el elemento "{selector}" debe estar deshabilitado')
def step_element_should_be_disabled_es(context, selector):
    """Verificar que un elemento esté deshabilitado"""
    assert not context.judo_context.is_element_enabled(selector), f"El elemento '{selector}' está habilitado"

@step('el elemento "{selector}" debe contener "{text}"')
def step_element_should_contain_text_es(context, selector, text):
    """Verificar que un elemento contenga texto específico"""
    actual_text = context.judo_context.get_element_text(selector)
    text = context.judo_context.interpolate_string(text)
    assert text in actual_text, f"El elemento '{selector}' no contiene '{text}'. Texto actual: '{actual_text}'"

@step('el elemento "{selector}" debe tener el texto "{text}"')
def step_element_should_have_exact_text_es(context, selector, text):
    """Verificar que un elemento tenga texto exacto"""
    actual_text = context.judo_context.get_element_text(selector)
    text = context.judo_context.interpolate_string(text)
    assert actual_text == text, f"Texto del elemento '{selector}' no coincide. Esperado: '{text}', Actual: '{actual_text}'"

@step('el elemento "{selector}" debe tener el atributo "{attribute}" con valor "{value}"')
def step_element_should_have_attribute_es(context, selector, attribute, value):
    """Verificar que un elemento tenga un valor de atributo específico"""
    actual_value = context.judo_context.get_element_attribute(selector, attribute)
    value = context.judo_context.interpolate_string(value)
    assert actual_value == value, f"Atributo '{attribute}' del elemento '{selector}' no coincide. Esperado: '{value}', Actual: '{actual_value}'"

# Pasos de Espera
@step('espero que el elemento "{selector}" sea visible')
def step_wait_for_element_visible_es(context, selector):
    """Esperar a que un elemento se vuelva visible"""
    context.judo_context.wait_for_element(selector, state='visible')

@step('espero que el elemento "{selector}" se oculte')
def step_wait_for_element_hidden_es(context, selector):
    """Esperar a que un elemento se oculte"""
    context.judo_context.wait_for_element(selector, state='hidden')

@step('espero que el elemento "{selector}" se adjunte')
def step_wait_for_element_attached_es(context, selector):
    """Esperar a que un elemento se adjunte al DOM"""
    context.judo_context.wait_for_element(selector, state='attached')

@step('espero que el elemento "{selector}" se desadjunte')
def step_wait_for_element_detached_es(context, selector):
    """Esperar a que un elemento se desadjunte del DOM"""
    context.judo_context.wait_for_element(selector, state='detached')

@step('espero que la URL contenga "{url_pattern}"')
def step_wait_for_url_pattern_es(context, url_pattern):
    """Esperar a que la URL coincida con un patrón"""
    context.judo_context.wait_for_url(f"**{url_pattern}**")

@step('espero que la URL sea "{url}"')
def step_wait_for_exact_url_es(context, url):
    """Esperar una URL exacta"""
    context.judo_context.wait_for_url(url)

@step('espero {seconds:d} segundos')
def step_wait_seconds_es(context, seconds):
    """Esperar un número específico de segundos"""
    context.judo_context.wait(seconds)

# Pasos de Capturas de Pantalla
@step('tomo una captura de pantalla')
def step_take_screenshot_es(context):
    """Tomar una captura de pantalla de la página actual"""
    context.judo_context.take_screenshot()

@step('tomo una captura de pantalla llamada "{name}"')
def step_take_named_screenshot_es(context, name):
    """Tomar una captura de pantalla con un nombre específico"""
    context.judo_context.take_screenshot(name)

@step('tomo una captura de pantalla del elemento "{selector}"')
def step_take_element_screenshot_es(context, selector):
    """Tomar una captura de pantalla de un elemento específico"""
    context.judo_context.take_element_screenshot(selector)

@step('tomo una captura de pantalla del elemento "{selector}" llamada "{name}"')
def step_take_named_element_screenshot_es(context, selector, name):
    """Tomar una captura de pantalla de un elemento específico con un nombre"""
    context.judo_context.take_element_screenshot(selector, name)

# Pasos de JavaScript
@step('ejecuto JavaScript')
def step_execute_javascript_es(context):
    """Ejecutar código JavaScript del texto del paso"""
    script = context.text
    result = context.judo_context.execute_javascript(script)
    context.judo_context.set_variable('js_result', result)

@step('ejecuto JavaScript "{script}"')
def step_execute_javascript_inline_es(context, script):
    """Ejecutar código JavaScript en línea"""
    result = context.judo_context.execute_javascript(script)
    context.judo_context.set_variable('js_result', result)

@step('ejecuto JavaScript y guardo el resultado en "{variable_name}"')
def step_execute_javascript_store_result_es(context, variable_name):
    """Ejecutar JavaScript y guardar el resultado en una variable"""
    script = context.text
    result = context.judo_context.execute_javascript(script)
    context.judo_context.set_variable(variable_name, result)

# Pasos de Cookies
@step('limpio todas las cookies')
def step_clear_cookies_es(context):
    """Limpiar todas las cookies"""
    context.judo_context.clear_cookies()

@step('agrego una cookie con nombre "{name}" y valor "{value}"')
def step_add_cookie_es(context, name, value):
    """Agregar una cookie"""
    name = context.judo_context.interpolate_string(name)
    value = context.judo_context.interpolate_string(value)
    
    cookie = {
        'name': name,
        'value': value,
        'url': context.judo_context.page.url if context.judo_context.page else 'http://localhost'
    }
    context.judo_context.add_cookie(cookie)

# Pasos de Local Storage
@step('establezco localStorage "{key}" a "{value}"')
def step_set_local_storage_es(context, key, value):
    """Establecer un elemento de localStorage"""
    context.judo_context.set_local_storage(key, value)

@step('limpio localStorage')
def step_clear_local_storage_es(context):
    """Limpiar localStorage"""
    context.judo_context.clear_local_storage()

@step('localStorage "{key}" debe ser "{value}"')
def step_local_storage_should_be_es(context, key, value):
    """Verificar valor de localStorage"""
    actual_value = context.judo_context.get_local_storage(key)
    value = context.judo_context.interpolate_string(value)
    assert actual_value == value, f"localStorage[{key}] no coincide. Esperado: '{value}', Actual: '{actual_value}'"

# Pasos de Extracción de Variables (API + UI Híbrido)
@step('extraigo "{json_path}" de la respuesta de la API y lo guardo como "{variable_name}"')
def step_extract_api_data_for_ui_es(context, json_path, variable_name):
    """Extraer datos de la respuesta de la API para usar en pruebas de UI"""
    context.judo_context.extract_api_data_to_ui(json_path, variable_name)

@step('capturo el texto del elemento "{selector}" y lo guardo como "{variable_name}"')
def step_capture_ui_text_for_api_es(context, selector, variable_name):
    """Capturar texto del elemento UI para usar en pruebas de API"""
    context.judo_context.capture_ui_data_for_api(selector, variable_name)

@step('capturo el atributo "{attribute}" del elemento "{selector}" y lo guardo como "{variable_name}"')
def step_capture_ui_attribute_for_api_es(context, selector, attribute, variable_name):
    """Capturar atributo del elemento UI para usar en pruebas de API"""
    context.judo_context.capture_ui_data_for_api(selector, variable_name, attribute)

# Pasos de Formularios
@step('envío el formulario "{selector}"')
def step_submit_form_es(context, selector):
    """Enviar un formulario"""
    # Usar JavaScript para enviar el formulario
    selector = context.judo_context.interpolate_string(selector)
    script = f"document.querySelector('{selector}').submit()"
    context.judo_context.execute_javascript(script)

@step('lleno el formulario')
def step_fill_form_from_table_es(context):
    """Llenar campos de formulario desde una tabla de datos"""
    if not context.table:
        raise ValueError("Este paso requiere una tabla de datos con columnas campo y valor")
    
    for row in context.table:
        field = row['campo']
        value = row['valor']
        context.judo_context.fill_input(field, value)

# Pasos de Interacción Avanzada
@step('paso el cursor sobre "{selector}"')
def step_hover_element_es(context, selector):
    """Pasar el cursor sobre un elemento"""
    if not context.judo_context.page:
        raise RuntimeError("No hay página disponible. Crea una página primero.")
    
    selector = context.judo_context.interpolate_string(selector)
    context.judo_context.page.hover(selector)
    context.judo_context.log(f"Pasé el cursor sobre el elemento: {selector}")

@step('hago doble clic en "{selector}"')
def step_double_click_element_es(context, selector):
    """Hacer doble clic en un elemento"""
    if not context.judo_context.page:
        raise RuntimeError("No hay página disponible. Crea una página primero.")
    
    selector = context.judo_context.interpolate_string(selector)
    context.judo_context.page.dblclick(selector)
    context.judo_context.log(f"Hice doble clic en el elemento: {selector}")

@step('hago clic derecho en "{selector}"')
def step_right_click_element_es(context, selector):
    """Hacer clic derecho en un elemento"""
    if not context.judo_context.page:
        raise RuntimeError("No hay página disponible. Crea una página primero.")
    
    selector = context.judo_context.interpolate_string(selector)
    context.judo_context.page.click(selector, button='right')
    context.judo_context.log(f"Hice clic derecho en el elemento: {selector}")

@step('arrastro "{source_selector}" a "{target_selector}"')
def step_drag_and_drop_es(context, source_selector, target_selector):
    """Arrastrar y soltar desde origen a destino"""
    if not context.judo_context.page:
        raise RuntimeError("No hay página disponible. Crea una página primero.")
    
    source_selector = context.judo_context.interpolate_string(source_selector)
    target_selector = context.judo_context.interpolate_string(target_selector)
    
    source = context.judo_context.page.locator(source_selector)
    target = context.judo_context.page.locator(target_selector)
    
    source.drag_to(target)
    context.judo_context.log(f"Arrastré {source_selector} a {target_selector}")

# Pasos de Subida de Archivos
@step('subo el archivo "{file_path}" a "{selector}"')
def step_upload_file_es(context, file_path, selector):
    """Subir un archivo a un input de archivo"""
    if not context.judo_context.page:
        raise RuntimeError("No hay página disponible. Crea una página primero.")
    
    file_path = context.judo_context.interpolate_string(file_path)
    selector = context.judo_context.interpolate_string(selector)
    
    context.judo_context.page.set_input_files(selector, file_path)
    context.judo_context.log(f"Subí el archivo {file_path} a {selector}")

# Pasos de Alertas/Diálogos
@step('acepto la alerta')
def step_accept_alert_es(context):
    """Aceptar un diálogo de alerta"""
    if not context.judo_context.page:
        raise RuntimeError("No hay página disponible. Crea una página primero.")
    
    # Configurar manejador de diálogo para aceptar
    context.judo_context.page.on("dialog", lambda dialog: dialog.accept())
    context.judo_context.log("Configuré la aceptación de alerta")

@step('rechazo la alerta')
def step_dismiss_alert_es(context):
    """Rechazar un diálogo de alerta"""
    if not context.judo_context.page:
        raise RuntimeError("No hay página disponible. Crea una página primero.")
    
    # Configurar manejador de diálogo para rechazar
    context.judo_context.page.on("dialog", lambda dialog: dialog.dismiss())
    context.judo_context.log("Configuré el rechazo de alerta")

@step('acepto la alerta con texto "{text}"')
def step_accept_alert_with_text_es(context, text):
    """Aceptar un diálogo de alerta e ingresar texto (para diálogos de prompt)"""
    if not context.judo_context.page:
        raise RuntimeError("No hay página disponible. Crea una página primero.")
    
    text = context.judo_context.interpolate_string(text)
    
    # Configurar manejador de diálogo para aceptar con texto
    context.judo_context.page.on("dialog", lambda dialog: dialog.accept(text))
    context.judo_context.log(f"Configuré la aceptación de alerta con texto: {text}")

# Pasos de Gestión de Ventanas/Pestañas
@step('cambio a la nueva pestaña')
def step_switch_to_new_tab_es(context):
    """Cambiar a la pestaña/ventana más nueva"""
    if not context.judo_context.browser_context:
        raise RuntimeError("No hay contexto de navegador disponible.")
    
    pages = context.judo_context.browser_context.pages
    if len(pages) > 1:
        # Cambiar a la última (más nueva) página
        newest_page = pages[-1]
        context.judo_context.page = newest_page
        context.judo_context.log("Cambié a la nueva pestaña")
    else:
        raise RuntimeError("No hay nueva pestaña disponible")

@step('cierro la pestaña actual')
def step_close_current_tab_es(context):
    """Cerrar la pestaña actual"""
    if not context.judo_context.page:
        raise RuntimeError("No hay página disponible.")
    
    context.judo_context.page.close()
    
    # Cambiar a otra página disponible si existe
    if context.judo_context.browser_context:
        pages = context.judo_context.browser_context.pages
        if pages:
            context.judo_context.page = pages[0]
        else:
            context.judo_context.page = None
    
    context.judo_context.log("Cerré la pestaña actual")