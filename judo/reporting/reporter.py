"""
Integrated Reporter - Captures test execution data automatically
"""

import json
import traceback
from datetime import datetime
from typing import Any, Dict, Optional
from .report_data import ReportData, FeatureReport, ScenarioReport, StepReport, StepStatus, ScenarioStatus
from .html_reporter import HTMLReporter


class JudoReporter:
    """
    Integrated reporter that captures test execution data
    """
    
    def __init__(self, title: str = "Judo Framework Test Report", output_dir: str = None):
        """Initialize reporter"""
        self.report_data = ReportData(title=title)
        self.current_feature: Optional[FeatureReport] = None
        self.current_scenario: Optional[ScenarioReport] = None
        self.current_step: Optional[StepReport] = None
        
        # Usar directorio del proyecto del usuario
        if output_dir is None:
            import os
            output_dir = os.path.join(os.getcwd(), "judo_reports")
        
        self.html_reporter = HTMLReporter(output_dir)
        
        # Capture environment info
        import os
        import platform
        self.report_data.environment = {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "judo_version": "1.0.0",
            "working_directory": os.getcwd(),
            "timestamp": datetime.now().isoformat()
        }
    
    def start_feature(self, name: str, description: str = "", file_path: str = "", 
                     tags: list = None) -> FeatureReport:
        """Start a new feature"""
        self.current_feature = self.report_data.add_feature(name, description, file_path, tags or [])
        return self.current_feature
    
    def start_scenario(self, name: str, tags: list = None) -> ScenarioReport:
        """Start a new scenario"""
        if not self.current_feature:
            self.current_feature = self.start_feature("Default Feature")
        
        self.current_scenario = self.current_feature.add_scenario(name, tags or [])
        return self.current_scenario
    
    def start_step(self, step_text: str, is_background: bool = False) -> StepReport:
        """Start a new step"""
        if not self.current_scenario:
            self.current_scenario = self.start_scenario("Default Scenario")
        
        if is_background:
            self.current_step = self.current_scenario.add_background_step(step_text)
        else:
            self.current_step = self.current_scenario.add_step(step_text)
        
        return self.current_step
    
    def log_request(self, method: str, url: str, headers: Dict = None, 
                   params: Dict = None, body: Any = None, body_type: str = "json"):
        """Log HTTP request data"""
        if self.current_step:
            self.current_step.add_request(method, url, headers, params, body, body_type)
    
    def log_response(self, status_code: int, headers: Dict = None, body: Any = None, 
                    body_type: str = "json", elapsed_time: float = 0.0):
        """Log HTTP response data"""
        if self.current_step:
            self.current_step.add_response(status_code, headers, body, body_type, elapsed_time)
    
    def log_assertion(self, description: str, expected: Any, actual: Any, passed: bool):
        """Log assertion result"""
        if self.current_step:
            self.current_step.add_assertion(description, expected, actual, passed)
    
    def log_variable_used(self, name: str, value: Any):
        """Log variable usage"""
        if self.current_step:
            self.current_step.variables_used[name] = value
    
    def log_variable_set(self, name: str, value: Any):
        """Log variable assignment"""
        if self.current_step:
            self.current_step.variables_set[name] = value
    
    def finish_step(self, status: StepStatus = StepStatus.PASSED, 
                   error_message: str = None, error_traceback: str = None):
        """Finish current step"""
        if self.current_step:
            self.current_step.finish(status, error_message, error_traceback)
    
    def finish_scenario(self, status: ScenarioStatus = None, error_message: str = None):
        """Finish current scenario"""
        if self.current_scenario:
            # Auto-determine status if not provided
            if status is None:
                failed_steps = [s for s in self.current_scenario.steps + self.current_scenario.background_steps 
                               if s.status == StepStatus.FAILED]
                status = ScenarioStatus.FAILED if failed_steps else ScenarioStatus.PASSED
            
            self.current_scenario.finish(status, error_message)
    
    def finish_feature(self):
        """Finish current feature"""
        if self.current_feature:
            self.current_feature.finish()
    
    def generate_html_report(self, filename: str = None) -> str:
        """Generate HTML report"""
        self.report_data.finish()
        return self.html_reporter.generate_report(self.report_data, filename)
    
    def get_report_data(self) -> ReportData:
        """Get current report data"""
        return self.report_data


# Global reporter instance
_global_reporter: Optional[JudoReporter] = None


def get_reporter() -> JudoReporter:
    """Get global reporter instance"""
    global _global_reporter
    if _global_reporter is None:
        _global_reporter = JudoReporter()
    return _global_reporter


def set_reporter(reporter: JudoReporter):
    """Set global reporter instance"""
    global _global_reporter
    _global_reporter = reporter


def reset_reporter():
    """Reset global reporter"""
    global _global_reporter
    _global_reporter = None