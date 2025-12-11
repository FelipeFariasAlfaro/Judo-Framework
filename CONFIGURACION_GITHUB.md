# Configuración de GitHub para Judo Framework

## 🔒 Política: Solo Issues, No Pull Requests

Este documento explica cómo configurar el repositorio de GitHub para reforzar la política de "solo issues".

---

## ⚠️ Importante: Limitaciones de GitHub

**No es posible hacer un repositorio público que no se pueda clonar.**

Si un repositorio es público en GitHub, cualquiera puede:
- ✅ Ver el código
- ✅ Clonar el repositorio (`git clone`)
- ✅ Hacer fork
- ✅ Descargar como ZIP

**No hay forma de prevenir esto en un repositorio público.**

---

## 🎯 Estrategia Recomendada

Mantener el repositorio **público** pero con políticas claras de contribución:

### 1. Documentación Clara
- ✅ Ya actualizado: `CONTRIBUTING.md`
- ✅ Ya actualizado: `README.md`
- ✅ Mensajes claros sobre la política

### 2. Configuración de GitHub

#### A. Deshabilitar Pull Requests (Opcional)

**Pasos:**
1. Ve a tu repositorio en GitHub
2. Click en **Settings** (Configuración)
3. En la sección **Features**, desmarca:
   - ☐ **Issues** - MANTENER ACTIVADO (necesitamos esto)
   - ☐ **Projects** - Opcional
   - ☐ **Wiki** - Opcional
   - ☐ **Discussions** - MANTENER ACTIVADO (para preguntas)

**Nota:** No hay opción para deshabilitar solo Pull Requests, pero puedes:
- Cerrarlos automáticamente con GitHub Actions
- Agregar mensaje automático explicando la política

#### B. Proteger la Rama Main

**Pasos:**
1. Ve a **Settings** → **Branches**
2. Click en **Add rule** o edita la regla existente
3. En "Branch name pattern" escribe: `main`
4. Activa:
   - ✅ **Require pull request reviews before merging**
   - ✅ **Dismiss stale pull request approvals when new commits are pushed**
   - ✅ **Require review from Code Owners**
   - ✅ **Restrict who can push to matching branches**
     - Solo agregar tu usuario

Esto previene que alguien haga push directo, pero no previene PRs.

#### C. Crear GitHub Action para Auto-Cerrar PRs

Crea el archivo `.github/workflows/close-prs.yml`:

```yaml
name: Close Pull Requests

on:
  pull_request_target:
    types: [opened]

jobs:
  close-pr:
    runs-on: ubuntu-latest
    steps:
      - name: Close Pull Request
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '⚠️ **This project does not accept Pull Requests.**\n\n' +
                    'Judo Framework is professionally maintained by CENTYC. ' +
                    'All development is handled internally.\n\n' +
                    '**How to contribute:**\n' +
                    '- 🐛 Report bugs via [Issues](https://github.com/FelipeFariasAlfaro/Judo-Framework/issues)\n' +
                    '- 💡 Suggest features via [Issues](https://github.com/FelipeFariasAlfaro/Judo-Framework/issues)\n' +
                    '- ❓ Ask questions in [Discussions](https://github.com/FelipeFariasAlfaro/Judo-Framework/discussions)\n\n' +
                    'See [CONTRIBUTING.md](https://github.com/FelipeFariasAlfaro/Judo-Framework/blob/main/CONTRIBUTING.md) for details.\n\n' +
                    'This PR will be closed automatically.'
            })
            github.rest.pulls.update({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              state: 'closed'
            })
```

#### D. Agregar CODEOWNERS

Crea el archivo `.github/CODEOWNERS`:

```
# Judo Framework - Code Owners
# All code is maintained exclusively by CENTYC

* @FelipeFariasAlfaro
```

#### E. Agregar Pull Request Template

