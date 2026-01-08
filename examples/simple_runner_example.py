#!/usr/bin/env python3
"""
Ejemplo de Runner Simplificado usando configuración desde .env

Este ejemplo demuestra cómo crear un runner extremadamente simple
que obtiene toda su configuración desde el archivo .env
"""

from judo.runner.base_runner import BaseRunner
import os


class SimpleRunner(BaseRunner):
    """
    Runner simplificado que usa configuración desde .env
    
    CONFIGURACIÓN:
    Todas las configuraciones se especifican en el archivo .env:
    - JUDO_FEATURES_DIR=features
    - JUDO_OUTPUT_DIR=judo_reports
    - JUDO_PARALLEL=false
    - JUDO_GENERATE_CUCUMBER_JSON=true
    - JUDO_SAVE_REQUESTS_RESPONSES=false
    - etc.
    """
    
    def __init__(self):
        # ¡Sin parámetros! Todo se carga desde .env
        super().__init__()
    
    def run_tests(self, tags=None):
        """Ejecuta tests con los tags especificados"""
        return self.run(tags=tags)


# Ejemplo de uso aún más simple usando el método de clase
def run_with_class_method():
    """Ejemplo usando el método de clase create_simple_runner()"""
    runner = BaseRunner.create_simple_runner()
    return runner.run(tags=["@smoke"])


if __name__ == "__main__":
    print("🥋 Judo Framework - Runner Simplificado")
    print("📋 Configuración cargada desde .env")
    
    # Opción 1: Usando clase personalizada
    runner = SimpleRunner()
    
    # Opción 2: Usando método de clase (aún más simple)
    # runner = BaseRunner.create_simple_runner()
    
    try:
        # Ejecutar todos los tests o con tags específicos
        results = runner.run_tests(tags=["@smoke"])  # o None para todos
        
        print(f"\n📊 Resultado: {results['passed']}/{results['total']} tests pasaron")
        
        if results['total'] > 0:
            success_rate = (results['passed'] / results['total']) * 100
            print(f"📈 Tasa de éxito: {success_rate:.1f}%")
            
            # El directorio de reportes se configura en .env
            output_dir = os.getenv('JUDO_OUTPUT_DIR', 'judo_reports')
            print(f"📄 Ver reporte HTML en: {output_dir}/test_execution_report.html")
        
        # Imprimir resumen
        runner.print_summary()
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        exit(1)