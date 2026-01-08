"""
HTML Reporter - Generate comprehensive HTML reports for Judo Framework tests
"""

import json
import os
import base64
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
from .report_data import ReportData


class HTMLReporter:
    """
    HTML report generator for Judo Framework
    Creates detailed reports with request/response data, assertions, and more
    """
    
    def __init__(self, output_dir: str = None, config_file: str = None):
        """Initialize HTML reporter"""
        if output_dir is None:
            # Usar directorio actual del proyecto del usuario
            import os
            output_dir = os.path.join(os.getcwd(), "judo_reports")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Cargar configuración personalizable
        self.config = self._load_config(config_file)
        
        # Cargar logos desde configuración o usar defaults
        self.primary_logo_b64 = self._get_logo_from_config("primary_logo")
        self.secondary_logo_b64 = self._get_logo_from_config("secondary_logo") 
        self.company_logo_b64 = self._get_logo_from_config("company_logo")
        
        # Fallback a logos por defecto si no hay configuración
        if not self.primary_logo_b64:
            self.primary_logo_b64 = self._load_logo_as_base64("logo_judo.png")
        if not self.secondary_logo_b64:
            self.secondary_logo_b64 = self._load_logo_as_base64("logo_centyc.png")
    
    def _load_config(self, config_file: str = None) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        default_config = {
            "project": {
                "name": "Judo Framework Test Report",
                "engineer": "Test Engineer",
                "team": "QA Team", 
                "product": "API Testing Suite",
                "company": "Your Company",
                "date_format": "%Y-%m-%d %H:%M:%S"
            },
            "branding": {
                "primary_logo": "",
                "secondary_logo": "",
                "company_logo": "",
                "primary_color": "#8b5cf6",
                "secondary_color": "#a855f7", 
                "accent_color": "#9333ea",
                "success_color": "#22c55e",
                "error_color": "#ef4444",
                "warning_color": "#f59e0b"
            },
            "charts": {
                "enabled": True,
                "show_pie_charts": True,
                "show_bar_charts": False,
                "colors": {
                    "passed": "#22c55e",
                    "failed": "#ef4444", 
                    "skipped": "#f59e0b"
                }
            },
            "footer": {
                "show_creator": False,
                "show_logo": True,
                "creator_name": "Felipe Farias",
                "creator_email": "felipe.farias@centyc.cl",
                "company_name": "CENTYC",
                "company_url": "https://www.centyc.cl",
                "documentation_url": "http://centyc.cl/judo-framework/",
                "github_url": "https://github.com/FelipeFariasAlfaro/Judo-Framework"
            },
            "display": {
                "show_request_details": True,
                "show_response_details": True,
                "show_variables": True,
                "show_assertions": True,
                "collapse_sections_by_default": True,
                "show_duration_in_ms": False
            }
        }
        
        # Buscar archivo de configuración
        config_paths = []
        
        # 1. Desde variable de entorno JUDO_REPORT_CONFIG_FILE
        env_config_file = os.getenv('JUDO_REPORT_CONFIG_FILE')
        if env_config_file:
            config_paths.append(env_config_file)
        
        # 2. Desde parámetro directo
        if config_file:
            config_paths.append(config_file)
        
        # 3. Buscar en ubicaciones estándar
        config_paths.extend([
            "report_config.json",
            "judo_report_config.json", 
            ".judo/report_config.json",
            "judo_reports/report_config.json",  # Ubicación recomendada
            os.path.join(os.getcwd(), "report_config.json"),
            os.path.join(os.getcwd(), "judo_reports", "report_config.json"),
            os.path.join(os.getcwd(), ".judo", "report_config.json")
        ])
        
        # Intentar cargar configuración
        for config_path in config_paths:
            try:
                if os.path.exists(config_path):
                    with open(config_path, 'r', encoding='utf-8') as f:
                        user_config = json.load(f)
                        # Merge con configuración por defecto
                        return self._merge_config(default_config, user_config)
            except Exception as e:
                print(f"Warning: Could not load config from {config_path}: {e}")
                continue
        
        return default_config
    
    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        """Merge user configuration with defaults"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result
    
    def _get_logo_from_config(self, logo_key: str) -> str:
        """Get logo from configuration"""
        try:
            logo_data = self.config.get("branding", {}).get(logo_key, "")
            
            # Si no hay datos de logo, retornar vacío
            if not logo_data:
                return ""
            
            # Si ya es un data URL válido, retornarlo directamente
            if logo_data.startswith("data:image"):
                return logo_data
            
            # Si es una ruta de archivo, cargarla
            if os.path.exists(logo_data):
                with open(logo_data, 'rb') as f:
                    file_data = f.read()
                    logo_b64 = base64.b64encode(file_data).decode('utf-8')
                    # Detectar tipo de imagen
                    ext = Path(logo_data).suffix.lower()
                    mime_type = {
                        '.png': 'image/png',
                        '.jpg': 'image/jpeg', 
                        '.jpeg': 'image/jpeg',
                        '.gif': 'image/gif',
                        '.svg': 'image/svg+xml'
                    }.get(ext, 'image/png')
                    return f"data:{mime_type};base64,{logo_b64}"
            
            # Si parece ser base64 sin el prefijo data:, agregarlo
            if len(logo_data) > 100 and not logo_data.startswith("data:"):
                # Asumir PNG por defecto
                return f"data:image/png;base64,{logo_data}"
                
        except Exception as e:
            print(f"Warning: Could not load logo {logo_key}: {e}")
        
        return ""
    
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
    <title>{self.config['project']['name']}</title>
    <style>
        {self._get_css_styles()}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        {self._generate_header(report_data, summary)}
        {self._generate_project_info()}
        {self._generate_summary_section(summary, report_data)}
        {self._generate_features_section(report_data.features)}
    </div>
    
    {self._generate_footer()}
    
    <script>
        {self._get_javascript()}
        {self._get_charts_javascript(summary) if self.config['charts']['enabled'] else ''}
    </script>
</body>
</html>
        """
        return html
    
    def _generate_header(self, report_data: ReportData, summary: Dict) -> str:
        """Generate report header"""
        status_class = "success" if summary["scenario_counts"]["failed"] == 0 else "failure"
        project_config = self.config['project']
        branding_config = self.config['branding']
        
        # Usar logos configurados o fallbacks
        secondary_logo = self.secondary_logo_b64 or self.company_logo_b64
        primary_logo = self.primary_logo_b64
        
        return f"""
        <header class="report-header">
            <div class="header-content">
                <div class="header-layout">
                    <!-- Logo secundario/empresa en esquina superior izquierda -->
                    <div class="secondary-logo">
                        {f'<a href="{self.config["footer"]["company_url"]}" target="_blank" class="secondary-link">' if self.config["footer"]["company_url"] else '<div class="secondary-link">'}
                            {f'<img src="{secondary_logo}" alt="Company Logo" class="secondary-img">' if secondary_logo else f'<span class="secondary-fallback">{project_config["company"]}</span>'}
                            <span class="secondary-text">{project_config["company"]}</span>
                        {f'</a>' if self.config["footer"]["company_url"] else '</div>'}
                    </div>
                    
                    <!-- Título centrado sin logo -->
                    <div class="main-title">
                        <h1 class="report-title">{project_config['name']}</h1>
                    </div>
                </div>
                
                <!-- Información del reporte en layout horizontal -->
                <div class="header-info-horizontal">
                    <div class="info-group">
                        <span class="info-label">Fecha:</span>
                        <span class="info-value">{report_data.start_time.strftime(project_config['date_format'])}</span>
                    </div>
                    <div class="info-group">
                        <span class="info-label">Duración:</span>
                        <span class="info-value">{report_data.duration:.2f}s</span>
                    </div>
                    <div class="info-group">
                        <span class="info-label">Estado:</span>
                        <span class="status-badge status-{status_class}">
                            {'✓' if status_class == 'success' else '✗'}
                        </span>
                    </div>
                </div>
            </div>
        </header>
        """
    
    def _generate_project_info(self) -> str:
        """Generate project information section"""
        project_config = self.config['project']
        
        return f"""
        <section class="project-info-section">
            <div class="project-info-grid">
                <div class="project-info-card">
                    <div class="info-icon">👨‍💻</div>
                    <div class="info-content">
                        <div class="info-title">Ingeniero</div>
                        <div class="info-value">{project_config['engineer']}</div>
                    </div>
                </div>
                <div class="project-info-card">
                    <div class="info-icon">👥</div>
                    <div class="info-content">
                        <div class="info-title">Equipo</div>
                        <div class="info-value">{project_config['team']}</div>
                    </div>
                </div>
                <div class="project-info-card">
                    <div class="info-icon">📦</div>
                    <div class="info-content">
                        <div class="info-title">Producto</div>
                        <div class="info-value">{project_config['product']}</div>
                    </div>
                </div>
                <div class="project-info-card">
                    <div class="info-icon">🏢</div>
                    <div class="info-content">
                        <div class="info-title">Empresa</div>
                        <div class="info-value">{project_config['company']}</div>
                    </div>
                </div>
            </div>
        </section>
        """
    
    def _generate_charts_section(self, summary: Dict) -> str:
        """Generate charts section with pie charts"""
        if not self.config['charts']['enabled']:
            return ""
        
        charts_html = """
        <section class="charts-section">
            <h2>📊 Gráficos de Resultados</h2>
            <div class="charts-grid">
        """
        
        if self.config['charts']['show_pie_charts']:
            charts_html += """
                <div class="chart-container">
                    <h3>Distribución de Escenarios</h3>
                    <canvas id="scenariosChart" width="300" height="300"></canvas>
                </div>
                <div class="chart-container">
                    <h3>Distribución de Pasos</h3>
                    <canvas id="stepsChart" width="300" height="300"></canvas>
                </div>
            """
        
        if self.config['charts']['show_bar_charts']:
            charts_html += """
                <div class="chart-container chart-wide">
                    <h3>Comparación de Resultados</h3>
                    <canvas id="comparisonChart" width="600" height="300"></canvas>
                </div>
            """
        
        charts_html += """
            </div>
        </section>
        """
        
        return charts_html
    
    def _generate_summary_section(self, summary: Dict, report_data: ReportData = None) -> str:
        """Generate summary section with integrated pie charts and execution info"""
        # Generar gráficos de torta si están habilitados
        charts_html = ""
        if self.config['charts']['enabled'] and self.config['charts']['show_pie_charts']:
            charts_html = f"""
            <div class="summary-charts-grid">
                <div class="summary-chart-card">
                    <div class="chart-header">
                        <span class="chart-icon">📁</span>
                        <span class="chart-title">Features</span>
                    </div>
                    <div class="chart-content">
                        <div class="chart-number">{summary['total_features']}</div>
                        <div class="chart-canvas-container">
                            <canvas id="scenariosChart" width="120" height="120"></canvas>
                        </div>
                        <div class="chart-stats">
                            <div class="stat-item passed">{summary['scenario_counts']['passed']} PASSED</div>
                            <div class="stat-item failed">{summary['scenario_counts']['failed']} FAILED</div>
                            <div class="stat-item skipped">{summary['scenario_counts']['skipped']} SKIPPED</div>
                        </div>
                    </div>
                </div>
                
                <div class="summary-chart-card">
                    <div class="chart-header">
                        <span class="chart-icon">📋</span>
                        <span class="chart-title">Scenarios</span>
                    </div>
                    <div class="chart-content">
                        <div class="chart-number">{summary['total_scenarios']}</div>
                        <div class="chart-canvas-container">
                            <canvas id="scenariosChart2" width="120" height="120"></canvas>
                        </div>
                        <div class="chart-stats">
                            <div class="stat-item passed">{summary['scenario_counts']['passed']} PASSED</div>
                            <div class="stat-item failed">{summary['scenario_counts']['failed']} FAILED</div>
                            <div class="stat-item skipped">{summary['scenario_counts']['skipped']} SKIPPED</div>
                        </div>
                    </div>
                </div>
                
                <div class="summary-chart-card">
                    <div class="chart-header">
                        <span class="chart-icon">🔸</span>
                        <span class="chart-title">Steps</span>
                    </div>
                    <div class="chart-content">
                        <div class="chart-number">{summary['total_steps']}</div>
                        <div class="chart-canvas-container">
                            <canvas id="stepsChart" width="120" height="120"></canvas>
                        </div>
                        <div class="chart-stats">
                            <div class="stat-item passed">{summary['step_counts']['passed']} PASSED</div>
                            <div class="stat-item failed">{summary['step_counts']['failed']} FAILED</div>
                            <div class="stat-item skipped">{summary['step_counts']['skipped']} SKIPPED</div>
                        </div>
                    </div>
                </div>
            </div>
            """
        
        # Usar datos reales si están disponibles
        if report_data:
            start_time = report_data.start_time.strftime(self.config['project']['date_format'])
            end_time = (report_data.start_time + timedelta(seconds=report_data.duration)).strftime(self.config['project']['date_format'])
            duration = f"{report_data.duration:.2f}s"
            browser = "Chromium"  # Default, could be made configurable
        else:
            # Fallback values
            start_time = "2026-01-07 12:31:59"
            end_time = "2026-01-07 12:32:26"
            duration = "27.47s"
            browser = "Chromium"
        
        return f"""
        <section class="summary-section">
            <div class="summary-layout">
                <!-- Información de ejecución a la izquierda -->
                <div class="execution-info">
                    <div class="execution-item">
                        <span class="execution-icon">🕐</span>
                        <span class="execution-label">Inicio</span>
                        <span class="execution-value">{start_time}</span>
                    </div>
                    <div class="execution-item">
                        <span class="execution-icon">🏁</span>
                        <span class="execution-label">Fin</span>
                        <span class="execution-value">{end_time}</span>
                    </div>
                    <div class="execution-item">
                        <span class="execution-icon">⏱️</span>
                        <span class="execution-label">Duración</span>
                        <span class="execution-value">{duration}</span>
                    </div>
                    <div class="execution-item">
                        <span class="execution-icon">🌐</span>
                        <span class="execution-label">Navegador</span>
                        <span class="execution-value">{browser}</span>
                    </div>
                </div>
                
                <!-- Gráficos de resultados a la derecha -->
                {charts_html}
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
        footer_config = self.config['footer']
        
        footer_html = f"""
        <footer class="report-footer">
            <div class="footer-content">
        """
        
        # Solo mostrar logo si está habilitado
        if footer_config.get('show_logo', False):
            if self.primary_logo_b64:
                footer_html += f"""
                <div class="footer-logo-only">
                    <img src="{self.primary_logo_b64}" alt="Logo" class="primary-logo-footer">
                </div>
                """
            else:
                footer_html += f"""
                <div class="footer-logo-only">
                    <span class="primary-fallback-footer">🥋</span>
                </div>
                """
        
        # Links siempre visibles (pero se pueden ocultar con CSS si se desea)
        footer_html += f"""
                <div class="footer-links">
                    <a href="{footer_config['company_url']}" target="_blank" class="footer-link">{footer_config['company_name']}</a>
                    <span class="separator">•</span>
                    <a href="{footer_config['documentation_url']}" target="_blank" class="footer-link">Documentación</a>
                    <span class="separator">•</span>
                    <a href="{footer_config['github_url']}" target="_blank" class="footer-link">GitHub</a>
                </div>
            </div>
        </footer>
        """
        
        return footer_html
    
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
        branding = self.config['branding']
        
        return f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* Header Styles */
        .report-header {{
            background: linear-gradient(135deg, {branding['primary_color']} 0%, {branding['secondary_color']} 50%, {branding['accent_color']} 100%);
            color: white;
            padding: 25px 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
        }}
        
        .header-layout {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 25px;
            position: relative;
        }}
        
        /* Logo secundario/empresa en esquina superior izquierda */
        .secondary-logo {{
            position: absolute;
            top: 0;
            left: 0;
        }}
        
        .secondary-link {{
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: white;
            transition: opacity 0.3s ease;
        }}
        
        .secondary-link:hover {{
            opacity: 0.8;
        }}
        
        .secondary-text {{
            font-size: 0.9em;
            font-weight: 500;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .secondary-img {{
            height: 30px;
            width: auto;
            max-width: 120px;
            transition: opacity 0.3s ease;
            border-radius: 4px;
        }}
        
        .secondary-img:hover {{
            opacity: 0.8;
        }}
        
        .secondary-fallback {{
            font-size: 1.2em;
            font-weight: bold;
            color: white;
        }}
        
        /* Logo principal y título centrados */
        .main-title {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin: 0 auto;
            padding-top: 10px;
        }}
        

        .primary-img {{
            height: 50px;
            width: 50px;
            border-radius: 50%;
            transition: transform 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            object-fit: cover;
        }}
        
        .primary-img:hover {{
            transform: scale(1.05);
        }}
        
        .primary-fallback {{
            font-size: 2em;
        }}
        
        .report-title {{
            font-size: 2.2em;
            margin: 0;
            font-weight: 600;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        
        /* Información horizontal */
        .header-info-horizontal {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 15px 25px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }}
        
        .info-group {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
        }}
        
        .info-label {{
            font-size: 0.85em;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 500;
        }}
        
        .info-value {{
            font-size: 1.1em;
            font-weight: 600;
            color: white;
        }}
        
        /* Status Badge */
        .status-badge {{
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 80px;
        }}
        
        .status-badge.status-success {{
            background: {branding['success_color']};
            color: white;
            box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
        }}
        
        .status-badge.status-failure {{
            background: {branding['error_color']};
            color: white;
            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
        }}
        
        /* Project Info Section */
        .project-info-section {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .project-info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}
        
        .project-info-card {{
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid {branding['primary_color']};
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .project-info-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .info-icon {{
            font-size: 2em;
            opacity: 0.8;
        }}
        
        .info-content {{
            flex: 1;
        }}
        
        .info-title {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
            font-weight: 500;
        }}
        
        .info-value {{
            font-size: 1.1em;
            font-weight: 600;
            color: #333;
        }}
        
        /* Charts Section */
        .charts-section {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .charts-section h2 {{
            margin-bottom: 25px;
            color: #333;
            text-align: center;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            align-items: start;
        }}
        
        .chart-container {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #e9ecef;
        }}
        
        .chart-container h3 {{
            margin-bottom: 20px;
            color: #333;
            font-size: 1.1em;
        }}
        
        .chart-container canvas {{
            max-width: 100%;
            height: 300px !important;
        }}
        
        .chart-wide {{
            grid-column: 1 / -1;
        }}
        
        .chart-wide canvas {{
            height: 400px !important;
        }}
        
        /* Summary Section */
        .summary-section {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .summary-layout {{
            display: flex;
            gap: 30px;
            align-items: flex-start;
        }}
        
        /* Información de ejecución a la izquierda */
        .execution-info {{
            flex: 0 0 200px;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid {branding['primary_color']};
        }}
        
        .execution-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            padding: 8px 0;
        }}
        
        .execution-item:last-child {{
            margin-bottom: 0;
        }}
        
        .execution-icon {{
            font-size: 1.2em;
            width: 24px;
            text-align: center;
        }}
        
        .execution-label {{
            font-size: 0.9em;
            color: #666;
            font-weight: 500;
            min-width: 70px;
        }}
        
        .execution-value {{
            font-size: 0.9em;
            color: #333;
            font-weight: 600;
        }}
        
        /* Gráficos de resumen */
        .summary-charts-grid {{
            flex: 1;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }}
        
        .summary-chart-card {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid #e9ecef;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .summary-chart-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .chart-header {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid {branding['primary_color']};
        }}
        
        .chart-icon {{
            font-size: 1.2em;
        }}
        
        .chart-title {{
            font-size: 1em;
            font-weight: 600;
            color: #333;
        }}
        
        .chart-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
        }}
        
        .chart-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: {branding['primary_color']};
            line-height: 1;
        }}
        
        .chart-canvas-container {{
            position: relative;
            width: 120px;
            height: 120px;
        }}
        
        .chart-canvas-container canvas {{
            max-width: 100% !important;
            max-height: 100% !important;
        }}
        
        .chart-stats {{
            display: flex;
            flex-direction: column;
            gap: 5px;
            width: 100%;
        }}
        
        .stat-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8em;
            font-weight: 500;
            padding: 2px 0;
        }}
        
        .stat-item.passed {{
            color: {branding['success_color']};
        }}
        
        .stat-item.failed {{
            color: {branding['error_color']};
        }}
        
        .stat-item.skipped {{
            color: {branding['warning_color']};
        }}
        
        /* Responsive design para summary */
        @media (max-width: 768px) {{
            .summary-layout {{
                flex-direction: column;
            }}
            
            .execution-info {{
                flex: none;
                width: 100%;
            }}
            
            .summary-charts-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        @media (max-width: 1024px) {{
            .summary-charts-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        .passed {{
            color: {branding['success_color']};
        }}
        
        .failed {{
            color: {branding['error_color']};
        }}
        
        .skipped {{
            color: {branding['warning_color']};
        }}
        
        /* Feature Section */
        .feature-section {{
            background: white;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .feature-header {{
            background: #f8f9fa;
            padding: 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .feature-header:hover {{
            background: #e9ecef;
        }}
        
        .feature-header h2 {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 0;
        }}
        
        .feature-info {{
            display: flex;
            align-items: center;
            gap: 15px;
            font-size: 0.9em;
            color: #666;
        }}
        
        .feature-content {{
            padding: 20px;
        }}
        
        /* Scenario Section */
        .scenario-section {{
            margin-bottom: 20px;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .scenario-header {{
            background: #f8f9fa;
            padding: 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .scenario-header:hover {{
            background: #e9ecef;
        }}
        
        .scenario-header h3 {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 0;
            font-size: 1.1em;
        }}
        
        .scenario-info {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.8em;
            color: #666;
        }}
        
        .scenario-content {{
            padding: 15px;
            background: #fafafa;
        }}
        
        /* Step Section */
        .step-section {{
            margin-bottom: 15px;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            overflow: hidden;
        }}
        
        .step-section.status-passed {{
            border-left: 4px solid {branding['success_color']};
        }}
        
        .step-section.status-failed {{
            border-left: 4px solid {branding['error_color']};
        }}
        
        .step-section.status-skipped {{
            border-left: 4px solid {branding['warning_color']};
        }}
        
        .step-header {{
            background: white;
            padding: 12px 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .step-header:hover {{
            background: #f8f9fa;
        }}
        
        .step-info {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .step-text {{
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9em;
        }}
        
        .step-meta {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.8em;
            color: #666;
        }}
        
        .step-content {{
            padding: 15px;
            background: #fafafa;
            display: none;
        }}
        
        .step-content.expanded {{
            display: block;
        }}
        
        /* Detail Sections */
        .detail-section {{
            margin-bottom: 20px;
            background: white;
            border-radius: 6px;
            padding: 15px;
            border: 1px solid #e9ecef;
        }}
        
        .detail-section h4 {{
            margin-bottom: 15px;
            color: #333;
            font-size: 1em;
        }}
        
        .detail-section h5 {{
            margin-bottom: 10px;
            color: #666;
            font-size: 0.9em;
        }}
        
        /* Request/Response Styles */
        .method-url {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .http-method {{
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.8em;
            color: white;
        }}
        
        .method-get {{ background: {branding['success_color']}; }}
        .method-post {{ background: #2196F3; }}
        .method-put {{ background: {branding['warning_color']}; }}
        .method-patch {{ background: #9c27b0; }}
        .method-delete {{ background: {branding['error_color']}; }}
        
        .url {{
            font-family: 'Monaco', 'Menlo', monospace;
            background: #f8f9fa;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        
        .status-line {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }}
        
        .status-code {{
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            color: white;
        }}
        
        .status-success {{ background: {branding['success_color']}; }}
        .status-error {{ background: {branding['error_color']}; }}
        
        .response-time {{
            font-size: 0.9em;
            color: #666;
        }}
        
        /* Headers and Parameters */
        .headers-section, .params-section, .body-section {{
            margin-bottom: 15px;
        }}
        
        .headers-list, .params-list {{
            background: #f8f9fa;
            border-radius: 4px;
            padding: 10px;
        }}
        
        .header-item, .param-item {{
            margin-bottom: 5px;
            font-size: 0.9em;
        }}
        
        .header-key, .param-key {{
            font-weight: bold;
            color: #666;
        }}
        
        .header-value, .param-value {{
            font-family: 'Monaco', 'Menlo', monospace;
        }}
        
        /* Code Content */
        .json-content, .text-content {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 15px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.8em;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
        
        /* Assertions */
        .assertions-list {{
            background: #f8f9fa;
            border-radius: 4px;
            padding: 10px;
        }}
        
        .assertion-item {{
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 4px;
            border-left: 4px solid #ccc;
        }}
        
        .assertion-item.status-passed {{
            border-left-color: {branding['success_color']};
            background: #f1f8e9;
        }}
        
        .assertion-item.status-failed {{
            border-left-color: {branding['error_color']};
            background: #ffebee;
        }}
        
        .assertion-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }}
        
        .assertion-description {{
            font-weight: bold;
        }}
        
        .assertion-details {{
            font-size: 0.9em;
        }}
        
        .assertion-expected, .assertion-actual {{
            margin-bottom: 4px;
        }}
        
        .assertion-expected code, .assertion-actual code {{
            background: rgba(0,0,0,0.1);
            padding: 2px 4px;
            border-radius: 2px;
            font-family: 'Monaco', 'Menlo', monospace;
        }}
        
        /* Error Section */
        .error-section {{
            border-left: 4px solid {branding['error_color']};
            background: #ffebee;
        }}
        
        .error-message {{
            color: #d32f2f;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .error-traceback {{
            background: #ffcdd2;
            border: 1px solid {branding['error_color']};
            color: #b71c1c;
            font-size: 0.8em;
        }}
        
        /* Toggle Icons */
        .toggle-icon {{
            transition: transform 0.3s ease;
        }}
        
        .toggle-icon.rotated {{
            transform: rotate(180deg);
        }}
        
        /* Footer Styles */
        .report-footer {{
            background: #2c3e50;
            color: white;
            padding: 20px 0;
            margin-top: 40px;
        }}
        
        .footer-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .footer-info {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .footer-logo-only {{
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 1;
        }}
        
        .primary-logo-footer {{
            height: 24px;
            width: 24px;
            opacity: 0.8;
            border-radius: 50%;
            object-fit: cover;
        }}
        
        .primary-fallback-footer {{
            font-size: 1.2em;
        }}
        
        .footer-text {{
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.8);
        }}
        
        .footer-email {{
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .footer-email:hover {{
            color: #5dade2;
            text-decoration: underline;
        }}
        
        .footer-links {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .footer-link {{
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            font-size: 0.9em;
            transition: color 0.3s ease;
        }}
        
        .footer-link:hover {{
            color: white;
            text-decoration: underline;
        }}
        
        .separator {{
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.8em;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .header-layout {{
                flex-direction: column;
                align-items: center;
                gap: 20px;
            }}
            
            .secondary-logo {{
                position: static;
                order: -1;
            }}
            
            .main-title {{
                flex-direction: column;
                gap: 10px;
                text-align: center;
            }}
            
            .report-title {{
                font-size: 1.8em;
            }}
            
            .header-info-horizontal {{
                flex-direction: column;
                gap: 15px;
            }}
            
            .info-group {{
                flex-direction: row;
                gap: 10px;
            }}
            
            .summary-grid {{
                grid-template-columns: 1fr;
            }}
            
            .project-info-grid {{
                grid-template-columns: 1fr;
            }}
            
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
            
            .method-url {{
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .feature-header, .scenario-header, .step-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
            
            .footer-content {{
                flex-direction: column;
                text-align: center;
                gap: 10px;
            }}
            
            .footer-links {{
                justify-content: center;
            }}
        }}
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
    
    def _get_charts_javascript(self, summary: Dict) -> str:
        """Get JavaScript for charts"""
        chart_colors = self.config['charts']['colors']
        
        return f"""
        // Chart.js configuration and initialization
        document.addEventListener('DOMContentLoaded', function() {{
            // Features Pie Chart (first chart in summary)
            if (document.getElementById('scenariosChart')) {{
                const featuresCtx = document.getElementById('scenariosChart').getContext('2d');
                new Chart(featuresCtx, {{
                    type: 'pie',
                    data: {{
                        labels: ['Exitosos', 'Fallidos', 'Omitidos'],
                        datasets: [{{
                            data: [{summary['scenario_counts']['passed']}, {summary['scenario_counts']['failed']}, {summary['scenario_counts']['skipped']}],
                            backgroundColor: [
                                '{chart_colors['passed']}',
                                '{chart_colors['failed']}',
                                '{chart_colors['skipped']}'
                            ],
                            borderWidth: 1,
                            borderColor: '#ffffff'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                display: false
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                        const percentage = ((context.parsed * 100) / total).toFixed(1);
                                        return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
            }}
            
            // Scenarios Pie Chart (second chart in summary)
            if (document.getElementById('scenariosChart2')) {{
                const scenariosCtx = document.getElementById('scenariosChart2').getContext('2d');
                new Chart(scenariosCtx, {{
                    type: 'pie',
                    data: {{
                        labels: ['Exitosos', 'Fallidos', 'Omitidos'],
                        datasets: [{{
                            data: [{summary['scenario_counts']['passed']}, {summary['scenario_counts']['failed']}, {summary['scenario_counts']['skipped']}],
                            backgroundColor: [
                                '{chart_colors['passed']}',
                                '{chart_colors['failed']}',
                                '{chart_colors['skipped']}'
                            ],
                            borderWidth: 1,
                            borderColor: '#ffffff'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                display: false
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                        const percentage = ((context.parsed * 100) / total).toFixed(1);
                                        return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
            }}
            
            // Steps Pie Chart (third chart in summary)
            if (document.getElementById('stepsChart')) {{
                const stepsCtx = document.getElementById('stepsChart').getContext('2d');
                new Chart(stepsCtx, {{
                    type: 'pie',
                    data: {{
                        labels: ['Exitosos', 'Fallidos', 'Omitidos'],
                        datasets: [{{
                            data: [{summary['step_counts']['passed']}, {summary['step_counts']['failed']}, {summary['step_counts']['skipped']}],
                            backgroundColor: [
                                '{chart_colors['passed']}',
                                '{chart_colors['failed']}',
                                '{chart_colors['skipped']}'
                            ],
                            borderWidth: 1,
                            borderColor: '#ffffff'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                display: false
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                        const percentage = ((context.parsed * 100) / total).toFixed(1);
                                        return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
            }}
        }});
        """