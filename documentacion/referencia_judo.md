# Referencia Judo Framework

1. Tema: Requisitos del sistema para instalar Judo Framework
Descripcion: Se requiere Python 3.8 o superior (recomendado 3.9+), pip como gestor de paquetes, y es compatible con Windows, Linux y macOS.

2. Tema: Instalación básica de Judo Framework
Descripcion: Se instala desde PyPI con el comando `pip install judo-framework`. Para verificar la instalación ejecutar: `python -c "import judo; print('Judo Framework instalado correctamente')"`.

3. Tema: Instalaciones opcionales con extras
Descripcion: Se pueden instalar funcionalidades específicas usando extras: `pip install judo-framework[excel]` para Excel, `[websocket]` para WebSocket, `[graphql]` para GraphQL, `[crypto]` para criptografía, `[xml]` para XML, o `[full]` para todas las funcionalidades. En algunos shells es necesario usar comillas: `pip install "judo-framework[full]"`.

4. Tema: Estructura de proyecto recomendada
Descripcion: La estructura recomendada incluye: archivo `.env` en la raíz, carpeta `features/` para archivos .feature, carpeta `steps/` para pasos personalizados (opcional), carpeta `test_data/` para datos de prueba, carpeta `judo_reports/` para reportes generados, archivo `runner.py` como runner principal, y `report_config.json` para configuración de reportes.

5. Tema: Configuración de variables de entorno (.env)
Descripcion: El archivo `.env` se coloca en la raíz del proyecto. Judo busca automáticamente en el directorio actual, directorio padre y raíz del proyecto. Las variables principales son: `JUDO_FEATURES_DIR` (directorio de features), `JUDO_OUTPUT_DIR` (directorio de salida), `JUDO_PARALLEL` (ejecución paralela), `JUDO_MAX_WORKERS` (workers paralelos), `JUDO_CONSOLE_FORMAT` (formato de consola), `JUDO_GENERATE_CUCUMBER_JSON` (generar JSON Cucumber), `JUDO_SAVE_REQUESTS_RESPONSES` (guardar requests/responses), `JUDO_TIMEOUT` (timeout en segundos), `JUDO_RETRY_COUNT` (reintentos), `JUDO_FAIL_FAST` (fallar rápido), `JUDO_VERBOSE` (modo verbose). Si no se encuentra .env, se usan valores por defecto.

6. Tema: Configuración de múltiples ambientes (dev, staging, prod)
Descripcion: Se pueden usar diferentes archivos .env por ambiente: `.env.dev`, `.env.staging`, `.env.prod`. Se carga el apropiado con `load_dotenv('.env.dev')`. También se puede usar la variable `TEST_ENV` para seleccionar el ambiente: `TEST_ENV=staging python runner.py`.

7. Tema: Creación de un runner básico
Descripcion: Se crea un archivo `runner.py` que hereda de `BaseRunner`. Ejemplo: importar `from judo.runner.base_runner import BaseRunner`, crear una clase que herede de `BaseRunner`, llamar a `super().__init__()` en el constructor, y usar `self.run_all_features()` para ejecutar todas las pruebas. El runner retorna `True` si todas las pruebas pasan.

8. Tema: Creación de un runner avanzado con configuración personalizada
Descripcion: El runner avanzado permite pasar parámetros al constructor de `BaseRunner`: `features_dir`, `output_dir`, `parallel`, `max_workers`, `console_format`. Se pueden configurar variables globales con `self.set_global_variable("BASE_URL", "https://api.ejemplo.com")` y ejecutar features específicos con `self.run_specific_features(["feature1.feature", "feature2.feature"])`.

9. Tema: Estructura básica de un archivo .feature
Descripcion: Un archivo .feature sigue la sintaxis BDD de Behave. Incluye: `Feature:` con descripción, `Background:` para configuración común a todos los scenarios, y `Scenario:` para cada caso de prueba. Los pasos usan keywords como Given, When, Then, And. Ejemplo: `Given I set base URL to "https://api.ejemplo.com"`, `When I send GET request to "/users"`, `Then the response status should be 200`.

10. Tema: Organización de archivos .feature
Descripcion: Se recomienda organizar features por funcionalidad en subcarpetas: `features/authentication/`, `features/users/`, `features/products/`, etc. Cada subcarpeta contiene los .feature relacionados con esa funcionalidad.

11. Tema: Escritura de pruebas en español
Descripcion: Judo Framework soporta completamente español con 166+ pasos predefinidos. Se usan las keywords de Behave en español: `Dado que`, `Cuando`, `Entonces`. Ejemplo: `Dado que configuro la URL base como "https://api.ejemplo.com"`. Se requiere importar `from judo.behave.steps_es import *` en environment.py.

12. Tema: Modo mixto inglés/español en pruebas
Descripcion: Se pueden mezclar keywords en inglés (Feature, Scenario) con pasos en español, o viceversa. Judo Framework soporta modo mixto para equipos bilingües.

13. Tema: Creación de pasos personalizados
Descripcion: Se crea un archivo `steps/custom_steps.py` usando el decorador `@step` de behave. Ejemplo: `from behave import step` y luego `@step('mi paso personalizado con "{valor}"')` seguido de la función que implementa la lógica del paso.

14. Tema: Uso de datos de prueba externos
Descripcion: Judo Framework soporta múltiples fuentes de datos: archivos JSON, archivos CSV, archivos Excel (con extra [excel]), variables de entorno, y datos generados con Faker. Se pueden usar para data-driven testing.

15. Tema: Configuración del archivo environment.py
Descripcion: El archivo `features/environment.py` configura hooks de Behave. Se debe importar `from judo.behave.hooks import *` y `from judo.behave.context import setup_judo_context`. En `before_all(context)` se llama a `setup_judo_context(context)` y se configuran variables globales. Se pueden usar hooks: `before_feature`, `after_feature`, `before_scenario`, `after_scenario` para configuración y limpieza.

16. Tema: Configuración avanzada de environment.py por ambiente
Descripcion: En `before_all` se puede leer `os.getenv('TEST_ENV', 'dev')` para seleccionar la URL base según el ambiente. Se pueden configurar políticas de retry con `context.judo.set_retry_policy(max_retries=3, backoff_strategy="exponential")` y rate limiting con `context.judo.set_rate_limit(requests_per_second=10)`. En `before_feature` se puede configurar OAuth2 para features con tags específicos.

17. Tema: Ejecución de pruebas
Descripcion: Hay varias formas de ejecutar: con runner personalizado (`python runner.py`), directamente con behave (`behave features/`), feature específico (`behave features/api_tests.feature`), con tags (`behave --tags=@smoke features/`). Se pueden combinar tags: `behave --tags="@api and not @slow" features/`.

18. Tema: Ejecución de pruebas en paralelo
Descripcion: Se configura con `JUDO_PARALLEL=true` en .env o pasando `parallel=True` al BaseRunner. Se controla el número de workers con `JUDO_MAX_WORKERS`. Recomendaciones: CPU de 4 cores usar 4-6 workers, CPU de 8 cores usar 8-12 workers. Considerar la capacidad del servidor destino.

19. Tema: Filtrado de pruebas por tags
Descripcion: Se agregan tags a los scenarios con `@tag`. Ejemplos de ejecución: `behave --tags=@smoke features/` (solo smoke), `behave --tags="not @slow" features/` (excluyendo lentas), `behave --tags="@api and @auth" features/` (combinando tags).

20. Tema: Formatos de consola disponibles
Descripcion: Judo Framework soporta 4 formatos: `progress` (por defecto, barra de progreso), `pretty` (salida detallada y colorida), `plain` (salida simple sin colores), `none` (sin salida de consola). Se configura con `JUDO_CONSOLE_FORMAT` en .env.

21. Tema: Configuración de timeouts
Descripcion: Se configura con `JUDO_TIMEOUT` en .env (valor en segundos, ej: `JUDO_TIMEOUT=300` para 5 minutos) o en el runner con `BaseRunner(timeout=300)`. Para CI/CD se recomienda un timeout mayor (ej: 900 segundos) ya que puede ser más lento.

22. Tema: Reintentos automáticos de pruebas fallidas
Descripcion: Se configura con `JUDO_RETRY_COUNT=3` en .env. También se pueden configurar estrategias de backoff: `context.judo.set_retry_policy(max_retries=3, backoff_strategy="exponential")`. Útil para pruebas flaky o servicios inestables.


23. Tema: Configuración de reportes HTML personalizados
Descripcion: Los reportes HTML se generan automáticamente en la carpeta `judo_reports/`. Se personalizan creando un archivo `report_config.json` con secciones: `project` (nombre, ingeniero, equipo, producto, empresa, formato de fecha), `branding` (logos, colores), `charts` (gráficos habilitados, tipos), `footer` (creador, logo, empresa, URLs), `display` (detalles de request/response, variables, assertions). Los reportes incluyen gráficos interactivos con Chart.js y métricas detalladas.

24. Tema: Estructura completa del archivo report_config.json
Descripcion: El archivo tiene 5 secciones principales. `project`: name, engineer, team, product, company, date_format. `branding`: primary_logo, secondary_logo, company_logo, primary_color, secondary_color, accent_color, success_color, error_color, warning_color. `charts`: enabled, show_pie_charts, show_bar_charts, colors (passed, failed, skipped). `footer`: show_creator, show_logo, creator_name, creator_email, company_name, company_url, documentation_url, github_url. `display`: show_request_details, show_response_details, show_variables, show_assertions, collapse_sections_by_default, show_duration_in_ms.

25. Tema: Configuración de logo en el header del reporte
Descripcion: Para mostrar el logo de empresa en la esquina superior izquierda del reporte, se configura `secondary_logo` en la sección `branding`: `"secondary_logo": "data:image/png;base64,TU_LOGO_BASE64_AQUI"`. También se puede usar `company_logo` como alternativa con el mismo propósito. El logo del header siempre es visible si está configurado.

26. Tema: Configuración de logo en el footer del reporte
Descripcion: Para mostrar únicamente el logo en el footer sin texto adicional, se configura `primary_logo` en `branding` y en `footer` se pone `"show_creator": false` y `"show_logo": true`. Para ocultar completamente el logo del footer, usar `"show_logo": false`. Esta funcionalidad de footer solo logo es nueva en v1.5.9.5.

27. Tema: Conversión de logos a formato base64
Descripcion: Hay varias opciones para convertir logos a base64: 1) Herramientas online como base64-image.de, base64.guru, codebeautify.org. 2) Línea de comandos: en Linux/Mac `base64 -i tu_logo.png`, en Windows PowerShell `[Convert]::ToBase64String([IO.File]::ReadAllBytes("tu_logo.png"))`. 3) Python: usar `base64.b64encode()` para leer el archivo y generar el string con prefijo `data:image/png;base64,`.

28. Tema: Tipos de logo soportados en reportes
Descripcion: Hay 3 tipos de logo: `primary_logo` (ubicación: footer, controlado por footer.show_logo), `secondary_logo` (ubicación: header superior izquierdo, siempre visible si está configurado), `company_logo` (alternativa al secondary_logo, mismo propósito). Formatos de imagen soportados: PNG (recomendado, soporta transparencia), JPG/JPEG, GIF, SVG como base64.

