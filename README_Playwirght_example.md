# 🥋 Judo Framework - Proyecto de Demostración

## 📋 Descripción

Este proyecto es una **demostración completa** de las capacidades de **Judo Framework**, un potente framework de testing de APIs basado en BDD (Behavior Driven Development) que utiliza Behave como base.

El proyecto incluye ejemplos prácticos de testing de APIs REST, validaciones avanzadas, manejo de datos, flujos de trabajo complejos y mucho más.

## 🎯 ¿Qué es Judo Framework?

Judo Framework es una herramienta que permite escribir tests de API de manera **declarativa y legible**, usando lenguaje natural (Gherkin) para describir los casos de prueba. Elimina la complejidad de escribir código de testing manual y se enfoca en **qué** probar, no en **cómo** probarlo.

### ✨ Características Principales

- 🌐 **Testing de APIs REST completo** (GET, POST, PUT, PATCH, DELETE)
- ✅ **Validaciones avanzadas** (JSONPath, esquemas, arrays, tipos de datos)
- 🔄 **Flujos de trabajo complejos** (CRUD, autenticación, peticiones encadenadas)
- 📁 **Manejo de archivos** (JSON externos, respuestas guardadas, variables)
- 🌍 **Soporte multiidioma** (inglés y español)
- 📊 **Reportes detallados** (HTML, JSON, logs de API)
- 🔧 **Configuración flexible** y fácil de usar

## 🚀 Inicio Rápido

### 1. **Prerrequisitos**

```bash
# Python 3.7 o superior
python --version

# Pip actualizado
pip install --upgrade pip
```

### 2. **Instalación**

```bash

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

pip install judo-framework

# Opcional: instalar judo y otras librerías
pip install -r requirements.txt

# Para testing de Frontend, instalar Playwright
pip install playwright
playwright install chromium


```

> **📝 Nota Importante:** Judo Framework se instala con `pip install judo-framework` (con guión), no `judo_framework` (con guión bajo).

### **📦 Archivos de Requirements Disponibles:**

- **`requirements.txt`** - Dependencias principales + utilidades recomendadas


## 🏃 Ejecutar Tests

### **Opción 1: Usando el Runner Personalizado (Recomendado)**

```bash
# Navegar al directorio Runner
cd Runner

# Ejecutar todos los tests (API + Frontend si están configurados)
python runner.py
```

**Ventajas del Runner:**
- ✅ Configuración optimizada
- ✅ Reportes HTML automáticos con screenshots
- ✅ Logs detallados de API
- ✅ Organización de resultados
- ✅ Soporte para tests mixtos (API + Frontend)

### **Opción 2: Usando Behave Directamente**

```bash
# Desde la raíz del proyecto

# Ejecutar todos los tests en inglés
behave features/ --tags=@eng_examples_all

# Ejecutar todos los tests en español
behave features/ --tags=@es_ejecutar_todo

# Ejecutar tests específicos por categoría
behave features/ --tags=@http          # Tests de métodos HTTP
behave features/ --tags=@validation    # Tests de validación
behave features/ --tags=@workflow      # Flujos de trabajo
behave features/ --tags=@files         # Operaciones con archivos
behave features/ --tags=@test-front    # Tests de Frontend con Playwright

# Ejecutar tests mixtos (API + Frontend)
behave features/ --tags=@mix

# Ejecutar con formato detallado
behave features/ --tags=@eng_examples_all --format=pretty

# Ejecutar tests específicos
behave features/ --tags=@get_en        # Solo tests GET en inglés
behave features/ --tags=@post          # Solo tests POST
```

### **Opción 3: Tests Específicos**

```bash
# Test de un escenario específico
behave features/all_examples.feature:15  # Línea específica

# Tests con nombre específico
behave features/ --name="GET request"

# Tests excluyendo algunos tags
behave features/ --tags="@eng_examples_all and not @slow"
```

## 📊 Ver Resultados

### **Reportes HTML**
Después de ejecutar con el Runner, abre:
```
Runner/judo_reports/test_execution_report.html
```

### **Logs de API**
Revisa las peticiones y respuestas detalladas en:
```
Runner/judo_reports/api_logs/
```

### **Reportes JSON**
Para integración con CI/CD:
```
Runner/judo_reports/cucumber-json/
```

