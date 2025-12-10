"""
Behave environment configuration for Judo Framework
This file is automatically loaded by Behave and sets up the test environment
"""

import os
import sys

# Add the project root to Python path so we can import judo
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import Judo Behave hooks
from judo.behave.hooks import before_all, before_scenario, after_scenario, after_all
from judo.reporting.reporter import get_reporter


def before_all(context):
    """Setup before all tests"""
    from judo.behave.hooks import before_all as judo_before_all
    judo_before_all(context)


def before_scenario(context, scenario):
    """Setup before each scenario"""
    from judo.behave.hooks import before_scenario as judo_before_scenario
    judo_before_scenario(context, scenario)
    
    # Start scenario in reporter
    reporter = get_reporter()
    if not hasattr(context, 'current_feature_started'):
        reporter.start_feature(scenario.feature.name, scenario.feature.description or "")
        context.current_feature_started = True
    
    reporter.start_scenario(scenario.name, [tag for tag in scenario.tags])


def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    from judo.behave.hooks import after_scenario as judo_after_scenario
    judo_after_scenario(context, scenario)
    
    # Finish scenario in reporter
    reporter = get_reporter()
    from judo.reporting.report_data import ScenarioStatus
    status = ScenarioStatus.PASSED if scenario.status == "passed" else ScenarioStatus.FAILED
    error_msg = str(scenario.exception) if hasattr(scenario, 'exception') and scenario.exception else None
    reporter.finish_scenario(status, error_msg)


def after_all(context):
    """Cleanup after all tests"""
    from judo.behave.hooks import after_all as judo_after_all
    judo_after_all(context)
    
    # Generate HTML report
    reporter = get_reporter()
    reporter.finish_feature()
    report_path = reporter.generate_html_report()
    print(f"\n📊 HTML Report generated: {report_path}")