29. Tema: Formatos de configuración de logos
Descripcion: Se soportan 4 formatos: 1) Base64 completo con prefijo: `"data:image/png;base64,iVBORw0KGgo..."`. 2) Base64 sin prefijo (se agrega automáticamente): `"iVBORw0KGgo..."`. 3) Ruta de archivo: `"assets/logos/mi-logo.png"`. 4) URL (no recomendado para reportes offline): `"https://miempresa.com/logo.png"`.

30. Tema: Recomendaciones para logos en reportes
Descripcion: Tamaño recomendado: logo principal (footer) 24x24px a 48x48px, logo secundario (header) 30x30px a 60x60px. Resolución: 72-150 DPI. Formato preferido: PNG con transparencia. Peso máximo: menos de 50KB por logo. Usar herramientas de compresión como TinyPNG o ImageOptim. Mantener proporciones originales y buen contraste.

31. Tema: Esquemas de colores predefinidos para reportes
Descripcion: Judo Framework ofrece 3 esquemas predefinidos: 1) Azul Corporativo: primary #1e40af, secondary #3b82f6, accent #60a5fa. 2) Verde Empresarial: primary #059669, secondary #10b981, accent #34d399. 3) Púrpura Moderno: primary #7c3aed, secondary #8b5cf6, accent #a78bfa. Todos incluyen colores de success (#22c55e o #10b981), error (#ef4444 o #f87171) y warning (#fbbf24 o #f59e0b).

32. Tema: Ubicaciones de búsqueda automática del archivo de configuración de reportes
Descripcion: Judo Framework busca el archivo de configuración en este orden: 1) Variable de entorno `JUDO_REPORT_CONFIG_FILE`. 2) Parámetro directo en el runner. 3) `./report_config.json`. 4) `./judo_report_config.json`. 5) `./.judo/report_config.json`. 6) `./judo_reports/report_config.json` (recomendado). 7) Directorio actual. 8) Directorio padre.

33. Tema: Configuración de reportes vía código Python
Descripcion: Se puede configurar el reporter directamente en el runner: `from judo.reporting.html_reporter import HTMLReporter` y luego `reporter = HTMLReporter(output_dir="mis_reportes", config_file="mi_configuracion.json")`. Para múltiples clientes, se puede usar un diccionario de configuraciones y seleccionar según variable de entorno.

34. Tema: Gráficos interactivos en reportes HTML
Descripcion: Los reportes incluyen gráficos de torta (distribución de escenarios y pasos), gráficos de barras (comparación de resultados, opcional), con colores personalizables por estado. Se habilitan con `"charts": {"enabled": true, "show_pie_charts": true, "show_bar_charts": true}`. Los gráficos usan Chart.js cargado desde CDN, por lo que requieren conexión a internet para visualizarse.

35. Tema: Sección display del report_config.json
Descripcion: Controla qué información se muestra en el reporte: `show_request_details` (detalles de requests), `show_response_details` (detalles de responses), `show_variables` (variables usadas), `show_assertions` (assertions realizadas), `collapse_sections_by_default` (secciones colapsadas por defecto), `show_duration_in_ms` (duración en milisegundos). Todos son booleanos true/false.

36. Tema: Reportes Cucumber JSON para CI/CD
Descripcion: Para integración con herramientas CI/CD, configurar `JUDO_GENERATE_CUCUMBER_JSON=true` y opcionalmente `JUDO_CUCUMBER_JSON_DIR=cucumber-reports` en .env. El JSON generado es compatible con Jenkins (Cucumber Reports Plugin), GitHub Actions, Azure DevOps y GitLab CI.

37. Tema: Logs de requests y responses para debugging
Descripcion: Para debugging detallado, activar `JUDO_SAVE_REQUESTS_RESPONSES=true` en .env. Los logs se guardan en la carpeta configurada con `JUDO_REQUESTS_RESPONSES_DIR=api_logs`. Combinado con `JUDO_VERBOSE=true` proporciona información completa de cada request y response.

38. Tema: Integración con GitHub Actions
Descripcion: Crear archivo `.github/workflows/api-tests.yml` con job que incluya: checkout del código, setup de Python 3.9, instalación con `pip install judo-framework[full]`, ejecución con `python runner.py`, y upload de artifacts desde `judo_reports/` usando `actions/upload-artifact@v2`.

39. Tema: Integración con Jenkins
Descripcion: Crear pipeline con stages: Install (`pip install judo-framework[full]`), Test (`python runner.py`), Reports (usar `publishHTML` para publicar reportes desde `judo_reports/`). Judo genera JSON Cucumber compatible con el plugin Cucumber Reports de Jenkins.

40. Tema: Uso de Docker para pruebas
Descripcion: Crear Dockerfile basado en `python:3.9`, copiar el proyecto, instalar `judo-framework[full]` y ejecutar `python runner.py` como CMD. Útil para ambientes reproducibles y CI/CD.

41. Tema: Manejo de secretos y API keys
Descripcion: Usar variables de entorno para datos sensibles: en `.env` para desarrollo local, como secrets en CI/CD. Nunca hardcodear credenciales en el código. En GitHub Actions usar `${{ secrets.API_KEY }}`, en Jenkins usar Credentials.

42. Tema: Uso de OAuth2 con Judo Framework
Descripcion: Configurar en environment.py: `context.judo.setup_oauth2(client_id="tu_client_id", client_secret="tu_client_secret", token_url="https://api.ejemplo.com/oauth/token")`. Verificar scopes requeridos y que el token no haya expirado. Se puede configurar en `before_feature` para features con tags de autenticación.

43. Tema: Validación de esquemas JSON
Descripcion: Usar pasos de validación de esquema: `Then the response should match schema "user_schema"`. Los esquemas se definen en archivos JSON separados. Permite validar que las respuestas de la API cumplen con la estructura esperada.

44. Tema: Configuración de rate limiting
Descripcion: Configurar límites de velocidad con `context.judo.set_rate_limit(requests_per_second=10)` y throttle con `context.judo.set_throttle(delay_ms=100)`. Útil para evitar errores 429 "Too Many Requests". También se puede reducir el número de workers paralelos y usar backoff exponencial.

45. Tema: Uso de WebSockets
Descripcion: Requiere instalar con extra `[websocket]`. Pasos disponibles: `Given I connect to WebSocket "ws://ejemplo.com/socket"`, `When I send WebSocket message "Hello"`, `Then I should receive WebSocket message "World"`.

46. Tema: Uso de GraphQL
Descripcion: Requiere instalar con extra `[graphql]`. Pasos disponibles: `Given I set GraphQL endpoint to "https://api.ejemplo.com/graphql"`, luego enviar queries con `When I send GraphQL query:` seguido del query en bloque de texto.

47. Tema: Pruebas de carga básicas
Descripcion: Usar data-driven testing con múltiples usuarios: `context.judo.run_data_driven_test("users.csv", test_function)`. Permite ejecutar el mismo test con diferentes datos para simular carga.


48. Tema: Uso de variables en features
Descripcion: Se definen variables con `Given I set variable "nombre" to "valor"` y se usan con sintaxis `${nombre}` o `{nombre}` en los pasos siguientes. Ejemplo: `Given I set variable "user_id" to "123"` y luego `When I send GET request to "/users/${user_id}"`. Las variables se pueden limpiar entre scenarios con `context.judo.clear_scenario_variables()`.

49. Tema: Navegación JSONPath en respuestas
Descripcion: Se usa JSONPath para acceder a campos de la respuesta. Ejemplos: `response.data[0].name` (primer elemento), `response.data[*].name` (todos los elementos), `users[0].address.city` (campos anidados). Se usa en pasos como `Then the response field "users[0].address.city" should be "Madrid"`.

50. Tema: Pruebas de file upload (multipart)
Descripcion: Usar pasos de multipart: `Given I set multipart field "file" to file "test_image.jpg"`, `And I set multipart field "description" to "Test upload"`, `When I send POST request to "/upload"`. Permite enviar archivos y campos de formulario en una misma petición.

51. Tema: Pruebas de APIs con paginación
Descripcion: Usar variables y extracción de datos para navegar páginas: `Given I set variable "page" to "1"`, `When I send GET request to "/users?page=${page}"`, `Then I extract "next_page" from response field "pagination.next"`. Se puede iterar sobre las páginas usando los valores extraídos.

52. Tema: Autenticación JWT
Descripcion: Configurar JWT en environment.py: `context.judo.configure_jwt(secret="tu_secret", algorithm="HS256")`. Verificar que el secret es correcto, el algoritmo coincide (HS256, RS256, etc.) y los claims requeridos (exp, iat) están presentes. Luego usar pasos de validación JWT en los features.

53. Tema: Autenticación básica (Basic Auth)
Descripcion: Usar el paso de autenticación básica: `Given I set basic authentication to "usuario:password"`. Verificar que el encoding base64 es correcto si se hace manualmente, que las credenciales son válidas y que el servidor soporta Basic Auth.

54. Tema: Autenticación con API Keys
Descripcion: Configurar el header de API key: `Given I set request header "X-API-Key" to "${API_KEY}"`. Asegurarse de que la variable está definida previamente con `Given I set variable "API_KEY" to "tu_api_key"`. Verificar el formato requerido por la API y que la key no haya expirado.

55. Tema: Circuit breakers para servicios inestables
Descripcion: Crear circuit breakers con `context.judo.create_circuit_breaker("api", failure_threshold=5)`. Combinado con retry policies: `context.judo.set_retry_policy(max_retries=3, backoff_strategy="exponential")`. Útil para manejar servicios que pueden estar temporalmente no disponibles.

56. Tema: Caching de responses
Descripcion: Habilitar caching con el paso `Given I enable response caching with TTL 300 seconds`. Útil para datos de referencia que no cambian frecuentemente, mejora el rendimiento al evitar requests repetidos al mismo endpoint.

57. Tema: Caso de uso empresarial - Empresa de consultoría
Descripcion: Configuración recomendada: logo del cliente en header (`secondary_logo`), logo de la consultora en footer (`primary_logo`), colores corporativos del cliente, información del proyecto específico. Permite generar reportes profesionales con branding del cliente.

58. Tema: Caso de uso empresarial - Equipo interno de QA
Descripcion: Configuración recomendada: logo de la empresa en header, información del equipo y producto, colores corporativos estándar, links a documentación interna. Sin logo en footer (`show_logo: false`) para un diseño limpio.

59. Tema: Caso de uso empresarial - Freelancer
Descripcion: Configuración recomendada: logo personal en header o footer, colores profesionales neutros, información de contacto en footer, `show_creator: false` para branding personal.

60. Tema: Migración desde versiones anteriores de Judo Framework
Descripcion: Desde v1.5.9.4 a v1.5.9.5: nueva funcionalidad de footer solo logo. Antes se usaba `"show_creator": true` que mostraba texto del creador. Ahora se puede usar `"show_creator": false` con `"show_logo": true` para mostrar solo el logo. Si no se tenía configuración de logos, crear `report_config.json`, agregar sección branding con logo, configurar footer y probar con herramienta de diagnóstico.

