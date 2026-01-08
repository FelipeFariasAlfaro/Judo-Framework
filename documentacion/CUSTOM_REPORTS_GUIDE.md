# 🎨 Guía de Reportes HTML Personalizables

## 📋 Descripción

Judo Framework v1.5.9.2 introduce un sistema completo de personalización para los reportes HTML, permitiendo a los usuarios configurar logos, colores, información del proyecto y gráficos según sus necesidades empresariales.

## 🚀 Características Principales

### ✨ Personalización Visual
- **Logos personalizables**: Logo principal, secundario y de empresa
- **Colores configurables**: Esquema completo de colores corporativos
- **Gráficos tipo torta**: Visualización de resultados con Chart.js
- **Información del proyecto**: Ingeniero, equipo, producto, empresa

### 📊 Gráficos Interactivos
- **Gráficos de torta**: Distribución de escenarios y pasos
- **Gráficos de barras**: Comparación de resultados (opcional)
- **Colores personalizables**: Esquema de colores para cada estado
- **Interactividad**: Tooltips con porcentajes y detalles

### 🎯 Configuración Flexible
- **Archivo JSON**: Configuración centralizada y versionable
- **Múltiples ubicaciones**: Búsqueda automática en ubicaciones estándar
- **Merge inteligente**: Combina configuración por defecto con personalizada
- **Validación robusta**: Manejo de errores y fallbacks

## 📁 Estructura de Configuración

### Archivo de Configuración: `report_config.json`

```json
{
  "project": {
    "name": "Mi Proyecto API Tests",
    "engineer": "Juan Pérez",
    "team": "Equipo QA",
    "product": "Sistema de Gestión",
    "company": "Mi Empresa S.A.",
    "date_format": "%d/%m/%Y %H:%M:%S"
  },
  "branding": {
    "primary_logo": "data:image/png;base64,iVBORw0KGgo...",
    "secondary_logo": "",
    "company_logo": "path/to/company-logo.png",
    "primary_color": "#1e40af",
    "secondary_color": "#3b82f6",
    "accent_color": "#60a5fa",
    "success_color": "#10b981",
    "error_color": "#f87171",
    "warning_color": "#fbbf24"
  },
  "charts": {
    "enabled": true,
    "show_pie_charts": true,
    "show_bar_charts": true,
    "colors": {
      "passed": "#10b981",
      "failed": "#f87171",
      "skipped": "#fbbf24"
    }
  },
  "footer": {
    "show_creator": true,
    "creator_name": "Juan Pérez",
    "creator_email": "juan.perez@miempresa.com",
    "company_name": "Mi Empresa S.A.",
    "company_url": "https://www.miempresa.com",
    "documentation_url": "https://docs.miempresa.com/testing",
    "github_url": "https://github.com/miempresa/testing-framework"
  },
  "display": {
    "show_request_details": true,
    "show_response_details": true,
    "show_variables": true,
    "show_assertions": true,
    "collapse_sections_by_default": false,
    "show_duration_in_ms": true
  }
}
```

## � ECstructura de Proyecto Recomendada

```
mi-proyecto/
├── features/
│   ├── api_tests.feature
│   └── environment.py
├── Runner/
│   ├── runner.py
│   └── judo_reports/
│       ├── report_config.json          ⭐ UBICACIÓN RECOMENDADA
│       ├── test_execution_report.html
│       ├── api_logs/
│       └── cucumber-json/
├── base_requests/
├── base_responses/
└── base_variables/
```

### 🎯 Configuración en `Runner/judo_reports/report_config.json`

```json
{
  "project": {
    "name": "Mi Proyecto - Pruebas API",
    "engineer": "Tu Nombre",
    "team": "Equipo QA",
    "product": "Sistema Principal",
    "company": "Tu Empresa"
  },
  "branding": {
    "primary_logo": "data:image/png;base64,{TU_LOGO_BASE64}",
    "primary_color": "#1e40af",
    "secondary_color": "#3b82f6"
  }
}
```

