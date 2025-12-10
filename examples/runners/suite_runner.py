"""
Ejemplo de Runner con Test Suites
Demuestra cómo usar TestSuite para organizar y ejecutar tests
"""

import sys
import os
from pathlib import Path

# Agregar judo al path (solo para desarrollo)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from judo.runner.base_runner import BaseRunner
from judo.runner.test_suite import TestSuite, CommonSuites


class MySuiteRunner(BaseRunner):
    """
    Runner que utiliza Test Suites para organizar ejecución
    """
    
    def __init__(self):
        super().__init__(
            features_dir="features",
            output_dir="suite_reports"
        )
        
        # Crear suites personalizadas
        self.suites = self._create_custom_suites()
    
    def _create_custom_suites(self) -> dict:
        """Crear suites de tests personalizadas"""
        suites = {}
        
        # Suite de Smoke Tests
        suites["smoke"] = TestSuite(
            name="Smoke Tests",
            description="Tests críticos que deben pasar siempre"
        ).add_features_by_tag(["@smoke"]).set_config(
            parallel=True,
            max_workers=2,
            fail_fast=True,
            timeout=120
        )
        
        # Suite de API Tests
        suites["api"] = TestSuite(
            name="API Tests",
            description="Tests completos de APIs REST"
        ).add_features_by_tag(["@api"]).exclude_by_tag(["@manual"]).set_config(
            parallel=True,
            max_workers=4,
            timeout=180
        )
        
        # Suite de Regression Tests
        suites["regression"] = TestSuite(
            name="Regression Tests",
            description="Tests de regresión completos"
        ).add_features_by_tag(["@regression"]).exclude_by_tag(["@wip", "@manual"]).set_config(
            parallel=True,
            max_workers=6,
            timeout=300
        )
        
        # Suite de Integration Tests
        suites["integration"] = TestSuite(
            name="Integration Tests",
            description="Tests de integración entre servicios"
        ).add_features_by_tag(["@integration"]).set_config(
            parallel=False,  # Integración puede requerir orden específico
            timeout=600
        )
        
        # Suite personalizada por features específicos
        suites["user_management"] = TestSuite(
            name="User Management Tests",
            description="Tests específicos de gestión de usuarios"
        ).add_feature("features/user_api.feature").add_feature("features/user_auth.feature").set_config(
            parallel=True,
            max_workers=2
        )
        
        # Suite de Performance Tests
        suites["performance"] = TestSuite(
            name="Performance Tests",
            description="Tests de rendimiento y carga"
        ).add_features_by_tag(["@performance", "@load"]).set_config(
            parallel=True,
            max_workers=8,
            timeout=900
        )
        
        return suites
    
    def run_suite(self, suite_name: str):
        """Ejecutar una suite específica"""
        if suite_name not in self.suites:
            self.log(f"❌ Suite desconocida: {suite_name}")
            self.log(f"Suites disponibles: {', '.join(self.suites.keys())}")
            return {"failed": 1}
        
        suite = self.suites[suite_name]
        self.log(f"🎯 Ejecutando suite: {suite.name}")
        self.log(f"📝 Descripción: {suite.description}")
        
        # Aplicar configuración de la suite
        config = suite.config
        if config.get("parallel"):
            self.set_parallel(True, config.get("max_workers", 4))
        else:
            self.set_parallel(False)
        
        self.configure(**{k: v for k, v in config.items() if k not in ["parallel", "max_workers"]})
        
        # Ejecutar con tags de la suite
        return self.run(
            tags=suite.get_tags(),
            exclude_tags=suite.get_exclude_tags()
        )
    
    def run_multiple_suites(self, suite_names: list):
        """Ejecutar múltiples suites secuencialmente"""
        self.log(f"🎯 Ejecutando múltiples suites: {', '.join(suite_names)}")
        
        all_results = {
            "total": 0, "passed": 0, "failed": 0, "skipped": 0,
            "suites": {}
        }
        
        for suite_name in suite_names:
            self.log(f"\n{'='*20} {suite_name.upper()} {'='*20}")
            
            # Reset estadísticas para cada suite
            self.results = {
                "total": 0, "passed": 0, "failed": 0, "skipped": 0,
                "start_time": None, "end_time": None, "duration": 0
            }
            
            suite_results = self.run_suite(suite_name)
            
            # Acumular resultados
            all_results["total"] += suite_results["total"]
            all_results["passed"] += suite_results["passed"]
            all_results["failed"] += suite_results["failed"]
            all_results["skipped"] += suite_results["skipped"]
            all_results["suites"][suite_name] = suite_results
        
        # Actualizar resultados globales
        self.results = all_results
        
        return all_results
    
    def create_custom_suite_from_config(self, config_file: str):
        """Crear suite desde archivo de configuración"""
        try:
            suite = TestSuite.load_from_file(config_file)
            self.suites[suite.name.lower().replace(" ", "_")] = suite
            self.log(f"✅ Suite cargada desde {config_file}: {suite.name}")
            return suite
        except Exception as e:
            self.log(f"❌ Error cargando suite desde {config_file}: {e}")
            return None
    
    def save_suite_to_file(self, suite_name: str, filepath: str):
        """Guardar suite a archivo"""
        if suite_name in self.suites:
            self.suites[suite_name].save_to_file(filepath)
            self.log(f"✅ Suite '{suite_name}' guardada en {filepath}")
        else:
            self.log(f"❌ Suite '{suite_name}' no encontrada")
    
    def list_suites(self):
        """Listar todas las suites disponibles"""
        self.log("📋 Suites disponibles:")
        for name, suite in self.suites.items():
            self.log(f"  • {name}: {suite.description}")
            if suite.tags:
                self.log(f"    Tags: {', '.join(suite.tags)}")
            if suite.exclude_tags:
                self.log(f"    Excluye: {', '.join(suite.exclude_tags)}")


def main():
    """Función principal"""
    print("🎯 Suite-based Test Runner")
    print("=" * 50)
    
    runner = MySuiteRunner()
    
    if len(sys.argv) < 2:
        runner.list_suites()
        print("\nUso: python suite_runner.py <suite_name>")
        print("     python suite_runner.py multiple <suite1> <suite2> ...")
        print("     python suite_runner.py list")
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == "list":
        runner.list_suites()
        sys.exit(0)
    elif command == "multiple":
        if len(sys.argv) < 3:
            print("❌ Especifica al menos una suite para ejecutar")
            sys.exit(1)
        
        suite_names = sys.argv[2:]
        results = runner.run_multiple_suites(suite_names)
        
        # Mostrar resumen de múltiples suites
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE MÚLTIPLES SUITES")
        print("=" * 60)
        
        for suite_name, suite_results in results["suites"].items():
            status = "✅" if suite_results["failed"] == 0 else "❌"
            print(f"{status} {suite_name}: {suite_results['passed']}/{suite_results['total']} passed")
        
        print(f"\n🎯 TOTAL GENERAL:")
        print(f"   Total: {results['total']}")
        print(f"   Exitosos: {results['passed']}")
        print(f"   Fallidos: {results['failed']}")
        
        success = results["failed"] == 0
        
    else:
        # Ejecutar suite individual
        results = runner.run_suite(command)
        success = runner.print_summary()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()