61. Tema: Migración desde Karate Framework
Descripcion: Judo Framework está inspirado en Karate. La mayoría de conceptos son similares: Features y Scenarios son idénticos, sintaxis de pasos es muy similar, JSONPath funciona igual, variables y contexto son compatibles. La migración es relativamente directa.

62. Tema: Solución - Error "No module named 'judo'" después de instalar
Descripcion: Verificar que pip instaló correctamente con `pip list | grep judo-framework`. Verificar que se usa el Python correcto con `which python`. Si se usan entornos virtuales, activar el correcto. Reinstalar si es necesario: `pip uninstall judo-framework` y luego `pip install judo-framework`.

63. Tema: Solución - Error de permisos durante instalación
Descripcion: En Linux/Mac usar `pip install --user judo-framework`. En Windows ejecutar como administrador. Mejor práctica: usar entorno virtual con `python -m venv judo_env`, activarlo y luego instalar.

64. Tema: Solución - Conflictos de dependencias
Descripcion: Crear entorno virtual limpio: `python -m venv fresh_env`, activarlo e instalar solo `judo-framework[full]`. Si persiste, usar `pip-tools` para resolver conflictos: `pip install pip-tools` y `pip-compile requirements.in`.

65. Tema: Solución - Variables de entorno no se cargan desde .env
Descripcion: Verificar que el archivo .env está en la raíz del proyecto. Verificar formato sin espacios alrededor del `=`. Verificar encoding UTF-8. Si es necesario, forzar carga manual con `from dotenv import load_dotenv; load_dotenv('.env')`.

66. Tema: Solución - Configuración JSON inválida
Descripcion: Validar JSON con `python -m json.tool report_config.json` o herramientas online como jsonlint.com. Errores comunes: usar comillas simples en vez de dobles, comas finales en objetos/arrays, encoding incorrecto. Siempre usar comillas dobles y encoding UTF-8.

67. Tema: Solución - Logo base64 no se muestra en reportes
Descripcion: Verificar que el base64 incluye el prefijo completo `data:image/png;base64,...`. Verificar que tiene longitud mayor a 100 caracteres. Verificar que no tiene espacios ni saltos de línea. Verificar que `show_logo: true` en la configuración del footer. Usar herramienta de diagnóstico: `python debug_logo_config.py`.

68. Tema: Solución - Rutas de archivos incorrectas
Descripcion: Usar rutas relativas desde la raíz del proyecto. En Windows usar barras normales `/` o dobles `\\`, no barras simples invertidas. Verificar permisos de lectura/escritura. Si es necesario, usar Path absolutos con `from pathlib import Path`.

69. Tema: Solución - "No features found"
Descripcion: Verificar que la carpeta `features/` existe y contiene archivos `.feature`. Verificar la variable `JUDO_FEATURES_DIR`. Verificar que la extensión de los archivos es `.feature`. Verificar permisos de lectura en el directorio.

70. Tema: Solución - Pruebas se cuelgan o no terminan
Descripcion: Configurar timeout apropiado con `JUDO_TIMEOUT=300`. Verificar conectividad de red. Usar Ctrl+C para interrumpir y revisar logs. Reducir `JUDO_MAX_WORKERS` si hay problemas de recursos. Verificar que no hay loops infinitos en pasos personalizados.

71. Tema: Solución - Errores de memoria (Out of Memory)
Descripcion: Reducir workers paralelos con `JUDO_MAX_WORKERS=2`. Desactivar logging detallado con `JUDO_SAVE_REQUESTS_RESPONSES=false`. Procesar features en lotes pequeños. Usar generadores en lugar de listas grandes en pasos personalizados.

72. Tema: Solución - Errores de encoding y caracteres especiales
Descripcion: Asegurar que todos los archivos usen UTF-8. En Windows configurar `set PYTHONIOENCODING=utf-8`. En archivos Python agregar `# -*- coding: utf-8 -*-`. En JSON se pueden usar caracteres directos (`"José Pérez"`) o escapes Unicode (`"Jos\u00e9 P\u00e9rez"`).

73. Tema: Solución - "Step not found" o "Undefined step"
Descripcion: Verificar la sintaxis exacta del paso en la referencia de pasos. Verificar que se usan comillas dobles (no simples) para parámetros. Verificar importación correcta en environment.py: `from judo.behave.steps import *` para inglés o `from judo.behave.steps_es import *` para español. Verificar que el paso existe en la versión instalada.

74. Tema: Solución - Parámetros no se pasan correctamente a los pasos
Descripcion: Verificar sintaxis de parámetros: `"/users/{user_id}"` o `"/users/${user_id}"`. Verificar que la variable fue definida previamente con `Given I set variable "user_id" to "123"`. Usar comillas dobles para valores string.

75. Tema: Solución - JSONPath no encuentra campos en la respuesta
Descripcion: Usar `Then I print the response` para debug y ver la estructura real del JSON. Verificar la sintaxis JSONPath correcta: `response.data[0].name` (correcto) vs `response.data.0.name` (incorrecto). Usar herramientas online para probar expresiones JSONPath.

76. Tema: Solución - No se generan reportes HTML
Descripcion: Verificar permisos de escritura en el directorio de salida. Verificar que el runner completó sin errores críticos. Verificar configuración `JUDO_OUTPUT_DIR`. Ejecutar con `JUDO_VERBOSE=true` para ver errores. Verificar espacio en disco disponible.

77. Tema: Solución - Reportes HTML sin estilos o gráficos
Descripcion: Verificar que el archivo HTML se generó completamente. Abrir en navegador moderno (Chrome, Firefox, Edge). Verificar conexión a internet ya que Chart.js se carga desde CDN. Verificar configuración JSON válida. Revisar consola del navegador (F12) para errores JavaScript.

78. Tema: Solución - Logo personalizado no aparece en reportes
Descripcion: Verificar formato base64 completo con prefijo `data:image/png;base64,...`. Verificar configuración del footer: `"show_logo": true` y `"show_creator": false`. Usar herramienta de diagnóstico `python debug_logo_config.py`. Verificar que el base64 tiene longitud mayor a 100 caracteres.

79. Tema: Solución - Reportes Cucumber JSON malformados
Descripcion: Verificar que `JUDO_GENERATE_CUCUMBER_JSON=true` está configurado. Validar JSON generado con `python -m json.tool cucumber-reports/results.json`. Si está corrupto, eliminar la carpeta y regenerar. Verificar permisos de escritura.

80. Tema: Solución - Pruebas muy lentas
Descripcion: Habilitar ejecución paralela con `JUDO_PARALLEL=true` y ajustar `JUDO_MAX_WORKERS`. Optimizar timeouts reduciendo valores innecesariamente altos. Usar caching para datos estáticos. Revisar latencia de red al servidor. Optimizar número de requests por prueba.

81. Tema: Solución - Alto uso de CPU y memoria
Descripcion: Reducir workers paralelos con `JUDO_MAX_WORKERS=2`. Desactivar logging detallado: `JUDO_SAVE_REQUESTS_RESPONSES=false` y `JUDO_VERBOSE=false`. Procesar en lotes más pequeños. Cerrar aplicaciones innecesarias. Monitorear con herramientas del sistema.

82. Tema: Solución - Timeouts frecuentes
Descripcion: Aumentar timeout global con `JUDO_TIMEOUT=600` (10 minutos). Verificar conectividad de red y carga del servidor destino. Implementar retry policy con `context.judo.set_retry_policy(max_retries=3)`. Usar circuit breakers para servicios inestables.

83. Tema: Solución - Rate limiting del servidor (Error 429)
Descripcion: Configurar rate limiting con `context.judo.set_rate_limit(requests_per_second=5)`. Añadir delays con `context.judo.set_throttle(delay_ms=200)`. Reducir workers paralelos. Implementar backoff exponencial. Coordinar con equipo de infraestructura.

84. Tema: Solución - Pruebas pasan localmente pero fallan en CI/CD
Descripcion: Verificar variables de entorno en CI (API keys, secrets, URLs). Verificar conectividad de red en CI. Ajustar timeouts para ambiente CI (`JUDO_TIMEOUT=900`). Verificar versión de Python en CI. Usar mismas dependencias con requirements.txt.

85. Tema: Solución - Reportes no se publican en CI/CD
Descripcion: Verificar que los reportes se generan correctamente. Configurar artifacts: en GitHub Actions usar `actions/upload-artifact@v2` con path `judo_reports/`. Verificar permisos de lectura. Verificar rutas relativas vs absolutas.

86. Tema: Solución - OAuth2 no funciona
Descripcion: Verificar configuración de client_id, client_secret y token_url. Verificar scopes requeridos. Verificar que el token no expiró. Activar debugging con `JUDO_SAVE_REQUESTS_RESPONSES=true` para ver los requests de autenticación.

87. Tema: Solución - JWT tokens inválidos
Descripcion: Verificar que el secret es correcto en `context.judo.configure_jwt()`. Verificar que el algoritmo coincide (HS256, RS256, etc.). Verificar claims requeridos como exp (expiración) e iat (issued at). Verificar que el token no ha expirado.

88. Tema: Solución - API Keys no funcionan
Descripcion: Verificar que el header es correcto: `Given I set request header "X-API-Key" to "${API_KEY}"`. Verificar que la variable está configurada. Verificar el formato requerido por la API. Verificar que la key no ha expirado.

89. Tema: Herramientas de diagnóstico disponibles
Descripcion: Judo Framework incluye varias herramientas: `debug_logo_config.py` para diagnosticar problemas con logos, logging detallado con `JUDO_VERBOSE=true` y `JUDO_SAVE_REQUESTS_RESPONSES=true`, validación de JSON con `python -m json.tool archivo.json`, verificación de dependencias con `pip list | grep judo`, verificación de versión con `python -c "import judo; print(judo.__version__)"`.

90. Tema: Niveles de logging y debugging
Descripcion: Hay 4 niveles de logging: ERROR (solo errores críticos), WARNING (advertencias y errores), INFO (información general, por defecto), DEBUG (información detallada con `JUDO_VERBOSE=true`). Para debugging completo configurar en .env: `JUDO_VERBOSE=true`, `JUDO_DEBUG_REPORTER=true`, `JUDO_SAVE_REQUESTS_RESPONSES=true`. Los logs se guardan en la carpeta `judo_reports/` y los requests/responses en `requests_responses/`.

91. Tema: Mejores prácticas de organización de código
Descripcion: Usar nombres descriptivos para features y scenarios. Agrupar features por funcionalidad en subcarpetas. Mantener scenarios independientes entre sí. Usar Background para configuración común. Usar tags para organizar y filtrar pruebas.

92. Tema: Mejores prácticas de gestión de datos de prueba
Descripcion: Usar archivos JSON para datos de prueba complejos. Implementar data-driven testing para múltiples casos. Usar variables de entorno para configuración sensible. Separar datos por ambiente (dev, staging, prod). Nunca hardcodear credenciales.

