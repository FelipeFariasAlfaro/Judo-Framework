"""
Ejemplo de Runner Básico
El usuario puede copiar este archivo a su proyecto y personalizarlo
"""

import sys
import os
from pathlib import Path

# Agregar judo al path (solo para desarrollo, no necesario si está instalado)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from judo.runner.base_runner import BaseRunner
from judo.runner.test_suite import TestSuite, CommonSuites


class MyBasicRunner(BaseRunner):
    """
    Runner básico personalizado
    Hereda de BaseRunner y agrega funcionalidad específica
    """
    
    def __init__(self):
        # Configurar directorios relativos al proyecto del usuario
        super().__init__(
            features_dir="features",           # Directorio con .feature files
            output_dir="test_reports",        # Directorio para reportes
            parallel=False,                   # Ejecución secuencial por defecto
            max_workers=4                     # Máximo 4 hilos si se habilita paralelo
        )
        
        # Configuración personalizada
        self.configure(
            timeout=300,        # 5 minutos por test
            fail_fast=False,    # Continuar aunque falle un test
            verbose=True        # Mostrar detalles
        )
    
    def setup_environment(self):
        """Configurar entorno antes de ejecutar tests"""
        self.log("🔧 Configurando entorno de pruebas...")
        
        # Configurar variables de entorno
        os.environ["JUDO_ENV"] = "test"
        os.environ["API_BASE_URL"] = "https://jsonplaceholder.typicode.com"
        
        # Crear directorios necesarios
        os.makedirs("test_data", exist_ok=True)
        os.makedirs("test_reports", exist_ok=True)
        
        self.log("✅ Entorno configurado")
    
    def cleanup_environment(self):
        """Limpiar después de ejecutar tests"""
        self.log("🧹 Limpiando entorno...")
        
        # Limpiar archivos temporales si es necesario
        # os.remove("temp_file.json")
        
        self.log("✅ Limpieza completada")
    
    def run_smoke_tests(self):
        """Ejecutar solo smoke tests"""
        self.log("💨 Ejecutando Smoke Tests")
        return self.run(tags=["@smoke"])
    
    def run_api_tests(self):
        """Ejecutar tests de API"""
        self.log("🌐 Ejecutando API Tests")
        return self.run(tags=["@api"])
    
    def run_regression_tests(self):
        """Ejecutar tests de regresión"""
        self.log("🔄 Ejecutando Regression Tests")
        return self.run(
            tags=["@regression", "@api"],
            exclude_tags=["@manual", "@slow"]
        )
    
    def run_all_tests(self):
        """Ejecutar todos los tests"""
        self.log("🎯 Ejecutando TODOS los tests")
        return self.run(exclude_tags=["@manual", "@wip"])


def main():
    """Función principal del runner"""
    print("🥋 My Basic Test Runner")
    print("=" * 50)
    
    # Crear runner
    runner = MyBasicRunner()
    
    # Configurar callbacks
    runner.set_callbacks(
        before_all=lambda: runner.setup_environment(),
        after_all=lambda results: runner.cleanup_environment()
    )
    
    # Determinar qué ejecutar basado en argumentos
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type == "smoke":
            results = runner.run_smoke_tests()
        elif test_type == "api":
            results = runner.run_api_tests()
        elif test_type == "regression":
            results = runner.run_regression_tests()
        elif test_type == "all":
            results = runner.run_all_tests()
        else:
            print(f"❌ Tipo de test desconocido: {test_type}")
            print("Tipos disponibles: smoke, api, regression, all")
            sys.exit(1)
    else:
        # Por defecto ejecutar smoke tests
        results = runner.run_smoke_tests()
    
    # Mostrar resumen
    success = runner.print_summary()
    
    # Exit code basado en resultados
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()