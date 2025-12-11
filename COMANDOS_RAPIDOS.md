# 🚀 Comandos Rápidos - Configuración GitHub

## 📤 1. Subir Cambios a GitHub

```bash
# Ver archivos nuevos
git status

# Agregar todos los archivos de configuración
git add .github/ CONTRIBUTING.md README.md CONFIGURACION_GITHUB.md RESUMEN_CONFIGURACION.md COMANDOS_RAPIDOS.md

# Hacer commit
git commit -m "feat: add contribution policy (issues only) and GitHub configuration

- Add GitHub Actions workflow to auto-close PRs
- Add issue templates for bugs and features
- Add CODEOWNERS file
- Update CONTRIBUTING.md with issues-only policy
- Update README.md with contribution policy
- Add comprehensive setup documentation"

# Push a GitHub
git push origin main
```

---

## 🧪 2. Probar Auto-Cierre de PRs

```bash
# Crear rama de prueba
git checkout -b test-pr-close

# Hacer un cambio pequeño
echo "# Test PR Auto-Close" > TEST_PR.md
git add TEST_PR.md
git commit -m "test: verify PR auto-close workflow"

# Push de la rama
git push origin test-pr-close

# Ahora ve a GitHub y crea un PR desde test-pr-close a main
# Debería cerrarse automáticamente

# Después de verificar, volver a main y limpiar
git checkout main
git branch -D test-pr-close
git push origin --delete test-pr-close
rm TEST_PR.md
```

---

## 🔍 3. Verificar Estado

```bash
# Ver archivos creados
ls -la .github/
ls -la .github/workflows/
ls -la .github/ISSUE_TEMPLATE/

# Ver contenido de archivos importantes
cat .github/workflows/close-prs.yml
cat .github/CODEOWNERS
cat CONTRIBUTING.md
```

---

## 🌐 4. URLs Importantes

Después del push, visita estas URLs (reemplaza con tu usuario si es diferente):

### Configuración del Repositorio
```
https://github.com/FelipeFariasAlfaro/Judo-Framework/settings
```

### Protección de Ramas
```
https://github.com/FelipeFariasAlfaro/Judo-Framework/settings/branches
```

### Configuración de Actions
```
https://github.com/FelipeFariasAlfaro/Judo-Framework/settings/actions
```

### Ver Issues
```
https://github.com/FelipeFariasAlfaro/Judo-Framework/issues
```

### Ver Discussions
```
https://github.com/FelipeFariasAlfaro/Judo-Framework/discussions
```

### Ver Actions (Workflows)
```
https://github.com/FelipeFariasAlfaro/Judo-Framework/actions
```

---

## ⚙️ 5. Configuración Manual en GitHub

### Proteger Rama Main
```
1. Ir a: Settings → Branches → Add rule
2. Branch name pattern: main
3. Activar:
   ☑ Require a pull request before merging
   ☑ Require review from Code Owners
   ☑ Restrict who can push to matching branches
     → Agregar: FelipeFariasAlfaro
4. Save changes
```

### Configurar Actions
```
1. Ir a: Settings → Actions → General
2. Actions permissions: Allow all actions
3. Workflow permissions: Read and write permissions
4. ☑ Allow GitHub Actions to create and approve pull requests
5. Save
```

### Habilitar Discussions
```
1. Ir a: Settings → General → Features
2. ☑ Discussions
3. Save
4. Ir a pestaña Discussions
5. Crear categorías: Q&A, Ideas, Show and tell, General
```

---

## 📊 6. Verificar Todo Funciona

### Checklist Rápido
```bash
# 1. Archivos existen
[ -f .github/workflows/close-prs.yml ] && echo "✅ Workflow existe" || echo "❌ Falta workflow"
[ -f .github/CODEOWNERS ] && echo "✅ CODEOWNERS existe" || echo "❌ Falta CODEOWNERS"
[ -f .github/PULL_REQUEST_TEMPLATE.md ] && echo "✅ PR template existe" || echo "❌ Falta PR template"
[ -f .github/ISSUE_TEMPLATE/bug_report.md ] && echo "✅ Bug template existe" || echo "❌ Falta bug template"
[ -f .github/ISSUE_TEMPLATE/feature_request.md ] && echo "✅ Feature template existe" || echo "❌ Falta feature template"
[ -f CONTRIBUTING.md ] && echo "✅ CONTRIBUTING.md existe" || echo "❌ Falta CONTRIBUTING.md"

# 2. Git status
git status

# 3. Ver último commit
git log -1 --oneline
```

---

## 🔄 7. Si Necesitas Revertir

```bash
# Ver commits recientes
git log --oneline -5

# Revertir último commit (mantiene cambios)
git reset --soft HEAD~1

# Revertir último commit (elimina cambios)
git reset --hard HEAD~1

# Eliminar archivos de .github
rm -rf .github/
git add .github/
git commit -m "revert: remove GitHub configuration"
git push origin main
```

---

## 📝 8. Actualizar Documentación

```bash
# Si necesitas editar algún archivo
nano CONTRIBUTING.md
# o
code CONTRIBUTING.md

# Después de editar
git add CONTRIBUTING.md
git commit -m "docs: update contributing guidelines"
git push origin main
```

---

## 🎯 9. Comandos de Mantenimiento

```bash
# Ver todas las ramas
git branch -a

# Limpiar ramas locales eliminadas en remoto
git fetch --prune

# Ver tamaño del repositorio
du -sh .git

# Ver archivos más grandes
git ls-files | xargs ls -lh | sort -k5 -hr | head -10
```

---

## 📧 10. Contacto y Soporte

Si algo no funciona:

```bash
# Verificar versión de Git
git --version

# Verificar usuario de Git
git config user.name
git config user.email

# Ver configuración de Git
git config --list
```

**Email:** farias3felipe@gmail.com  
**CENTYC:** https://www.centyc.cl

---

## ✅ Resumen de Comandos Esenciales

```bash
# 1. Subir todo
git add .github/ CONTRIBUTING.md README.md *.md
git commit -m "feat: add contribution policy and GitHub config"
git push origin main

# 2. Verificar
git status
ls -la .github/

# 3. Probar PR auto-close
git checkout -b test-pr-close
echo "test" > test.txt
git add test.txt
git commit -m "test"
git push origin test-pr-close
# Crear PR en GitHub, verificar que se cierra
git checkout main
git branch -D test-pr-close
git push origin --delete test-pr-close
```

---

**Made with ❤️ at CENTYC** 🥋
