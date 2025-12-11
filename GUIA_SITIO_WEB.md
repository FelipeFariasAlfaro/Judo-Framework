# 🌐 Guía Completa: Crear Sitio Web para Judo Framework

## 📊 Comparación de Opciones

| Opción | Costo | Dificultad | Profesionalismo | Recomendación |
|--------|-------|------------|-----------------|---------------|
| **GitHub Pages** | ✅ GRATIS | ⭐ Fácil | ⭐⭐⭐ Bueno | ✅ **RECOMENDADO para proyecto open source** |
| **CENTYC** | 💰 Ya pagado | ⭐⭐ Media | ⭐⭐⭐⭐⭐ Excelente | ✅ **RECOMENDADO para uso comercial** |
| **Netlify** | ✅ GRATIS | ⭐ Fácil | ⭐⭐⭐⭐ Muy bueno | Alternativa |
| **Vercel** | ✅ GRATIS | ⭐ Fácil | ⭐⭐⭐⭐ Muy bueno | Alternativa |

---

## 🎯 Mi Recomendación

### **Opción 1: GitHub Pages (Para el Proyecto Open Source)**

**URL resultante**: `https://felipefariaساlfaro.github.io/Judo-Framework/`

**Ventajas:**
- ✅ 100% GRATIS
- ✅ Integrado con tu repositorio
- ✅ Actualización automática con cada commit
- ✅ SSL/HTTPS incluido
- ✅ Perfecto para proyectos open source
- ✅ Credibilidad en la comunidad de desarrolladores

**Desventajas:**
- ❌ URL no personalizada (a menos que uses dominio custom)
- ❌ Asociado a tu cuenta personal de GitHub

### **Opción 2: CENTYC (Para Uso Comercial/Profesional)**

**URL resultante**: `https://judo.centyc.cl/` o `https://centyc.cl/judo/`

**Ventajas:**
- ✅ Dominio profesional de empresa
- ✅ Ya tienes el hosting pagado
- ✅ Más control sobre el dominio
- ✅ Imagen corporativa
- ✅ Puedes ofrecer soporte comercial

**Desventajas:**
- ❌ Requiere configuración en servidor CENTYC
- ❌ Menos "open source friendly"
- ❌ Mantenimiento manual

---

## 💡 Mi Sugerencia: ¡AMBAS!

### Estrategia Dual:

1. **GitHub Pages** → Documentación oficial del proyecto open source
   - `https://felipefariaساlfaro.github.io/Judo-Framework/`
   - Para la comunidad de desarrolladores
   - Gratis y automático

2. **CENTYC** → Landing page comercial + soporte
   - `https://judo.centyc.cl/`
   - Para clientes empresariales
   - Servicios de consultoría y soporte
   - Casos de éxito
   - Contacto comercial

**Ejemplo**: Karate hace algo similar:
- Docs técnicos: https://karatelabs.github.io/karate/
- Sitio comercial: https://karatelabs.io/

---

## 🚀 OPCIÓN 1: GitHub Pages (GRATIS - RECOMENDADO)

### Paso 1: Instalar MkDocs

```bash
pip install -r docs-site/requirements.txt
```

### Paso 2: Probar Localmente

```bash
cd docs-site
mkdocs serve
```

Abre http://127.0.0.1:8000 para ver el sitio.

### Paso 3: Desplegar a GitHub Pages

```bash
mkdocs gh-deploy
```

Este comando:
1. Construye el sitio estático
2. Crea/actualiza la rama `gh-pages`
3. Sube los archivos a GitHub

### Paso 4: Activar GitHub Pages

1. Ve a tu repositorio: https://github.com/FelipeFariasAlfaro/Judo-Framework
2. Click en **Settings** (⚙️)
3. En el menú izquierdo, click en **Pages**
4. En **Source**, selecciona:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
5. Click **Save**

### Paso 5: Esperar (2-5 minutos)

GitHub construirá tu sitio. Recibirás un mensaje:
> "Your site is published at https://felipefariaساlfaro.github.io/Judo-Framework/"

### Paso 6: Verificar

Abre: https://felipefariaساlfaro.github.io/Judo-Framework/

¡Listo! Tu sitio está en línea.

### Actualizar el Sitio

Cada vez que quieras actualizar:

```bash
# 1. Edita archivos en docs-site/docs/
# 2. Despliega
cd docs-site
mkdocs gh-deploy
```

**¡Automático y gratis!**

---

## 🏢 OPCIÓN 2: CENTYC (Hosting Propio)

### Requisitos Previos

Necesitas acceso a:
- Panel de control de CENTYC (cPanel, Plesk, etc.)
- FTP o SSH
- Configuración de subdominios

### Paso 1: Construir el Sitio

```bash
cd docs-site
mkdocs build
```

