"""
HTML Reporter - Generate comprehensive HTML reports for Judo Framework tests
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from .report_data import ReportData


class HTMLReporter:
    """
    HTML report generator for Judo Framework
    Creates detailed reports with request/response data, assertions, and more
    """
    
    def __init__(self, output_dir: str = None):
        """Initialize HTML reporter"""
        if output_dir is None:
            # Usar directorio actual del proyecto del usuario
            import os
            output_dir = os.path.join(os.getcwd(), "judo_reports")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, report_data: ReportData, filename: str = None) -> str:
        """Generate HTML report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"judo_report_{timestamp}.html"
        
        report_path = self.output_dir / filename
        
        # Generate HTML content
        html_content = self._generate_html(report_data)
        
        # Write to file
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(report_path)
    
    def _generate_html(self, report_data: ReportData) -> str:
        """Generate complete HTML report"""
        summary = report_data.get_summary()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_data.title}</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        {self._generate_header(report_data, summary)}
        {self._generate_summary_section(summary)}
        {self._generate_features_section(report_data.features)}
    </div>
    
    <script>
        {self._get_javascript()}
    </script>
</body>
</html>
        """
        return html
    
    def _generate_header(self, report_data: ReportData, summary: Dict) -> str:
        """Generate report header"""
        status_class = "success" if summary["scenario_counts"]["failed"] == 0 else "failure"
        
        return f"""
        <header class="report-header">
            <div class="header-content">
                <h1>🥋 {report_data.title}</h1>
                <div class="header-info">
                    <div class="info-item">
                        <span class="label">Start Time:</span>
                        <span class="value">{report_data.start_time.strftime('%Y-%m-%d %H:%M:%S')}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">Duration:</span>
                        <span class="value">{report_data.duration:.2f}s</span>
                    </div>
                    <div class="info-item">
                        <span class="label">Status:</span>
                        <span class="value status-{status_class}">
                            {'✅ PASSED' if status_class == 'success' else '❌ FAILED'}
                        </span>
                    </div>
                </div>
            </div>
        </header>
        """
    
    def _generate_summary_section(self, summary: Dict) -> str:
        """Generate summary section"""
        return f"""
        <section class="summary-section">
            <h2>📊 Test Summary</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="card-header">Features</div>
                    <div class="card-value">{summary['total_features']}</div>
                </div>
                <div class="summary-card">
                    <div class="card-header">Scenarios</div>
                    <div class="card-value">{summary['total_scenarios']}</div>
                    <div class="card-breakdown">
                        <span class="passed">{summary['scenario_counts']['passed']} passed</span>
                        <span class="failed">{summary['scenario_counts']['failed']} failed</span>
                        <span class="skipped">{summary['scenario_counts']['skipped']} skipped</span>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="card-header">Steps</div>
                    <div class="card-value">{summary['total_steps']}</div>
                    <div class="card-breakdown">
                        <span class="passed">{summary['step_counts']['passed']} passed</span>
                        <span class="failed">{summary['step_counts']['failed']} failed</span>
                        <span class="skipped">{summary['step_counts']['skipped']} skipped</span>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="card-header">Success Rate</div>
                    <div class="card-value">{summary['success_rate']:.1f}%</div>
                </div>
            </div>
        </section>
        """
    
    def _generate_features_section(self, features) -> str:
        """Generate features section"""
        features_html = ""
        
        for i, feature in enumerate(features):
            feature_status = "passed" if all(s.status.value == "passed" for s in feature.scenarios) else "failed"
            
            features_html += f"""
            <section class="feature-section">
                <div class="feature-header" onclick="toggleFeature({i})">
                    <h2>
                        <span class="status-icon status-{feature_status}">
                            {'✅' if feature_status == 'passed' else '❌'}
                        </span>
                        📋 {feature.name}
                    </h2>
                    <div class="feature-info">
                        <span class="duration">{feature.duration:.2f}s</span>
                        <span class="scenario-count">{len(feature.scenarios)} scenarios</span>
                        <span class="toggle-icon">▼</span>
                    </div>
                </div>
                
                <div class="feature-content" id="feature-{i}">
                    {self._generate_scenarios_section(feature.scenarios, i)}
                </div>
            </section>
            """
        
        return features_html
    
    def _generate_scenarios_section(self, scenarios, feature_index) -> str:
        """Generate scenarios section"""
        scenarios_html = ""
        
        for j, scenario in enumerate(scenarios):
            status_class = scenario.status.value
            
            scenarios_html += f"""
            <div class="scenario-section">
                <div class="scenario-header" onclick="toggleScenario({feature_index}, {j})">
                    <h3>
                        <span class="status-icon status-{status_class}">
                            {'✅' if status_class == 'passed' else '❌' if status_class == 'failed' else '⏭️'}
                        </span>
                        🎯 {scenario.name}
                    </h3>
                    <div class="scenario-info">
                        <span class="duration">{scenario.duration:.2f}s</span>
                        <span class="step-count">{len(scenario.steps)} steps</span>
                        <span class="toggle-icon">▼</span>
                    </div>
                </div>
                
                <div class="scenario-content" id="scenario-{feature_index}-{j}">
                    {self._generate_steps_section(scenario.background_steps + scenario.steps)}
                </div>
            </div>
            """
        
        return scenarios_html
    
    def _generate_steps_section(self, steps) -> str:
        """Generate steps section"""
        steps_html = ""
        
        for k, step in enumerate(steps):
            status_class = step.status.value
            
            steps_html += f"""
            <div class="step-section status-{status_class}">
                <div class="step-header" onclick="toggleStep(this)">
                    <div class="step-info">
                        <span class="status-icon">
                            {'✅' if status_class == 'passed' else '❌' if status_class == 'failed' else '⏭️'}
                        </span>
                        <span class="step-text">{step.step_text}</span>
                    </div>
                    <div class="step-meta">
                        <span class="duration">{step.duration:.3f}s</span>
                        <span class="toggle-icon">▼</span>
                    </div>
                </div>
                
                <div class="step-content">
                    {self._generate_step_details(step)}
                </div>
            </div>
            """
        
        return steps_html
    
    def _generate_step_details(self, step) -> str:
        """Generate detailed step information"""
        details_html = ""
        
        # Variables used
        if step.variables_used:
            details_html += f"""
            <div class="detail-section">
                <h4>📝 Variables Used</h4>
                <pre class="json-content">{json.dumps(step.variables_used, indent=2)}</pre>
            </div>
            """
        
        # Request details
        if step.request_data:
            req = step.request_data
            details_html += f"""
            <div class="detail-section">
                <h4>📤 Request</h4>
                <div class="request-info">
                    <div class="method-url">
                        <span class="http-method method-{req.method.lower()}">{req.method}</span>
                        <span class="url">{req.url}</span>
                    </div>
                    
                    {self._generate_headers_section("Request Headers", req.headers)}
                    
                    {self._generate_params_section(req.params) if req.params else ""}
                    
                    {self._generate_body_section("Request Body", req.body, req.body_type) if req.body else ""}
                </div>
            </div>
            """
        
        # Response details
        if step.response_data:
            resp = step.response_data
            status_class = "success" if 200 <= resp.status_code < 300 else "error"
            
            details_html += f"""
            <div class="detail-section">
                <h4>📥 Response</h4>
                <div class="response-info">
                    <div class="status-line">
                        <span class="status-code status-{status_class}">{resp.status_code}</span>
                        <span class="response-time">{resp.elapsed_time:.3f}s</span>
                    </div>
                    
                    {self._generate_headers_section("Response Headers", resp.headers)}
                    
                    {self._generate_body_section("Response Body", resp.body, resp.body_type) if resp.body else ""}
                </div>
            </div>
            """
        
        # Assertions
        if step.assertions:
            details_html += f"""
            <div class="detail-section">
                <h4>✅ Assertions</h4>
                <div class="assertions-list">
                    {self._generate_assertions_section(step.assertions)}
                </div>
            </div>
            """
        
        # Variables set
        if step.variables_set:
            details_html += f"""
            <div class="detail-section">
                <h4>💾 Variables Set</h4>
                <pre class="json-content">{json.dumps(step.variables_set, indent=2)}</pre>
            </div>
            """
        
        # Error details
        if step.error_message:
            details_html += f"""
            <div class="detail-section error-section">
                <h4>❌ Error</h4>
                <div class="error-message">{step.error_message}</div>
                {f'<pre class="error-traceback">{step.error_traceback}</pre>' if step.error_traceback else ''}
            </div>
            """
        
        return details_html
    
    def _generate_headers_section(self, title: str, headers: Dict) -> str:
        """Generate headers section"""
        if not headers:
            return ""
        
        headers_html = ""
        for key, value in headers.items():
            headers_html += f'<div class="header-item"><span class="header-key">{key}:</span> <span class="header-value">{value}</span></div>'
        
        return f"""
        <div class="headers-section">
            <h5>{title}</h5>
            <div class="headers-list">
                {headers_html}
            </div>
        </div>
        """
    
    def _generate_params_section(self, params: Dict) -> str:
        """Generate query parameters section"""
        if not params:
            return ""
        
        params_html = ""
        for key, value in params.items():
            params_html += f'<div class="param-item"><span class="param-key">{key}:</span> <span class="param-value">{value}</span></div>'
        
        return f"""
        <div class="params-section">
            <h5>Query Parameters</h5>
            <div class="params-list">
                {params_html}
            </div>
        </div>
        """
    
    def _generate_body_section(self, title: str, body: Any, body_type: str) -> str:
        """Generate body section"""
        if body is None:
            return ""
        
        if body_type == "json":
            body_content = json.dumps(body, indent=2) if isinstance(body, (dict, list)) else str(body)
            css_class = "json-content"
        else:
            body_content = str(body)
            css_class = "text-content"
        
        return f"""
        <div class="body-section">
            <h5>{title}</h5>
            <pre class="{css_class}">{body_content}</pre>
        </div>
        """
    
    def _generate_assertions_section(self, assertions: list) -> str:
        """Generate assertions section"""
        assertions_html = ""
        
        for assertion in assertions:
            status_class = "passed" if assertion["passed"] else "failed"
            icon = "✅" if assertion["passed"] else "❌"
            
            assertions_html += f"""
            <div class="assertion-item status-{status_class}">
                <div class="assertion-header">
                    <span class="assertion-icon">{icon}</span>
                    <span class="assertion-description">{assertion['description']}</span>
                </div>
                <div class="assertion-details">
                    <div class="assertion-expected">Expected: <code>{json.dumps(assertion['expected'])}</code></div>
                    <div class="assertion-actual">Actual: <code>{json.dumps(assertion['actual'])}</code></div>
                </div>
            </div>
            """
        
        return assertions_html  
  
    def _get_css_styles(self) -> str:
        """Get CSS styles for the report"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Header Styles */
        .report-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .header-content h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .header-info {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .info-item {
            text-align: center;
        }
        
        .info-item .label {
            display: block;
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        
        .info-item .value {
            display: block;
            font-size: 1.2em;
            font-weight: bold;
        }
        
        .status-success {
            color: #4CAF50;
        }
        
        .status-failure {
            color: #f44336;
        }
        
        /* Summary Section */
        .summary-section {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .summary-section h2 {
            margin-bottom: 20px;
            color: #333;
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .summary-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #667eea;
        }
        
        .card-header {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
        }
        
        .card-value {
            font-size: 2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        
        .card-breakdown {
            font-size: 0.8em;
            display: flex;
            justify-content: space-around;
            gap: 10px;
        }
        
        .passed {
            color: #4CAF50;
        }
        
        .failed {
            color: #f44336;
        }
        
        .skipped {
            color: #ff9800;
        }
        
        /* Feature Section */
        .feature-section {
            background: white;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .feature-header {
            background: #f8f9fa;
            padding: 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #e9ecef;
        }
        
        .feature-header:hover {
            background: #e9ecef;
        }
        
        .feature-header h2 {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 0;
        }
        
        .feature-info {
            display: flex;
            align-items: center;
            gap: 15px;
            font-size: 0.9em;
            color: #666;
        }
        
        .feature-content {
            padding: 20px;
        }
        
        /* Scenario Section */
        .scenario-section {
            margin-bottom: 20px;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .scenario-header {
            background: #f8f9fa;
            padding: 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .scenario-header:hover {
            background: #e9ecef;
        }
        
        .scenario-header h3 {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 0;
            font-size: 1.1em;
        }
        
        .scenario-info {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.8em;
            color: #666;
        }
        
        .scenario-content {
            padding: 15px;
            background: #fafafa;
        }
        
        /* Step Section */
        .step-section {
            margin-bottom: 15px;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            overflow: hidden;
        }
        
        .step-section.status-passed {
            border-left: 4px solid #4CAF50;
        }
        
        .step-section.status-failed {
            border-left: 4px solid #f44336;
        }
        
        .step-section.status-skipped {
            border-left: 4px solid #ff9800;
        }
        
        .step-header {
            background: white;
            padding: 12px 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .step-header:hover {
            background: #f8f9fa;
        }
        
        .step-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .step-text {
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9em;
        }
        
        .step-meta {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.8em;
            color: #666;
        }
        
        .step-content {
            padding: 15px;
            background: #fafafa;
            display: none;
        }
        
        .step-content.expanded {
            display: block;
        }
        
        /* Detail Sections */
        .detail-section {
            margin-bottom: 20px;
            background: white;
            border-radius: 6px;
            padding: 15px;
            border: 1px solid #e9ecef;
        }
        
        .detail-section h4 {
            margin-bottom: 15px;
            color: #333;
            font-size: 1em;
        }
        
        .detail-section h5 {
            margin-bottom: 10px;
            color: #666;
            font-size: 0.9em;
        }
        
        /* Request/Response Styles */
        .method-url {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        .http-method {
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.8em;
            color: white;
        }
        
        .method-get { background: #4CAF50; }
        .method-post { background: #2196F3; }
        .method-put { background: #ff9800; }
        .method-patch { background: #9c27b0; }
        .method-delete { background: #f44336; }
        
        .url {
            font-family: 'Monaco', 'Menlo', monospace;
            background: #f8f9fa;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.9em;
        }
        
        .status-line {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .status-code {
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            color: white;
        }
        
        .status-success { background: #4CAF50; }
        .status-error { background: #f44336; }
        
        .response-time {
            font-size: 0.9em;
            color: #666;
        }
        
        /* Headers and Parameters */
        .headers-section, .params-section, .body-section {
            margin-bottom: 15px;
        }
        
        .headers-list, .params-list {
            background: #f8f9fa;
            border-radius: 4px;
            padding: 10px;
        }
        
        .header-item, .param-item {
            margin-bottom: 5px;
            font-size: 0.9em;
        }
        
        .header-key, .param-key {
            font-weight: bold;
            color: #666;
        }
        
        .header-value, .param-value {
            font-family: 'Monaco', 'Menlo', monospace;
        }
        
        /* Code Content */
        .json-content, .text-content {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 15px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.8em;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        
        /* Assertions */
        .assertions-list {
            background: #f8f9fa;
            border-radius: 4px;
            padding: 10px;
        }
        
        .assertion-item {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 4px;
            border-left: 4px solid #ccc;
        }
        
        .assertion-item.status-passed {
            border-left-color: #4CAF50;
            background: #f1f8e9;
        }
        
        .assertion-item.status-failed {
            border-left-color: #f44336;
            background: #ffebee;
        }
        
        .assertion-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }
        
        .assertion-description {
            font-weight: bold;
        }
        
        .assertion-details {
            font-size: 0.9em;
        }
        
        .assertion-expected, .assertion-actual {
            margin-bottom: 4px;
        }
        
        .assertion-expected code, .assertion-actual code {
            background: rgba(0,0,0,0.1);
            padding: 2px 4px;
            border-radius: 2px;
            font-family: 'Monaco', 'Menlo', monospace;
        }
        
        /* Error Section */
        .error-section {
            border-left: 4px solid #f44336;
            background: #ffebee;
        }
        
        .error-message {
            color: #d32f2f;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .error-traceback {
            background: #ffcdd2;
            border: 1px solid #f44336;
            color: #b71c1c;
            font-size: 0.8em;
        }
        
        /* Toggle Icons */
        .toggle-icon {
            transition: transform 0.3s ease;
        }
        
        .toggle-icon.rotated {
            transform: rotate(180deg);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header-info {
                flex-direction: column;
                gap: 10px;
            }
            
            .summary-grid {
                grid-template-columns: 1fr;
            }
            
            .method-url {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .feature-header, .scenario-header, .step-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
        }
        """
    
    def _get_javascript(self) -> str:
        """Get JavaScript for interactive features"""
        return """
        function toggleFeature(index) {
            const content = document.getElementById(`feature-${index}`);
            const icon = content.previousElementSibling.querySelector('.toggle-icon');
            
            if (content.style.display === 'none') {
                content.style.display = 'block';
                icon.classList.remove('rotated');
            } else {
                content.style.display = 'none';
                icon.classList.add('rotated');
            }
        }
        
        function toggleScenario(featureIndex, scenarioIndex) {
            const content = document.getElementById(`scenario-${featureIndex}-${scenarioIndex}`);
            const icon = content.previousElementSibling.querySelector('.toggle-icon');
            
            if (content.style.display === 'none') {
                content.style.display = 'block';
                icon.classList.remove('rotated');
            } else {
                content.style.display = 'none';
                icon.classList.add('rotated');
            }
        }
        
        function toggleStep(header) {
            const content = header.nextElementSibling;
            const icon = header.querySelector('.toggle-icon');
            
            if (content.classList.contains('expanded')) {
                content.classList.remove('expanded');
                icon.classList.add('rotated');
            } else {
                content.classList.add('expanded');
                icon.classList.remove('rotated');
            }
        }
        
        // Initialize collapsed state
        document.addEventListener('DOMContentLoaded', function() {
            // Collapse all features initially
            document.querySelectorAll('[id^="feature-"]').forEach(el => {
                el.style.display = 'none';
            });
            
            // Collapse all scenarios initially
            document.querySelectorAll('[id^="scenario-"]').forEach(el => {
                el.style.display = 'none';
            });
            
            // Rotate all toggle icons initially
            document.querySelectorAll('.toggle-icon').forEach(icon => {
                icon.classList.add('rotated');
            });
        });
        """