93. Tema: Mejores prácticas de mantenimiento de pruebas
Descripcion: Revisar y actualizar regularmente las pruebas. Usar tags para organizar y filtrar. Implementar retry policies para pruebas flaky. Monitorear métricas de performance. Mantener configuraciones en control de versiones. Documentar cambios en configuración.

94. Tema: Mejores prácticas de seguridad
Descripcion: No incluir información sensible en archivos de configuración. Usar variables de entorno para datos sensibles. Revisar permisos de archivos de configuración. No commitear configuraciones con datos reales. Usar secrets en CI/CD para credenciales.

95. Tema: Mejores prácticas de performance en reportes
Descripcion: Usar logos optimizados (menos de 50KB). Evitar URLs externas para logos. Usar base64 para logos pequeños. Considerar caching para logos grandes. Validar configuración después de cambios. Mantener backups de configuraciones funcionales.

96. Tema: Soporte y recursos de la comunidad
Descripcion: Documentación oficial en http://centyc.cl/judo-framework/. GitHub del proyecto: https://github.com/FelipeFariasAlfaro/Judo-Framework. Email de soporte: felipe.farias@centyc.cl. Para reportar bugs usar GitHub Issues incluyendo: descripción detallada, pasos para reproducir, versión de Judo Framework, logs de error y configuración relevante. El proyecto acepta contribuciones vía Pull Request.

97. Tema: Ejemplo - Petición GET básica que valida código 200
Descripcion: Este scenario demuestra la forma más simple de probar un endpoint GET y validar que responde correctamente. Se configura la URL base en el Background, se envía la petición y se verifica el status code. Ejemplo:
```gherkin
Background:
  Given I have a Judo API client
  And the base URL is "https://jsonplaceholder.typicode.com"

Scenario: Validar que el endpoint de posts responde 200
  When I send a GET request to "/posts/1"
  Then the response status should be 200
  And the response should contain "title"
```

98. Tema: Ejemplo - Petición POST con cuerpo JSON para crear un recurso
Descripcion: Demuestra cómo enviar una petición POST con un body JSON para crear un nuevo recurso. Se define el cuerpo en un bloque de texto multilínea y se valida que el servidor responde con 201 (Created). Ejemplo:
```gherkin
Scenario: Crear un nuevo post
  When hago una petición POST a "/posts" con el cuerpo
    """
    {
      "title": "Test Post",
      "body": "This is a test",
      "userId": 1
    }
    """
  Then el código de respuesta debe ser 201
```

99. Tema: Ejemplo - Petición PUT para actualizar un recurso completo
Descripcion: Demuestra cómo enviar una petición PUT para reemplazar completamente un recurso existente. Se envía el objeto completo con todos los campos. Ejemplo:
```gherkin
Scenario: Actualizar un post existente
  When hago una petición PUT a "/posts/1" con el cuerpo
    """
    {
      "id": 1,
      "title": "Updated Title",
      "body": "Updated body content",
      "userId": 1
    }
    """
  Then el código de respuesta debe ser 200
```

100. Tema: Ejemplo - Petición PATCH para actualización parcial
Descripcion: Demuestra cómo enviar una petición PATCH para modificar solo algunos campos de un recurso sin enviar el objeto completo. Ejemplo:
```gherkin
Scenario: Actualizar parcialmente un post
  When hago una petición PATCH a "/posts/1" con el cuerpo
    """
    {
      "title": "Patched Title"
    }
    """
  Then el código de respuesta debe ser 200
```

101. Tema: Ejemplo - Petición DELETE para eliminar un recurso
Descripcion: Demuestra cómo enviar una petición DELETE para eliminar un recurso y validar que el servidor responde exitosamente. Ejemplo:
```gherkin
Scenario: Eliminar un post
  When hago una petición DELETE a "/posts/1"
  Then el código de respuesta debe ser 200
```

102. Tema: Ejemplo - Autenticación con Bearer Token
Descripcion: Demuestra cómo configurar autenticación Bearer Token antes de enviar una petición. El token se establece y se incluye automáticamente en el header Authorization. Ejemplo:
```gherkin
Scenario: Petición autenticada con Bearer Token
  Given I set bearer token "test-token-12345"
  When I send a GET request to "/posts/1"
  Then the response status should be 200
```

103. Tema: Ejemplo - Autenticación básica con usuario y contraseña
Descripcion: Demuestra cómo configurar autenticación Basic Auth con credenciales de usuario. Judo codifica automáticamente las credenciales en base64. Ejemplo:
```gherkin
Scenario: Petición con autenticación básica
  Given uso autenticación básica con usuario "testuser" y contraseña "testpass"
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
```

104. Tema: Ejemplo - Configurar headers personalizados en la petición
Descripcion: Demuestra cómo agregar headers personalizados a una petición. Se pueden agregar múltiples headers usando pasos And consecutivos. Ejemplo:
```gherkin
Scenario: Petición con headers personalizados
  Given establezco el header "X-Custom-Header" a "CustomValue"
  And establezco el header "X-Request-ID" a "req-12345"
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
```

105. Tema: Ejemplo - Uso de query parameters en peticiones
Descripcion: Demuestra cómo agregar parámetros de consulta (query params) a una petición GET. Los parámetros se agregan automáticamente a la URL. Ejemplo:
```gherkin
Scenario: Filtrar posts por userId usando query params
  Given establezco el parámetro "userId" a "1"
  When hago una petición GET a "/posts"
  Then el código de respuesta debe ser 200
  And la respuesta debe ser una lista
```

106. Tema: Ejemplo - Validar campos específicos de la respuesta
Descripcion: Demuestra cómo validar que campos específicos del JSON de respuesta tienen los valores esperados. Se pueden encadenar múltiples validaciones. Ejemplo:
```gherkin
Scenario: Validar campos del post
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
  And el campo "userId" debe ser 1
  And el campo "id" debe ser 1
  And la respuesta debe contener el campo "title"
  And la respuesta debe contener el campo "body"
```

107. Tema: Ejemplo - Validar respuesta contra esquema JSON
Descripcion: Demuestra cómo validar que la estructura completa de la respuesta cumple con un esquema JSON definido. Útil para validación de contratos. Ejemplo:
```gherkin
Scenario: Validar esquema JSON de un post
  When I send a GET request to "/posts/1"
  Then the response status should be 200
  And the response should match JSON schema:
    """
    {
      "type": "object",
      "properties": {
        "userId": {"type": "number"},
        "id": {"type": "number"},
        "title": {"type": "string"},
        "body": {"type": "string"}
      },
      "required": ["userId", "id", "title", "body"]
    }
    """
```

108. Tema: Ejemplo - Validar que la respuesta es un array con elementos
Descripcion: Demuestra cómo validar que la respuesta es un array y que contiene elementos. Se puede verificar la cantidad mínima de items y que cada elemento tenga los campos esperados. Ejemplo:
```gherkin
Scenario: Validar lista de posts
  When I send a GET request to "/posts"
  Then the response status should be 200
  And the response array should have more than 0 items
  And the response should contain all fields: ["userId", "id", "title", "body"]
```

109. Tema: Ejemplo - Extraer y almacenar datos de la respuesta en variables
Descripcion: Demuestra cómo extraer un valor de la respuesta y guardarlo en una variable para usarlo en pasos posteriores. Fundamental para encadenar peticiones. Ejemplo:
```gherkin
Scenario: Extraer título del post y verificar
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
  And guardo el valor del campo "title" en la variable "post_title"
  And debo tener la variable "post_title" con valor "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
```

110. Tema: Ejemplo - Usar variables en peticiones encadenadas
Descripcion: Demuestra cómo definir variables y usarlas en URLs y cuerpos de peticiones. Las variables se referencian con `{nombre}` o `${nombre}`. Ejemplo:
```gherkin
Scenario: Usar variables para construir peticiones dinámicas
  Given establezco la variable "user_id" a "1"
  And establezco la variable "post_id" a "1"
  When hago una petición GET a "/posts/{post_id}"
  Then el código de respuesta debe ser 200
  And el campo "userId" debe ser 1
```

111. Tema: Ejemplo - Validar tiempo de respuesta del endpoint
Descripcion: Demuestra cómo verificar que un endpoint responde dentro de un tiempo aceptable. Útil para pruebas de performance básicas y SLAs. Ejemplo:
```gherkin
Scenario: Validar que el endpoint responde en menos de 5 segundos
  When I send a GET request to "/posts/1"
  Then the response status should be 200
  And the response time should be less than 5000 milliseconds
```

112. Tema: Ejemplo - Validación de tipos de datos en la respuesta
Descripcion: Demuestra cómo verificar que los campos de la respuesta son del tipo de dato correcto (string, número, etc.). Ejemplo:
```gherkin
Scenario: Validar tipos de datos de los campos
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
  And la respuesta "$.title" debe ser una cadena
  And la respuesta "$.userId" debe ser un número
  And la respuesta "$.id" debe ser un número
```

113. Tema: Ejemplo - Validación con JSONPath avanzado
Descripcion: Demuestra el uso de expresiones JSONPath para acceder a campos específicos de la respuesta y validar sus valores. Ejemplo:
```gherkin
Scenario: Validar campos con JSONPath
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
  And la respuesta "$.title" debe ser "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
  And la respuesta "$.userId" debe ser 1
```

114. Tema: Ejemplo - Validar que cada elemento de un array tiene campos requeridos
Descripcion: Demuestra cómo iterar sobre un array de respuesta y verificar que todos los elementos contienen los campos esperados. Ejemplo:
```gherkin
Scenario: Validar que todos los posts tienen campos requeridos
  When hago una petición GET a "/posts"
  Then el código de respuesta debe ser 200
  And la respuesta debe ser una lista
  And cada elemento debe tener el campo "userId"
  And cada elemento debe tener el campo "title"
```

115. Tema: Ejemplo - Buscar un elemento específico dentro de un array
Descripcion: Demuestra cómo verificar que un array contiene al menos un elemento que cumple con una condición específica. Ejemplo:
```gherkin
Scenario: Verificar que existe un post del usuario 1
  When hago una petición GET a "/posts"
  Then el código de respuesta debe ser 200
  And el array "." debe contener un elemento con "userId" igual a "1"
```

116. Tema: Ejemplo - Enviar petición POST usando datos desde una variable JSON
Descripcion: Demuestra cómo definir un JSON completo en una variable y luego usarlo como cuerpo de una petición POST. Útil para separar datos de la lógica del test. Ejemplo:
```gherkin
Scenario: Crear post usando variable con datos JSON
  Given establezco la variable "post_data" al JSON
    """
    {
      "title": "New Post",
      "body": "Post content",
      "userId": 1
    }
    """
  When hago una petición POST a "/posts" con la variable "post_data"
  Then el código de respuesta debe ser 201
```

