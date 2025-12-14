"""
HTML Reporter - Generate comprehensive HTML reports for Judo Framework tests
"""

import json
import os
import base64
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
        
        # Cargar logos como base64
        self.centyc_logo_b64 = self._load_logo_as_base64("logo_centyc.png")
        self.judo_logo_b64 = self._load_logo_as_base64("logo_judo.png")
    
    def _load_logo_as_base64(self, logo_filename: str) -> str:
        """Load logo file and convert to base64 data URL"""
        try:
            # Método 1: Buscar desde el paquete instalado usando importlib.resources
            try:
                import importlib.resources as resources
                
                # Intentar cargar desde judo.assets.logos
                try:
                    logo_data = resources.read_binary('judo.assets.logos', logo_filename)
                    logo_b64 = base64.b64encode(logo_data).decode('utf-8')
                    return f"data:image/png;base64,{logo_b64}"
                except:
                    pass
                
                # Fallback: intentar desde judo/assets/logos/
                try:
                    logo_data = resources.read_binary('judo', f'assets/logos/{logo_filename}')
                    logo_b64 = base64.b64encode(logo_data).decode('utf-8')
                    return f"data:image/png;base64,{logo_b64}"
                except:
                    pass
                    
            except ImportError:
                pass
            
            # Método 2: Buscar desde el directorio del paquete (desarrollo y fallback)
            current_dir = Path(__file__).parent.parent  # judo/reporting/ -> judo/
            logo_path = current_dir / "assets" / "logos" / logo_filename
            
            if logo_path.exists():
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                    logo_b64 = base64.b64encode(logo_data).decode('utf-8')
                    return f"data:image/png;base64,{logo_b64}"
            
            # Método 3: Buscar desde la raíz del proyecto (desarrollo)
            root_dir = Path(__file__).parent.parent.parent  # Subir a la raíz
            logo_path = root_dir / "assets" / "logos" / logo_filename
            
            if logo_path.exists():
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                    logo_b64 = base64.b64encode(logo_data).decode('utf-8')
                    return f"data:image/png;base64,{logo_b64}"
            
            # Método 4: Fallback a pkg_resources para compatibilidad
            try:
                import pkg_resources
                
                # Intentar diferentes rutas en el paquete
                for resource_path in [
                    f'assets/logos/{logo_filename}',
                    f'assets\\logos\\{logo_filename}',  # Windows path
                    logo_filename
                ]:
                    try:
                        logo_data = pkg_resources.resource_string('judo', resource_path)
                        logo_b64 = base64.b64encode(logo_data).decode('utf-8')
                        return f"data:image/png;base64,{logo_b64}"
                    except:
                        continue
            except ImportError:
                pass
            
            print(f"Warning: Logo not found: {logo_filename}")
            return ""
            
        except Exception as e:
            print(f"Warning: Could not load logo {logo_filename}: {e}")
            return ""
    
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
    
    {self._generate_footer()}
    
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
                <div class="header-layout">
                    <!-- Logo CENTYC en esquina superior izquierda -->
                    <div class="centyc-logo">
                        <a href="https://www.centyc.cl" target="_blank" class="centyc-link">
                            {f'<img src="{self.centyc_logo_b64}" alt="CENTYC Logo" class="centyc-img">' if self.centyc_logo_b64 else '<span class="centyc-fallback">CENTYC</span>'}
                            <span class="centyc-text">www.centyc.cl</span>
                        </a>
                    </div>
                    
                    <!-- Logo Judo Framework y título centrados -->
                    <div class="main-title">
                        <div class="judo-logo-circle">
                            {f'<img src="{self.judo_logo_b64}" alt="Judo Framework Logo" class="judo-img">' if self.judo_logo_b64 else '<span class="judo-fallback">🥋</span>'}
                        </div>
                        <h1 class="report-title">{report_data.title}</h1>
                    </div>
                </div>
                
                <!-- Información del reporte en layout horizontal -->
                <div class="header-info-horizontal">
                    <div class="info-group">
                        <span class="info-label">Start Time:</span>
                        <span class="info-value">{report_data.start_time.strftime('%Y-%m-%d %H:%M:%S')}</span>
                    </div>
                    <div class="info-group">
                        <span class="info-label">Duration:</span>
                        <span class="info-value">{report_data.duration:.2f}s</span>
                    </div>
                    <div class="info-group">
                        <span class="info-label">Status:</span>
                        <span class="status-badge status-{status_class}">
                            {'✓' if status_class == 'success' else '✗'}
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
    
    def _generate_footer(self) -> str:
        """Generate report footer"""
        logo_html = f'<img src="{self.judo_logo_b64}" alt="Judo Framework Logo" class="judo-logo-footer">' if self.judo_logo_b64 else '<span class="judo-fallback-footer">🥋</span>'
        
        return f"""
        <footer class="report-footer">
            <div class="footer-content">
                <div class="footer-logo">
                    {logo_html}
                    <span class="footer-text">Framework creado por Felipe Farias - </span>
                    <a href="mailto:felipe.farias@centyc.cl" class="footer-email">felipe.farias@centyc.cl</a>
                </div>
                <div class="footer-links">
                    <a href="https://www.centyc.cl" target="_blank" class="footer-link">CENTYC</a>
                    <span class="separator">•</span>
                    <a href="http://centyc.cl/judo-framework/" target="_blank" class="footer-link">Documentación</a>
                    <span class="separator">•</span>
                    <a href="https://github.com/FelipeFariasAlfaro/Judo-Framework" target="_blank" class="footer-link">GitHub</a>
                </div>
            </div>
        </footer>
        """
    
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
        
        # ✅ SCREENSHOTS
        if hasattr(step, 'screenshot_path') and step.screenshot_path:
            screenshot_html = self._generate_screenshot_section(step.screenshot_path)
            if screenshot_html:
                details_html += screenshot_html
        
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
    
    def _generate_screenshot_section(self, screenshot_path: str) -> str:
        """Generate screenshot section with embedded image"""
        if not screenshot_path:
            return ""
        
        try:
            # Convert screenshot to base64
            from pathlib import Path
            screenshot_file = Path(screenshot_path)
            
            if not screenshot_file.exists():
                return f"""
                <div class="detail-section">
                    <h4>📸 Screenshot</h4>
                    <div class="screenshot-error">Screenshot file not found: {screenshot_path}</div>
                </div>
                """
            
            with open(screenshot_file, 'rb') as f:
                screenshot_data = f.read()
                screenshot_b64 = base64.b64encode(screenshot_data).decode('utf-8')
            
            # Determine image type from extension
            ext = screenshot_file.suffix.lower()
            mime_type = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }.get(ext, 'image/png')
            
            return f"""
            <div class="detail-section screenshot-section">
                <h4>📸 Screenshot</h4>
                <div class="screenshot-container">
                    <img src="data:{mime_type};base64,{screenshot_b64}" 
                         alt="Step Screenshot" 
                         class="screenshot-image"
                         onclick="toggleScreenshotFullscreen(this)">
                    <div class="screenshot-info">
                        <span class="screenshot-filename">{screenshot_file.name}</span>
                        <span class="screenshot-hint">Click to view fullscreen</span>
                    </div>
                </div>
            </div>
            """
        except Exception as e:
            return f"""
            <div class="detail-section">
                <h4>📸 Screenshot</h4>
                <div class="screenshot-error">Error loading screenshot: {str(e)}</div>
            </div>
            """
  
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
            background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 50%, #9333ea 100%);
            color: white;
            padding: 25px 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
        }
        
        .header-layout {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 25px;
            position: relative;
        }
        
        /* Logo CENTYC en esquina superior izquierda */
        .centyc-logo {
            position: absolute;
            top: 0;
            left: 0;
        }
        
        .centyc-link {
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: white;
            transition: opacity 0.3s ease;
        }
        
        .centyc-link:hover {
            opacity: 0.8;
        }
        
        .centyc-text {
            font-size: 0.9em;
            font-weight: 500;
            color: rgba(255, 255, 255, 0.9);
        }
        
        .centyc-img {
            height: 30px;
            width: auto;
            max-width: 120px;
            transition: opacity 0.3s ease;
            border-radius: 4px;
        }
        
        .centyc-img:hover {
            opacity: 0.8;
        }
        
        .centyc-fallback {
            font-size: 1.2em;
            font-weight: bold;
            color: white;
        }
        
        /* Logo Judo Framework y título centrados */
        .main-title {
            display: flex;
            align-items: center;
            gap: 15px;
            margin: 0 auto;
            padding-top: 10px;
        }
        
        .judo-logo-circle {
            transition: transform 0.3s ease;
        }
        
        .judo-logo-circle:hover {
            transform: scale(1.05);
        }
        
        .judo-img {
            height: 50px;
            width: 50px;
            border-radius: 50%;
            transition: transform 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            object-fit: cover;
        }
        
        .judo-img:hover {
            transform: scale(1.05);
        }
        
        .judo-fallback {
            font-size: 2em;
        }
        
        .report-title {
            font-size: 2.2em;
            margin: 0;
            font-weight: 600;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        /* Información horizontal */
        .header-info-horizontal {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 15px 25px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        
        .info-group {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
        }
        
        .info-label {
            font-size: 0.85em;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 500;
        }
        
        .info-value {
            font-size: 1.1em;
            font-weight: 600;
            color: white;
        }
        
        /* Status Badge */
        .status-badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 80px;
        }
        
        .status-badge.status-success {
            background: #22c55e;
            color: white;
            box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
        }
        
        .status-badge.status-failure {
            background: #ef4444;
            color: white;
            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
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
        
        /* Screenshot Section */
        .screenshot-section {
            border-left: 4px solid #2196F3;
        }
        
        .screenshot-container {
            text-align: center;
        }
        
        .screenshot-image {
            max-width: 100%;
            height: auto;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .screenshot-image:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .screenshot-info {
            margin-top: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            font-size: 0.85em;
            color: #666;
        }
        
        .screenshot-filename {
            font-family: 'Monaco', 'Menlo', monospace;
            background: #f8f9fa;
            padding: 4px 8px;
            border-radius: 4px;
        }
        
        .screenshot-hint {
            color: #999;
            font-style: italic;
        }
        
        .screenshot-error {
            color: #f44336;
            padding: 10px;
            background: #ffebee;
            border-radius: 4px;
            font-size: 0.9em;
        }
        
        /* Screenshot Fullscreen Modal */
        .screenshot-fullscreen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            cursor: pointer;
        }
        
        .screenshot-fullscreen.active {
            display: flex;
        }
        
        .screenshot-fullscreen img {
            max-width: 95%;
            max-height: 95%;
            object-fit: contain;
            box-shadow: 0 0 30px rgba(255,255,255,0.3);
        }
        
        /* Toggle Icons */
        .toggle-icon {
            transition: transform 0.3s ease;
        }
        
        .toggle-icon.rotated {
            transform: rotate(180deg);
        }
        
        /* Footer Styles */
        .report-footer {
            background: #2c3e50;
            color: white;
            padding: 20px 0;
            margin-top: 40px;
        }
        
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .footer-logo {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .judo-logo-footer {
            height: 24px;
            width: 24px;
            opacity: 0.8;
            border-radius: 50%;
            object-fit: cover;
        }
        
        .judo-fallback-footer {
            font-size: 1.2em;
        }
        
        .footer-text {
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.8);
        }
        
        .footer-email {
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
        }
        
        .footer-email:hover {
            color: #5dade2;
            text-decoration: underline;
        }
        
        .footer-links {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .footer-link {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            font-size: 0.9em;
            transition: color 0.3s ease;
        }
        
        .footer-link:hover {
            color: white;
            text-decoration: underline;
        }
        
        .separator {
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.8em;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header-layout {
                flex-direction: column;
                align-items: center;
                gap: 20px;
            }
            
            .centyc-logo {
                position: static;
                order: -1;
            }
            
            .main-title {
                flex-direction: column;
                gap: 10px;
                text-align: center;
            }
            
            .report-title {
                font-size: 1.8em;
            }
            
            .header-info-horizontal {
                flex-direction: column;
                gap: 15px;
            }
            
            .info-group {
                flex-direction: row;
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
            
            .footer-content {
                flex-direction: column;
                text-align: center;
                gap: 10px;
            }
            
            .footer-links {
                justify-content: center;
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
        
        // Screenshot fullscreen functionality
        function toggleScreenshotFullscreen(img) {
            // Create fullscreen modal if it doesn't exist
            let modal = document.getElementById('screenshot-fullscreen-modal');
            if (!modal) {
                modal = document.createElement('div');
                modal.id = 'screenshot-fullscreen-modal';
                modal.className = 'screenshot-fullscreen';
                modal.onclick = function() {
                    this.classList.remove('active');
                };
                document.body.appendChild(modal);
            }
            
            // Clone the image and show in fullscreen
            const fullscreenImg = img.cloneNode(true);
            fullscreenImg.onclick = function(e) {
                e.stopPropagation();
            };
            
            modal.innerHTML = '';
            modal.appendChild(fullscreenImg);
            modal.classList.add('active');
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