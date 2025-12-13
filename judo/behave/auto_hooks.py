"""
Auto Hooks - Hooks automáticos para captura de reportes
El usuario solo necesita importar esto en su environment.py
"""

import traceback
from ..reporting.reporter import get_reporter, reset_reporter
from ..reporting.report_data import StepStatus, ScenarioStatus


# Variables globales para el reporter
_reporter = None
_report_generated = False


def _get_or_create_reporter(context):
    """Obtener o crear reporter global"""
    global _reporter
    
    # Primero intentar usar el reporter global existente
    existing_reporter = get_reporter()
    if existing_reporter is not None:
        _reporter = existing_reporter
        context.judo_reporter = _reporter
        return _reporter
    
    # Solo crear uno nuevo si no existe ninguno
    if _reporter is None:
        reset_reporter()
        _reporter = get_reporter()
        context.judo_reporter = _reporter
    return _reporter


def before_all_judo(context):
    """Hook automático: antes de todos los tests"""
    global _reporter, _report_generated
    
    # IMPORTANTE: NO hacer reset si ya existe un reporter global (configurado por BaseRunner)
    # Solo obtener el reporter existente o crear uno nuevo si no existe
    existing_reporter = get_reporter()
    if existing_reporter is not None:
        _reporter = existing_reporter
    else:
        reset_reporter()
        _reporter = get_reporter()
    
    _report_generated = False  # Reset flag
    context.judo_reporter = _reporter
    
    # IMPORTANT: Also call the main Judo hooks for request/response logging
    from .hooks import before_all as judo_main_before_all
    judo_main_before_all(context)
    
    from ..utils.safe_print import safe_emoji_print
    safe_emoji_print("🥋", "Judo Framework - Captura automática de reportes activada")


def before_feature_judo(context, feature):
    """Hook automático: antes de cada feature"""
    reporter = _get_or_create_reporter(context)
    reporter.start_feature(
        name=feature.name,
        description='\n'.join(feature.description) if feature.description else "",
        file_path=str(feature.filename) if hasattr(feature, 'filename') else "",
        tags=[tag for tag in feature.tags]
    )
    from ..utils.safe_print import safe_emoji_print
    safe_emoji_print("📋", f"Feature: {feature.name}")


def after_feature_judo(context, feature):
    """Hook automático: después de cada feature"""
    reporter = _get_or_create_reporter(context)
    reporter.finish_feature()
    from ..utils.safe_print import safe_emoji_print
    safe_emoji_print("✅", f"Feature completado: {feature.name}")


def before_scenario_judo(context, scenario):
    """Hook automático: antes de cada scenario"""
    # IMPORTANT: Call the main Judo hooks for request/response logging FIRST
    from .hooks import before_scenario as judo_main_before_scenario
    judo_main_before_scenario(context, scenario)
    
    # Then handle reporting
    reporter = _get_or_create_reporter(context)
    reporter.start_scenario(
        name=scenario.name,
        tags=[tag for tag in scenario.tags]
    )
    from ..utils.safe_print import safe_emoji_print
    safe_emoji_print("📝", f"Scenario: {scenario.name}")


def after_scenario_judo(context, scenario):
    """Hook automático: después de cada scenario"""
    # IMPORTANT: Call the main Judo hooks for cleanup FIRST
    from .hooks import after_scenario as judo_main_after_scenario
    judo_main_after_scenario(context, scenario)
    
    reporter = _get_or_create_reporter(context)
    
    # Determinar status
    if scenario.status.name == "passed":
        status = ScenarioStatus.PASSED
    elif scenario.status.name == "failed":
        status = ScenarioStatus.FAILED
    else:
        status = ScenarioStatus.SKIPPED
    
    # Capturar error si falló
    error_message = None
    if scenario.status.name == "failed":
        for step in scenario.steps:
            if step.status.name == "failed" and step.exception:
                error_message = str(step.exception)
                break
    
    reporter.finish_scenario(status, error_message)
    
    from ..utils.safe_print import safe_print
    status_icon = "✅" if scenario.status.name == "passed" else "❌"
    safe_print(f"  {status_icon} Scenario completado: {scenario.name}\n", f"  [{scenario.status.name.upper()}] Scenario completado: {scenario.name}\n")


def before_step_judo(context, step):
    """Hook automático: antes de cada step"""
    reporter = _get_or_create_reporter(context)
    step_text = f"{step.keyword} {step.name}"
    reporter.start_step(step_text, is_background=False)


def after_step_judo(context, step):
    """Hook automático: después de cada step"""
    reporter = _get_or_create_reporter(context)
    
    # Determinar status
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
    
    reporter.finish_step(status, error_message, error_traceback)
    
    from ..utils.safe_print import safe_print
    status_icon = "✅" if step.status.name == "passed" else "❌" if step.status.name == "failed" else "⏭️"
    safe_print(f"    {status_icon} {step.keyword} {step.name}", f"    [{step.status.name.upper()}] {step.keyword} {step.name}")


def after_all_judo(context):
    """Hook automático: después de todos los tests"""
    global _report_generated
    
    # Solo generar reporte si no se ha generado ya (evitar duplicados)
    if not _report_generated:
        reporter = _get_or_create_reporter(context)
        
        try:
            # Generar reporte con nombre fijo
            report_path = reporter.generate_html_report("test_execution_report.html")
            from ..utils.safe_print import safe_print, safe_emoji_print
            safe_emoji_print("📊", f"Reporte HTML generado: {report_path}")
            _report_generated = True
            
            summary = reporter.get_report_data().get_summary()
            print(f"\n{'='*60}")
            safe_emoji_print("📈", "RESUMEN DE EJECUCIÓN")
            print(f"{'='*60}")
            print(f"Features:  {summary['total_features']}")
            
            # Safe print for scenario summary with emojis
            scenario_summary = f"Scenarios: {summary['total_scenarios']} (✅ {summary['scenario_counts']['passed']} | ❌ {summary['scenario_counts']['failed']} | ⏭️ {summary['scenario_counts']['skipped']})"
            scenario_fallback = f"Scenarios: {summary['total_scenarios']} (PASSED: {summary['scenario_counts']['passed']} | FAILED: {summary['scenario_counts']['failed']} | SKIPPED: {summary['scenario_counts']['skipped']})"
            safe_print(scenario_summary, scenario_fallback)
            
            # Safe print for steps summary with emojis
            steps_summary = f"Steps:     {summary['total_steps']} (✅ {summary['step_counts']['passed']} | ❌ {summary['step_counts']['failed']} | ⏭️ {summary['step_counts']['skipped']})"
            steps_fallback = f"Steps:     {summary['total_steps']} (PASSED: {summary['step_counts']['passed']} | FAILED: {summary['step_counts']['failed']} | SKIPPED: {summary['step_counts']['skipped']})"
            safe_print(steps_summary, steps_fallback)
            
            print(f"Tasa de éxito: {summary['success_rate']:.1f}%")
            print(f"{'='*60}\n")
        except Exception as e:
            from ..utils.safe_print import safe_emoji_print
            safe_emoji_print("⚠️", f"Error generando reporte: {e}")
            traceback.print_exc()
    
    # IMPORTANT: Also call the main Judo hooks for cleanup
    from .hooks import after_all as judo_main_after_all
    judo_main_after_all(context)
