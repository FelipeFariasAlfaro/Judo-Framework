# Ejemplo de Migración - Para Usuario Actual

## 📋 Tu Environment.py Actual

```python
# environment.py - ACTUAL
from judo.behave import *

before_all = before_all_judo
before_feature = before_feature_judo
after_feature = after_feature_judo
before_scenario = before_scenario_judo
after_scenario = after_scenario_judo
before_step = before_step_judo
after_step = after_step_judo
after_all = after_all_judo
```

## 🎯 Opciones de Migración

### Opción 1: Sin Cambios (Solo API)

**Cambios requeridos**: **NINGUNO** ❌

```python
# environment.py - MANTENER EXACTAMENTE IGUAL
from judo.behave import *

before_all = before_all_judo
before_feature = before_feature_judo
after_feature = after_feature_judo
before_scenario = before_scenario_judo
after_scenario = after_scenario_judo
before_step = before_step_judo
after_step = after_step_judo
after_all = after_all_judo
```

**Resultado**: Todo funciona exactamente igual que antes.

---

### Opción 2: Agregar UI Testing (Recomendado)

**Cambios requeridos**: **Solo variables de entorno** ✅

#### Paso 1: Instalar Playwright (una sola vez)
```bash
pip install 'judo-framework[browser]'
playwright install
```

#### Paso 2: Crear archivo .env
```bash
# .env - NUEVO ARCHIVO
JUDO_USE_BROWSER=true
JUDO_BROWSER=chromium
JUDO_HEADLESS=false
JUDO_SCREENSHOTS=true
```

#### Paso 3: Environment.py
```python
# environment.py - SIN CAMBIOS
from judo.behave import *

before_all = before_all_judo
before_feature = before_feature_judo
after_feature = after_feature_judo
before_scenario = before_scenario_judo
after_scenario = after_scenario_judo
before_step = before_step_judo
after_step = after_step_judo
after_all = after_all_judo
```

**Resultado**: 
- ✅ Todos tus tests API funcionan igual
- ✅ Nuevos steps de UI disponibles
- ✅ Screenshots automáticos en fallos
- ✅ Testing híbrido disponible

---

### Opción 3: Control Total (Avanzado)

**Cambios requeridos**: **Modificar environment.py** ⚙️

```python
# environment.py - VERSIÓN AVANZADA
from judo.behave import *

# Importar funciones de Playwright (solo si quieres control total)
try:
    from judo.playwright.hooks import integrate_playwright_hooks, configure_playwright_from_env
    playwright_config = configure_playwright_from_env()
    PLAYWRIGHT_ENABLED = playwright_config.get('use_browser', False)
except ImportError:
    PLAYWRIGHT_ENABLED = False

def before_all(context):
    # Llamar tu hook original
    before_all_judo(context)
    
    # Agregar Playwright si está habilitado
    if PLAYWRIGHT_ENABLED:
        integrate_playwright_hooks(context, 'before_all')
        print("🎭 Browser testing enabled")

def before_scenario(context, scenario):
    before_scenario_judo(context, scenario)
    if PLAYWRIGHT_ENABLED:
        integrate_playwright_hooks(context, 'before_scenario', scenario)

def after_scenario(context, scenario):
    if PLAYWRIGHT_ENABLED:
        integrate_playwright_hooks(context, 'after_scenario', scenario)
    after_scenario_judo(context, scenario)

def after_all(context):
    if PLAYWRIGHT_ENABLED:
        integrate_playwright_hooks(context, 'after_all')
    after_all_judo(context)

# Mantener hooks originales
before_feature = before_feature_judo
after_feature = after_feature_judo
before_step = before_step_judo
after_step = after_step_judo
```

**Resultado**: Control completo sobre cuándo y cómo se usa Playwright.

## 🧪 Ejemplos de Tests

### Test API (Funciona con cualquier opción)

```gherkin
# features/api_test.feature
Feature: API Testing
  Scenario: Create user
    Given I have a Judo API client
    And the base URL is "https://api.example.com"
    When I send a POST request to "/users" with JSON:
      """
      {"name": "John", "email": "john@example.com"}
      """
    Then the response status should be 201
    And the response should contain "id"
```

### Test UI (Solo con Opción 2 o 3)

```gherkin
# features/ui_test.feature
Feature: UI Testing
  @ui
  Scenario: Login form
    Given I start a browser
    When I navigate to "https://app.example.com/login"
    And I fill "#username" with "john_doe"
    And I fill "#password" with "secret123"
    And I click on "#login-button"
    Then the element "#dashboard" should be visible
    And I take a screenshot named "successful_login"
```

