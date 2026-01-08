# Guía de Configuración via .env - Judo Framework v1.5.9.2

## 🚀 Nueva Funcionalidad: Configuración Centralizada

A partir de la versión 1.5.9.0, Judo Framework soporta configuración completa via archivos `.env`. En la versión 1.5.9.2 se agregó soporte para configuración de reportes HTML personalizables via la variable `JUDO_REPORT_CONFIG_FILE`.

## 📋 Beneficios

- **Runners Ultra-Simples**: Reducción de código de configuración en 80%+
- **Configuración Centralizada**: Un solo archivo .env para todo el proyecto
- **Reutilización**: Misma configuración entre diferentes runners
- **Mantenibilidad**: Cambios de configuración sin tocar código
- **Compatibilidad**: Cero breaking changes para usuarios existentes

## 🔧 Variables de Entorno Soportadas

### Configuración de Directorios
```bash
# Directorio con archivos .feature
JUDO_FEATURES_DIR=features

# Directorio para reportes HTML y otros outputs
JUDO_OUTPUT_DIR=judo_reports

# Directorio para archivos Cucumber JSON
JUDO_CUCUMBER_JSON_DIR=judo_reports/cucumber-json

# Directorio para logs de requests/responses
JUDO_REQUESTS_RESPONSES_DIR=judo_reports/requests_responses
```

### Configuración de Ejecución
```bash
# Ejecutar tests en paralelo (true/false)
JUDO_PARALLEL=false

# Número máximo de hilos para ejecución paralela
JUDO_MAX_WORKERS=4

# Ejecutar todos los features juntos en una sola ejecución
JUDO_RUN_ALL_FEATURES_TOGETHER=true

# Timeout en segundos para ejecución de tests
JUDO_TIMEOUT=300

# Número de reintentos en caso de fallo
JUDO_RETRY_COUNT=0

# Parar ejecución en el primer fallo
JUDO_FAIL_FAST=false
```

### Configuración de Reportes
```bash
# Generar archivos JSON en formato Cucumber
JUDO_GENERATE_CUCUMBER_JSON=true

# Guardar automáticamente requests y responses de API
JUDO_SAVE_REQUESTS_RESPONSES=false

# Formato de salida en consola: progress, pretty, plain, none
JUDO_CONSOLE_FORMAT=progress

# Salida verbose con detalles
JUDO_VERBOSE=true

# Habilitar modo debug para el reporter
JUDO_DEBUG_REPORTER=false

# Archivo de configuración para reportes HTML personalizables
JUDO_REPORT_CONFIG_FILE=judo_reports/report_config.json
```

## 🎨 Configuración de Reportes HTML Personalizables

### Variable de Entorno para Configuración de Reportes

```bash
# Ruta al archivo JSON de configuración para reportes HTML personalizables
JUDO_REPORT_CONFIG_FILE=judo_reports/report_config.json
```

### Ejemplo de Configuración Completa

**.env:**
```bash
# Configuración básica
JUDO_OUTPUT_DIR=judo_reports
JUDO_VERBOSE=true

# Configuración de reportes personalizables
JUDO_REPORT_CONFIG_FILE=judo_reports/custom_report_config.json
```

**judo_reports/custom_report_config.json:**
```json
{
  "project": {
    "name": "Mi Proyecto API Tests",
    "engineer": "Juan Pérez",
    "team": "QA Team",
    "product": "Sistema de Gestión",
    "company": "Mi Empresa S.A."
  },
  "branding": {
    "primary_logo": "assets/logo_empresa.png",
    "primary_color": "#2563eb",
    "secondary_color": "#1d4ed8"
  },
  "charts": {
    "enabled": true,
    "show_pie_charts": true
  }
}
```

### Prioridad de Configuración de Reportes

1. **Variable de entorno JUDO_REPORT_CONFIG_FILE** (mayor prioridad)
2. **Parámetro config_file en HTMLReporter**
3. **Ubicaciones estándar automáticas:**
   - `report_config.json`
   - `judo_report_config.json`
   - `.judo/report_config.json`
   - `judo_reports/report_config.json`
4. **Configuración por defecto** (menor prioridad)

### Beneficios de la Configuración via .env

- **Flexibilidad**: Cambiar configuración sin modificar código
- **Entornos**: Diferentes configuraciones para dev/test/prod
- **Mantenimiento**: Centralización de configuración
- **Reutilización**: Misma configuración entre múltiples runners

Para más detalles sobre reportes personalizables, consulta `CUSTOM_REPORTS_GUIDE.md`.

## 📝 Ejemplos de Uso

