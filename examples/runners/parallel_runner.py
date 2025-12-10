"""
Ejemplo de Runner con Ejecución Paralela
Demuestra cómo ejecutar tests en paralelo con diferentes configuraciones
"""

import sys
import os
from pathlib import Path

# Agregar judo al path (solo para desarrollo)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from judo.runner.base_runner import BaseRunner
from judo.runner.test_suite import TestSuite, CommonSuites


class MyParallelRunner(BaseRunner):
    """
    Runner con ejecución paralela optimizada
    """
    
    def __init__(self, max_workers: int = 6):
        super().__init__(
            features_dir="features",
            output_dir="parallel_reports",
            parallel=True,
            max_workers=max_workers
        )
        
        # Configuración para ejecución paralela
        self.configure(
            timeout=180,        # 3 minutos por test (más corto para paralelo)
            fail_fast=False,    # No parar en paralelo
            verbose=True
        )
        
        self.log(f"🚀 Runner paralelo configurado con {max_workers} hilos")
    
    def before_feature_execution(self, feature_file):
        """Callback antes de ejecutar cada feature"""
        self.log(f"🎬 Iniciando: {feature_file.name}")
    
    def after_feature_execution(self, feature_file, result):
        """Callback después de ejecutar cada feature"""
        status = "✅" if result["success"] else "❌"
        self.log(f"{status} Completado: {feature_file.name} ({result['duration']:.2f}s)")
    
    def run_fast_suite(self):
        """Ejecutar suite rápida en paralelo"""
        self.log("⚡ Ejecutando Fast Test Suite")
        
        # Configurar para máxima velocidad
        self.set_parallel(True, max_workers=8)
        self.configure(timeout=120, fail_fast=False)
        
        return self.run(
            tags=["@fast", "@smoke", "@api"],
            exclude_tags=["@slow", "@manual", "@integration"]
        )
    
    def run_comprehensive_suite(self):
        """Ejecutar suite completa en paralelo"""
        self.log("🎯 Ejecutando Comprehensive Test Suite")
        
        # Configurar para ejecución completa
        self.set_parallel(True, max_workers=4)
        self.configure(timeout=300, fail_fast=False)
        
        return self.run(exclude_tags=["@manual", "@wip"])
    
    def run_by_environment(self, environment: str):
        """Ejecutar tests para un entorno específico"""
        self.log(f"🌍 Ejecutando tests para entorno: {environment}")
        
        # Configurar variables de entorno
        env_configs = {
            "dev": {
                "API_BASE_URL": "https://api-dev.example.com",
                "TIMEOUT": "30"
            },
            "test": {
                "API_BASE_URL": "https://api-test.example.com", 
                "TIMEOUT": "60"
            },
            "prod": {
                "API_BASE_URL": "https://api.example.com",
                "TIMEOUT": "120"
            }
        }
        
        if environment in env_configs:
            for key, value in env_configs[environment].items():
                os.environ[key] = value
            
            return self.run(
                tags=[f"@{environment}", "@api"],
                exclude_tags=["@manual"]
            )
        else:
            self.log(f"❌ Entorno desconocido: {environment}")
            return {"failed": 1}


class AdvancedParallelRunner(MyParallelRunner):
    """
    Runner avanzado con funcionalidades adicionales
    """
    
    def __init__(self):
        super().__init__(max_workers=8)
        
        # Estadísticas avanzadas
        self.feature_stats = {}
        self.thread_stats = {}
    
    def run_with_retry(self, max_retries: int = 2):
        """Ejecutar con reintentos automáticos"""
        self.log(f"🔄 Ejecutando con hasta {max_retries} reintentos")
        
        for attempt in range(max_retries + 1):
            if attempt > 0:
                self.log(f"🔁 Intento {attempt + 1}/{max_retries + 1}")
            
            results = self.run(exclude_tags=["@manual"])
            
            if results["failed"] == 0:
                self.log("✅ Todos los tests pasaron!")
                return results
            
            if attempt < max_retries:
                self.log(f"⚠️ {results['failed']} tests fallaron, reintentando...")
                # Reset estadísticas para el siguiente intento
                self.results = {
                    "total": 0, "passed": 0, "failed": 0, "skipped": 0,
                    "start_time": None, "end_time": None, "duration": 0
                }
        
        self.log(f"❌ Tests fallaron después de {max_retries + 1} intentos")
        return results
    
    def run_load_test(self, concurrent_users: int = 10):
        """Simular carga con múltiples usuarios concurrentes"""
        self.log(f"🏋️ Ejecutando load test con {concurrent_users} usuarios concurrentes")
        
        # Configurar para alta concurrencia
        self.set_parallel(True, max_workers=concurrent_users)
        self.configure(timeout=60, fail_fast=False)
        
        return self.run(tags=["@load", "@performance"])


def main():
    """Función principal"""
    print("🚀 Parallel Test Runner")
    print("=" * 50)
    
    # Determinar tipo de runner
    runner_type = sys.argv[1] if len(sys.argv) > 1 else "basic"
    
    if runner_type == "advanced":
        runner = AdvancedParallelRunner()
    else:
        runner = MyParallelRunner()
    
    # Configurar callbacks
    runner.set_callbacks(
        before_feature=runner.before_feature_execution,
        after_feature=runner.after_feature_execution
    )
    
    # Determinar qué ejecutar
    command = sys.argv[2] if len(sys.argv) > 2 else "fast"
    
    if command == "fast":
        results = runner.run_fast_suite()
    elif command == "comprehensive":
        results = runner.run_comprehensive_suite()
    elif command.startswith("env:"):
        env = command.split(":")[1]
        results = runner.run_by_environment(env)
    elif command == "retry" and isinstance(runner, AdvancedParallelRunner):
        results = runner.run_with_retry(max_retries=3)
    elif command == "load" and isinstance(runner, AdvancedParallelRunner):
        results = runner.run_load_test(concurrent_users=15)
    else:
        print(f"❌ Comando desconocido: {command}")
        print("Comandos disponibles: fast, comprehensive, env:dev, env:test, env:prod")
        if runner_type == "advanced":
            print("Comandos avanzados: retry, load")
        sys.exit(1)
    
    # Mostrar resumen
    success = runner.print_summary()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()