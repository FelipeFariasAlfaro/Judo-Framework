# 🚀 Desplegar Sitio de Documentación

## Opción 1: GitHub Pages (Recomendado)

### Paso 1: Instalar MkDocs

```bash
pip install -r docs-site/requirements.txt
```

### Paso 2: Probar Localmente

```bash
cd docs-site
mkdocs serve
```

Abre http://127.0.0.1:8000 en tu navegador.

### Paso 3: Desplegar a GitHub Pages

```bash
mkdocs gh-deploy
```

Esto construirá el sitio y lo publicará en la rama `gh-pages`.

### Paso 4: Configurar GitHub Pages

1. Ve a tu repositorio en GitHub
2. Settings → Pages
3. Source: Deploy from a branch
4. Branch: `gh-pages` / `root`
5. Save

Tu sitio estará disponible en:
`https://felipefariaساlfaro.github.io/Judo-Framework/`

## Opción 2: Netlify

1. Conecta tu repositorio a Netlify
2. Build command: `mkdocs build`
3. Publish directory: `site`
4. Deploy!

## Opción 3: Vercel

1. Conecta tu repositorio a Vercel
2. Framework Preset: Other
3. Build Command: `pip install -r docs-site/requirements.txt && mkdocs build`
4. Output Directory: `site`
5. Deploy!

## Actualizar Documentación

1. Edita archivos en `docs-site/docs/`
2. Commit y push
3. Ejecuta `mkdocs gh-deploy` para actualizar

## Estructura del Sitio

```
docs-site/
├── mkdocs.yml          # Configuración
├── docs/               # Contenido
│   ├── index.md       # Página principal
│   ├── getting-started/
│   ├── features/
│   ├── runners/
│   ├── reporting/
│   ├── advanced/
│   ├── reference/
│   └── about/
└── requirements.txt    # Dependencias
```

## Personalización

Edita `mkdocs.yml` para:
- Cambiar colores del tema
- Agregar/quitar secciones
- Configurar plugins
- Personalizar navegación
