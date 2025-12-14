# 🚀 Judo Framework - Guía de Instalación Simplificada

## ✨ Nueva Experiencia de Usuario (v1.3.38+)

**¡Ahora es más simple que nunca!** Playwright viene incluido por defecto.

## 📦 Instalación

### Para API Testing + Browser Testing

```bash
# Una sola instalación para todo
pip install judo-framework

# Instalar browsers (solo una vez)
playwright install
```

**¡Eso es todo!** Ya tienes acceso completo a:
- ✅ API Testing (como siempre)
- ✅ Browser Testing (nuevo)
- ✅ Testing Híbrido (API + UI)
- ✅ Screenshots automáticos
- ✅ Reportes integrados

## 🎯 Comparación: Antes vs Ahora

### ❌ Antes (v1.3.37)
```bash
# Confuso para nuevos usuarios
pip install judo-framework                    # Solo API
pip install 'judo-framework[browser]'         # Con browser
playwright install
```

### ✅ Ahora (v1.3.38+)
```bash
# Simple y directo
pip install judo-framework    # Todo incluido
playwright install           # Solo browsers
```

## 🧪 Primer Test

### 1. Crear environment.py
```python
# features/environment.py
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

### 2. Crear .env (opcional)
```bash
# .env - Para habilitar browser testing
JUDO_USE_BROWSER=true
JUDO_BROWSER=chromium
JUDO_HEADLESS=false
JUDO_SCREENSHOTS=true
```

### 3. Crear tu primer test
```gherkin
# features/test_complete.feature
Feature: API + Browser Testing

  @api
  Scenario: Test API
    Given the base URL is "https://jsonplaceholder.typicode.com"
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "name"

  @ui
  Scenario: Test Browser
    Given I start a browser
    When I navigate to "https://example.com"
    Then the element "h1" should be visible
    And I take a screenshot named "example_page"
```

### 4. Ejecutar
```bash
# Todos los tests
behave

# Solo API
behave --tags=@api

# Solo Browser
behave --tags=@ui
```

## 🎉 Beneficios de la Nueva Versión

### ✅ Para Nuevos Usuarios
- **Instalación simple**: Un solo comando
- **Sin confusión**: No hay que entender `[extras]`
- **Capacidades completas**: Todo disponible desde el inicio
- **Mejor onboarding**: Menos fricción para empezar

### ✅ Para Usuarios Existentes
- **Sin breaking changes**: Todo funciona igual
- **Actualización simple**: `pip install --upgrade judo-framework`
- **Misma API**: Todos los métodos y steps funcionan igual
- **Compatibilidad**: Proyectos existentes no necesitan cambios

### ✅ Para Equipos
- **Consistencia**: Todos tienen las mismas capacidades
- **Documentación simple**: Una sola forma de instalar
- **CI/CD más fácil**: Menos pasos en pipelines
- **Menos soporte**: Menos preguntas sobre instalación

## 🔄 Migración desde Versiones Anteriores

### Si usabas solo API
```bash
# Actualizar (sin cambios en código)
pip install --upgrade judo-framework
```

### Si usabas `[browser]`
```bash
# Actualizar (sin cambios en código)
pip install --upgrade judo-framework
# Ya no necesitas [browser]!
```

## 🎯 Próximos Pasos

1. **Actualiza**: `pip install --upgrade judo-framework`
2. **Instala browsers**: `playwright install`
3. **Prueba**: Ejecuta tus tests existentes
4. **Experimenta**: Crea un test con `@ui` tag
5. **Disfruta**: La nueva experiencia simplificada

---

**¡Bienvenido a la nueva era de Judo Framework!** 🥋✨