## 📁 Estructura del Proyecto

```
📦 judo-framework-demo/
├── 📁 features/                    # Tests BDD en Gherkin
│   ├── 📄 all_examples.feature     # Ejemplos completos (inglés)
│   ├── 📄 ejemplos_completos.feature # Ejemplos completos (español)
│   ├── 📄 environment.py           # Configuración de Behave
│   └── 📁 steps/                   # Steps personalizados (si los hay)
├── 📁 Runner/                      # Ejecutor personalizado
│   ├── 📄 runner.py                # Runner principal
│   └── 📁 judo_reports/            # Reportes generados
├── 📁 base_requests/               # Datos JSON de entrada
│   ├── 📄 simple_post.json
│   ├── 📄 simple_schema.json
│   └── 📄 update_post.json
├── 📁 base_responses/              # Respuestas guardadas
├── 📁 base_variables/              # Variables extraídas
├── 📄 debug_judo.py                # Script de diagnóstico
├── 📄 .env                         # Variables de entorno
└── 📄 README.md                    # Este archivo
```

## 🎯 Ejemplos de Casos de Uso

### **1. Test Básico de API**
```gherkin
Scenario: GET request - Retrieve a resource
  When I send a GET request to "/users/1"
  Then the response status should be 200
  And the response should contain "id"
  And the response should contain "name"
```

### **2. Test con Datos JSON**
```gherkin
Scenario: POST request - Create a new resource
  When I send a POST request to "/posts" with JSON
    """
    {
      "title": "Judo Framework Test",
      "body": "Testing POST request",
      "userId": 1
    }
    """
  Then the response status should be 201
  And the response field "title" should equal "Judo Framework Test"
```

### **3. Test con Archivos Externos**
```gherkin
Scenario: POST request using JSON file
  When I POST to "/posts" with JSON file "../base_requests/simple_post.json"
  Then the response status should be 201
  And the response should contain "id"
```

### **4. Flujo de Trabajo Complejo**
```gherkin
Scenario: Complete CRUD workflow
  # CREATE
  When I send a POST request to "/posts" with JSON
    """
    {"title": "New Post", "body": "Content", "userId": 1}
    """
  Then the response status should be 201
  And I extract "$.id" from the response as "postId"
  
  # READ
  When I send a GET request to "/posts/{postId}"
  Then the response status should be 200
  
  # UPDATE
  When I send a PUT request to "/posts/{postId}" with JSON
    """
    {"id": 1, "title": "Updated", "body": "Updated", "userId": 1}
    """
  Then the response status should be 200
  
  # DELETE
  When I send a DELETE request to "/posts/{postId}"
  Then the response status should be 200
```

## 📦 Gestión de Dependencias

### **Requirements Files**

El proyecto incluye tres archivos de requirements para diferentes necesidades:

#### **requirements.txt** (Recomendado)
```bash
pip install -r requirements.txt
```
Incluye:
- ✅ Judo Framework (incluye automáticamente behave, requests, jsonpath-ng, etc.)
- ✅ Python-dotenv para variables de entorno
- ✅ Colorama para colores en terminal
- ✅ Dependencias opcionales comentadas

#### **requirements-minimal.txt** (Básico)
```bash
pip install -r requirements-minimal.txt
```
Incluye solo:
- ✅ Judo Framework (con todas sus dependencias automáticas)
- ✅ Python-dotenv (para archivos .env)

#### **requirements-dev.txt** (Desarrollo)
```bash
pip install -r requirements-dev.txt
```
Incluye todo lo anterior más:
- 🧪 Testing (pytest, coverage)
- 🎨 Formateo (black, isort, flake8)
- 📚 Documentación (sphinx, mkdocs)
- 🔧 Herramientas de desarrollo (pre-commit, tox)

### **Para Contribuidores**
```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Configurar pre-commit hooks
pre-commit install
```

## 🔧 Configuración

### **Variables de Entorno (.env)**
```bash
# API Configuration
API_BASE_URL=https://jsonplaceholder.typicode.com
API_TOKEN=Bearer your-token-here
TIMEOUT_SECONDS=30

# Playwright Configuration (Frontend Testing)
JUDO_USE_BROWSER=true              # Activar Playwright
JUDO_SCREENSHOT_DIR=screenshots    # Directorio de screenshots

# Debug Configuration
JUDO_DEBUG_REPORTER=false
JUDO_LOG_LEVEL=INFO
```

