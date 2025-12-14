# Pruebas en español para validar la integración bilingüe

Característica: Pruebas en Español con Integración Playwright

  Antecedentes:
    Dado que tengo un cliente Judo API
    Y que la URL base es "https://httpbin.org"

  @api @español
  Escenario: Prueba básica de API en español
    Cuando hago una petición GET a "/get"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener "url"
    Y la respuesta debe contener "headers"

  @ui @español
  Escenario: Prueba básica de UI en español
    Dado que inicio un navegador
    Y creo una nueva página
    Cuando navego a "https://httpbin.org/forms/post"
    
    # Llenar formulario
    Y lleno "#custname" con "Usuario Prueba"
    Y lleno "#custemail" con "prueba@ejemplo.com"
    Y lleno "#custtel" con "555-0123"
    Y selecciono "medium" de "#size"
    Y marco la casilla "#topping[value='cheese']"
    
    # Verificar estado del formulario
    Entonces el elemento "#custname" debe tener el atributo "value" con valor "Usuario Prueba"
    Y el elemento "#custemail" debe tener el atributo "value" con valor "prueba@ejemplo.com"
    
    # Tomar captura de pantalla
    Y tomo una captura de pantalla llamada "formulario_español"
    
    # Enviar formulario
    Cuando hago clic en "input[type='submit']"
    Y espero que el elemento "pre" sea visible
    Entonces el elemento "pre" debe contener "Usuario Prueba"
    Y el elemento "pre" debe contener "prueba@ejemplo.com"
    
    Y cierro el navegador

  @hybrid @español
  Escenario: Prueba híbrida API + UI en español
    # Obtener datos de API
    Cuando hago una petición GET a "/json"
    Entonces el código de respuesta debe ser 200
    Y la respuesta debe contener "slideshow"
    Y extraigo "$.slideshow.author" de la respuesta de la API y lo guardo como "autorNombre"
    Y extraigo "$.slideshow.title" de la respuesta de la API y lo guardo como "tituloSlide"
    
    # Usar datos de API en UI
    Dado que inicio un navegador
    Y creo una nueva página
    Cuando navego a "https://httpbin.org/forms/post"
    Y lleno "#custname" con "{autorNombre}"
    Y lleno "#custemail" con "autor@presentacion.com"
    Y lleno "#custtel" con "555-AUTOR"
    Y selecciono "large" de "#size"
    
    # Verificar que los datos se llenaron correctamente
    Entonces el elemento "#custname" debe tener el atributo "value" con valor "{autorNombre}"
    
    # Capturar datos de UI para usar en API
    Cuando capturo el texto del elemento "#custname" y lo guardo como "nombreUI"
    Y capturo el texto del elemento "#custemail" y lo guardo como "emailUI"
    
    # Usar datos capturados de UI en llamada API
    Cuando hago una petición POST a "/post" con JSON:
      """
      {
        "nombre": "{nombreUI}",
        "email": "{emailUI}",
        "origen": "captura_ui_español",
        "titulo_original": "{tituloSlide}"
      }
      """
    Entonces el código de respuesta debe ser 200
    Y la respuesta "$.json.nombre" debe ser "{nombreUI}"
    Y la respuesta "$.json.email" debe ser "{emailUI}"
    Y la respuesta "$.json.origen" debe ser "captura_ui_español"
    
    # Tomar captura final
    Y tomo una captura de pantalla llamada "hibrido_español_final"
    
    Y cierro el navegador

  @ui @javascript @español
  Escenario: Ejecución de JavaScript en español
    Dado que inicio un navegador
    Y creo una nueva página
    Cuando navego a "https://httpbin.org"
    
    # Establecer almacenamiento local
    Y establezco localStorage "idioma" a "español"
    Y establezco localStorage "usuario" a "prueba_js"
    
    # Verificar almacenamiento local
    Entonces localStorage "idioma" debe ser "español"
    Y localStorage "usuario" debe ser "prueba_js"
    
    # Ejecutar JavaScript
    Cuando ejecuto JavaScript "return document.title"
    Entonces debo tener la variable "js_result" con valor "httpbin.org"
    
    # Ejecutar JavaScript complejo y guardar resultado
    Cuando ejecuto JavaScript y guardo el resultado en "infoPageEspañol":
      """
      return {
        titulo: document.title,
        url: window.location.href,
        idioma: localStorage.getItem('idioma'),
        usuario: localStorage.getItem('usuario'),
        timestamp: new Date().toISOString()
      };
      """
    Entonces debo tener la variable "infoPageEspañol"
    
    # Limpiar almacenamiento
    Cuando limpio localStorage
    Entonces localStorage "idioma" debe ser "null"
    
    Y cierro el navegador

  @ui @multi-pagina @español
  Escenario: Gestión de múltiples páginas en español
    Dado que inicio un navegador
    Y creo una nueva página llamada "pagina_principal"
    Y creo una nueva página llamada "pagina_formulario"
    
    # Usar página principal
    Cuando cambio a la página "pagina_principal"
    Y navego a "https://httpbin.org"
    Entonces el elemento "h1" debe contener "httpbin"
    
    # Usar página de formulario
    Cuando cambio a la página "pagina_formulario"
    Y navego a "https://httpbin.org/forms/post"
    Entonces el elemento "form" debe ser visible
    
    # Llenar formulario en página de formulario
    Cuando lleno "#custname" con "Prueba Multi Página"
    Y lleno "#custemail" con "multipagina@prueba.com"
    
    # Cambiar de vuelta a página principal
    Cuando cambio a la página "pagina_principal"
    Entonces el elemento "h1" debe contener "httpbin"
    
    # Volver a página de formulario y verificar que los datos siguen ahí
    Cuando cambio a la página "pagina_formulario"
    Entonces el elemento "#custname" debe tener el atributo "value" con valor "Prueba Multi Página"
    
    # Tomar capturas de ambas páginas
    Cuando tomo una captura de pantalla llamada "pagina_formulario_español"
    Y cambio a la página "pagina_principal"
    Y tomo una captura de pantalla llamada "pagina_principal_español"
    
    Y cierro el navegador

  @ui @esperas @español
  Escenario: Esperas avanzadas y temporización en español
    Dado que inicio un navegador
    Y creo una nueva página
    Cuando navego a "https://httpbin.org/delay/1"
    
    # Esperar respuesta con retraso
    Y espero que el elemento "pre" sea visible
    Entonces el elemento "pre" debe contener "origin"
    
    # Navegar a formulario y esperar elementos
    Cuando navego a "https://httpbin.org/forms/post"
    Y espero que el elemento "#custname" sea visible
    Y espero que el elemento "#size" sea visible
    
    # Probar temporización con esperas
    Cuando lleno "#custname" con "Prueba Tiempo"
    Y espero 1 segundos
    Y lleno "#custemail" con "tiempo@prueba.com"
    Y espero 2 segundos
    
    # Verificar que los elementos están listos
    Entonces el elemento "#custname" debe estar habilitado
    Y el elemento "#custemail" debe estar habilitado
    Y el elemento "input[type='submit']" debe estar habilitado
    
    Y cierro el navegador