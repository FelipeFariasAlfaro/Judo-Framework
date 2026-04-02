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
            # Preferir la variable de entorno seteada por el runner (ya es ruta absoluta)
            env_output = os.environ.get('JUDO_REPORT_OUTPUT_DIR')
            if env_output:
                output_dir = env_output
            else:
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
    
    def _cfg(self, *keys, default=None):
        """Safe nested config getter: self._cfg('theme','background_color')"""
        node = self.config
        for k in keys:
            if not isinstance(node, dict):
                return default
            node = node.get(k, default)
        return node if node is not None else default

    def generate_report(self, report_data: ReportData, filename: str = None) -> str:
        """Generate HTML report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"judo_report_{timestamp}.html"

        report_path = self.output_dir / filename
        html_content = self._generate_html(report_data)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return str(report_path)



    # ------------------------------------------------------------------ #
    #  HTML GENERATION                                                     #
    # ------------------------------------------------------------------ #

    def _generate_html(self, report_data: ReportData) -> str:
        summary = report_data.get_summary()
        charts_enabled = self._cfg("charts", "enabled", default=True)
        title = self._cfg("project", "name", default="Judo Report")
        css = self._get_css_styles()
        header = self._generate_header(report_data, summary)
        proj = self._generate_project_info()
        summ = self._generate_summary_section(summary, report_data)
        feats = self._generate_features_section(report_data.features)
        footer = self._generate_footer()
        js = self._get_javascript()
        charts_js = self._get_charts_javascript(summary) if charts_enabled else ""
        return (
            "<!DOCTYPE html>\n"
            '<html lang="en">\n'
            "<head>\n"
            '<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f"<title>{title}</title>\n"
            '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>\n'
            f"<style>{css}</style>\n"
            "</head>\n"
            "<body>\n"
            '<div class="app">\n'
            f"{header}\n"
            '<main class="main">\n'
            f"{proj}\n"
            f"{summ}\n"
            f"{feats}\n"
            "</main>\n"
            f"{footer}\n"
            "</div>\n"
            "<script>\n"
            f"{js}\n"
            f"{charts_js}\n"
            "</script>\n"
            "</body>\n"
            "</html>\n"
        )


    def _generate_header(self, report_data: ReportData, summary: Dict) -> str:
        b = self.config.get("branding", {})
        p = self.config.get("project", {})
        hcfg = self.config.get("header", {})
        failed = summary["scenario_counts"]["failed"]
        status_ok = failed == 0
        status_label = "PASSED" if status_ok else "FAILED"
        status_cls = "badge-pass" if status_ok else "badge-fail"
        duration = f"{report_data.duration:.2f}s"
        date_str = report_data.start_time.strftime(p.get("date_format", "%Y-%m-%d %H:%M:%S"))
        secondary = self.secondary_logo_b64 or self.company_logo_b64
        footer_cfg = self.config.get("footer", {})
        company_url = footer_cfg.get("company_url", "#")

        logo_html = ""
        if hcfg.get("show_company_logo", True) and secondary:
            logo_html = (
                f'<a href="{company_url}" target="_blank" class="header-logo-link">'
                f'<img src="{secondary}" alt="Logo" class="header-logo-img"></a>'
            )
        elif hcfg.get("show_company_logo", True):
            logo_html = f'<span class="header-logo-text">{p.get("company","")}</span>'

        badge_html = ""
        if hcfg.get("show_status_badge", True):
            badge_html = f'<span class="status-badge {status_cls}">{status_label}</span>'

        meta_items = []
        if hcfg.get("show_date", True):
            meta_items.append(f'<div class="header-meta-item"><span class="meta-label">Fecha</span><span class="meta-val">{date_str}</span></div>')
        if hcfg.get("show_duration", True):
            meta_items.append(f'<div class="header-meta-item"><span class="meta-label">Duración</span><span class="meta-val">{duration}</span></div>')
        meta_html = "\n".join(meta_items)

        return (
            '<header class="report-header">\n'
            '  <div class="header-inner">\n'
            '    <div class="header-top">\n'
            f'      <div class="header-logo">{logo_html}</div>\n'
            f'      <h1 class="header-title">{p.get("name","Test Report")}</h1>\n'
            f'      <div class="header-right">{badge_html}</div>\n'
            '    </div>\n'
            f'    <div class="header-meta">{meta_html}</div>\n'
            '  </div>\n'
            '</header>\n'
        )

    def _generate_project_info(self) -> str:
        p = self.config.get("project", {})
        pcfg = self.config.get("project_info", {})
        if not pcfg.get("show_section", True):
            return ""
        icon_size = pcfg.get("icon_size", "1.4em")
        cards = []
        if pcfg.get("show_engineer", True):
            cards.append(("&#128104;&#8205;&#128187;", "Ingeniero", p.get("engineer", "")))
        if pcfg.get("show_team", True):
            cards.append(("&#128101;", "Equipo", p.get("team", "")))
        if pcfg.get("show_product", True):
            cards.append(("&#128230;", "Producto", p.get("product", "")))
        if pcfg.get("show_company", True):
            cards.append(("&#127970;", "Empresa", p.get("company", "")))
        items = ""
        for icon, label, val in cards:
            items += (
                '<div class="info-card">'
                f'<span class="info-card-icon" style="font-size:{icon_size}">{icon}</span>'
                '<div class="info-card-body">'
                f'<div class="info-card-label">{label}</div>'
                f'<div class="info-card-value">{val}</div>'
                '</div></div>\n'
            )
        return f'<section class="project-info"><div class="info-cards">{items}</div></section>\n'


    def _generate_summary_section(self, summary: Dict, report_data: ReportData = None) -> str:
        b = self.config.get("branding", {})
        ccfg = self.config.get("charts", {})
        scfg = self.config.get("summary", {})
        sc = summary["scenario_counts"]
        stc = summary["step_counts"]
        total_sc = summary["total_scenarios"]
        total_st = summary["total_steps"]
        total_fe = summary["total_features"]
        pass_rate = round(sc["passed"] / max(total_sc, 1) * 100, 1)

        # Execution info
        exec_html = ""
        if scfg.get("show_execution_info", True) and report_data:
            start = report_data.start_time.strftime(
                self.config.get("project", {}).get("date_format", "%Y-%m-%d %H:%M:%S")
            )
            end = (report_data.start_time + __import__("datetime").timedelta(seconds=report_data.duration)).strftime(
                self.config.get("project", {}).get("date_format", "%Y-%m-%d %H:%M:%S")
            )
            dur = f"{report_data.duration:.2f}s"
            env_name = scfg.get("environment_name", "")
            env_row = f'<div class="exec-row"><span class="exec-label">Entorno</span><span class="exec-val">{env_name}</span></div>' if scfg.get("show_environment") and env_name else ""
            exec_html = (
                '<div class="exec-info">'
                f'<div class="exec-row"><span class="exec-label">Inicio</span><span class="exec-val">{start}</span></div>'
                f'<div class="exec-row"><span class="exec-label">Fin</span><span class="exec-val">{end}</span></div>'
                f'<div class="exec-row"><span class="exec-label">Duración</span><span class="exec-val">{dur}</span></div>'
                f'{env_row}'
                '</div>'
            )

        # Pass rate pill
        rate_html = ""
        if scfg.get("show_pass_rate", True):
            rate_color = b.get("success_color", "#22c55e") if pass_rate >= 80 else (b.get("warning_color", "#f59e0b") if pass_rate >= 50 else b.get("error_color", "#ef4444"))
            rate_html = f'<div class="pass-rate" style="color:{rate_color}"><span class="rate-num">{pass_rate}%</span><span class="rate-label">Pass Rate</span></div>'

        # Chart cards
        charts_html = ""
        if ccfg.get("enabled", True):
            cards = []
            if ccfg.get("show_features_chart", True):
                cards.append(("&#128193;", "Features", total_fe, "featuresChart", sc["passed"], sc["failed"], sc["skipped"]))
            if ccfg.get("show_scenarios_chart", True):
                cards.append(("&#128203;", "Scenarios", total_sc, "scenariosChart", sc["passed"], sc["failed"], sc["skipped"]))
            if ccfg.get("show_steps_chart", True):
                cards.append(("&#128312;", "Steps", total_st, "stepsChart", stc["passed"], stc["failed"], stc["skipped"]))
            card_html = ""
            for icon, label, total, cid, passed, failed, skipped in cards:
                card_html += (
                    '<div class="chart-card">'
                    f'<div class="chart-card-header"><span class="chart-card-icon">{icon}</span><span class="chart-card-title">{label}</span></div>'
                    f'<div class="chart-card-total">{total}</div>'
                    f'<div class="chart-wrap"><canvas id="{cid}" width="110" height="110"></canvas></div>'
                    '<div class="chart-legend">'
                    f'<span class="leg-dot" style="background:{b.get("success_color","#22c55e")}"></span><span class="leg-txt">{passed} Pass</span>'
                    f'<span class="leg-dot" style="background:{b.get("error_color","#ef4444")}"></span><span class="leg-txt">{failed} Fail</span>'
                    f'<span class="leg-dot" style="background:{b.get("warning_color","#f59e0b")}"></span><span class="leg-txt">{skipped} Skip</span>'
                    '</div></div>\n'
                )
            charts_html = f'<div class="charts-row">{card_html}</div>'

        return (
            '<section class="summary-section">'
            '<div class="summary-inner">'
            f'{exec_html}'
            f'{rate_html}'
            f'{charts_html}'
            '</div>'
            '</section>\n'
        )


    def _generate_features_section(self, features) -> str:
        fcfg = self.config.get("features", {})
        collapsed = fcfg.get("collapsed_by_default", True)
        html = '<div class="features-list">\n'
        for i, feature in enumerate(features):
            all_passed = all(s.status.value == "passed" for s in feature.scenarios)
            fstatus = "passed" if all_passed else "failed"
            icon = "&#9989;" if all_passed else "&#10060;"
            dur = f"{feature.duration:.2f}s" if fcfg.get("show_duration", True) else ""
            sc_count = f"{len(feature.scenarios)} scenarios" if fcfg.get("show_scenario_count", True) else ""
            display = "none" if collapsed else "block"
            html += (
                f'<div class="feature-block">'
                f'<div class="feature-hdr status-{fstatus}" onclick="toggleEl(\'feat-{i}\')">'
                f'<span class="fhdr-icon">{icon}</span>'
                f'<span class="fhdr-name">{feature.name}</span>'
                f'<span class="fhdr-meta">{dur} &nbsp; {sc_count}</span>'
                f'<span class="toggle-arrow" id="arr-feat-{i}">&#9660;</span>'
                f'</div>'
                f'<div class="feature-body" id="feat-{i}" style="display:{display}">'
                f'{self._generate_scenarios_section(feature.scenarios, i)}'
                f'</div></div>\n'
            )
        html += '</div>\n'
        return html

    def _generate_scenarios_section(self, scenarios, fi) -> str:
        scfg = self.config.get("scenarios", {})
        collapsed = scfg.get("collapsed_by_default", True)
        html = ""
        for j, sc in enumerate(scenarios):
            st = sc.status.value
            icon = "&#9989;" if st == "passed" else ("&#10060;" if st == "failed" else "&#9193;")
            dur = f"{sc.duration:.2f}s" if scfg.get("show_duration", True) else ""
            step_count = f"{len(sc.steps)} steps" if scfg.get("show_step_count", True) else ""
            tags_html = ""
            if scfg.get("show_tags", True) and getattr(sc, "tags", None):
                tags_html = " ".join(f'<span class="tag">@{t}</span>' for t in sc.tags)
            display = "none" if collapsed else "block"
            html += (
                f'<div class="scenario-block">'
                f'<div class="scenario-hdr status-{st}" onclick="toggleEl(\'sc-{fi}-{j}\')">'
                f'<span class="shdr-icon">{icon}</span>'
                f'<span class="shdr-name">{sc.name}</span>'
                f'<span class="shdr-meta">{tags_html} {dur} &nbsp; {step_count}</span>'
                f'<span class="toggle-arrow" id="arr-sc-{fi}-{j}">&#9660;</span>'
                f'</div>'
                f'<div class="scenario-body" id="sc-{fi}-{j}" style="display:{display}">'
                f'{self._generate_steps_section(list(getattr(sc,"background_steps",None) or []) + list(sc.steps or []))}'
                f'</div></div>\n'
            )
        return html

    def _generate_steps_section(self, steps) -> str:
        html = '<div class="steps-list">\n'
        for step in steps:
            st = step.status.value
            icon = "&#9989;" if st == "passed" else ("&#10060;" if st == "failed" else "&#9193;")
            dur = f"{step.duration:.3f}s"
            details = self._generate_step_details(step)
            has_details = bool(details.strip())
            sid = str(id(step))
            onclick = f'onclick="toggleEl(\'step-{sid}\')"'  if has_details else ""
            arrow = f'<span class="toggle-arrow" id="arr-step-{sid}">&#9660;</span>' if has_details else ""
            cursor = "cursor:pointer" if has_details else ""
            html += (
                f'<div class="step-block status-{st}">'
                f'<div class="step-hdr" style="{cursor}" {onclick}>'
                f'<span class="step-icon">{icon}</span>'
                f'<span class="step-text">{step.step_text}</span>'
                f'<span class="step-dur">{dur}</span>'
                f'{arrow}'
                f'</div>'
            )
            if has_details:
                html += f'<div class="step-details" id="step-{sid}" style="display:none">{details}</div>'
            html += '</div>\n'
        html += '</div>\n'
        return html

    def _generate_step_details(self, step) -> str:
        scfg = self.config.get("steps", {})
        html = ""
        max_body = scfg.get("max_body_length", 5000)
        if scfg.get("show_variables", True) and getattr(step, "variables_used", None):
            html += self._detail_block("&#128221; Variables", f'<pre class="code-block">{json.dumps(step.variables_used, indent=2, ensure_ascii=False)}</pre>')
        if scfg.get("show_request_details", True) and getattr(step, "request_data", None):
            req = step.request_data
            method = getattr(req, "method", "")
            url = getattr(req, "url", "")
            inner = f'<div class="req-url"><span class="http-badge method-{method.lower()}">{method}</span><code class="url-code">{url}</code></div>\n'
            if scfg.get("show_request_headers", True) and getattr(req, "headers", None):
                inner += self._kv_table("Headers", req.headers)
            if scfg.get("show_query_params", True) and getattr(req, "params", None):
                inner += self._kv_table("Query Params", req.params)
            if scfg.get("show_request_body", True) and getattr(req, "body", None):
                body_str = json.dumps(req.body, indent=2, ensure_ascii=False) if isinstance(req.body, (dict, list)) else str(req.body)
                inner += f'<div class="body-block"><div class="block-label">Body</div><pre class="code-block">{body_str[:max_body]}</pre></div>\n'
            html += self._detail_block("&#128228; Request", inner)
        if scfg.get("show_response_details", True) and getattr(step, "response_data", None):
            resp = step.response_data
            status_code = getattr(resp, "status_code", "")
            elapsed = getattr(resp, "elapsed_time", 0)
            elapsed_ms = round(elapsed * 1000) if elapsed else 0
            sc_cls = "status-ok" if str(status_code).startswith("2") else "status-err"
            inner = f'<div class="resp-status"><span class="status-code-badge {sc_cls}">{status_code}</span><span class="resp-time">{elapsed_ms}ms</span></div>\n'
            if scfg.get("show_response_headers", True) and getattr(resp, "headers", None):
                inner += self._kv_table("Headers", resp.headers)
            if scfg.get("show_response_body", True) and getattr(resp, "body", None):
                body_str = json.dumps(resp.body, indent=2, ensure_ascii=False) if isinstance(resp.body, (dict, list)) else str(resp.body)
                inner += f'<div class="body-block"><div class="block-label">Body</div><pre class="code-block">{body_str[:max_body]}</pre></div>\n'
            html += self._detail_block("&#128229; Response", inner)
        if scfg.get("show_assertions", True) and getattr(step, "assertions", None):
            html += self._generate_assertions_section(step.assertions)
        if getattr(step, "error_message", None):
            tb = ""
            if scfg.get("show_error_traceback", True) and getattr(step, "error_traceback", None):
                tb = f'<pre class="code-block error-tb">{step.error_traceback}</pre>'
            html += self._detail_block("&#10060; Error", f'<div class="error-msg">{step.error_message}</div>{tb}')
        return html

    def _detail_block(self, title: str, content: str) -> str:
        return f'<div class="detail-block"><div class="detail-title">{title}</div><div class="detail-content">{content}</div></div>\n'

    def _kv_table(self, title: str, data: dict) -> str:
        if not data:
            return ""
        rows = "".join(f'<tr><td class="kv-key">{k}</td><td class="kv-val"><code>{v}</code></td></tr>' for k, v in data.items())
        return f'<div class="kv-block"><div class="block-label">{title}</div><table class="kv-table">{rows}</table></div>\n'

    def _generate_headers_section(self, title, headers):
        return self._kv_table(title, headers)

    def _generate_params_section(self, params):
        return self._kv_table("Params", params)

    def _generate_body_section(self, title, body, body_type):
        if not body:
            return ""
        body_str = json.dumps(body, indent=2, ensure_ascii=False) if isinstance(body, (dict, list)) else str(body)
        return f'<div class="body-block"><div class="block-label">{title}</div><pre class="code-block">{body_str}</pre></div>\n'

    def _generate_assertions_section(self, assertions: list) -> str:
        if not assertions:
            return ""
        rows = ""
        for a in assertions:
            st = getattr(a, "status", None)
            st_val = st.value if hasattr(st, "value") else str(st)
            icon = "&#9989;" if st_val == "passed" else "&#10060;"
            desc = getattr(a, "description", "")
            exp = getattr(a, "expected", "")
            act = getattr(a, "actual", "")
            rows += (
                f'<div class="assertion-row status-{st_val}">'
                f'<span class="assert-icon">{icon}</span>'
                f'<span class="assert-desc">{desc}</span>'
                f'<span class="assert-exp">Expected: <code>{exp}</code></span>'
                f'<span class="assert-act">Actual: <code>{act}</code></span>'
                f'</div>\n'
            )
        return self._detail_block("&#9989; Assertions", rows)

    def _generate_footer(self) -> str:
        fc = self.config.get("footer", {})
        bg = fc.get("background_color", "#1e293b")
        tc = fc.get("text_color", "rgba(255,255,255,0.75)")
        inner = ""
        if fc.get("show_logo", True) and self.primary_logo_b64:
            inner += f'<img src="{self.primary_logo_b64}" alt="Logo" class="footer-logo">'
        if fc.get("show_links", True):
            links = []
            if fc.get("company_url") and fc.get("company_name"):
                links.append(f'<a href="{fc["company_url"]}" target="_blank" class="footer-link">{fc["company_name"]}</a>')
            if fc.get("documentation_url"):
                links.append(f'<a href="{fc["documentation_url"]}" target="_blank" class="footer-link">Docs</a>')
            if fc.get("github_url"):
                links.append(f'<a href="{fc["github_url"]}" target="_blank" class="footer-link">GitHub</a>')
            if links:
                inner += '<div class="footer-links">' + '<span class="footer-sep">·</span>'.join(links) + '</div>'
        if fc.get("show_creator", False):
            name = fc.get("creator_name", "")
            email = fc.get("creator_email", "")
            inner += f'<div class="footer-creator">Created by <a href="mailto:{email}" class="footer-link">{name}</a></div>'
        return (
            f'<footer class="report-footer" style="background:{bg};color:{tc}">'
            f'<div class="footer-inner">{inner}</div>'
            f'</footer>\n'
        )


    def _get_css_styles(self) -> str:
        b = self.config.get("branding", {})
        t = self.config.get("theme", {})
        pc  = b.get("primary_color",   "#8b5cf6")
        sc  = b.get("secondary_color", "#a855f7")
        ac  = b.get("accent_color",    "#9333ea")
        ok  = b.get("success_color",   "#22c55e")
        err = b.get("error_color",     "#ef4444")
        wrn = b.get("warning_color",   "#f59e0b")
        inf = b.get("info_color",      "#3b82f6")
        bg      = t.get("background_color", "#f0f2f5")
        surf    = t.get("surface_color",    "#ffffff")
        surf2   = t.get("surface_alt_color","#f8f9fa")
        border  = t.get("border_color",     "#e5e7eb")
        txt1    = t.get("text_primary",     "#111827")
        txt2    = t.get("text_secondary",   "#6b7280")
        txt3    = t.get("text_muted",       "#9ca3af")
        htc     = t.get("header_text_color","#ffffff")
        font    = t.get("font_family",      "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif")
        fsize   = t.get("font_size_base",   "14px")
        radius  = t.get("border_radius",    "10px")
        shadow  = t.get("shadow",           "0 1px 3px rgba(0,0,0,0.08)")
        shadow2 = t.get("shadow_md",        "0 4px 6px rgba(0,0,0,0.07)")
        fc = self.config.get("footer", {})
        footer_bg = fc.get("background_color", "#1e293b")

        return f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:{font};font-size:{fsize};line-height:1.6;color:{txt1};background:{bg}}}
a{{color:inherit;text-decoration:none}}
.app{{min-height:100vh;display:flex;flex-direction:column}}

/* ── HEADER ─────────────────────────────────────────── */
.report-header{{
  background:linear-gradient(135deg,{pc} 0%,{sc} 55%,{ac} 100%);
  color:{htc};padding:20px 28px;
  box-shadow:0 2px 12px rgba(0,0,0,0.15)
}}
.header-inner{{max-width:1280px;margin:0 auto}}
.header-top{{display:flex;align-items:center;gap:16px;margin-bottom:14px}}
.header-logo{{flex:0 0 auto}}
.header-logo-img{{height:32px;width:auto;border-radius:6px;opacity:.92}}
.header-logo-text{{font-size:.95em;font-weight:600;opacity:.9}}
.header-title{{flex:1;font-size:1.6em;font-weight:700;letter-spacing:-.3px;color:{htc}}}
.header-right{{flex:0 0 auto}}
.status-badge{{display:inline-flex;align-items:center;padding:5px 14px;border-radius:20px;font-size:.8em;font-weight:700;letter-spacing:.5px}}
.badge-pass{{background:rgba(34,197,94,.25);border:1px solid rgba(34,197,94,.5);color:#bbf7d0}}
.badge-fail{{background:rgba(239,68,68,.25);border:1px solid rgba(239,68,68,.5);color:#fecaca}}
.header-meta{{display:flex;gap:24px;background:rgba(255,255,255,.1);border-radius:8px;padding:10px 16px;backdrop-filter:blur(8px)}}
.header-meta-item{{display:flex;flex-direction:column;gap:2px}}
.meta-label{{font-size:.72em;opacity:.75;text-transform:uppercase;letter-spacing:.5px}}
.meta-val{{font-size:.9em;font-weight:600}}

/* ── MAIN ────────────────────────────────────────────── */
.main{{flex:1;max-width:1280px;width:100%;margin:0 auto;padding:20px 20px 40px}}

/* ── PROJECT INFO ────────────────────────────────────── */
.project-info{{background:{surf};border-radius:{radius};box-shadow:{shadow};padding:18px 20px;margin-bottom:18px}}
.info-cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}}
.info-card{{display:flex;align-items:center;gap:12px;padding:14px 16px;background:{surf2};border-radius:8px;border-left:3px solid {pc}}}
.info-card-icon{{font-size:1.4em;line-height:1}}
.info-card-label{{font-size:.75em;color:{txt2};text-transform:uppercase;letter-spacing:.4px;margin-bottom:2px}}
.info-card-value{{font-size:.95em;font-weight:600;color:{txt1}}}

/* ── SUMMARY ─────────────────────────────────────────── */
.summary-section{{background:{surf};border-radius:{radius};box-shadow:{shadow};padding:20px;margin-bottom:18px}}
.summary-inner{{display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start}}
.exec-info{{flex:0 0 200px;background:{surf2};border-radius:8px;padding:14px 16px;border-left:3px solid {pc}}}
.exec-row{{display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid {border}}}
.exec-row:last-child{{border-bottom:none}}
.exec-label{{font-size:.78em;color:{txt2};font-weight:500}}
.exec-val{{font-size:.82em;font-weight:600;color:{txt1}}}
.pass-rate{{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:10px 20px;background:{surf2};border-radius:8px;min-width:90px}}
.rate-num{{font-size:2em;font-weight:800;line-height:1}}
.rate-label{{font-size:.72em;color:{txt2};text-transform:uppercase;letter-spacing:.5px;margin-top:2px}}
.charts-row{{flex:1;display:flex;flex-wrap:wrap;gap:14px}}
.chart-card{{flex:1;min-width:150px;background:{surf2};border-radius:10px;padding:16px;text-align:center;border:1px solid {border};transition:box-shadow .2s}}
.chart-card:hover{{box-shadow:{shadow2}}}
.chart-card-header{{display:flex;align-items:center;justify-content:center;gap:6px;margin-bottom:8px;padding-bottom:8px;border-bottom:2px solid {pc}}}
.chart-card-icon{{font-size:1em}}
.chart-card-title{{font-size:.85em;font-weight:700;color:{txt1}}}
.chart-card-total{{font-size:2em;font-weight:800;color:{pc};line-height:1;margin-bottom:8px}}
.chart-wrap{{width:110px;height:110px;margin:0 auto 10px}}
.chart-wrap canvas{{width:110px!important;height:110px!important}}
.chart-legend{{display:flex;flex-direction:column;gap:4px;text-align:left}}
.leg-dot{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px;vertical-align:middle}}
.leg-txt{{font-size:.75em;color:{txt2}}}

/* ── FEATURES ────────────────────────────────────────── */
.features-list{{display:flex;flex-direction:column;gap:12px}}
.feature-block{{background:{surf};border-radius:{radius};box-shadow:{shadow};overflow:hidden}}
.feature-hdr{{display:flex;align-items:center;gap:10px;padding:14px 18px;cursor:pointer;user-select:none;transition:background .15s}}
.feature-hdr:hover{{background:{surf2}}}
.feature-hdr.status-passed{{border-left:4px solid {ok}}}
.feature-hdr.status-failed{{border-left:4px solid {err}}}
.fhdr-icon{{font-size:.95em}}
.fhdr-name{{flex:1;font-size:1em;font-weight:600;color:{txt1}}}
.fhdr-meta{{font-size:.78em;color:{txt2}}}
.toggle-arrow{{font-size:.7em;color:{txt3};transition:transform .2s;margin-left:6px}}
.toggle-arrow.open{{transform:rotate(180deg)}}
.feature-body{{padding:14px 18px;background:{surf2}}}

/* ── SCENARIOS ───────────────────────────────────────── */
.scenario-block{{background:{surf};border-radius:8px;margin-bottom:10px;overflow:hidden;border:1px solid {border}}}
.scenario-hdr{{display:flex;align-items:center;gap:8px;padding:11px 14px;cursor:pointer;user-select:none;transition:background .15s}}
.scenario-hdr:hover{{background:{surf2}}}
.scenario-hdr.status-passed{{border-left:3px solid {ok}}}
.scenario-hdr.status-failed{{border-left:3px solid {err}}}
.scenario-hdr.status-skipped{{border-left:3px solid {wrn}}}
.shdr-icon{{font-size:.85em}}
.shdr-name{{flex:1;font-size:.92em;font-weight:600;color:{txt1}}}
.shdr-meta{{font-size:.75em;color:{txt2};display:flex;align-items:center;gap:6px;flex-wrap:wrap}}
.tag{{background:{surf2};border:1px solid {border};border-radius:4px;padding:1px 6px;font-size:.72em;color:{txt2}}}
.scenario-body{{padding:12px 14px;background:{surf2}}}

/* ── STEPS ───────────────────────────────────────────── */
.steps-list{{display:flex;flex-direction:column;gap:6px}}
.step-block{{background:{surf};border-radius:6px;overflow:hidden;border:1px solid {border}}}
.step-block.status-passed{{border-left:3px solid {ok}}}
.step-block.status-failed{{border-left:3px solid {err}}}
.step-block.status-skipped{{border-left:3px solid {wrn}}}
.step-hdr{{display:flex;align-items:center;gap:8px;padding:8px 12px;transition:background .15s}}
.step-hdr:hover{{background:{surf2}}}
.step-icon{{font-size:.8em;flex:0 0 auto}}
.step-text{{flex:1;font-family:'Monaco','Menlo','Consolas',monospace;font-size:.82em;color:{txt1}}}
.step-dur{{font-size:.72em;color:{txt3};flex:0 0 auto}}
.step-details{{padding:12px 14px;background:{surf2};border-top:1px solid {border}}}

/* ── DETAIL BLOCKS ───────────────────────────────────── */
.detail-block{{margin-bottom:12px;background:{surf};border-radius:6px;border:1px solid {border};overflow:hidden}}
.detail-title{{padding:7px 12px;background:{surf2};font-size:.78em;font-weight:700;color:{txt2};text-transform:uppercase;letter-spacing:.4px;border-bottom:1px solid {border}}}
.detail-content{{padding:10px 12px}}
.req-url{{display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap}}
.http-badge{{padding:3px 8px;border-radius:4px;font-size:.72em;font-weight:700;color:#fff}}
.method-get{{background:{ok}}}
.method-post{{background:{inf}}}
.method-put{{background:{wrn}}}
.method-patch{{background:#8b5cf6}}
.method-delete{{background:{err}}}
.url-code{{font-family:monospace;font-size:.82em;background:{surf2};padding:3px 7px;border-radius:4px;color:{txt1};word-break:break-all}}
.resp-status{{display:flex;align-items:center;gap:10px;margin-bottom:8px}}
.status-code-badge{{padding:3px 8px;border-radius:4px;font-size:.78em;font-weight:700;color:#fff}}
.status-ok{{background:{ok}}}
.status-err{{background:{err}}}
.resp-time{{font-size:.78em;color:{txt2}}}
.kv-block{{margin-bottom:8px}}
.block-label{{font-size:.72em;font-weight:700;color:{txt2};text-transform:uppercase;letter-spacing:.4px;margin-bottom:4px}}
.kv-table{{width:100%;border-collapse:collapse;font-size:.8em}}
.kv-key{{padding:3px 8px;color:{txt2};font-weight:600;white-space:nowrap;width:35%;vertical-align:top}}
.kv-val{{padding:3px 8px;color:{txt1};word-break:break-all}}
.kv-table tr:nth-child(even){{background:{surf2}}}
.body-block{{margin-top:6px}}
.code-block{{background:#1e293b;color:#e2e8f0;padding:10px 12px;border-radius:6px;font-family:'Monaco','Menlo','Consolas',monospace;font-size:.78em;overflow-x:auto;white-space:pre-wrap;word-break:break-word;max-height:400px;overflow-y:auto}}
.error-tb{{background:#450a0a;color:#fca5a5}}
.error-msg{{color:{err};font-weight:600;font-size:.88em;margin-bottom:6px}}
.assertion-row{{display:flex;align-items:flex-start;gap:8px;padding:6px 8px;border-radius:4px;margin-bottom:4px;font-size:.82em;flex-wrap:wrap}}
.assertion-row.status-passed{{background:#f0fdf4;border-left:3px solid {ok}}}
.assertion-row.status-failed{{background:#fef2f2;border-left:3px solid {err}}}
.assert-icon{{flex:0 0 auto}}
.assert-desc{{flex:1;font-weight:600;color:{txt1}}}
.assert-exp,.assert-act{{color:{txt2};font-size:.9em}}
.assert-exp code,.assert-act code{{background:{surf2};padding:1px 4px;border-radius:3px;font-family:monospace}}

/* ── FOOTER ──────────────────────────────────────────── */
.report-footer{{padding:16px 28px;margin-top:auto}}
.footer-inner{{max-width:1280px;margin:0 auto;display:flex;align-items:center;gap:16px;flex-wrap:wrap}}
.footer-logo{{height:22px;width:auto;opacity:.7;border-radius:4px}}
.footer-links{{display:flex;align-items:center;gap:8px;flex-wrap:wrap}}
.footer-link{{font-size:.82em;opacity:.75;transition:opacity .2s}}
.footer-link:hover{{opacity:1;text-decoration:underline}}
.footer-sep{{opacity:.4;font-size:.8em}}
.footer-creator{{font-size:.8em;opacity:.7}}

/* ── RESPONSIVE ──────────────────────────────────────── */
@media(max-width:768px){{
  .header-top{{flex-wrap:wrap}}
  .header-title{{font-size:1.2em}}
  .header-meta{{flex-wrap:wrap;gap:12px}}
  .summary-inner{{flex-direction:column}}
  .exec-info{{flex:none;width:100%}}
  .charts-row{{justify-content:center}}
  .info-cards{{grid-template-columns:1fr 1fr}}
}}
"""

    def _get_javascript(self) -> str:
        collapsed_features = str(self.config.get("features", {}).get("collapsed_by_default", True)).lower()
        collapsed_scenarios = str(self.config.get("scenarios", {}).get("collapsed_by_default", True)).lower()
        return """
function toggleEl(id) {
    var el = document.getElementById(id);
    if (!el) return;
    var open = el.style.display === 'none' || el.style.display === '';
    el.style.display = open ? 'block' : 'none';
    // rotate arrow
    var arrId = 'arr-' + id;
    var arr = document.getElementById(arrId);
    if (arr) arr.classList.toggle('open', open);
}

document.addEventListener('DOMContentLoaded', function() {
    // Expand failed features/scenarios automatically
    document.querySelectorAll('.feature-hdr.status-failed').forEach(function(hdr) {
        var bodyId = hdr.nextElementSibling ? hdr.nextElementSibling.id : null;
        if (bodyId) {
            var body = document.getElementById(bodyId);
            if (body) body.style.display = 'block';
            var arr = hdr.querySelector('.toggle-arrow');
            if (arr) arr.classList.add('open');
        }
    });
    document.querySelectorAll('.scenario-hdr.status-failed').forEach(function(hdr) {
        var bodyId = hdr.nextElementSibling ? hdr.nextElementSibling.id : null;
        if (bodyId) {
            var body = document.getElementById(bodyId);
            if (body) body.style.display = 'block';
            var arr = hdr.querySelector('.toggle-arrow');
            if (arr) arr.classList.add('open');
        }
    });
});
"""


    def _get_charts_javascript(self, summary: dict) -> str:
        cc = self.config.get("charts", {})
        colors = cc.get("colors", {})
        ok  = colors.get("passed",  "#22c55e")
        err = colors.get("failed",  "#ef4444")
        wrn = colors.get("skipped", "#f59e0b")
        cutout = cc.get("cutout", "72%")
        animation = str(cc.get("animation", True)).lower()
        sc = summary["scenario_counts"]
        stc = summary["step_counts"]

        def chart_js(canvas_id, passed, failed, skipped):
            return f"""
if (document.getElementById('{canvas_id}')) {{
    new Chart(document.getElementById('{canvas_id}'), {{
        type: 'doughnut',
        data: {{
            labels: ['Passed', 'Failed', 'Skipped'],
            datasets: [{{
                data: [{passed}, {failed}, {skipped}],
                backgroundColor: ['{ok}', '{err}', '{wrn}'],
                borderWidth: 2,
                borderColor: '#ffffff',
                hoverOffset: 4
            }}]
        }},
        options: {{
            responsive: false,
            animation: {{ duration: {1 if animation == 'true' else 0} == 1 ? 600 : 0 }},
            cutout: '{cutout}',
            plugins: {{
                legend: {{ display: false }},
                tooltip: {{
                    callbacks: {{
                        label: function(ctx) {{
                            var total = ctx.dataset.data.reduce(function(a,b){{return a+b}}, 0);
                            var pct = total > 0 ? ((ctx.parsed / total) * 100).toFixed(1) : 0;
                            return ctx.label + ': ' + ctx.parsed + ' (' + pct + '%)';
                        }}
                    }}
                }}
            }}
        }}
    }});
}}"""

        js = "document.addEventListener('DOMContentLoaded', function() {"
        if cc.get("show_features_chart", True):
            js += chart_js("featuresChart", sc["passed"], sc["failed"], sc["skipped"])
        if cc.get("show_scenarios_chart", True):
            js += chart_js("scenariosChart", sc["passed"], sc["failed"], sc["skipped"])
        if cc.get("show_steps_chart", True):
            js += chart_js("stepsChart", stc["passed"], stc["failed"], stc["skipped"])
        js += "});"
        return js

