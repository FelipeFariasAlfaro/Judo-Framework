# Configuración del Repositorio en GitHub

Este documento describe cómo configurar el repositorio de Judo Framework en GitHub.

---

## ✅ Archivos Creados

Los siguientes archivos ya están en el repositorio:

- ✅ `.github/workflows/close-prs.yml` - Auto-cierra Pull Requests
- ✅ `.github/CODEOWNERS` - Define propietarios del código
- ✅ `.github/PULL_REQUEST_TEMPLATE.md` - Template para PRs
- ✅ `.github/ISSUE_TEMPLATE/bug_report.md` - Template para reportar bugs
- ✅ `.github/ISSUE_TEMPLATE/feature_request.md` - Template para sugerir features
- ✅ `.github/ISSUE_TEMPLATE/config.yml` - Configuración de issue templates
- ✅ `CONTRIBUTING.md` - Guía de contribución
- ✅ `README.md` - Actualizado con política de contribución

---

## 🔧 Configuración Manual en GitHub

Después de hacer push de estos archivos, configura lo siguiente en GitHub:

### 1. Proteger la Rama Main

**Pasos:**
1. Ve a tu repositorio: https://github.com/FelipeFariasAlfaro/Judo-Framework
2. Click en **Settings** (Configuración)
3. En el menú lateral, click en **Branches**
4. Click en **Add branch protection rule** (o edita si ya existe)
5. En "Branch name pattern" escribe: `main`
6. Activa las siguientes opciones:

   **Protect matching branches:**
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals: 1
     - ✅ Dismiss stale pull request approvals when new commits are pushed
     - ✅ Require review from Code Owners
   
   - ✅ **Require status checks to pass before merging**
     - Busca y agrega los checks que quieras (tests, linting, etc.)
   
   - ✅ **Require conversation resolution before merging**
   
   - ✅ **Require signed commits** (opcional pero recomendado)
   
   - ✅ **Require linear history** (opcional)
   
   - ✅ **Do not allow bypassing the above settings**
   
   - ✅ **Restrict who can push to matching branches**
     - Agrega solo tu usuario: `FelipeFariasAlfaro`

7. Click en **Create** o **Save changes**

### 2. Configurar Features del Repositorio

**Pasos:**
1. Ve a **Settings** → **General**
2. En la sección **Features**, asegúrate de tener:
   - ✅ **Issues** - ACTIVADO (necesario para reportes)
   - ✅ **Discussions** - ACTIVADO (necesario para preguntas)
   - ☐ **Projects** - Opcional (puedes desactivar)
   - ☐ **Wiki** - Opcional (puedes desactivar si no lo usas)
   - ☐ **Sponsorships** - Opcional

### 3. Configurar Descripción y Topics

**Pasos:**
1. Ve a la página principal del repositorio
2. Click en el ícono de engranaje ⚙️ junto a "About"
3. Agrega:

   **Description:**
   ```
   🥋 A comprehensive API testing framework for Python, inspired by Karate Framework. As simple as Karate, as powerful as Python.
   ```

   **Website:**
   ```
   https://www.centyc.cl
   ```

   **Topics:** (agrega estos tags)
   - `api-testing`
   - `python`
   - `bdd`
   - `gherkin`
   - `behave`
   - `testing-framework`
   - `api`
   - `rest-api`
   - `karate`
   - `test-automation`
   - `quality-assurance`
   - `centyc`

4. Click en **Save changes**

### 4. Configurar GitHub Actions

**Pasos:**
1. Ve a **Settings** → **Actions** → **General**
2. En "Actions permissions":
   - Selecciona: **Allow all actions and reusable workflows**
3. En "Workflow permissions":
   - Selecciona: **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
4. Click en **Save**

Esto permite que el workflow `close-prs.yml` funcione correctamente.

### 5. Habilitar Discussions

**Pasos:**
1. Ve a **Settings** → **General**
2. En la sección **Features**
3. Activa ✅ **Discussions**
4. Ve a la pestaña **Discussions** en tu repositorio
5. Crea categorías:
   - **Q&A** - Para preguntas
   - **Ideas** - Para discutir ideas
   - **Show and tell** - Para compartir casos de uso
   - **General** - Para discusión general

### 6. Configurar Notificaciones (Opcional)

**Pasos:**
1. Ve a **Settings** → **Notifications**
2. Configura cómo quieres recibir notificaciones de:
   - Issues
   - Pull Requests
   - Discussions

---

## 🧪 Probar la Configuración

### Probar Auto-Cierre de PRs

1. Crea una rama de prueba:
   ```bash
   git checkout -b test-pr-close
   echo "test" > test.txt
   git add test.txt
   git commit -m "test: PR auto-close"
   git push origin test-pr-close
   ```

2. Ve a GitHub y crea un Pull Request desde `test-pr-close` a `main`

3. Verifica que:
   - El workflow se ejecuta automáticamente
   - Se agrega un comentario explicando la política
   - El PR se cierra automáticamente

4. Limpia:
   ```bash
   git checkout main
   git branch -D test-pr-close
   git push origin --delete test-pr-close
   ```

### Probar Issue Templates

1. Ve a **Issues** → **New Issue**
2. Verifica que aparecen las opciones:
   - Bug Report
   - Feature Request
   - Links a Discussions y Documentation

---

## 📋 Checklist Final

Después de configurar todo, verifica:

### Archivos en el Repositorio
- [ ] `.github/workflows/close-prs.yml` existe
- [ ] `.github/CODEOWNERS` existe
- [ ] `.github/PULL_REQUEST_TEMPLATE.md` existe
- [ ] `.github/ISSUE_TEMPLATE/bug_report.md` existe
- [ ] `.github/ISSUE_TEMPLATE/feature_request.md` existe
- [ ] `.github/ISSUE_TEMPLATE/config.yml` existe
- [ ] `CONTRIBUTING.md` actualizado
- [ ] `README.md` actualizado

### Configuración en GitHub
- [ ] Rama `main` protegida
- [ ] Solo tú puedes hacer push a `main`
- [ ] Issues activados
- [ ] Discussions activados
- [ ] GitHub Actions configurado con permisos
- [ ] Descripción y topics agregados
- [ ] Templates de issues funcionando

### Pruebas
- [ ] Workflow de auto-cierre de PRs probado
- [ ] Templates de issues visibles
- [ ] Discussions habilitado

---

## 🎯 Resultado Esperado

Con esta configuración:

1. ✅ El repositorio es público (código visible para todos)
2. ✅ Cualquiera puede clonar y usar el código (MIT License)
3. ✅ Los Pull Requests se cierran automáticamente con mensaje explicativo
4. ✅ Issues disponibles para reportar bugs y sugerir features
5. ✅ Discussions disponibles para preguntas y discusión
6. ✅ Solo tú puedes modificar el código en `main`
7. ✅ Documentación clara sobre la política de contribución
8. ✅ Templates profesionales para issues

---

## 📞 Soporte

Si tienes problemas con la configuración:
- Email: farias3felipe@gmail.com
- CENTYC: https://www.centyc.cl

---

**Made with ❤️ at CENTYC for API testing excellence** 🥋