### **Personalizar el Runner**
Edita `Runner/runner.py` para:
- Cambiar tags de ejecución
- Modificar directorios de salida
- Habilitar/deshabilitar funciones
- Configurar paralelización

## 🎨 Características Demostradas

### **✅ Métodos HTTP**
- GET, POST, PUT, PATCH, DELETE
- Query parameters
- Headers personalizados
- Autenticación Bearer Token

### **✅ Validaciones**
- Códigos de estado HTTP
- Campos de respuesta específicos
- JSONPath para datos anidados
- Validación de tipos de datos
- Arrays y colecciones
- Esquemas JSON

### **✅ Manejo de Datos**
- Variables dinámicas
- Extracción de datos de respuestas
- Archivos JSON externos
- Variables de entorno
- Almacenamiento de respuestas

### **✅ Flujos Avanzados**
- Operaciones CRUD completas
- Autenticación con tokens
- Peticiones encadenadas
- Tests parametrizados
- Manejo de errores

## 🐛 Troubleshooting

### **Problema: "No module named 'judo'"**
```bash
# Solución: Instalar Judo Framework
pip install judo-framework

# Verificar instalación
python debug_judo.py
```

### **Problema: "No steps found"**
```bash
# Verificar environment.py
cat features/environment.py

# Debe contener:
from judo.behave import *
```

### **Problema: "Connection refused"**
```bash
# Verificar conectividad
curl -I https://jsonplaceholder.typicode.com/users/1

# Verificar proxy si es necesario
export HTTP_PROXY=http://proxy:8080
```

### **Problema: Tests no se ejecutan**
```bash
# Verificar estructura
ls -la features/
ls -la Runner/

# Ejecutar diagnóstico completo
python debug_judo.py
```

## 🌐 Testing de Frontend con Playwright

Este proyecto incluye soporte para **testing de frontend** usando **Playwright**, permitiendo combinar tests de API y UI en el mismo framework.

### **Instalación de Playwright**

```bash
# Instalar Playwright
pip install playwright

# Instalar browsers (Chromium recomendado)
playwright install chromium

# Verificar instalación
playwright --version
```

### **Configuración**

#### **1. Variables de Entorno (.env)**
```bash
# Activar Playwright
JUDO_USE_BROWSER=true

# Configuración de screenshots
JUDO_SCREENSHOT_DIR=screenshots
```

#### **2. Tags de Activación**
Para que Playwright se active, el escenario debe tener uno de estos tags:
- `@test-front`
- `@front`

**Importante:** Ambas condiciones deben cumplirse:
1. ✅ Variable `JUDO_USE_BROWSER=true` en `.env`
2. ✅ Escenario con tag `@test-front` o `@front`

### **Características de Playwright en este Proyecto**

✅ **Navegador en pantalla completa** - Configurado con `no_viewport=True`  
✅ **Screenshots automáticos** - Captura después de cada step  
✅ **Screenshots de página completa** - Usa `full_page=True`  
✅ **Nombres normalizados** - Sin tildes ni caracteres inválidos  
✅ **Integración con reportes** - Screenshots adjuntos al HTML  
✅ **Activación condicional** - Solo se inicia cuando es necesario  
✅ **Sin conflictos con API tests** - Conviven en la misma ejecución  

### **Ejemplo de Test Frontend**

```gherkin
@test-front
Scenario: Navegación en pantalla completa
  Given go to url "https://www.centyc.cl"
  # Screenshot automático capturado después de cada step
```

### **Ejecutar Tests Frontend**

```bash
# Opción 1: Usando el Runner (recomendado)
cd Runner
python runner.py

# Opción 2: Usando Behave directamente
behave features/frontend.feature --tags=@test-front

# Opción 3: Ejecutar tests mixtos (API + Frontend)
behave features/ --tags=@mix
```

### **Estructura de Screenshots**

Los screenshots se guardan en:
```
Runner/judo_reports/screenshots/
├── Given_go_to_url_https_www.centyc.cl__passed.png
├── When_I_click_on_button_passed.png
└── Then_I_should_see_text_passed.png
```