### 💻 Uso con BaseRunner y Variable de Entorno

```python
# Runner/runner.py
from judo.runner.base_runner import BaseRunner

class MyRunner(BaseRunner):
    def __init__(self):
        super().__init__(
            features_dir="../features",
            output_dir="./judo_reports",
            # ¡No necesitas especificar config_file!
            # Se carga automáticamente desde JUDO_REPORT_CONFIG_FILE
            generate_cucumber_json=True,
            save_requests_responses=True
        )
```

```bash
# .env
JUDO_REPORT_CONFIG_FILE=judo_reports/report_config.json
JUDO_OUTPUT_DIR=judo_reports
JUDO_FEATURES_DIR=../features
JUDO_SAVE_REQUESTS_RESPONSES=true
```

**¡El sistema encontrará automáticamente tu configuración desde .env!** 🎉

### 🔧 Configuración Alternativa (Parámetro Directo)

Si prefieres especificar el archivo directamente:

```python
# Runner/runner.py
from judo.runner.base_runner import BaseRunner

class MyRunner(BaseRunner):
    def __init__(self):
        super().__init__(
            features_dir="../features",
            output_dir="./judo_reports",
            config_file="./judo_reports/report_config.json"  # Especificado directamente
        )
```

### Opción 1: Base64 (Recomendado)
```json
{
  "branding": {
    "primary_logo": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
  }
}
```

### Opción 2: Ruta de Archivo
```json
{
  "branding": {
    "company_logo": "./assets/logos/company-logo.png"
  }
}
```

### Conversión a Base64
```python
import base64

def convert_image_to_base64(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
        base64_string = base64.b64encode(image_data).decode('utf-8')
        return f"data:image/png;base64,{base64_string}"

# Uso
logo_base64 = convert_image_to_base64("mi-logo.png")
print(logo_base64)
```

## 📍 Ubicaciones de Configuración

El sistema busca automáticamente el archivo de configuración en estas ubicaciones (en orden de prioridad):

1. **Variable de entorno** (⭐ **RECOMENDADO**): `JUDO_REPORT_CONFIG_FILE=judo_reports/report_config.json`
2. **Especificado directamente**: `config_file` parameter
3. **Directorio actual**: `./report_config.json`
4. **Nombre alternativo**: `./judo_report_config.json`
5. **Carpeta .judo**: `./.judo/report_config.json`
6. **📁 Carpeta judo_reports**: `./judo_reports/report_config.json`
7. **Directorio de trabajo**: `{cwd}/report_config.json`
8. **Carpeta judo_reports en cwd**: `{cwd}/judo_reports/report_config.json`
9. **Carpeta .judo en cwd**: `{cwd}/.judo/report_config.json`

### 🎯 **Configuración Recomendada: Variable de Entorno**

La forma más elegante y consistente con el framework es usar la variable de entorno:

```bash
# En tu archivo .env
JUDO_REPORT_CONFIG_FILE=judo_reports/report_config.json
```

**Ventajas:**
- ✅ Consistente con todas las demás configuraciones del framework
- ✅ Se puede versionar en el archivo .env.example
- ✅ Fácil de cambiar entre entornos (dev, staging, prod)
- ✅ No requiere modificar código Python

## 🎨 Esquemas de Colores Predefinidos

### Esquema Azul Corporativo
```json
{
  "branding": {
    "primary_color": "#1e40af",
    "secondary_color": "#3b82f6",
    "accent_color": "#60a5fa",
    "success_color": "#10b981",
    "error_color": "#f87171",
    "warning_color": "#fbbf24"
  }
}
```

### Esquema Verde Empresarial
```json
{
  "branding": {
    "primary_color": "#059669",
    "secondary_color": "#10b981",
    "accent_color": "#34d399",
    "success_color": "#22c55e",
    "error_color": "#ef4444",
    "warning_color": "#f59e0b"
  }
}
```