117. Tema: Ejemplo - Política de reintentos con backoff exponencial
Descripcion: Demuestra cómo configurar reintentos automáticos con estrategia de backoff exponencial para manejar fallos transitorios de red o del servidor. Ejemplo:
```gherkin
Scenario: Petición con reintentos automáticos
  Given I set retry policy with max_retries=3 and backoff_strategy="exponential"
  When I send a GET request to "/posts/1"
  Then the response status should be 200
  And the response should contain "title"
```

118. Tema: Ejemplo - Patrón Circuit Breaker para prevenir fallos en cascada
Descripcion: Demuestra cómo crear un circuit breaker que se abre después de un número de fallos consecutivos, previniendo que el sistema siga enviando peticiones a un servicio caído. Ejemplo:
```gherkin
Scenario: Circuit breaker protege contra fallos en cascada
  Given I create a circuit breaker named "api_breaker" with failure_threshold=5
  When I send a GET request to "/posts/1"
  Then the response status should be 200
  And the circuit breaker "api_breaker" should be in CLOSED state
```

119. Tema: Ejemplo - Interceptores de request para agregar headers automáticos
Descripcion: Demuestra cómo agregar interceptores que modifican automáticamente cada petición, por ejemplo agregando un timestamp o un token de autorización. Ejemplo:
```gherkin
Scenario: Interceptores agregan headers automáticamente
  Given I add a timestamp interceptor with header name "X-Request-Time"
  And I add an authorization interceptor with token "test-token"
  When I send a GET request to "/posts/1"
  Then the response status should be 200
```

120. Tema: Ejemplo - Rate limiting para respetar límites de la API
Descripcion: Demuestra cómo configurar un límite de velocidad para no exceder la cantidad de peticiones permitidas por segundo por la API destino. Ejemplo:
```gherkin
Scenario: Respetar límite de velocidad de la API
  Given I set rate limit to 10 requests per second
  When I send 5 GET requests to "/posts/1"
  Then all responses should have status 200
```

121. Tema: Ejemplo - Throttling con delay fijo entre peticiones
Descripcion: Demuestra cómo agregar un retraso fijo entre peticiones consecutivas para evitar sobrecargar el servidor. Ejemplo:
```gherkin
Scenario: Retraso fijo entre peticiones
  Given I set throttle with delay 100 milliseconds
  When I send a GET request to "/posts/1"
  And I send a GET request to "/posts/2"
  Then both responses should have status 200
```

122. Tema: Ejemplo - Caché de respuestas para mejorar rendimiento
Descripcion: Demuestra cómo habilitar el caché de respuestas GET con un tiempo de vida (TTL). La segunda petición al mismo endpoint se sirve desde caché sin hacer request real. Ejemplo:
```gherkin
Scenario: Cachear respuestas para evitar peticiones repetidas
  Given I enable response caching with TTL 300 seconds
  When I send a GET request to "/posts/1"
  And I send the same GET request to "/posts/1" again
  Then both responses should have status 200
  And the second response should come from cache
```

123. Tema: Ejemplo - Monitoreo de métricas de rendimiento
Descripcion: Demuestra cómo enviar múltiples peticiones y recopilar métricas de rendimiento como tiempo promedio, percentil 95 y tasa de error. Ejemplo:
```gherkin
Scenario: Recopilar métricas de rendimiento
  When I send 10 GET requests to "/posts/1"
  Then I should have performance metrics:
    | metric            | condition      |
    | avg_response_time | less than 5000 |
    | p95_response_time | less than 5000 |
    | error_rate        | equals 0       |
```

124. Tema: Ejemplo - Autenticación OAuth2 con refresh automático de token
Descripcion: Demuestra cómo configurar OAuth2 con client credentials. Judo obtiene el token automáticamente y lo incluye en las peticiones. Ejemplo:
```gherkin
Scenario: Autenticación OAuth2 automática
  Given I setup OAuth2 with:
    | client_id     | test-client                    |
    | client_secret | test-secret                    |
    | token_url     | https://auth.example.com/token |
  When I send a GET request to "/posts/1"
  Then the request should include Authorization header
```

125. Tema: Ejemplo - Creación y verificación de token JWT
Descripcion: Demuestra cómo configurar JWT con un secreto y algoritmo, crear un token con payload personalizado y verificar que es válido. Ejemplo:
```gherkin
Scenario: Crear y validar token JWT
  Given I setup JWT with secret "my-secret" and algorithm "HS256"
  When I create JWT token with payload:
    """
    {"user_id": 123, "username": "john"}
    """
  Then the token should be valid
```

126. Tema: Ejemplo - Validación de contrato OpenAPI
Descripcion: Demuestra cómo cargar una especificación OpenAPI y validar que la respuesta de un endpoint cumple con el contrato definido. Ejemplo:
```gherkin
Scenario: Validar respuesta contra contrato OpenAPI
  Given I load OpenAPI spec from "specs/jsonplaceholder-openapi.yaml"
  When I send a GET request to "/posts/1"
  Then the response should match OpenAPI contract for GET /posts/{id}
```

127. Tema: Ejemplo - Validar estructura de datos con tabla de campos requeridos
Descripcion: Demuestra cómo validar que la respuesta tiene campos específicos con tipos de datos correctos usando una tabla de Behave. Ejemplo:
```gherkin
Scenario: Validar estructura con tabla de campos
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
  And la respuesta debe tener los campos requeridos
    | campo  | tipo   | requerido |
    | id     | entero | true      |
    | userId | entero | true      |
    | title  | cadena | true      |
    | body   | cadena | true      |
```

128. Tema: Ejemplo - Validar patrones con expresiones regulares en campos
Descripcion: Demuestra cómo validar que un campo de la respuesta cumple con un patrón regex específico. Útil para validar formatos de email, teléfono, etc. Ejemplo:
```gherkin
Scenario: Validar formato de email y teléfono con regex
  When hago una petición GET a "/users/1"
  Then el código de respuesta debe ser 200
  And el campo de respuesta "email" debe coincidir con el patrón "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
  And el campo de respuesta "phone" debe coincidir con el patrón "^\d{1}-\d{3}-\d{3}-\d{4}$"
```

129. Tema: Ejemplo - Validar estructura JSON anidada compleja
Descripcion: Demuestra cómo validar una estructura JSON con múltiples niveles de anidamiento, verificando que cada campo existe y es del tipo correcto. Ejemplo:
```gherkin
Scenario: Validar estructura anidada de usuario
  When hago una petición GET a "/users/1"
  Then el código de respuesta debe ser 200
  And la respuesta debe tener estructura anidada
    """
    {
      "id": "integer",
      "name": "string",
      "email": "string",
      "address": {
        "street": "string",
        "city": "string",
        "geo": {
          "lat": "string",
          "lng": "string"
        }
      },
      "company": {
        "name": "string",
        "catchPhrase": "string"
      }
    }
    """
```

130. Tema: Ejemplo - Ingeniería del caos con inyección de latencia
Descripcion: Demuestra cómo inyectar latencia artificial para probar la resiliencia de la aplicación ante respuestas lentas. Verifica que el sistema sigue funcionando a pesar del retraso. Ejemplo:
```gherkin
Scenario: Probar resiliencia con latencia inyectada
  Given I enable chaos engineering
  And I inject latency between 100 and 500 milliseconds
  When I send a GET request to "/posts/1"
  Then the response should complete despite injected latency
```

131. Tema: Ejemplo - Ingeniería del caos con inyección de errores
Descripcion: Demuestra cómo inyectar errores aleatorios para probar cómo el sistema maneja fallos parciales. Se configura un porcentaje de error y se envían múltiples peticiones. Ejemplo:
```gherkin
Scenario: Probar resiliencia con errores inyectados
  Given I enable chaos engineering
  And I inject error rate of 10 percent
  When I send 10 GET requests to "/posts/1"
  Then some requests may fail due to injected errors
```

132. Tema: Ejemplo - Guardar respuesta en archivo para análisis posterior
Descripcion: Demuestra cómo guardar la respuesta completa de una petición en un archivo JSON. Útil para debugging, comparación de datos o alimentar otros procesos. Ejemplo:
```gherkin
Scenario: Guardar respuesta en archivo
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
  And guardo la respuesta en el archivo "test_data/response.json"
```

133. Tema: Ejemplo - Cargar datos de prueba desde archivo externo
Descripcion: Demuestra cómo cargar datos de prueba desde un archivo JSON externo para usarlos en las peticiones. Permite separar los datos de la lógica del test. Ejemplo:
```gherkin
Scenario: Cargar datos desde archivo JSON
  Given cargo datos de prueba del archivo "test_data/sample.json"
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
```

134. Tema: Ejemplo - Esperar entre peticiones consecutivas
Descripcion: Demuestra cómo agregar una pausa explícita entre peticiones. Útil cuando el servidor necesita tiempo para procesar o cuando se prueba comportamiento asíncrono. Ejemplo:
```gherkin
Scenario: Esperar entre peticiones
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
  And espero 1.0 segundos
  When hago una petición GET a "/posts/2"
  Then el código de respuesta debe ser 200
```

135. Tema: Ejemplo - Habilitar logging detallado de peticiones y respuestas
Descripcion: Demuestra cómo activar el guardado automático de todas las peticiones y respuestas en archivos para debugging posterior. Ejemplo:
```gherkin
Scenario: Habilitar logging de peticiones
  Given habilito el guardado de peticiones y respuestas
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
```

136. Tema: Ejemplo - Obtener valores desde variables de entorno
Descripcion: Demuestra cómo leer un valor desde las variables de entorno del sistema y almacenarlo en una variable de Judo para usarlo en los tests. Ejemplo:
```gherkin
Scenario: Usar variable de entorno en el test
  Given obtengo el valor "BASE_URL" desde env y lo almaceno en "base_url"
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
```

137. Tema: Ejemplo - Comparar dos variables entre sí
Descripcion: Demuestra cómo comparar el valor de dos variables almacenadas durante la ejecución del test. Útil para verificar consistencia de datos entre peticiones. Ejemplo:
```gherkin
Scenario: Comparar valores de dos variables
  Given establezco la variable "value1" a "test"
  And establezco la variable "value2" a "test"
  When hago una petición GET a "/posts/1"
  Then la variable "value1" debe ser igual a la variable "value2"
```

138. Tema: Ejemplo - Imprimir respuesta para debugging
Descripcion: Demuestra cómo imprimir la respuesta completa en la consola para inspeccionar su contenido durante el desarrollo de tests. Ejemplo:
```gherkin
Scenario: Imprimir respuesta para debug
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
  And imprimo la respuesta
```

139. Tema: Ejemplo - Validar que un campo no es null
Descripcion: Demuestra cómo verificar que un campo específico de la respuesta tiene un valor y no es null. Ejemplo:
```gherkin
Scenario: Verificar que el título no es null
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
  And la respuesta "$.title" no debe ser null
```

140. Tema: Ejemplo - Validar respuesta exitosa sin verificar código específico
Descripcion: Demuestra cómo validar que la respuesta fue exitosa (código 2xx) sin especificar un código exacto. Útil cuando el código puede variar entre 200 y 204. Ejemplo:
```gherkin
Scenario: Verificar respuesta exitosa genérica
  When hago una petición GET a "/posts/1"
  Then la respuesta debe ser exitosa
```

