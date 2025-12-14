"""
Report Data Models - Data structures for test reporting
"""

import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class StepStatus(Enum):
    """Step execution status"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    PENDING = "pending"


class ScenarioStatus(Enum):
    """Scenario execution status"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class RequestData:
    """HTTP request data"""
    method: str = ""
    url: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)
    body: Any = None
    body_type: str = "json"  # json, form, text, binary
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "method": self.method,
            "url": self.url,
            "headers": self.headers,
            "params": self.params,
            "body": self.body,
            "body_type": self.body_type
        }


@dataclass
class ResponseData:
    """HTTP response data"""
    status_code: int = 0
    headers: Dict[str, str] = field(default_factory=dict)
    body: Any = None
    body_type: str = "json"  # json, text, binary
    elapsed_time: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "status_code": self.status_code,
            "headers": self.headers,
            "body": self.body,
            "body_type": self.body_type,
            "elapsed_time": self.elapsed_time
        }


@dataclass
class StepReport:
    """Individual step report"""
    step_text: str
    status: StepStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: float = 0.0
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    request_data: Optional[RequestData] = None
    response_data: Optional[ResponseData] = None
    variables_used: Dict[str, Any] = field(default_factory=dict)
    variables_set: Dict[str, Any] = field(default_factory=dict)
    assertions: List[Dict[str, Any]] = field(default_factory=list)
    screenshot_path: Optional[str] = None
    
    def finish(self, status: StepStatus, error_message: str = None, error_traceback: str = None):
        """Mark step as finished"""
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.status = status
        if error_message:
            self.error_message = error_message
        if error_traceback:
            self.error_traceback = error_traceback
    
    def add_request(self, method: str, url: str, headers: Dict = None, 
                   params: Dict = None, body: Any = None, body_type: str = "json"):
        """Add request data"""
        self.request_data = RequestData(
            method=method,
            url=url,
            headers=headers or {},
            params=params or {},
            body=body,
            body_type=body_type
        )
    
    def add_response(self, status_code: int, headers: Dict = None, 
                    body: Any = None, body_type: str = "json", elapsed_time: float = 0.0):
        """Add response data"""
        self.response_data = ResponseData(
            status_code=status_code,
            headers=headers or {},
            body=body,
            body_type=body_type,
            elapsed_time=elapsed_time
        )
    
    def add_assertion(self, description: str, expected: Any, actual: Any, passed: bool):
        """Add assertion result"""
        self.assertions.append({
            "description": description,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "timestamp": datetime.now().isoformat()
        })
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "step_text": self.step_text,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "error_message": self.error_message,
            "error_traceback": self.error_traceback,
            "request_data": self.request_data.to_dict() if self.request_data else None,
            "response_data": self.response_data.to_dict() if self.response_data else None,
            "variables_used": self.variables_used,
            "variables_set": self.variables_set,
            "assertions": self.assertions,
            "screenshot_path": self.screenshot_path
        }


@dataclass
class ScenarioReport:
    """Scenario report"""
    name: str
    feature_name: str
    tags: List[str] = field(default_factory=list)
    status: ScenarioStatus = ScenarioStatus.PASSED
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration: float = 0.0
    steps: List[StepReport] = field(default_factory=list)
    background_steps: List[StepReport] = field(default_factory=list)
    error_message: Optional[str] = None
    
    def add_step(self, step_text: str) -> StepReport:
        """Add a new step"""
        step = StepReport(step_text=step_text, status=StepStatus.PENDING, start_time=datetime.now())
        self.steps.append(step)
        return step
    
    def add_background_step(self, step_text: str) -> StepReport:
        """Add a background step"""
        step = StepReport(step_text=step_text, status=StepStatus.PENDING, start_time=datetime.now())
        self.background_steps.append(step)
        return step
    
    def finish(self, status: ScenarioStatus, error_message: str = None):
        """Mark scenario as finished"""
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.status = status
        if error_message:
            self.error_message = error_message
    
    def get_step_counts(self) -> Dict[str, int]:
        """Get step counts by status"""
        all_steps = self.background_steps + self.steps
        counts = {status.value: 0 for status in StepStatus}
        for step in all_steps:
            counts[step.status.value] += 1
        return counts
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "feature_name": self.feature_name,
            "tags": self.tags,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "background_steps": [step.to_dict() for step in self.background_steps],
            "steps": [step.to_dict() for step in self.steps],
            "error_message": self.error_message,
            "step_counts": self.get_step_counts()
        }


@dataclass
class FeatureReport:
    """Feature report"""
    name: str
    description: str = ""
    file_path: str = ""
    tags: List[str] = field(default_factory=list)
    scenarios: List[ScenarioReport] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration: float = 0.0
    
    def add_scenario(self, name: str, tags: List[str] = None) -> ScenarioReport:
        """Add a new scenario"""
        scenario = ScenarioReport(
            name=name,
            feature_name=self.name,
            tags=tags or []
        )
        self.scenarios.append(scenario)
        return scenario
    
    def finish(self):
        """Mark feature as finished"""
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
    
    def get_scenario_counts(self) -> Dict[str, int]:
        """Get scenario counts by status"""
        counts = {status.value: 0 for status in ScenarioStatus}
        for scenario in self.scenarios:
            counts[scenario.status.value] += 1
        return counts
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "file_path": self.file_path,
            "tags": self.tags,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "scenarios": [scenario.to_dict() for scenario in self.scenarios],
            "scenario_counts": self.get_scenario_counts()
        }


@dataclass
class ReportData:
    """Main report data container"""
    title: str = "Judo Framework Test Report"
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration: float = 0.0
    features: List[FeatureReport] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)
    configuration: Dict[str, Any] = field(default_factory=dict)
    
    def add_feature(self, name: str, description: str = "", file_path: str = "", 
                   tags: List[str] = None) -> FeatureReport:
        """Add a new feature"""
        feature = FeatureReport(
            name=name,
            description=description,
            file_path=file_path,
            tags=tags or []
        )
        self.features.append(feature)
        return feature
    
    def finish(self):
        """Mark report as finished"""
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        
        # Finish all features
        for feature in self.features:
            if not feature.end_time:
                feature.finish()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get report summary"""
        total_scenarios = sum(len(f.scenarios) for f in self.features)
        total_steps = sum(
            len(s.steps) + len(s.background_steps) 
            for f in self.features 
            for s in f.scenarios
        )
        
        scenario_counts = {status.value: 0 for status in ScenarioStatus}
        step_counts = {status.value: 0 for status in StepStatus}
        
        for feature in self.features:
            for scenario in feature.scenarios:
                scenario_counts[scenario.status.value] += 1
                for step in scenario.steps + scenario.background_steps:
                    step_counts[step.status.value] += 1
        
        return {
            "total_features": len(self.features),
            "total_scenarios": total_scenarios,
            "total_steps": total_steps,
            "scenario_counts": scenario_counts,
            "step_counts": step_counts,
            "success_rate": (scenario_counts["passed"] / total_scenarios * 100) if total_scenarios > 0 else 0
        }
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "title": self.title,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "features": [feature.to_dict() for feature in self.features],
            "environment": self.environment,
            "configuration": self.configuration,
            "summary": self.get_summary()
        }