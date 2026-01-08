# 🎨 Guía de Configuración de Logos en Reportes HTML

## 📋 Resumen de Problemas Solucionados

### ✅ Problemas Resueltos:
1. **Logo base64 no se mostraba**: Ahora funciona correctamente
2. **Logo pequeño fijo en footer**: Ahora se puede ocultar completamente
3. **Mejor manejo de logos**: Soporte mejorado para diferentes formatos

## 🔧 Configuración de Logos

### 1. Logo en el Header (Empresa)
Para mostrar tu logo de empresa en la esquina superior izquierda del reporte:

```json
{
  "branding": {
    "secondary_logo": "data:image/png;base64,TU_LOGO_BASE64_AQUI"
  }
}
```

### 2. Ocultar Logo del Footer
Para eliminar completamente el logo pequeño del footer:

```json
{
  "footer": {
    "show_logo": false
  }
}
```

## 📝 Cómo Convertir tu Logo a Base64

### Opción 1: Herramientas Online
1. Ve a https://www.base64-image.de/
2. Sube tu logo (PNG, JPG, GIF)
3. Copia el resultado completo (incluye `data:image/png;base64,`)

### Opción 2: Línea de Comandos
```bash
# En Linux/Mac
base64 -i tu_logo.png

# En Windows PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("tu_logo.png"))
```

### Opción 3: Python
```python
import base64

with open("tu_logo.png", "rb") as img_file:
    logo_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    print(f"data:image/png;base64,{logo_base64}")
```

## 🎯 Configuración Completa de Ejemplo

```json
{
  "project": {
    "name": "Mi Empresa - API Tests",
    "company": "Mi Empresa S.A."
  },
  "branding": {
    "secondary_logo": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU77zgAAAABJRU5ErkJggg==",
    "primary_color": "#1e40af",
    "secondary_color": "#1d4ed8"
  },
  "footer": {
    "show_logo": false,
    "company_name": "Mi Empresa S.A.",
    "company_url": "https://www.miempresa.com"
  }
}
```

## 🔍 Tipos de Logo Soportados

### Logo Principal (`primary_logo`)
- **Ubicación**: Footer (opcional)
- **Uso**: Logo del framework o herramienta
- **Control**: `footer.show_logo` (true/false)

### Logo Secundario (`secondary_logo`)
- **Ubicación**: Header superior izquierdo
- **Uso**: Logo de tu empresa/organización
- **Siempre visible**: Si está configurado

### Logo de Empresa (`company_logo`)
- **Ubicación**: Alternativa al secondary_logo
- **Uso**: Mismo propósito que secondary_logo

## ⚙️ Formatos Soportados

### Formatos de Imagen
- ✅ PNG (recomendado)
- ✅ JPG/JPEG
- ✅ GIF
- ✅ SVG

### Formatos de Configuración
- ✅ Base64 completo: `data:image/png;base64,ABC123...`
- ✅ Base64 simple: `ABC123...` (se agrega el prefijo automáticamente)
- ✅ Ruta de archivo: `./mi_logo.png`

## 🎨 Recomendaciones de Diseño

### Tamaños Recomendados
- **Header Logo**: 120x30px (máximo)
- **Footer Logo**: 24x24px (si se usa)

### Formato Recomendado
- **PNG con transparencia** para mejor integración
- **Tamaño de archivo**: < 50KB para mejor rendimiento

## 🚀 Ejemplo de Uso

1. **Convierte tu logo a base64**
2. **Crea tu archivo de configuración**:
```json
{
  "branding": {
    "secondary_logo": "data:image/png;base64,TU_LOGO_AQUI"
  },
  "footer": {
    "show_logo": false
  }
}
```
3. **Genera el reporte**:
```python
from judo.reporting.html_reporter import HTMLReporter

reporter = HTMLReporter(config_file="mi_config.json")
reporter.generate_report(report_data, "mi_reporte.html")
```

## ✅ Verificación

Para verificar que tu configuración funciona:
1. El logo debe aparecer en la esquina superior izquierda
2. No debe haber logo pequeño en el footer
3. Los colores deben coincidir con tu configuración

## 🆘 Solución de Problemas

### Logo no aparece
- ✅ Verifica que el base64 esté completo
- ✅ Asegúrate de incluir el prefijo `data:image/png;base64,`
- ✅ Verifica que el archivo JSON sea válido

### Logo muy grande
- ✅ Redimensiona la imagen antes de convertir a base64
- ✅ Usa PNG con transparencia para mejor resultado

### Logo del footer sigue apareciendo
- ✅ Asegúrate de que `footer.show_logo` esté en `false`
- ✅ Verifica que estés usando la versión más reciente del framework