### Esquema Púrpura Moderno
```json
{
  "branding": {
    "primary_color": "#7c3aed",
    "secondary_color": "#8b5cf6",
    "accent_color": "#a78bfa",
    "success_color": "#22c55e",
    "error_color": "#ef4444",
    "warning_color": "#f59e0b"
  }
}
```

## 💻 Uso Programático

### Con BaseRunner
```python
from judo.runner.base_runner import BaseRunner

runner = BaseRunner(
    features_dir="features",
    output_dir="judo_reports",
    config_file="mi_config_personalizado.json"  # Nuevo parámetro
)

results = runner.run()
```

### Con JudoReporter Directamente
```python
from judo.reporting.reporter import JudoReporter

reporter = JudoReporter(
    title="Mi Proyecto - Reportes de Pruebas",
    output_dir="reportes_personalizados",
    config_file="config/report_config.json"
)

# Usar el reporter...
report_path = reporter.generate_html_report("mi_reporte.html")
```

### En environment.py (Behave)
```python
from judo.behave import *

# Configurar reporter personalizado
def before_all_custom(context):
    context.judo_reporter = JudoReporter(
        title="Mi Empresa - Pruebas API",
        config_file="config/empresa_config.json"
    )

before_all = before_all_custom
before_feature = before_feature_judo
after_feature = after_feature_judo
before_scenario = before_scenario_judo
after_scenario = after_scenario_judo
before_step = before_step_judo
after_step = after_step_judo
after_all = after_all_judo
```

## 📊 Configuración de Gráficos

### Habilitar Solo Gráficos de Torta
```json
{
  "charts": {
    "enabled": true,
    "show_pie_charts": true,
    "show_bar_charts": false,
    "colors": {
      "passed": "#22c55e",
      "failed": "#ef4444",
      "skipped": "#f59e0b"
    }
  }
}
```

### Deshabilitar Gráficos Completamente
```json
{
  "charts": {
    "enabled": false
  }
}
```

### Colores Personalizados para Gráficos
```json
{
  "charts": {
    "enabled": true,
    "show_pie_charts": true,
    "show_bar_charts": true,
    "colors": {
      "passed": "#28a745",    // Verde corporativo
      "failed": "#dc3545",    // Rojo corporativo
      "skipped": "#ffc107"    // Amarillo corporativo
    }
  }
}
```

## 🎯 Casos de Uso Empresariales

### Caso 1: Empresa con Branding Corporativo
```json
{
  "project": {
    "name": "Sistema ERP - Pruebas de Integración",
    "engineer": "María González",
    "team": "QA Automation Team",
    "product": "ERP Enterprise v2.0",
    "company": "TechCorp Solutions",
    "date_format": "%d/%m/%Y %H:%M"
  },
  "branding": {
    "primary_logo": "data:image/png;base64,{LOGO_BASE64}",
    "company_logo": "./assets/techcorp-logo.png",
    "primary_color": "#003366",
    "secondary_color": "#0066cc",
    "accent_color": "#3399ff"
  },
  "footer": {
    "creator_name": "María González",
    "creator_email": "maria.gonzalez@techcorp.com",
    "company_name": "TechCorp Solutions",
    "company_url": "https://www.techcorp.com"
  }
}
```

### Caso 2: Equipo de Desarrollo Ágil
```json
{
  "project": {
    "name": "Sprint 15 - API Testing",
    "engineer": "Carlos Ruiz",
    "team": "Scrum Team Alpha",
    "product": "Mobile Banking App",
    "company": "FinTech Innovations"
  },
  "charts": {
    "enabled": true,
    "show_pie_charts": true,
    "show_bar_charts": true
  },
  "display": {
    "collapse_sections_by_default": false,
    "show_duration_in_ms": true
  }
}
```

