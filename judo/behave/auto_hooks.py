"""
Auto Hooks - Hooks automáticos para captura de reportes
El usuario solo necesita importar esto en su environment.py
"""

import traceback
from ..reporting.reporter import get_reporter, reset_reporter
from ..reporting.report_data import StepStatus, ScenarioStatus


# Variables globales para el reporter
_reporter = None


def _get_or_create_reporter(context):
    """Obtener o crear reporter global"""
    global _reporter
    if _reporter is None:
        reset_reporter()
        _reporter = get_reporter()
        context.judo_reporter = _reporter
    return _reporter


def before_all_judo(context):
    """Hook automático: antes de todos los tests"""
    global _reporter
    reset_reporter()
    _reporter = get_reporter()
    context.judo_reporter = _reporter
    print("🥋 Judo Framework - Captura automática de reportes activada")


def before_feature_judo(context, feature):
    """Hook automático: antes de cada feature"""
    reporter = _get_or_create_reporter(context)
    reporter.start_feature(
        name=feature.name,
        description='\n'.join(feature.description) if feature.description else "",
        file_path=str(feature.filename) if hasattr(feature, 'filename') else "",
        tags=[tag for tag in feature.tags]
    )
    print(f"\n📋 Feature: {feature.name}")


def after_feature_judo(context, feature):
    """Hook automático: después de cada feature"""
    reporter = _get_or_create_reporter(context)
    reporter.finish_feature()
    print(f"✅ Feature completado: {feature.name}\n")


def before_scenario_judo(context, scenario):
    """Hook automático: antes de cada scenario"""
    reporter = _get_or_create_reporter(context)
    reporter.start_scenario(
        name=scenario.name,
        tags=[tag for tag in scenario.tags]
    )
    print(f"  📝 Scenario: {scenario.name}")


def after_scenario_judo(context, scenario):
    """Hook automático: después de cada scenario"""
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
    
    status_icon = "✅" if scenario.status.name == "passed" else "❌"
    print(f"  {status_icon} Scenario completado: {scenario.name}\n")


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
    
    status_icon = "✅" if step.status.name == "passed" else "❌" if step.status.name == "failed" else "⏭️"
    print(f"    {status_icon} {step.keyword} {step.name}")


def after_all_judo(context):
    """Hook automático: después de todos los tests"""
    reporter = _get_or_create_reporter(context)
    
    try:
        report_path = reporter.generate_html_report()
        print(f"\n📊 Reporte HTML generado: {report_path}")
        
        summary = reporter.get_report_data().get_summary()
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