### Ejemplo 1: Runner Ultra-Simple

**Antes (v1.5.8.2):**
```python
from judo.runner.base_runner import BaseRunner
import os

os.environ['JUDO_DEBUG_REPORTER'] = 'false'

class MyRunner(BaseRunner):
    def __init__(self):
        super().__init__(
            features_dir="../features",
            output_dir="./judo_reports",
            generate_cucumber_json=True,
            cucumber_json_dir="./judo_reports/cucumber-json",
            parallel=False,
            max_workers=6,
            save_requests_responses=False,
            requests_responses_dir="./judo_reports/api_logs"
        )
    
    def run_tests(self, tags=None):
        tags = tags or ["@mix_ejecutar_todo"]
        return self.run(tags=tags)

if __name__ == "__main__":
    runner = MyRunner()
    results = runner.run_tests()
```

**Ahora (v1.5.9.0):**

**.env:**
```bash
JUDO_FEATURES_DIR=../features
JUDO_OUTPUT_DIR=./judo_reports
JUDO_GENERATE_CUCUMBER_JSON=true
JUDO_CUCUMBER_JSON_DIR=./judo_reports/cucumber-json
JUDO_PARALLEL=false
JUDO_MAX_WORKERS=6
JUDO_SAVE_REQUESTS_RESPONSES=false
JUDO_REQUESTS_RESPONSES_DIR=./judo_reports/api_logs
JUDO_DEBUG_REPORTER=false
```

**runner.py:**
```python
from judo.runner.base_runner import BaseRunner

class MyRunner(BaseRunner):
    def run_tests(self, tags=None):
        tags = tags or ["@mix_ejecutar_todo"]
        return self.run(tags=tags)

if __name__ == "__main__":
    runner = MyRunner()  # ¡Toda la configuración desde .env!
    results = runner.run_tests()
```

### Ejemplo 2: Runner Aún Más Simple

```python
from judo.runner.base_runner import BaseRunner

# ¡Una sola línea!
runner = BaseRunner.create_simple_runner()
results = runner.run(tags=["@smoke"])
```

### Ejemplo 3: Compatibilidad hacia Atrás

Los runners existentes siguen funcionando sin cambios:

```python
# Esto sigue funcionando exactamente igual
runner = BaseRunner(
    features_dir="features",
    output_dir="reports",
    parallel=True
)
```

## 🔄 Prioridad de Configuración

1. **Parámetros del constructor** (mayor prioridad)
2. **Variables de entorno (.env)**
3. **Valores por defecto** (menor prioridad)

Ejemplo:
```python
# .env tiene JUDO_PARALLEL=true
# Pero el constructor lo sobrescribe:
runner = BaseRunner(parallel=False)  # parallel será False
```

## 📁 Estructura de Proyecto Recomendada

```
mi_proyecto/
├── .env                    # Configuración centralizada
├── runner.py              # Runner simplificado
├── features/              # Features de prueba
│   ├── api_tests.feature
│   └── smoke_tests.feature
└── judo_reports/          # Reportes generados
    ├── test_execution_report.html
    ├── cucumber-json/
    └── requests_responses/
```

## 🧪 Validación y Tests

Para validar que tu configuración funciona correctamente:

```bash
# Ejecutar tests de validación
python test_env_configuration.py
python test_runner_integration.py
```

## 🔍 Debugging

Si tienes problemas con la configuración:

1. **Habilita logging detallado:**
   ```bash
   JUDO_VERBOSE=true
   JUDO_DEBUG_REPORTER=true
   ```

2. **Verifica que el .env se carga:**
   El runner muestra toda la configuración cargada al inicializar.

3. **Verifica la ubicación del .env:**
   El framework busca .env en:
   - Directorio actual
   - Directorios padre
   - Directorio raíz del proyecto

## 📚 Recursos Adicionales

- **examples/simple_runner_example.py**: Ejemplo completo funcional
- **examples/.env.runner_example**: Archivo .env de ejemplo
- **.env.example**: Plantilla con todas las variables disponibles
- **ENV_CONFIGURATION_GUIDE.md**: Esta guía completa

## 🎯 Migración desde Versiones Anteriores

### Paso 1: Crear archivo .env
Copia las configuraciones de tu runner actual al archivo .env.

### Paso 2: Simplificar runner
Elimina parámetros del constructor que ahora están en .env.

### Paso 3: Validar
Ejecuta los tests de validación para confirmar que todo funciona.

### Paso 4: (Opcional) Usar create_simple_runner()
Para máxima simplicidad, usa el método de clase.

¡La migración es completamente opcional y no rompe código existente!