### Caso 3: Consultoría Externa
```json
{
  "project": {
    "name": "Auditoría de Calidad - Cliente XYZ",
    "engineer": "Ana Martínez",
    "team": "QA Consulting",
    "product": "Sistema de Facturación",
    "company": "QA Excellence Consulting"
  },
  "footer": {
    "show_creator": true,
    "creator_name": "Ana Martínez - QA Consultant",
    "creator_email": "ana.martinez@qaexcellence.com",
    "company_name": "QA Excellence Consulting",
    "documentation_url": "https://docs.qaexcellence.com"
  }
}
```

## 🔧 Troubleshooting

### Problema: Logo no se muestra
**Solución**: Verificar que el Base64 esté completo y tenga el prefijo correcto:
```json
"primary_logo": "data:image/png;base64,iVBORw0KGgo..."
```

### Problema: Colores no se aplican
**Solución**: Verificar que los colores estén en formato hexadecimal válido:
```json
"primary_color": "#1e40af"  // ✅ Correcto
"primary_color": "blue"     // ❌ Incorrecto
```

### Problema: Configuración no se carga
**Solución**: Verificar la sintaxis JSON y ubicación del archivo:
```bash
# Validar JSON
python -m json.tool report_config.json

# Verificar ubicación
ls -la report_config.json
```

### Problema: Gráficos no aparecen
**Solución**: Verificar que Chart.js se cargue correctamente y que `charts.enabled` sea `true`.

## 📚 Ejemplos Completos

### Archivo de Ejemplo: `report_config_example.json`
```json
{
  "project": {
    "name": "Mi Proyecto API Tests",
    "engineer": "Juan Pérez",
    "team": "Equipo QA",
    "product": "Sistema de Gestión",
    "company": "Mi Empresa S.A.",
    "date_format": "%d/%m/%Y %H:%M:%S"
  },
  "branding": {
    "primary_logo": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
    "secondary_logo": "",
    "company_logo": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
    "primary_color": "#1e40af",
    "secondary_color": "#3b82f6",
    "accent_color": "#60a5fa",
    "success_color": "#10b981",
    "error_color": "#f87171",
    "warning_color": "#fbbf24"
  },
  "charts": {
    "enabled": true,
    "show_pie_charts": true,
    "show_bar_charts": true,
    "colors": {
      "passed": "#10b981",
      "failed": "#f87171",
      "skipped": "#fbbf24"
    }
  },
  "footer": {
    "show_creator": true,
    "creator_name": "Juan Pérez",
    "creator_email": "juan.perez@miempresa.com",
    "company_name": "Mi Empresa S.A.",
    "company_url": "https://www.miempresa.com",
    "documentation_url": "https://docs.miempresa.com/testing",
    "github_url": "https://github.com/miempresa/testing-framework"
  },
  "display": {
    "show_request_details": true,
    "show_response_details": true,
    "show_variables": true,
    "show_assertions": true,
    "collapse_sections_by_default": false,
    "show_duration_in_ms": true
  }
}
```

## 🚀 Migración desde Versiones Anteriores

Los reportes existentes seguirán funcionando sin cambios. Para aprovechar las nuevas características:

1. **Copia el archivo de ejemplo**: `cp report_config_example.json report_config.json`
2. **Personaliza la configuración**: Edita `report_config.json` con tus datos
3. **Añade tus logos**: Convierte tus logos a Base64 o usa rutas de archivo
4. **Ejecuta las pruebas**: Los reportes usarán automáticamente la nueva configuración

## 📈 Beneficios Empresariales

- **Branding Corporativo**: Reportes con identidad visual de la empresa
- **Información Contextual**: Datos del proyecto, equipo e ingeniero
- **Visualización Mejorada**: Gráficos interactivos para mejor comprensión
- **Flexibilidad**: Configuración adaptable a diferentes proyectos
- **Profesionalismo**: Reportes de calidad empresarial para stakeholders

---

**¡Disfruta de los nuevos reportes HTML personalizables de Judo Framework!** 🎨✨