Crea el archivo `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
# ⚠️ Pull Requests Not Accepted

**This project does not accept Pull Requests.**

Judo Framework is professionally maintained by CENTYC (Centro Latinoamericano de Testing y Calidad del Software). All development and maintenance is handled exclusively by the CENTYC team.

## How to Contribute

We welcome your feedback through:

- 🐛 **Bug Reports** - [Create an Issue](https://github.com/FelipeFariasAlfaro/Judo-Framework/issues)
- 💡 **Feature Suggestions** - [Create an Issue](https://github.com/FelipeFariasAlfaro/Judo-Framework/issues)
- ❓ **Questions** - [GitHub Discussions](https://github.com/FelipeFariasAlfaro/Judo-Framework/discussions)

## Why This Policy?

This ensures:
- ✅ Consistent code quality and architecture
- ✅ Reliable releases and stability
- ✅ Professional support and maintenance
- ✅ Clear roadmap and direction

See [CONTRIBUTING.md](CONTRIBUTING.md) for complete details.

---

**This Pull Request will be closed automatically.**
```

#### F. Agregar Issue Templates

Crea el archivo `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug Report
about: Report a bug to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Create feature file with '...'
2. Run command '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g., Windows 10, macOS 13, Ubuntu 22.04]
- Python version: [e.g., 3.9.7]
- Judo Framework version: [e.g., 1.2.11]
- Behave version: [e.g., 1.2.6]

**Code sample**
```python
# Minimal code to reproduce the issue
```

**Error message/Stack trace**
```
Paste the complete error message here
```

**Additional context**
Add any other context about the problem here.
```

Crea el archivo `.github/ISSUE_TEMPLATE/feature_request.md`:

```markdown
---
name: Feature Request
about: Suggest an idea for Judo Framework
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

**Is your feature request related to a problem?**
A clear description of the problem. Ex. "I'm always frustrated when..."

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions or features you've considered.

**Use case**
Describe how this feature would be used in real scenarios.

**Example usage**
```gherkin
# Show how you envision using this feature
Feature: Example
  Scenario: Using new feature
    Given ...
    When ...
    Then ...
```

**Additional context**
Any other relevant information, mockups, examples from other tools, etc.
```

---

## 📋 Checklist de Configuración

### Archivos a Crear:

- [ ] `.github/workflows/close-prs.yml` - Auto-cierra PRs
- [ ] `.github/CODEOWNERS` - Define propietarios del código
- [ ] `.github/PULL_REQUEST_TEMPLATE.md` - Template para PRs
- [ ] `.github/ISSUE_TEMPLATE/bug_report.md` - Template para bugs
- [ ] `.github/ISSUE_TEMPLATE/feature_request.md` - Template para features

### Configuración en GitHub:

- [ ] Proteger rama `main` en Settings → Branches
- [ ] Activar Issues en Settings → Features
- [ ] Activar Discussions en Settings → Features
- [ ] Agregar descripción del repo mencionando la política
- [ ] Agregar topics: `api-testing`, `python`, `bdd`, `gherkin`, `behave`

### Documentación:

- [x] `CONTRIBUTING.md` actualizado
- [x] `README.md` actualizado con política
- [ ] Agregar badge en README: "Contributions: Issues Only"

---

## 🎯 Resultado Final

Con esta configuración:

1. ✅ El repositorio es público (necesario para PyPI y comunidad)
2. ✅ Cualquiera puede clonar y usar el código (MIT License)
3. ✅ Los PRs se cierran automáticamente con mensaje explicativo
4. ✅ Issues y Discussions están disponibles para feedback
5. ✅ Documentación clara sobre la política
6. ✅ Solo tú puedes hacer cambios en el código

---

## 💡 Alternativas Consideradas

### Opción 1: Repositorio Privado
- ❌ No permite que la comunidad vea el código
- ❌ No permite reportar issues públicamente
- ❌ No es apropiado para un framework open source

### Opción 2: Repositorio Público con Restricciones (RECOMENDADO)
- ✅ Código visible para todos
- ✅ Issues públicos para feedback
- ✅ Control total del desarrollo
- ✅ Apropiado para open source con mantenimiento profesional

### Opción 3: Aceptar PRs con Revisión Estricta
- ❌ Requiere tiempo para revisar
- ❌ Puede generar expectativas
- ❌ Difícil mantener consistencia

---

## 📞 Contacto

Si tienes dudas sobre esta configuración:
- Email: farias3felipe@gmail.com
- CENTYC: https://www.centyc.cl
