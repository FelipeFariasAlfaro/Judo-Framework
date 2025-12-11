# 🌐 Sitio Web de Documentación - Judo Framework

## 📋 Resumen

He creado la estructura completa para un sitio web de documentación similar al de Karate Framework usando **MkDocs Material**.

## 🎨 Características del Sitio

- ✅ **Diseño moderno** similar a Karate
- ✅ **Modo claro/oscuro** automático
- ✅ **Búsqueda integrada**
- ✅ **Navegación por tabs**
- ✅ **Syntax highlighting** para código
- ✅ **Responsive** (móvil, tablet, desktop)
- ✅ **Iconos y emojis**
- ✅ **Tabs para ejemplos** (English/Spanish)

## 📁 Estructura Creada

```
docs-site/
├── mkdocs.yml              # Configuración principal
├── requirements.txt        # Dependencias
├── deploy.md              # Guía de despliegue
└── docs/
    ├── index.md           # Página principal ✅
    ├── getting-started/
    │   ├── installation.md    ✅
    │   ├── quick-start.md     (por crear)
    │   └── first-test.md      (por crear)
    ├── features/              (por crear)
    ├── runners/               (por crear)
    ├── reporting/             (por crear)
    ├── advanced/              (por crear)
    ├── reference/             (por crear)
    └── about/                 (por crear)
```

## 🚀 Cómo Usar

### 1. Instalar Dependencias

```bash
pip install -r docs-site/requirements.txt
```

### 2. Probar Localmente

```bash
cd docs-site
mkdocs serve
```

Abre http://127.0.0.1:8000 en tu navegador.

### 3. Desplegar a GitHub Pages

```bash
cd docs-site
mkdocs gh-deploy
```

Tu sitio estará en: `https://felipefariaساlfaro.github.io/Judo-Framework/`

## 📝 Próximos Pasos

### Contenido por Crear

Puedo ayudarte a crear el contenido para:

1. **Getting Started**
   - Quick Start
   - First Test

2. **Features**
   - HTTP Testing
   - Assertions
   - Variables
   - File Support
   - Authentication
   - Parallel Execution

3. **Runners**
   - Creating Runners
   - Configuration
   - Test Suites

4. **Reporting**
   - HTML Reports
   - Cucumber JSON
   - Xray Integration

5. **Advanced**
   - Schema Validation
   - Mock Server
   - Custom Steps

6. **Reference**
   - Step Reference
   - API Reference
   - Examples

7. **About**
   - Changelog
   - Contributing
   - License

### Personalización

Puedes personalizar en `mkdocs.yml`:
- Colores del tema
- Logo y favicon
- Navegación
- Plugins adicionales

## 🎨 Tema Material

El sitio usa **Material for MkDocs**, que incluye:

- 📱 Diseño responsive
- 🌓 Modo claro/oscuro
- 🔍 Búsqueda instantánea
- 📑 Navegación por tabs
- 🎨 Syntax highlighting
- 📊 Diagramas con Mermaid
- 🔗 Enlaces sociales
- 📝 Anotaciones de código

## 🌐 Ejemplo de Sitio

Similar a:
- https://karatelabs.github.io/karate/
- https://squidfunk.github.io/mkdocs-material/
- https://www.mkdocs.org/

## 📦 Despliegue

### GitHub Pages (Gratis)

```bash
mkdocs gh-deploy
```

### Netlify (Gratis)

1. Conecta tu repo
2. Build: `mkdocs build`
3. Publish: `site`

### Vercel (Gratis)

1. Conecta tu repo
2. Build: `pip install -r docs-site/requirements.txt && mkdocs build`
3. Output: `site`

## ✅ Estado Actual

- ✅ Estructura creada
- ✅ Configuración completa
- ✅ Página principal creada
- ✅ Página de instalación creada
- ⏳ Resto del contenido por crear

## 🤔 ¿Quieres que Continue?

Puedo:
1. Crear todo el contenido restante
2. Agregar más ejemplos
3. Crear diagramas
4. Agregar screenshots
5. Personalizar el diseño
6. Desplegar el sitio

¿Qué prefieres?