141. Tema: Ejemplo - Validar que la respuesta es un objeto JSON válido
Descripcion: Demuestra cómo verificar que la respuesta es un objeto JSON (no un array, string u otro tipo). Ejemplo:
```gherkin
Scenario: Verificar que la respuesta es un objeto JSON
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
  And la respuesta debe ser un objeto
```

142. Tema: Ejemplo - Pruebas dirigidas por datos con archivo CSV
Descripcion: Demuestra cómo ejecutar la misma prueba con múltiples conjuntos de datos cargados desde un archivo CSV. Cada fila del CSV se ejecuta como un caso de prueba independiente. Ejemplo:
```gherkin
Scenario: Ejecutar pruebas con datos desde CSV
  Given I load test data from file "test_data/posts.csv"
  When I run data-driven test for each row
  Then all tests should complete successfully
```

143. Tema: Ejemplo - Logging avanzado con nivel DEBUG
Descripcion: Demuestra cómo configurar el nivel de logging a DEBUG y habilitar el guardado de peticiones en un directorio específico para análisis detallado. Ejemplo:
```gherkin
Scenario: Configurar logging detallado
  Given I set logging level to "DEBUG"
  And I enable request logging to directory "request_logs"
  When I send a GET request to "/posts/1"
  Then request and response should be logged to file
```

144. Tema: Ejemplo - Scenario completo en español con Background
Descripcion: Demuestra un scenario completo escrito enteramente en español, incluyendo Background con configuración inicial, petición y validaciones múltiples. Ejemplo:
```gherkin
Antecedentes:
  Dado que tengo un cliente API Judo
  Y la URL base es "https://jsonplaceholder.typicode.com"

Escenario: Obtener y validar un post en español
  Cuando envío una solicitud GET a "/posts/1"
  Entonces el estado de la respuesta debe ser 200
  Y la respuesta debe contener "title"
```

145. Tema: Ejemplo - Scenario con reintentos, rate limit, caché y monitoreo combinados
Descripcion: Demuestra cómo combinar múltiples características avanzadas en un solo scenario: reintentos automáticos, limitación de velocidad, caché de respuestas y alertas de rendimiento. Ejemplo:
```gherkin
Scenario: Pila completa de características avanzadas
  Given I set retry policy with max_retries=3
  And I set rate limit to 10 requests per second
  And I enable response caching with TTL 300 seconds
  And I set performance alert for response_time threshold 1000 milliseconds
  When I send 5 GET requests to "/posts/1"
  Then all responses should have status 200
  And performance metrics should be collected
  And cache should contain 1 entry
```

146. Tema: Ejemplo - Prueba de resiliencia combinando caos y circuit breaker
Descripcion: Demuestra un scenario de prueba de resiliencia que combina ingeniería del caos (latencia y errores inyectados) con circuit breaker para verificar que el sistema se mantiene estable. Ejemplo:
```gherkin
Scenario: Prueba de resiliencia completa
  Given I enable chaos engineering
  And I inject latency between 100 and 300 milliseconds
  And I inject error rate of 5 percent
  And I create circuit breaker with failure_threshold=10
  When I send 20 GET requests to "/posts/1"
  Then circuit breaker should remain in CLOSED state
  And error rate should be less than 10 percent
```

147. Tema: Ejemplo - Validar tipos de datos específicos (entero, cadena, email, URL)
Descripcion: Demuestra cómo validar que los campos de la respuesta son de tipos específicos como entero, cadena, email válido o URL válida. Ejemplo:
```gherkin
Scenario: Validar tipos de datos de un usuario
  When hago una petición GET a "/users/1"
  Then el código de respuesta debe ser 200
  And el campo de respuesta "id" debe ser de tipo "entero"
  And el campo de respuesta "name" debe ser de tipo "cadena"
  And el campo de respuesta "email" debe ser un email válido
  And el campo de respuesta "website" debe ser una URL válida
```

148. Tema: Ejemplo - Validación comprensiva de contrato con headers
Descripcion: Demuestra una validación completa de contrato que incluye verificar la respuesta contra la especificación OpenAPI y también validar los headers de respuesta. Ejemplo:
```gherkin
Scenario: Validación comprensiva de contrato
  Given cargo el contrato OpenAPI desde "specs/jsonplaceholder-openapi.yaml"
  When hago una petición GET a "/posts/1"
  Then el código de respuesta debe ser 200
  And la respuesta debe coincidir con especificación completa del contrato de datos
  And valido los headers de respuesta contra contrato
```

149. Tema: Mock Server integrado - Qué es y para qué sirve
Descripcion: Judo Framework incluye un Mock Server integrado que permite simular APIs sin depender de servicios externos. Es útil para pruebas offline, desarrollo sin backend disponible, pruebas de integración aisladas y simulación de respuestas específicas (errores, datos controlados). El mock server se basa en la clase `MockServer` del módulo `judo.mock.server` y soporta todos los métodos HTTP: GET, POST, PUT, PATCH y DELETE.

150. Tema: Mock Server - Iniciar desde línea de comandos (CLI)
Descripcion: Se puede iniciar el mock server directamente desde la terminal usando el CLI de Judo: `judo mock --port 8080`. Opcionalmente se puede pasar un archivo de configuración con `judo mock --port 8080 --config mock_config.json`. Sin configuración, el servidor inicia con rutas de demostración: `/health` (retorna status ok) y `/users/*` (retorna un usuario de ejemplo). El servidor se detiene con Ctrl+C.

151. Tema: Mock Server - Iniciar desde código Python
Descripcion: Se puede iniciar el mock server programáticamente usando la clase Judo. Ejemplo:
```python
from judo import Judo

judo = Judo()

# Iniciar mock server en puerto 8080
mock = judo.start_mock(port=8080)

# Agregar rutas personalizadas
mock.get("/api/users", {
    "status": 200,
    "body": [{"id": 1, "name": "Juan"}, {"id": 2, "name": "Ana"}]
})

# El servidor está corriendo en http://localhost:8080
# Detener cuando ya no se necesite
judo.stop_mock()
```

152. Tema: Mock Server - Usar MockServer directamente sin clase Judo
Descripcion: También se puede usar la clase MockServer directamente sin pasar por Judo. Ejemplo:
```python
from judo.mock.server import MockServer

server = MockServer(port=9090)

# Agregar rutas
server.get("/health", {"status": 200, "body": {"status": "ok"}})
server.post("/api/login", {
    "status": 200,
    "body": {"token": "abc123"},
    "headers": {"Content-Type": "application/json"}
})

# Iniciar
server.start()

# ... ejecutar pruebas contra http://localhost:9090 ...

# Detener
server.stop()
```

153. Tema: Mock Server - Agregar rutas con métodos HTTP específicos
Descripcion: El MockServer tiene métodos dedicados para cada verbo HTTP: `mock.get(path, response)`, `mock.post(path, response)`, `mock.put(path, response)`, `mock.delete(path, response)`. También se puede usar el método genérico `mock.add_route(method, path, response)` para cualquier método. Cada ruta recibe un path (string) y un diccionario de respuesta con las claves: `status` (código HTTP, por defecto 200), `body` (cuerpo de la respuesta, puede ser dict o string), y `headers` (diccionario de headers opcionales).

154. Tema: Mock Server - Estructura del diccionario de respuesta
Descripcion: Cada ruta del mock server recibe un diccionario de respuesta con la siguiente estructura:
```python
{
    "status": 200,              # Código HTTP (int), por defecto 200
    "body": {"key": "value"},   # Cuerpo de respuesta (dict o string)
    "headers": {                # Headers de respuesta (dict, opcional)
        "Content-Type": "application/json",
        "X-Custom": "valor"
    }
}
```
Si el body es un diccionario, se serializa automáticamente a JSON. Si es un string, se envía tal cual. Si no se define una ruta para un path solicitado, el servidor retorna 404 con `{"error": "Route not found"}`.

155. Tema: Mock Server - Rutas con wildcards (comodines)
Descripcion: El mock server soporta wildcards en las rutas usando el carácter `*`. Esto permite que una sola ruta responda a múltiples paths. Ejemplo: `mock.get("/users/*", response)` responderá a `/users/1`, `/users/abc`, `/users/123/profile`, etc. El wildcard se convierte internamente en una expresión regular `.*` para el matching.

156. Tema: Mock Server - Rutas con condiciones personalizadas
Descripcion: Se pueden agregar condiciones a las rutas para que solo respondan cuando se cumple cierta lógica. La condición es una función que recibe un diccionario con los datos del request (`method`, `path`, `query`, `body`, `headers`) y retorna True/False. Ejemplo:
```python
# Solo responder si el header Authorization está presente
def requiere_auth(request):
    return "Authorization" in request["headers"]

mock.get("/api/protected", {
    "status": 200,
    "body": {"data": "secret"}
}, condition=requiere_auth)

# Sin auth, retorna 404. Con auth, retorna los datos.
```

157. Tema: Mock Server - Limpiar rutas y obtener URL
Descripcion: El mock server ofrece métodos utilitarios: `mock.clear_routes()` elimina todas las rutas configuradas (útil para resetear entre tests), `mock.get_url()` retorna la URL completa del servidor (ej: `http://localhost:8080`), `mock.is_running()` retorna True/False indicando si el servidor está activo.

158. Tema: Mock Server - Usar como fixture de Behave en features
Descripcion: Judo incluye un fixture de Behave para iniciar y detener el mock server automáticamente. Se usa con el tag `@fixture.mock_server` en el feature. El fixture inicia el servidor antes del scenario y lo detiene al finalizar. El mock queda disponible en `context.mock_server`. Además, el hook `after_all` de Judo detiene automáticamente cualquier mock server que esté corriendo al finalizar todas las pruebas.

159. Tema: Mock Server - Ejemplo completo simulando una API REST
Descripcion: Ejemplo completo de cómo configurar un mock server que simula una API REST con múltiples endpoints:
```python
from judo.mock.server import MockServer

mock = MockServer(port=8080)

# GET /health - Health check
mock.get("/health", {
    "status": 200,
    "body": {"status": "ok", "version": "1.0.0"}
})

# GET /api/users - Lista de usuarios
mock.get("/api/users", {
    "status": 200,
    "body": [
        {"id": 1, "name": "Juan", "email": "juan@ejemplo.com"},
        {"id": 2, "name": "Ana", "email": "ana@ejemplo.com"}
    ],
    "headers": {"Content-Type": "application/json"}
})

# GET /api/users/* - Usuario por ID (wildcard)
mock.get("/api/users/*", {
    "status": 200,
    "body": {"id": 1, "name": "Juan", "email": "juan@ejemplo.com"}
})

# POST /api/users - Crear usuario
mock.post("/api/users", {
    "status": 201,
    "body": {"id": 3, "name": "Nuevo Usuario", "message": "Created"}
})

# DELETE /api/users/* - Eliminar usuario
mock.delete("/api/users/*", {
    "status": 204,
    "body": ""
})

mock.start()
# Ahora se pueden ejecutar pruebas contra http://localhost:8080
```

