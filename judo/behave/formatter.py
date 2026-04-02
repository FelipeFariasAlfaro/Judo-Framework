"""
Judo Behave Formatter - Captura automática de datos para reportes
Se registra automáticamente como formatter de Behave
"""

import traceback
import os
from datetime import datetime
from behave.formatter.base import Formatter
from behave.model import Step, Scenario, Feature, ScenarioOutline
from ..reporting.reporter import get_reporter, reset_reporter
from ..reporting.report_data import StepStatus, ScenarioStatus


class JudoFormatter(Formatter):
    """
    Formatter de Behave que captura automáticamente todos los datos
    para generar reportes HTML completos sin necesidad de environment.py
    """
    
    name = 'judo'
    description = 'Judo Framework HTML Reporter'
    
    def __init__(self, stream_opener, config):
        """Inicializar formatter"""
        super(JudoFormatter, self).__init__(stream_opener, config)
        
        # Obtener directorio de salida desde variable de entorno (configurado por BaseRunner)
        import os
        output_dir = os.environ.get('JUDO_REPORT_OUTPUT_DIR', None)
        
        # Resetear reporter para nueva ejecución
        reset_reporter()
        self.reporter = get_reporter(output_dir=output_dir)
        
        # Estado actual
        self.current_feature = None
        self.current_scenario = None
        self.current_step = None
        
        # Tracking de scenarios procesados
        self.scenarios_in_feature = []
        
        from ..utils.safe_print import safe_emoji_print
        safe_emoji_print("🥋", "Judo Framework - Captura automática de reportes activada")
    
    def uri(self, uri):
        """Callback cuando se procesa un archivo"""
        pass
    
    def feature(self, feature):
        """Callback cuando comienza un feature"""
        # Finalizar feature anterior si existe
        if self.current_feature:
            self._finish_current_feature()
        
        self.current_feature = self.reporter.start_feature(
            name=feature.name,
            description='\n'.join(feature.description) if feature.description else "",
            file_path=str(feature.filename) if hasattr(feature, 'filename') else "",
            tags=[tag for tag in feature.tags]
        )
        self.scenarios_in_feature = []
        print(f"\n📋 Feature: {feature.name}")
    
    def background(self, background):
        """Callback para background"""
        pass
    
    def scenario(self, scenario):
        """Callback cuando comienza un scenario"""
        # Finalizar scenario anterior si existe
        if self.current_scenario:
            self._finish_current_scenario()
        
        self.current_scenario = self.reporter.start_scenario(
            name=scenario.name,
            tags=[tag for tag in scenario.tags]
        )
        self.scenarios_in_feature.append(self.current_scenario)
        print(f"  📝 Scenario: {scenario.name}")
    
    def step(self, step):
        """Callback cuando se ejecuta un step"""
        # Iniciar step si no existe
        if not self.current_step or self.current_step.step_text != f"{step.keyword}{step.name}":
            step_text = f"{step.keyword}{step.name}"
            self.current_step = self.reporter.start_step(step_text, is_background=False)
        
        # Determinar status del step
        if step.status.name == "passed":
            status = StepStatus.PASSED
        elif step.status.name == "failed":
            status = StepStatus.FAILED
        elif step.status.name == "skipped":
            status = StepStatus.SKIPPED
        else:
            status = StepStatus.PENDING
        
        # Capturar error si falló
        error_message = None
        error_traceback = None
        if step.status.name == "failed" and step.exception:
            error_message = str(step.exception)
            error_traceback = ''.join(traceback.format_exception(
                type(step.exception), 
                step.exception, 
                step.exception.__traceback__
            ))
        
        # Finalizar step
        self.reporter.finish_step(status, error_message, error_traceback)
        
        # Mostrar status
        status_icon = "✅" if step.status.name == "passed" else "❌" if step.status.name == "failed" else "⏭️"
        print(f"    {status_icon} {step.keyword}{step.name}")
        
        # Reset current step
        self.current_step = None
    
    def match(self, match):
        """Callback cuando se encuentra un match para un step"""
        pass
    
    def result(self, step):
        """Callback cuando termina un step con resultado"""
        # Este método se llama después de step(), así que no hacemos nada aquí
        pass
    
    def _finish_current_scenario(self):
        """Finalizar el scenario actual"""
        if self.current_scenario:
            # Determinar status basado en steps
            failed_steps = [s for s in self.current_scenario.steps 
                           if s.status == StepStatus.FAILED]
            status = ScenarioStatus.FAILED if failed_steps else ScenarioStatus.PASSED
            
            self.reporter.finish_scenario(status)
            print(f"  ✅ Scenario completado: {self.current_scenario.name}\n")
            self.current_scenario = None
    
    def _finish_current_feature(self):
        """Finalizar el feature actual"""
        # Finalizar scenario pendiente
        if self.current_scenario:
            self._finish_current_scenario()
        
        if self.current_feature:
            self.reporter.finish_feature()
            print(f"✅ Feature completado: {self.current_feature.name}\n")
            self.current_feature = None
    
    def eof(self):
        """Callback cuando termina el archivo (feature)"""
        self._finish_current_feature()
    
    def close(self):
        """Callback cuando se cierra el formatter (fin de ejecución)"""
        # Finalizar cualquier feature/scenario pendiente
        self._finish_current_feature()
        
        # Importar el módulo para evitar duplicados
        import judo.behave.auto_hooks as auto_hooks_module
        
        # Solo generar reporte si no se ha generado ya
        if not auto_hooks_module._report_generated:
            try:
                # Generar reporte HTML con nombre fijo
                report_path = self.reporter.generate_html_report("test_execution_report.html")
                print(f"\n📊 Reporte HTML generado: {report_path}")
                
                # Marcar como generado
                auto_hooks_module._report_generated = True
                
                # Mostrar resumen
                summary = self.reporter.get_report_data().get_summary()
                print(f"\n{'='*60}")
                print(f"📈 RESUMEN DE EJECUCIÓN")
                print(f"{'='*60}")
                print(f"Features:  {summary['total_features']}")
                print(f"Scenarios: {summary['total_scenarios']} (✅ {summary['scenario_counts']['passed']} | ❌ {summary['scenario_counts']['failed']} | ⏭️ {summary['scenario_counts']['skipped']})")
                print(f"Steps:     {summary['total_steps']} (✅ {summary['step_counts']['passed']} | ❌ {summary['step_counts']['failed']} | ⏭️ {summary['step_counts']['skipped']})")
                print(f"Tasa de éxito: {summary['success_rate']:.1f}%")
                print(f"{'='*60}\n")
                
            except Exception as e:
                print(f"⚠️ Error generando reporte: {e}")
                traceback.print_exc()
        
        super(JudoFormatter, self).close()
