#!/usr/bin/env python3
"""
Script para publicar Judo Framework en PyPI
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔄 {description}...")
    print(f"Ejecutando: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} completado exitosamente")
        if result.stdout:
            print(f"Output: {result.stdout}")
    else:
        print(f"❌ Error en {description}")
        print(f"Error: {result.stderr}")
        return False
    
    return True

def main():
    """Función principal de publicación"""
    print("🥋 Judo Framework - Script de Publicación")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("setup.py"):
        print("❌ Error: No se encontró setup.py. Ejecuta desde la raíz del proyecto.")
        sys.exit(1)
    
    # Limpiar builds anteriores
    if not run_command("rmdir /s /q build dist judo_framework.egg-info 2>nul || echo Limpieza completada", "Limpiando builds anteriores"):
        print("⚠️ Advertencia: No se pudieron limpiar algunos directorios (puede ser normal)")
    
    # Construir el paquete
    if not run_command("python -m build", "Construyendo el paquete"):
        print("❌ Error construyendo el paquete")
        sys.exit(1)
    
    # Verificar el paquete
    if not run_command("python -m twine check dist/*", "Verificando el paquete"):
        print("❌ Error verificando el paquete")
        sys.exit(1)
    
    # Publicar en PyPI
    if not run_command("python -m twine upload dist/*", "Publicando en PyPI"):
        print("❌ Error publicando en PyPI")
        sys.exit(1)
    
    print("\n🎉 ¡Publicación completada exitosamente!")
    print("🔗 https://pypi.org/project/judo-framework/1.3.38/")

if __name__ == "__main__":
    main()