160. Tema: Mock Server - Ejemplo simulando errores y respuestas de error
Descripcion: El mock server puede simular respuestas de error para probar el manejo de errores de la aplicación:
```python
from judo.mock.server import MockServer

mock = MockServer(port=8080)

# Simular error 401 Unauthorized
mock.get("/api/private", {
    "status": 401,
    "body": {"error": "Unauthorized", "message": "Token inválido"}
})

# Simular error 500 Internal Server Error
mock.get("/api/broken", {
    "status": 500,
    "body": {"error": "Internal Server Error"}
})

# Simular error 429 Too Many Requests
mock.get("/api/limited", {
    "status": 429,
    "body": {"error": "Rate limit exceeded"},
    "headers": {"Retry-After": "60"}
})

mock.start()
```

161. Tema: Mock Server - Uso combinado con pruebas BDD en features
Descripcion: Para usar el mock server en pruebas BDD, se configura en el `environment.py` y se apunta la URL base al mock. Ejemplo de flujo: 1) En `before_all` o `before_feature`, iniciar el mock con `context.judo_context.judo.start_mock(port=8080)` y agregar las rutas necesarias. 2) En el feature, configurar la URL base como `http://localhost:8080`. 3) Ejecutar las peticiones normalmente contra el mock. 4) El mock se detiene automáticamente en `after_all`. Esto permite ejecutar pruebas sin depender de servicios externos.

162. Tema: Nota sobre Playwright - Removido del framework
Descripcion: Playwright fue removido como dependencia obligatoria en la versión 1.4.0. Judo Framework se enfoca exclusivamente en pruebas de API. La eliminación redujo el tamaño de instalación en un 90% (de 150MB a 10MB) y el tiempo de instalación en un 95%. Si se necesita automatización de navegador, se debe instalar Playwright por separado con `pip install playwright && playwright install chromium`, pero no es parte del framework Judo.


163. Tema: GenAI Testing - Qué es y para qué sirve
Descripcion: Judo Framework incluye un módulo para evaluar respuestas de sistemas de Inteligencia Artificial Generativa. El enfoque es: primero obtienes la respuesta de tu API GenAI usando los pasos REST normales de Judo, luego usas los pasos de evaluación para verificar la calidad de esa respuesta. Hay tres estrategias: RAG (comparar contra documentos o bases de datos), validaciones semánticas (similitud, relevancia, toxicidad, etc.) y LLM como juez (usar un modelo de IA para evaluar la calidad). Importar en environment.py: `from judo.genai.steps_genai import *` (inglés) o `from judo.genai.steps_genai_es import *` (español).

164. Tema: GenAI Testing - Flujo de trabajo correcto
Descripcion: El flujo correcto tiene 3 pasos: 1) Llamar al endpoint de tu API GenAI con pasos REST normales (`When I send POST request to "/chat"`). 2) Extraer el campo de respuesta con el paso de conexión (`And I use response field "answer" as AI response`). 3) Evaluar con una o más estrategias (RAG, semántica, juez). Los pasos de evaluación GenAI NO hacen llamadas HTTP por sí solos — trabajan sobre el texto ya obtenido por los pasos REST.

165. Tema: GenAI Testing - Configuración en .env (solo para el juez LLM)
Descripcion: Las variables de entorno solo son necesarias si usas la estrategia LLM como juez. Las validaciones semánticas y RAG no requieren API key. Variables para el juez: `JUDO_AI_PROVIDER` (openai, claude o gemini), `JUDO_AI_MODEL` (ej: gpt-4o), `JUDO_OPENAI_API_KEY` / `JUDO_CLAUDE_API_KEY` / `JUDO_GEMINI_API_KEY`, `JUDO_AI_TEMPERATURE` (default 0.0), `JUDO_AI_TIMEOUT` (default 60). Dependencias opcionales: `pip install openai` / `pip install anthropic` / `pip install google-generativeai`.

166. Tema: GenAI Testing - Paso de conexión: extraer campo de respuesta
Descripcion: Después de hacer una llamada REST, se extrae el campo que contiene la respuesta de IA. En inglés: `And I use response field "answer" as AI response`. Soporta notación de punto para campos anidados: `And I use response field "data.choices.0.message.content" as AI response`. Con valor por defecto: `And I use response field "answer" as AI response with fallback "sin respuesta"`. En español: `Y uso el campo de respuesta "respuesta" como respuesta de IA`. También se puede establecer manualmente: `And I set AI response text to "texto"` o desde una variable: `And I use variable "mi_var" as AI response`.

167. Tema: GenAI Testing - Paso de conexión: almacenar texto evaluado en variable
Descripcion: Para reutilizar el texto de respuesta en otros pasos o features. En inglés: `And I store AI response text in variable "ai_result"`. En español: `Y almaceno el texto de respuesta de IA en la variable "resultado_ia"`. La variable queda disponible para interpolación en pasos REST siguientes o para comparaciones.

168. Tema: GenAI Testing - Estrategia RAG: cargar contexto desde archivo local
Descripcion: Carga un documento local como contexto de referencia para comparar contra la respuesta de IA. Formatos soportados: .txt, .md, .json, .yaml, .csv, .pdf (requiere `pip install pypdf`), .docx (requiere `pip install python-docx`). En inglés: `Given I load RAG context from file "docs/manual.pdf"`. En español: `Dado que cargo el contexto RAG desde el archivo "docs/manual.pdf"`. El contenido del archivo se usa como verdad de referencia en las evaluaciones siguientes.

169. Tema: GenAI Testing - Estrategia RAG: cargar contexto desde URL
Descripcion: Obtiene contenido de una URL y lo usa como contexto RAG. Útil para documentación online, APIs de conocimiento o bases de datos accesibles por HTTP. En inglés: `Given I load RAG context from URL "https://docs.miapi.com/faq"`. En español: `Dado que cargo el contexto RAG desde la URL "https://docs.miapi.com/faq"`. Requiere `pip install requests`.

170. Tema: GenAI Testing - Estrategia RAG: cargar múltiples archivos
Descripcion: Carga varios documentos como contexto RAG combinado. Se usa una tabla con columna `file` (inglés) o `archivo` (español). En inglés: `Given I load RAG context from multiple files` con tabla `| file |`. En español: `Dado que cargo el contexto RAG desde múltiples archivos` con tabla `| archivo |`. Los contenidos se concatenan con separadores para formar un contexto unificado.

171. Tema: GenAI Testing - Estrategia RAG: establecer contexto inline
Descripcion: Define el contexto RAG directamente en el feature sin cargar archivos. Útil para contextos pequeños o datos de prueba. En inglés: `Given I set RAG context` con bloque multilínea `"""..."""` o `Given I set RAG context "texto corto"`. En español: `Dado que establezco el contexto RAG` con bloque multilínea o `Dado que establezco el contexto RAG como "texto"`.

172. Tema: GenAI Testing - Estrategia RAG: verificar fundamentación (anti-alucinación)
Descripcion: Verifica que la respuesta de IA está fundamentada en el contexto RAG cargado. Detecta alucinaciones — contenido inventado no respaldado por el contexto. En inglés: `Then the AI response should be grounded in RAG context with threshold 0.7`. En español: `Entonces la respuesta de IA debe estar fundamentada en el contexto RAG con umbral 0.7`. Umbral recomendado: 0.6-0.8. Un umbral de 0.7 significa que al menos el 70% de las oraciones de la respuesta deben tener soporte en el contexto.

173. Tema: GenAI Testing - Estrategia RAG: verificar hechos del contexto
Descripcion: Verifica que la respuesta contiene términos y hechos clave extraídos automáticamente del contexto RAG. En inglés: `Then the AI response should contain RAG facts with threshold 0.6`. En español: `Entonces la respuesta de IA debe contener hechos del contexto RAG con umbral 0.6`. Umbral recomendado: 0.5-0.8. Complementa la verificación de fundamentación con un enfoque en términos específicos.

174. Tema: GenAI Testing - Estrategia RAG: similitud semántica con el contexto
Descripcion: Verifica que la respuesta es semánticamente similar al contexto RAG, asegurando que se mantiene en el mismo tema. En inglés: `Then the AI response semantic similarity to RAG context should be at least 0.5`. En español: `Entonces la similitud semántica de la respuesta de IA con el contexto RAG debe ser al menos 0.5`. Umbral recomendado: 0.4-0.7. Requiere `pip install scikit-learn` para mejor precisión.

175. Tema: GenAI Testing - Validaciones semánticas: básicas
Descripcion: Pasos para validar propiedades básicas del texto de respuesta. No vacía: `Then the AI response should not be empty` / `Entonces la respuesta de IA no debe estar vacía`. Contiene texto: `Then the AI response should contain "Paris"` / `Entonces la respuesta de IA debe contener "París"`. No contiene: `Then the AI response should not contain "error"` / `Entonces la respuesta de IA no debe contener "error"`. Longitud máxima: `Then the AI response length should be less than 500 characters`. Longitud mínima: `Then the AI response length should be more than 50 characters`.

176. Tema: GenAI Testing - Validaciones semánticas: similitud con respuesta esperada
Descripcion: Compara la respuesta de IA con una respuesta esperada conocida. Usa tres niveles de precisión según las dependencias instaladas: 1) Sentence Transformers (mejor, embeddings semánticos reales — `pip install sentence-transformers`), 2) TF-IDF scikit-learn (bueno — `pip install scikit-learn`), 3) Jaccard (básico, sin dependencias). En inglés: `Then the AI response semantic similarity to "Tokyo is the capital of Japan." should be at least 0.5`. En español: `Entonces la similitud semántica de la respuesta de IA con "Tokio es la capital de Japón." debe ser al menos 0.5`. Umbral recomendado: 0.5-0.8.

177. Tema: GenAI Testing - Validaciones semánticas: relevancia al prompt
Descripcion: Verifica que la respuesta es relevante para la pregunta o prompt original. Usa solapamiento de palabras clave entre el prompt y la respuesta. En inglés: `Then the AI response should be relevant to "What is machine learning?" with threshold 0.4`. En español: `Entonces la respuesta de IA debe ser relevante para "¿Qué es el aprendizaje automático?" con umbral 0.4`. Umbral recomendado: 0.3-0.6.

178. Tema: GenAI Testing - Validaciones semánticas: toxicidad
Descripcion: Detecta contenido tóxico, dañino o inapropiado en la respuesta. Puntuación 1.0 = limpio, 0.0 = muy tóxico. En inglés: `Then the AI response should not be toxic with threshold 0.9`. En español: `Entonces la respuesta de IA no debe ser tóxica con umbral 0.9`. Umbral recomendado: 0.8-0.95 para contenido de producción. No requiere API key externa.

