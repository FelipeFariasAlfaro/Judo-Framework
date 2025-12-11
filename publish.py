"""
Script para publicar Judo Framework a PyPI
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n{'='*70}")
    print(f"📦 {description}")
    print(f"{'='*70}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error: {description}")
        print(result.stderr)
        return False
    
    print(f"✅ {description} - Completado")
    return True

def main():
    print("🥋 Judo Framework - Publicación a PyPI")
    print("="*70)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("setup.py"):
        print("❌ Error: No se encuentra setup.py")
        print("   Ejecuta este script desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # Leer versión
    with open("setup.py", "r") as f:
        for line in f:
            if "version=" in line:
                version = line.split('"')[1]
                break
    
    print(f"📌 Versión a publicar: {version}")
    
    # Confirmar
    response = input("\n¿Deseas continuar con la publicación? (si/no): ")
    if response.lower() not in ['si', 's', 'yes', 'y']:
        print("❌ Publicación cancelada")
        sys.exit(0)
    
    # Limpiar builds anteriores
    print("\n🧹 Limpiando builds anteriores...")
    if os.path.exists("dist"):
        import shutil
        shutil.rmtree("dist")
    if os.path.exists("build"):
        import shutil
        shutil.rmtree("build")
    
    # Construir paquete
    if not run_command(
        "python setup.py sdist bdist_wheel",
        "Construyendo paquete"
    ):
        sys.exit(1)
    
    # Verificar que el archivo existe
    wheel_file = f"dist/judo_framework-{version}-py3-none-any.whl"
    if not os.path.exists(wheel_file):
        print(f"❌ Error: No se encontró {wheel_file}")
        sys.exit(1)
    
    print(f"\n✅ Paquete construido: {wheel_file}")
    
    # Verificar con twine
    print("\n🔍 Verificando paquete con twine...")
    if not run_command(
        "python -m twine check dist/*",
        "Verificación con twine"
    ):
        print("⚠️  Advertencia: twine check falló")
        print("   Instala twine con: pip install twine")
        response = input("¿Continuar de todas formas? (si/no): ")
        if response.lower() not in ['si', 's', 'yes', 'y']:
            sys.exit(1)
    
    # Publicar a PyPI
    print("\n" + "="*70)
    print("🚀 PUBLICANDO A PyPI")
    print("="*70)
    print("\nSe te pedirán tus credenciales de PyPI:")
    print("  - Username: tu_usuario_pypi")
    print("  - Password: tu_token_o_password")
    print("\nO puedes usar un token de API configurado en ~/.pypirc")
    
    response = input("\n¿Continuar con la publicación? (si/no): ")
    if response.lower() not in ['si', 's', 'yes', 'y']:
        print("❌ Publicación cancelada")
        sys.exit(0)
    
    # Publicar
    result = subprocess.run(
        "python -m twine upload dist/*",
        shell=True
    )
    
    if result.returncode == 0:
        print("\n" + "="*70)
        print("🎉 ¡PUBLICACIÓN EXITOSA!")
        print("="*70)
        print(f"\n✅ Judo Framework v{version} publicado en PyPI")
        print(f"\n📦 Instalar con: pip install judo-framework=={version}")
        print(f"🔗 Ver en PyPI: https://pypi.org/project/judo-framework/{version}/")
    else:
        print("\n❌ Error en la publicación")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Publicación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