Esto crea la carpeta `site/` con todos los archivos HTML.

### Paso 2: Crear Subdominio en CENTYC

1. Entra al panel de control de CENTYC
2. Busca "Subdominios" o "Domains"
3. Crea subdominio: `judo.centyc.cl`
4. Apunta a una carpeta (ej: `/public_html/judo/`)

### Paso 3: Subir Archivos

**Opción A: FTP**
1. Conecta con FileZilla o similar
2. Sube todo el contenido de `site/` a `/public_html/judo/`

**Opción B: SSH**
```bash
scp -r site/* usuario@centyc.cl:/public_html/judo/
```

### Paso 4: Configurar SSL (HTTPS)

En el panel de CENTYC:
1. Busca "SSL/TLS"
2. Activa Let's Encrypt para `judo.centyc.cl`
3. Espera 5-10 minutos

### Paso 5: Verificar

Abre: https://judo.centyc.cl/

### Actualizar el Sitio

```bash
# 1. Edita archivos
# 2. Reconstruye
mkdocs build

# 3. Sube por FTP o SSH
scp -r site/* usuario@centyc.cl:/public_html/judo/
```

---

## 🎨 OPCIÓN 3: Netlify (GRATIS - Alternativa)

### Ventajas
- ✅ GRATIS
- ✅ Deploy automático con Git
- ✅ SSL incluido
- ✅ CDN global
- ✅ Dominio custom gratis

### Pasos

1. Ve a https://netlify.com
2. Sign up con GitHub
3. Click "New site from Git"
4. Selecciona tu repositorio
5. Configuración:
   - Build command: `pip install -r docs-site/requirements.txt && cd docs-site && mkdocs build`
   - Publish directory: `docs-site/site`
6. Deploy!

URL: `https://judo-framework.netlify.app/`

---

## 🎨 OPCIÓN 4: Vercel (GRATIS - Alternativa)

Similar a Netlify, muy fácil de usar.

1. Ve a https://vercel.com
2. Sign up con GitHub
3. Import tu repositorio
4. Configuración:
   - Framework: Other
   - Build: `pip install -r docs-site/requirements.txt && cd docs-site && mkdocs build`
   - Output: `docs-site/site`
5. Deploy!

URL: `https://judo-framework.vercel.app/`

---

## 🎯 Mi Recomendación Final

### Para Empezar YA (5 minutos):

**GitHub Pages** - Es perfecto porque:
1. ✅ GRATIS
2. ✅ 3 comandos y listo
3. ✅ Actualización automática
4. ✅ Profesional para open source
5. ✅ No requiere configuración de servidor

```bash
pip install -r docs-site/requirements.txt
cd docs-site
mkdocs gh-deploy
```

### Para el Futuro (Opcional):

**CENTYC** - Para:
- Landing page comercial
- Servicios de consultoría
- Soporte empresarial
- Casos de éxito

---

## 📝 Resumen de Costos

| Opción | Costo Mensual | Costo Anual | Setup |
|--------|---------------|-------------|-------|
| GitHub Pages | $0 | $0 | 5 min |
| CENTYC | Ya pagado | Ya pagado | 30 min |
| Netlify | $0 | $0 | 10 min |
| Vercel | $0 | $0 | 10 min |

---

## 🚀 Acción Recomendada

### AHORA (5 minutos):

```bash
# 1. Instalar
pip install -r docs-site/requirements.txt

# 2. Desplegar
cd docs-site
mkdocs gh-deploy

# 3. Activar en GitHub
# Settings → Pages → Source: gh-pages
```

### DESPUÉS (Opcional):

- Configurar dominio custom en GitHub Pages
- O crear landing comercial en CENTYC
- O ambas estrategias

---

## ❓ Preguntas Frecuentes

### ¿Puedo usar mi propio dominio con GitHub Pages?

Sí! Puedes usar `judo.centyc.cl` apuntando a GitHub Pages:
1. En GitHub Settings → Pages → Custom domain
2. Agrega `judo.centyc.cl`
3. En CENTYC, crea un CNAME apuntando a `felipefariaساlfaro.github.io`

### ¿Cuál es más profesional?

- Para **open source**: GitHub Pages
- Para **comercial**: CENTYC
- **Ideal**: Ambas

### ¿Cuál es más fácil?

GitHub Pages - 3 comandos y listo.

### ¿Cuál recomendarías?

**GitHub Pages** para empezar. Es gratis, fácil, y perfecto para proyectos open source.

---

## 📞 ¿Necesitas Ayuda?

Dime qué opción prefieres y te guío paso a paso:

1. **GitHub Pages** (5 min) ← Recomendado
2. **CENTYC** (30 min)
3. **Ambas** (35 min)

¿Cuál prefieres?