179. Tema: GenAI Testing - Validaciones semánticas: hechos requeridos
Descripcion: Verifica que la respuesta contiene hechos específicos definidos en una tabla. En inglés: `Then the AI response should contain required facts` con tabla de columna `fact`. En español: `Entonces la respuesta de IA debe contener los hechos requeridos` con tabla de columna `hecho`. Ejemplo: verificar que una respuesta sobre Python menciona "Python", "programación", "lenguaje". El umbral se puede definir en la tabla con columna `threshold` / `umbral`.

180. Tema: GenAI Testing - Validaciones semánticas: tono
Descripcion: Verifica que la respuesta tiene el tono esperado. Tonos soportados: `professional` (usa conectores lógicos y vocabulario formal), `friendly` (usa palabras positivas y amigables), `formal` (vocabulario legal/académico), `concise` (menos de 100 palabras), `empathetic` (muestra comprensión y apoyo). En inglés: `Then the AI response tone should be "professional" with threshold 0.4`. En español: `Entonces el tono de la respuesta de IA debe ser "professional" con umbral 0.4`. Umbral recomendado: 0.3-0.6.

181. Tema: GenAI Testing - Validaciones semánticas: completitud de temas
Descripcion: Verifica que la respuesta cubre todos los temas requeridos definidos en una tabla. En inglés: `Then the AI response should cover required topics with threshold 0.8` con tabla de columna `topic`. En español: `Entonces la respuesta de IA debe cubrir los temas requeridos con umbral 0.8` con tabla de columna `tema`. Ejemplo: verificar que una explicación de HTTP menciona GET, POST, PUT y DELETE. Umbral recomendado: 0.7-0.9.

182. Tema: GenAI Testing - Estrategia LLM como juez: configurar el juez
Descripcion: Por defecto el juez usa el proveedor configurado en `JUDO_AI_PROVIDER` del .env. Para usar un modelo específico como juez (recomendado: usar el modelo más potente disponible): En inglés: `Given I configure judge AI with provider "openai" and model "gpt-4o"`. En español: `Dado que configuro el juez de IA con proveedor "openai" y modelo "gpt-4o"`. Permite usar un modelo diferente al que genera las respuestas, por ejemplo GPT-4o evalúa respuestas de GPT-4o-mini.

183. Tema: GenAI Testing - Estrategia LLM como juez: establecer prompt y criterios
Descripcion: Antes de evaluar, se puede establecer el prompt original para que el juez tenga contexto. En inglés: `Given I set judge prompt "¿Qué es REST?"`. En español: `Dado que establezco el prompt del juez como "¿Qué es REST?"`. Los criterios de evaluación se pueden establecer por separado: `Given I set judge criteria "criterio"` / `Dado que establezco el criterio del juez como "criterio"`. O se pasan directamente en el paso de evaluación.

184. Tema: GenAI Testing - Estrategia LLM como juez: evaluar con criterio simple
Descripcion: Usa un LLM para evaluar la respuesta con un criterio en lenguaje natural. El juez retorna puntuación (0.0-1.0), veredicto (PASS/FAIL) y razonamiento detallado. En inglés: `Then I evaluate the AI response as judge with criteria "criterio" and threshold 0.7`. En español: `Entonces evalúo la respuesta de IA con el juez usando criterio "criterio" y umbral 0.7`. Luego verificar: `Then the judge evaluation should pass` / `Entonces la evaluación del juez debe pasar`.

185. Tema: GenAI Testing - Estrategia LLM como juez: evaluar con rúbrica multilínea
Descripcion: Para criterios complejos con múltiples dimensiones, usar bloque multilínea. En inglés: `Then I evaluate the AI response as judge with threshold 0.7` seguido de bloque `"""rúbrica detallada..."""`. En español: `Entonces evalúo la respuesta de IA con el juez usando umbral 0.7` con bloque multilínea. Permite definir rúbricas con múltiples puntos como: ser preciso, ser conciso, usar lenguaje profesional, no inventar información.

186. Tema: GenAI Testing - Estrategia LLM como juez: evaluar contra contexto RAG
Descripcion: Combina RAG y LLM como juez — el juez recibe el contexto RAG como verdad de referencia para evaluar si la respuesta es factualmente consistente. En inglés: `Then I evaluate the AI response as judge against RAG context with criteria "criterio" and threshold 0.7`. En español: `Entonces evalúo la respuesta de IA con el juez contra el contexto RAG usando criterio "criterio" y umbral 0.7`. También disponible con criterios multilínea. Es la combinación más poderosa para testing de sistemas RAG.

187. Tema: GenAI Testing - Estrategia LLM como juez: verificar resultado
Descripcion: Después de evaluar, verificar que pasó: `Then the judge evaluation should pass` / `Entonces la evaluación del juez debe pasar`. Para verificar puntuación mínima específica: `Then the judge score should be at least 0.8` / `Entonces la puntuación del juez debe ser al menos 0.8`. Para debug: `And I print the judge evaluation result` / `Y imprimo el resultado de la evaluación del juez` (imprime veredicto, puntuación, umbral y razonamiento completo).

188. Tema: GenAI Testing - Ejemplo completo: RAG con documento local
Descripcion: Flujo completo usando RAG con un documento local:
```gherkin
Dado que cargo el contexto RAG desde el archivo "docs/manual_producto.pdf"
Y establezco el prompt del juez como "¿Cuál es el precio del plan básico?"
Cuando envío una petición POST a "/chat" con el cuerpo
  """
  {"pregunta": "¿Cuál es el precio del plan básico?"}
  """
Entonces el código de respuesta debe ser 200
Y uso el campo de respuesta "respuesta" como respuesta de IA
Y la respuesta de IA no debe estar vacía
Y la respuesta de IA debe estar fundamentada en el contexto RAG con umbral 0.6
Y la respuesta de IA debe contener hechos del contexto RAG con umbral 0.5
```

189. Tema: GenAI Testing - Ejemplo completo: validaciones semánticas
Descripcion: Flujo completo usando validaciones semánticas sin API key externa:
```gherkin
Cuando envío una petición POST a "/ai/explain" con el cuerpo
  """
  {"topic": "HTTP methods"}
  """
Entonces el código de respuesta debe ser 200
Y uso el campo de respuesta "explanation" como respuesta de IA
Y la respuesta de IA no debe estar vacía
Y la respuesta de IA no debe ser tóxica con umbral 0.9
Y la respuesta de IA debe ser relevante para "HTTP methods" con umbral 0.4
Y la respuesta de IA debe cubrir los temas requeridos con umbral 0.8
  | topic  |
  | GET    |
  | POST   |
  | DELETE |
```

190. Tema: GenAI Testing - Ejemplo completo: LLM como juez
Descripcion: Flujo completo usando LLM como juez con rúbrica multilínea:
```gherkin
Dado que configuro el juez de IA con proveedor "openai" y modelo "gpt-4o"
Y establezco el prompt del juez como "Explica qué es una API REST"
Cuando envío una petición POST a "/ai/explain" con el cuerpo
  """
  {"question": "Explica qué es una API REST"}
  """
Entonces el código de respuesta debe ser 200
Y uso el campo de respuesta "answer" como respuesta de IA
Y evalúo la respuesta de IA con el juez usando umbral 0.7
  """
  La respuesta debe:
  1. Explicar correctamente qué es una API REST
  2. Mencionar al menos un método HTTP
  3. Ser comprensible para un no técnico
  4. No contener información incorrecta
  """
Y la evaluación del juez debe pasar
Y imprimo el resultado de la evaluación del juez
```

191. Tema: GenAI Testing - Ejemplo completo: combinación de las 3 estrategias
Descripcion: Flujo completo combinando RAG + validaciones semánticas + LLM como juez para máxima cobertura:
```gherkin
Dado que cargo el contexto RAG desde el archivo "docs/politica_soporte.txt"
Y configuro el juez de IA con proveedor "openai" y modelo "gpt-4o"
Y establezco el prompt del juez como "¿Cómo soluciono el error de conexión?"
Cuando envío una petición POST a "/support/ai" con el cuerpo
  """
  {"issue": "Connection timeout error"}
  """
Entonces el código de respuesta debe ser 200
Y uso el campo de respuesta "solution" como respuesta de IA
Y la respuesta de IA no debe ser tóxica con umbral 0.9
Y la respuesta de IA debe estar fundamentada en el contexto RAG con umbral 0.5
Y el tono de la respuesta de IA debe ser "professional" con umbral 0.4
Y evalúo la respuesta de IA con el juez contra el contexto RAG usando criterio "La respuesta debe dar pasos concretos y ser consistente con la documentación." y umbral 0.7
Y la evaluación del juez debe pasar
```

192. Tema: GenAI Testing - Arquitectura del módulo judo.genai
Descripcion: El módulo `judo.genai` está compuesto por: `client.py` (GenAIClient — cliente unificado para OpenAI, Claude y Gemini, usado solo por el juez), `judge.py` (GenAIJudge — implementa LLM-as-a-Judge), `context_loader.py` (ContextLoader — carga documentos de múltiples formatos para RAG), `evaluators.py` (7 evaluadores: SemanticSimilarityEvaluator, RelevanceEvaluator, ToxicityEvaluator, FactualAccuracyEvaluator, HallucinationEvaluator, ToneEvaluator, CompletenessEvaluator), `models.py` (GenAIConfig, JudgeResult, EvaluationResult), `steps_genai.py` (pasos en inglés), `steps_genai_es.py` (pasos en español).

193. Tema: GenAI Testing - Dependencias opcionales por funcionalidad
Descripcion: Las dependencias son opcionales y solo se instalan según lo que se use. Instalar todo con `pip install judo-framework[genai]`. Por funcionalidad: juez con OpenAI `pip install openai`, juez con Claude `pip install anthropic`, juez con Gemini `pip install google-generativeai`. Similitud semántica (mejor calidad): `pip install sentence-transformers` — usa embeddings reales con modelo all-MiniLM-L6-v2. Similitud semántica (media): `pip install scikit-learn` — usa TF-IDF. Sin dependencias: Jaccard como fallback automático. Contexto RAG desde PDF: `pip install pypdf`. Contexto RAG desde DOCX: `pip install python-docx`. Las validaciones de toxicidad, relevancia, tono, completitud y hechos no requieren ninguna dependencia adicional.

194. Tema: GenAI Testing - Modelos recomendados para el juez LLM
Descripcion: Para el juez se recomienda usar el modelo más potente disponible para obtener evaluaciones más precisas. OpenAI: `gpt-4o` (mejor calidad), `gpt-4o-mini` (más económico). Anthropic Claude: `claude-3-5-sonnet-20241022` (mejor balance), `claude-3-opus-20240229` (máxima calidad). Google Gemini: `gemini-1.5-pro` (mejor calidad), `gemini-1.5-flash` (más rápido). Patrón recomendado: usar el modelo más económico para generar respuestas (vía REST) y el más potente como juez evaluador.

195. Tema: GenAI Testing - Nota sobre Playwright
Descripcion: Playwright fue removido del framework en la versión 1.4.0. Judo Framework se enfoca exclusivamente en pruebas de API. Si se necesita automatización de navegador, instalar por separado: `pip install playwright && playwright install chromium`. No es parte del módulo GenAI ni del framework Judo.
