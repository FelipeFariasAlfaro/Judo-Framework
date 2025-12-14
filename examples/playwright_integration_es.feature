# Ejemplo de Integración Playwright - Pruebas Híbridas API + UI
# Este ejemplo demuestra cómo combinar pruebas de API con pruebas de UI en el mismo escenario

Característica: Pruebas Híbridas API y UI con Integración Playwright

  Antecedentes:
    Dado que tengo un cliente Judo API
    Y que la URL base es "https://jsonplaceholder.typicode.com"

  @ui @api @hibrido
  Escenario: Crear usuario vía API y verificar en UI
    # Pruebas API - Crear un usuario
    Cuando hago una petición POST a "/users" con JSON:
      """
      {
        "name": "Juan Pérez",
        "username": "juanperez",
        "email": "juan@ejemplo.com",
        "phone": "1-770-736-8031 x56442",
        "website": "juanperez.org"
      }
      """
    Entonces el código de respuesta debe ser 201
    Y la respuesta debe contener "id"
    Y extraigo "$.id" de la respuesta de la API y lo guardo como "userId"
    Y extraigo "$.name" de la respuesta de la API y lo guardo como "userName"
    
    # Pruebas UI - Navegar a un sitio demo y usar los datos de la API
    Dado que inicio un navegador
    Y creo una nueva página
    Cuando navego a "https://httpbin.org/forms/post"
    Y lleno "#custname" con "{userName}"
    Y lleno "#custtel" con "123-456-7890"
    Y lleno "#custemail" con "juan@ejemplo.com"
    Y selecciono "large" de "#size"
    Y marco la casilla "#topping[value='bacon']"
    Y tomo una captura de pantalla llamada "formulario_lleno"
    
    # Capturar datos de UI para uso en API
    Cuando capturo el texto del elemento "#custname" y lo guardo como "uiName"
    Entonces debo tener la variable "uiName" con valor "{userName}"
    
    # Enviar formulario y verificar
    Cuando hago clic en "input[type='submit']"
    Entonces espero que el elemento "pre" sea visible
    Y el elemento "pre" debe contener "juan@ejemplo.com"
    Y tomo una captura de pantalla llamada "formulario_enviado"

  @ui @navegador
  Escenario: Pruebas UI Puras - Validación de Formulario
    Dado que inicio un navegador con cabeza
    Y creo una nueva página
    Cuando navego a "https://httpbin.org/forms/post"
    
    # Probar validación de formulario
    Cuando hago clic en "input[type='submit']"
    Entonces el elemento "#custname:invalid" debe ser visible
    
    # Llenar formulario paso a paso
    Cuando lleno "#custname" con "Usuario Prueba"
    Y lleno "#custtel" con "555-0123"
    Y lleno "#custemail" con "prueba@ejemplo.com"
    Y selecciono "medium" de "#size"
    Y marco la casilla "#topping[value='cheese']"
    Y marco la casilla "#topping[value='onion']"
    
    # Verificar estado del formulario
    Entonces el elemento "#custname" debe tener el atributo "value" con valor "Usuario Prueba"
    Y el elemento "#size" debe tener el atributo "value" con valor "medium"
    
    # Enviar y verificar
    Cuando hago clic en "input[type='submit']"
    Y espero que el elemento "pre" sea visible
    Entonces el elemento "pre" debe contener "Usuario Prueba"
    Y el elemento "pre" debe contener "prueba@ejemplo.com"
    Y el elemento "pre" debe contener "cheese"
    Y el elemento "pre" debe contener "onion"

  @api @ui @multi-pagina
  Escenario: UI Multi-página con sincronización de datos API
    # Obtener datos de usuario desde API
    Cuando hago una petición GET a "/users/1"
    Entonces el código de respuesta debe ser 200
    Y extraigo "$.name" de la respuesta de la API y lo guardo como "apiUserName"
    Y extraigo "$.email" de la respuesta de la API y lo guardo como "apiUserEmail"
    
    # Iniciar navegador con múltiples páginas
    Dado que inicio un navegador
    Y creo una nueva página llamada "pagina_formulario"
    Y creo una nueva página llamada "pagina_resultado"
    
    # Llenar formulario en primera página
    Cuando cambio a la página "pagina_formulario"
    Y navego a "https://httpbin.org/forms/post"
    Y lleno "#custname" con "{apiUserName}"
    Y lleno "#custemail" con "{apiUserEmail}"
    Y lleno "#custtel" con "123-456-7890"
    Y selecciono "large" de "#size"
    Y tomo una captura de pantalla llamada "multi_pagina_formulario"
    
    # Enviar formulario
    Cuando hago clic en "input[type='submit']"
    Y espero que el elemento "pre" sea visible
    
    # Cambiar a página de resultado y verificar
    Cuando cambio a la página "pagina_resultado"
    Y navego a "https://httpbin.org/get"
    Entonces el elemento "pre" debe ser visible
    
    # Tomar capturas de ambas páginas
    Cuando cambio a la página "pagina_formulario"
    Y tomo una captura de pantalla llamada "pagina_formulario_final"
    Y cambio a la página "pagina_resultado"
    Y tomo una captura de pantalla llamada "pagina_resultado_final"

  @ui @javascript
  Escenario: Ejecución de JavaScript y almacenamiento local
    Dado que inicio un navegador
    Y creo una nueva página
    Cuando navego a "https://httpbin.org"
    
    # Establecer almacenamiento local
    Y establezco localStorage "claveTest" a "valorTest"
    Y establezco localStorage "prefUsuario" a "modo_oscuro"
    
    # Verificar almacenamiento local
    Entonces localStorage "claveTest" debe ser "valorTest"
    Y localStorage "prefUsuario" debe ser "modo_oscuro"
    
    # Ejecutar JavaScript
    Cuando ejecuto JavaScript "return document.title"
    Entonces debo tener la variable "js_result" con valor "httpbin.org"
    
    # Ejecutar JavaScript complejo y guardar resultado
    Cuando ejecuto JavaScript y guardo el resultado en "infoPage":
      """
      return {
        title: document.title,
        url: window.location.href,
        userAgent: navigator.userAgent.substring(0, 50),
        timestamp: new Date().toISOString()
      };
      """
    Entonces debo tener la variable "infoPage"
    
    # Limpiar almacenamiento
    Cuando limpio localStorage
    Entonces localStorage "claveTest" debe ser "null"

  @ui @capturas
  Escenario: Pruebas de capturas de pantalla y verificación visual
    Dado que inicio un navegador
    Y creo una nueva página
    Cuando navego a "https://httpbin.org"
    
    # Tomar captura de página completa
    Y tomo una captura de pantalla llamada "httpbin_inicio"
    
    # Navegar y tomar captura de elemento
    Cuando navego a "https://httpbin.org/forms/post"
    Y tomo una captura de pantalla del elemento "form" llamada "formulario_contacto"
    
    # Llenar formulario y tomar otra captura
    Cuando lleno "#custname" con "Prueba Captura"
    Y lleno "#custemail" con "prueba@captura.com"
    Y tomo una captura de pantalla del elemento "form" llamada "formulario_lleno"
    
    # Tomar captura final de página completa
    Y tomo una captura de pantalla llamada "pagina_formulario_completa"

  @ui @espera @tiempo
  Escenario: Esperas avanzadas y temporización
    Dado que inicio un navegador
    Y creo una nueva página
    Cuando navego a "https://httpbin.org/delay/2"
    
    # Esperar carga de página
    Y espero que el elemento "pre" sea visible
    Entonces el elemento "pre" debe contener "origin"
    
    # Navegar a formulario y esperar elementos
    Cuando navego a "https://httpbin.org/forms/post"
    Y espero que el elemento "#custname" sea visible
    Y espero que el elemento "#size" sea visible
    
    # Probar temporización
    Cuando lleno "#custname" con "Prueba Tiempo"
    Y espero 1 segundos
    Y lleno "#custemail" con "tiempo@prueba.com"
    Y espero 2 segundos
    
    # Verificar que los elementos están listos
    Entonces el elemento "#custname" debe estar habilitado
    Y el elemento "#custemail" debe estar habilitado
    Y el elemento "input[type='submit']" debe estar habilitado