### Test Híbrido (Solo con Opción 2 o 3)

```gherkin
# features/hybrid_test.feature
Feature: Hybrid API + UI Testing
  @hybrid
  Scenario: Create user via API and verify in UI
    # Crear usuario por API
    Given I have a Judo API client
    And the base URL is "https://api.example.com"
    When I send a POST request to "/users" with JSON:
      """
      {"name": "John Doe", "email": "john@example.com"}
      """
    Then the response status should be 201
    And I extract "$.id" from the API response and store it as "userId"
    
    # Verificar en UI
    Given I start a browser
    When I navigate to "https://app.example.com/users/{userId}"
    Then the element "#user-name" should contain "John Doe"
    And I take a screenshot named "user_profile"
```

## 🚀 Comandos de Ejecución

```bash
# Ejecutar solo tests API (funciona con cualquier opción)
behave --tags=@api

# Ejecutar solo tests UI (requiere Opción 2 o 3)
behave --tags=@ui

# Ejecutar tests híbridos (requiere Opción 2 o 3)
behave --tags=@hybrid

# Ejecutar todos los tests
behave

# Ejecutar en modo headless (para CI/CD)
JUDO_HEADLESS=true behave

# Ejecutar con screenshots deshabilitados
JUDO_SCREENSHOTS=false behave
```

## 📊 Comparación de Opciones

| Característica | Opción 1<br>(Sin cambios) | Opción 2<br>(Variables env) | Opción 3<br>(Control total) |
|----------------|---------------------------|----------------------------|----------------------------|
| **Cambios en código** | ❌ Ninguno | ❌ Ninguno | ✅ Modificar environment.py |
| **API Testing** | ✅ Funciona | ✅ Funciona | ✅ Funciona |
| **UI Testing** | ❌ No disponible | ✅ Disponible | ✅ Disponible |
| **Testing Híbrido** | ❌ No disponible | ✅ Disponible | ✅ Disponible |
| **Screenshots** | ❌ No disponible | ✅ Automáticos | ✅ Configurables |
| **Configuración** | ❌ Ninguna | ✅ Variables env | ✅ Código personalizado |
| **Complejidad** | 🟢 Muy simple | 🟡 Simple | 🔴 Avanzado |

## 🎯 Recomendación

**Para empezar**: Usa **Opción 2** (Variables de entorno)

1. **Instala Playwright**: `pip install 'judo-framework[browser]' && playwright install`
2. **Crea .env**: Con las variables mostradas arriba
3. **No cambies environment.py**: Mantén tu código actual
4. **Prueba**: Ejecuta tus tests existentes (deben funcionar igual)
5. **Experimenta**: Crea un test simple con `@ui` tag

**Ventajas**:
- ✅ Cero riesgo (tu código actual no cambia)
- ✅ Fácil de revertir (solo eliminar .env)
- ✅ Todas las funcionalidades disponibles
- ✅ Configuración flexible con variables

**Si necesitas más control**: Migra a **Opción 3** más adelante.

## 🔧 Variables de Entorno Completas

```bash
# .env - Configuración completa
# Básico
JUDO_USE_BROWSER=true
JUDO_BROWSER=chromium
JUDO_HEADLESS=false

# Screenshots
JUDO_SCREENSHOTS=true
JUDO_SCREENSHOT_ON_FAILURE=true
JUDO_SCREENSHOT_DIR=screenshots

# Comportamiento
JUDO_AUTO_START_BROWSER=true
JUDO_CLOSE_BROWSER_AFTER_SCENARIO=false

# Viewport
JUDO_VIEWPORT_WIDTH=1280
JUDO_VIEWPORT_HEIGHT=720

# API (existentes - no cambiar)
JUDO_SAVE_REQUESTS_RESPONSES=true
JUDO_OUTPUT_DIRECTORY=judo_reports
```

---

## ✅ Resumen para Ti

**Tu situación actual**: Environment.py simple y funcional

**Para seguir igual**: No hagas nada ❌

**Para agregar UI testing**: 
1. Instalar: `pip install 'judo-framework[browser]' && playwright install`
2. Crear .env con `JUDO_USE_BROWSER=true`
3. Mantener tu environment.py sin cambios ✅

**Resultado**: Todas tus funcionalidades actuales + nuevas capacidades de UI testing, sin riesgo ni breaking changes.

¡Es así de simple! 🚀