**Formato del nombre:**
```
{Keyword}_{step_name}_{status}.png
```

Ejemplo: `Given_voy_a_la_url_https_www.centyc.cl__passed.png`

### **Steps Disponibles para Frontend**

```gherkin
# Navegación
Given go to url "https://example.com"
Given voy a la url "https://example.com"

# Más steps disponibles en features/steps/steps_examples.py
```

### **Troubleshooting Playwright**

#### **Problema: "Playwright Sync API inside asyncio loop"**
```bash
# Solución: Asegúrate de que solo los escenarios con tags @test-front/@front inicialicen Playwright
# El framework detecta automáticamente y evita conflictos con tests de API
```

#### **Problema: "Browser not found"**
```bash
# Solución: Instalar browsers de Playwright
playwright install chromium

# O instalar todos los browsers
playwright install
```

#### **Problema: Screenshots no aparecen en el reporte**
```bash
# Verificar configuración en .env
JUDO_SCREENSHOT_DIR=screenshots  # Sin "Runner/" al inicio

# Verificar que el escenario tenga el tag correcto
@test-front
Scenario: Mi test frontend
```

#### **Problema: "WinError 123" al guardar screenshot**
```bash
# Causa: Caracteres inválidos en nombre de archivo (: / \ | ? *)
# Solución: El framework normaliza automáticamente los nombres
# Si persiste, verifica que no haya caracteres especiales en el nombre del step
```

### **Mezclar Tests de API y Frontend**

Puedes ejecutar tests de API y Frontend en la misma ejecución:

```gherkin
Feature: Tests Mixtos

  @api
  Scenario: Test de API
    When I send a GET request to "/users/1"
    Then the response status should be 200
    # Playwright NO se inicializa (sin tag @test-front)

  @test-front
  Scenario: Test de Frontend
    Given go to url "https://example.com"
    # Playwright SÍ se inicializa (tiene tag @test-front)
```

**Ventajas:**
- ✅ Sin conflictos entre asyncio y Playwright Sync API
- ✅ Mejor rendimiento (Playwright solo cuando es necesario)
- ✅ Reportes unificados
- ✅ Ejecución flexible

### **Configuración Avanzada**

Para personalizar Playwright, edita `features/environment.py`:

```python
# Cambiar browser
context.judo_context.browser = context.judo_context.playwright.firefox.launch(...)

# Modo headless
browser_options = {
    'headless': True,  # Sin interfaz gráfica
    'args': ['--start-maximized']
}

# Viewport personalizado (en lugar de pantalla completa)
context.judo_context.browser_context = context.judo_context.browser.new_context(
    viewport={'width': 1920, 'height': 1080}
)
```

## 📚 Recursos Adicionales

### **Documentación**
- [Judo Framework Docs](https://judo-framework.readthedocs.io/)
- [Behave Documentation](https://behave.readthedocs.io/)
- [JSONPath Syntax](https://goessner.net/articles/JsonPath/)

### **API de Testing**
Este proyecto usa [JSONPlaceholder](https://jsonplaceholder.typicode.com/) como API de prueba:
- Gratuita y pública
- No requiere autenticación
- Simula operaciones CRUD
- Perfecta para aprendizaje

## 🤝 Contribuir

¿Quieres añadir más ejemplos o mejorar el proyecto?

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Añade tus cambios y tests
4. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
5. Push a la rama (`git push origin feature/nueva-funcionalidad`)
6. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la [MIT License](LICENSE).

## 🙏 Agradecimientos

- **Judo Framework Team** - Centyc.cl y Felipe Farias, Por crear esta excelente herramienta
- **JSONPlaceholder** - Por proporcionar una API gratuita para testing
- **Behave Community** - Por la base sólida de BDD

---

## 🚀 ¡Empieza Ahora!

```bash
# Clona el proyecto
git clone <repository-url>
cd judo-framework-demo

# Instala Judo Framework y Behave
pip install judo-framework
pip install behave

# Ejecuta los tests
cd Runner
python runner.py

# ¡Disfruta explorando Judo Framework! 🥋
```

**¿Tienes preguntas?** 
Ingresa en https://www.centyc.cl/judo-framwork-es