"""
Base Runner - Clase base para que los usuarios creen sus propios runners
"""

import os
import sys
import time
import threading
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path
import subprocess

from ..reporting.reporter import JudoReporter


class BaseRunner:
    """
    Clase base para crear runners personalizados
    Los usuarios pueden heredar de esta clase para crear sus propios runners
    """
    
    def __init__(self, 
                 features_dir: str = "features",
                 output_dir: str = "judo_reports",
                 parallel: bool = False,
                 max_workers: int = 4,
                 generate_cucumber_json: bool = True,
                 cucumber_json_dir: str = None,
                 console_format: str = "progress",
                 save_requests_responses: bool = False,
                 requests_responses_dir: str = None,
                 run_all_features_together: bool = True):
        """
        Inicializar runner base
        
        Args:
            features_dir: Directorio con archivos .feature
            output_dir: Directorio para reportes
            parallel: Ejecutar en paralelo
            max_workers: Número máximo de hilos
            generate_cucumber_json: Generar JSON en formato Cucumber
            cucumber_json_dir: Directorio para JSON Cucumber (default: output_dir/cucumber-json)
            console_format: Formato de salida en consola ('progress', 'progress2', 'pretty', 'plain', 'none')
                           'progress' (default) es limpio y minimalista
                           'pretty' muestra todos los detalles de cada step
            save_requests_responses: Guardar automáticamente requests y responses en archivos JSON
            requests_responses_dir: Directorio para guardar requests/responses (default: output_dir/requests_responses)
            run_all_features_together: Ejecutar todos los features en una sola llamada a behave (genera un solo reporte HTML)
                                      Si es False, ejecuta cada feature por separado (útil para paralelo)
        """
        self.features_dir = Path(features_dir)
        self.output_dir = Path(output_dir)
        self.parallel = parallel
        self.max_workers = max_workers
        self.console_format = console_format
        self.run_all_features_together = run_all_features_together
        
        # Configurar el reporter global para que el formatter lo use
        from ..reporting.reporter import set_reporter
        self.reporter = JudoReporter("Test Execution Report", str(output_dir))
        set_reporter(self.reporter)
        
        # Configuración de Cucumber JSON
        self.generate_cucumber_json = generate_cucumber_json
        if cucumber_json_dir:
            self.cucumber_json_dir = Path(cucumber_json_dir)
        else:
            self.cucumber_json_dir = self.output_dir / "cucumber-json"
        
        # Crear directorio si no existe
        if self.generate_cucumber_json:
            self.cucumber_json_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuración de Request/Response logging
        self.save_requests_responses = save_requests_responses
        if requests_responses_dir:
            self.requests_responses_dir = Path(requests_responses_dir)
        else:
            self.requests_responses_dir = self.output_dir / "requests_responses"
        
        # Configurar variables de entorno para que los hooks las usen
        import os
        # IMPORTANTE: Configurar el directorio de salida para que el formatter lo use
        os.environ['JUDO_REPORT_OUTPUT_DIR'] = str(self.output_dir)
        
        if self.save_requests_responses:
            os.environ['JUDO_SAVE_REQUESTS_RESPONSES'] = 'true'
            os.environ['JUDO_OUTPUT_DIRECTORY'] = str(self.requests_responses_dir)
            # Crear directorio si no existe
            self.requests_responses_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuración
        self.config = {
            "timeout": 300,  # 5 minutos por defecto
            "retry_count": 0,
            "fail_fast": False,
            "verbose": True
        }
        
        # Resultados
        self.results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "start_time": None,
            "end_time": None,
            "duration": 0
        }
        
        # Tags para filtrar scenarios
        self.current_tags: List[str] = []
        self.current_exclude_tags: List[str] = []
        
        # Callbacks
        self.before_all_callback: Optional[Callable] = None
        self.after_all_callback: Optional[Callable] = None
        self.before_feature_callback: Optional[Callable] = None
        self.after_feature_callback: Optional[Callable] = None
    
    def configure(self, **kwargs):
        """Configurar el runner"""
        self.config.update(kwargs)
        return self
    
    def set_parallel(self, enabled: bool, max_workers: int = 4):
        """Configurar ejecución paralela"""
        self.parallel = enabled
        self.max_workers = max_workers
        return self
    
    def set_request_response_logging(self, enabled: bool, directory: str = None):
        """
        Configurar el guardado automático de requests y responses
        
        Args:
            enabled: True para habilitar, False para deshabilitar
            directory: Directorio donde guardar los archivos (opcional)
        """
        self.save_requests_responses = enabled
        
        if directory:
            self.requests_responses_dir = Path(directory)
        elif not hasattr(self, 'requests_responses_dir'):
            self.requests_responses_dir = self.output_dir / "requests_responses"
        
        # Configurar variables de entorno
        import os
        if enabled:
            os.environ['JUDO_SAVE_REQUESTS_RESPONSES'] = 'true'
            os.environ['JUDO_OUTPUT_DIRECTORY'] = str(self.requests_responses_dir)
            # Crear directorio si no existe
            self.requests_responses_dir.mkdir(parents=True, exist_ok=True)
            self.log(f"📁 Request/Response logging habilitado: {self.requests_responses_dir}")
        else:
            os.environ['JUDO_SAVE_REQUESTS_RESPONSES'] = 'false'
            self.log("🚫 Request/Response logging deshabilitado")
        
        return self
    
    def set_callbacks(self, 
                     before_all: Callable = None,
                     after_all: Callable = None,
                     before_feature: Callable = None,
                     after_feature: Callable = None):
        """Configurar callbacks"""
        if before_all:
            self.before_all_callback = before_all
        if after_all:
            self.after_all_callback = after_all
        if before_feature:
            self.before_feature_callback = before_feature
        if after_feature:
            self.after_feature_callback = after_feature
        return self
    
    def find_features(self, tags: List[str] = None, exclude_tags: List[str] = None) -> List[Path]:
        """
        Encontrar archivos .feature basado en tags
        
        Args:
            tags: Tags a incluir (ej: ["@smoke", "@api"])
            exclude_tags: Tags a excluir (ej: ["@slow", "@manual"])
        """
        feature_files = []
        
        # Try to find features directory with different case variations
        possible_dirs = [
            self.features_dir,
            Path(str(self.features_dir).lower()),  # features
            Path(str(self.features_dir).capitalize()),  # Features
            Path("features"),  # Default behave convention
            Path("Features")   # Windows common variation
        ]
        
        features_dir = None
        for possible_dir in possible_dirs:
            if possible_dir.exists():
                features_dir = possible_dir
                break
        
        if not features_dir:
            self.log(f"❌ Directorio de features no existe. Probé: {[str(d) for d in possible_dirs]}")
            return feature_files
        
        # Update the features_dir to the one that actually exists
        self.features_dir = features_dir
        self.log(f"📁 Usando directorio de features: {self.features_dir}")
        
        # Buscar todos los archivos .feature
        for feature_file in self.features_dir.rglob("*.feature"):
            if self._should_include_feature(feature_file, tags, exclude_tags):
                feature_files.append(feature_file)
        
        return feature_files
    
    def _should_include_feature(self, feature_file: Path, tags: List[str], exclude_tags: List[str]) -> bool:
        """Determinar si incluir un feature basado en tags"""
        if not tags and not exclude_tags:
            return True
        
        try:
            content = feature_file.read_text(encoding='utf-8')
            
            # Extraer tags del archivo
            file_tags = self._extract_tags_from_content(content)
            
            # Verificar tags de exclusión
            if exclude_tags:
                for exclude_tag in exclude_tags:
                    if exclude_tag in file_tags:
                        return False
            
            # Verificar tags de inclusión
            if tags:
                for tag in tags:
                    if tag in file_tags:
                        return True
                return False  # No se encontró ningún tag requerido
            
            return True
            
        except Exception as e:
            self.log(f"⚠️ Error leyendo feature {feature_file}: {e}")
            return True
    
    def _extract_tags_from_content(self, content: str) -> List[str]:
        """Extraer tags de un archivo .feature"""
        import re
        tags = []
        
        # Buscar líneas que empiecen con @
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('@'):
                # Extraer todos los tags de la línea
                # Incluye letras, números, guiones medios (-) y guiones bajos (_)
                # Esto permite tags como @PROJ-123, @api-test, @smoke_test, etc.
                found_tags = re.findall(r'@[\w-]+', line)
                tags.extend(found_tags)
        
        return tags
    
    def run_behave_command(self, feature_file: Path, extra_args: List[str] = None) -> Dict[str, Any]:
        """
        Ejecutar comando behave para un feature
        
        Args:
            feature_file: Archivo .feature a ejecutar
            extra_args: Argumentos adicionales para behave
        """
        cmd = [sys.executable, "-m", "behave"]
        
        # Agregar archivo feature
        cmd.append(str(feature_file))
        
        # Agregar tags si están configurados
        if self.current_tags:
            for tag in self.current_tags:
                cmd.extend(["--tags", tag])
        
        # Agregar exclude tags si están configurados
        if self.current_exclude_tags:
            for tag in self.current_exclude_tags:
                cmd.extend(["--tags", f"~{tag}"])
        
        # Agregar argumentos adicionales
        if extra_args:
            cmd.extend(extra_args)
        
        # Configurar formato de salida multiplataforma
        import tempfile
        from datetime import datetime
        
        # Crear archivo temporal para capturar JSON (funciona en todos los OS)
        json_output_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False)
        json_output_path = json_output_file.name
        json_output_file.close()
        
        # Configurar formatos de salida
        cmd.extend(["--format", "json", "--outfile", json_output_path])
        
        # NO agregar el formatter de Judo aquí porque los auto_hooks ya capturan los datos
        # El formatter causaría duplicados
        
        # Si está habilitado, también generar Cucumber JSON
        cucumber_json_path = None
        if self.generate_cucumber_json:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            feature_name = feature_file.stem
            cucumber_json_path = self.cucumber_json_dir / f"{feature_name}_{timestamp}.json"
            cmd.extend(["--format", "json", "--outfile", str(cucumber_json_path)])
        
        # Usar formato de consola configurado
        # 'progress' es más limpio que 'pretty', 'judo-simple' es el más minimalista
        if self.console_format != "none":
            cmd.extend(["--format", self.console_format])
        cmd.extend(["--no-capture"])
        
        start_time = time.time()
        
        try:
            # Ejecutar con salida en tiempo real si verbose está habilitado
            if self.config.get("verbose", True):
                result = subprocess.run(
                    cmd,
                    text=True,
                    timeout=self.config.get("timeout", 300),
                    cwd=os.getcwd(),
                    encoding='utf-8',
                    errors='replace',
                    capture_output=False,  # Mostrar salida en consola
                    env=os.environ  # Pass environment variables
                )
                stdout_content = ""
                stderr_content = ""
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.config.get("timeout", 300),
                    cwd=os.getcwd(),
                    encoding='utf-8',
                    env=os.environ,  # Pass environment variables
                    errors='replace'
                )
                stdout_content = result.stdout
                stderr_content = result.stderr
            
            duration = time.time() - start_time
            
            # Leer datos JSON del reporte
            json_data = None
            try:
                if os.path.exists(json_output_path):
                    with open(json_output_path, 'r', encoding='utf-8', errors='replace') as f:
                        json_content = f.read()
                        if json_content.strip():
                            json_data = json.loads(json_content)
                    
                    # Limpiar archivo temporal (multiplataforma)
                    try:
                        os.unlink(json_output_path)
                    except (OSError, PermissionError):
                        # En Windows a veces hay problemas de permisos, intentar después
                        try:
                            os.remove(json_output_path)
                        except:
                            pass  # Si no se puede eliminar, no es crítico
            except Exception as e:
                self.log(f"⚠️ Error leyendo JSON de reporte: {e}")
                # Intentar limpiar archivo temporal aunque haya error
                try:
                    if os.path.exists(json_output_path):
                        os.unlink(json_output_path)
                except:
                    pass
            
            return {
                "feature_file": str(feature_file),
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": stdout_content,
                "stderr": stderr_content,
                "duration": duration,
                "json_data": json_data,  # Agregar datos JSON para el reporte
                "cucumber_json": str(cucumber_json_path) if cucumber_json_path else None
            }
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            # Limpiar archivo temporal
            try:
                if os.path.exists(json_output_path):
                    os.unlink(json_output_path)
            except:
                pass
            
            return {
                "feature_file": str(feature_file),
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Timeout after {self.config.get('timeout')} seconds",
                "duration": duration,
                "json_data": None
            }
        except Exception as e:
            duration = time.time() - start_time
            # Limpiar archivo temporal
            try:
                if os.path.exists(json_output_path):
                    os.unlink(json_output_path)
            except:
                pass
            
            return {
                "feature_file": str(feature_file),
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "duration": duration,
                "json_data": None
            }
    
    def run_single_feature(self, feature_file: Path) -> Dict[str, Any]:
        """Ejecutar un solo feature (para override por usuarios)"""
        if self.before_feature_callback:
            self.before_feature_callback(feature_file)
        
        result = self.run_behave_command(feature_file)
        
        if self.after_feature_callback:
            self.after_feature_callback(feature_file, result)
        
        return result
    
    def run_all_features_in_one_execution(self, feature_files: List[Path]) -> Dict[str, Any]:
        """
        Ejecutar todos los features en una sola llamada a behave
        Esto genera un solo reporte HTML con todos los features
        """
        if not feature_files:
            return {"success": False, "duration": 0, "stdout": "", "stderr": "No features to run"}
        
        self.log(f"🎯 Ejecutando {len(feature_files)} features en una sola ejecución")
        
        cmd = [sys.executable, "-m", "behave"]
        
        # Agregar todos los archivos feature
        for feature_file in feature_files:
            cmd.append(str(feature_file))
        
        # Agregar tags si están configurados
        if self.current_tags:
            for tag in self.current_tags:
                cmd.extend(["--tags", tag])
        
        # Agregar exclude tags si están configurados
        if self.current_exclude_tags:
            for tag in self.current_exclude_tags:
                cmd.extend(["--tags", f"~{tag}"])
        
        # Configurar formato de salida
        import tempfile
        from datetime import datetime
        
        json_output_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False)
        json_output_path = json_output_file.name
        json_output_file.close()
        
        cmd.extend(["--format", "json", "--outfile", json_output_path])
        
        # Cucumber JSON si está habilitado
        cucumber_json_path = None
        if self.generate_cucumber_json:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cucumber_json_path = self.cucumber_json_dir / f"all_features_{timestamp}.json"
            cmd.extend(["--format", "json", "--outfile", str(cucumber_json_path)])
        
        # Formato de consola
        if self.console_format != "none":
            cmd.extend(["--format", self.console_format])
        cmd.extend(["--no-capture"])
        
        start_time = time.time()
        
        try:
            if self.config.get("verbose", True):
                result = subprocess.run(
                    cmd,
                    text=True,
                    timeout=self.config.get("timeout", 300),
                    cwd=os.getcwd(),
                    encoding='utf-8',
                    errors='replace',
                    capture_output=False,
                    env=os.environ
                )
                stdout_content = ""
                stderr_content = ""
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.config.get("timeout", 300),
                    cwd=os.getcwd(),
                    encoding='utf-8',
                    env=os.environ,
                    errors='replace'
                )
                stdout_content = result.stdout
                stderr_content = result.stderr
            
            duration = time.time() - start_time
            
            # Limpiar archivo temporal
            try:
                os.unlink(json_output_path)
            except:
                pass
            
            return {
                "success": result.returncode == 0,
                "duration": duration,
                "stdout": stdout_content,
                "stderr": stderr_content,
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return {
                "success": False,
                "duration": duration,
                "stdout": "",
                "stderr": "Test execution timed out",
                "returncode": -1
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "success": False,
                "duration": duration,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    def run_features_sequential(self, feature_files: List[Path]) -> List[Dict[str, Any]]:
        """Ejecutar features secuencialmente"""
        results = []
        
        for i, feature_file in enumerate(feature_files, 1):
            self.log(f"🏃 Ejecutando feature {i}/{len(feature_files)}: {feature_file.name}")
            
            result = self.run_single_feature(feature_file)
            results.append(result)
            
            # Actualizar estadísticas
            self.results["total"] += 1
            if result["success"]:
                self.results["passed"] += 1
                self.log(f"✅ {feature_file.name} - PASSED ({result['duration']:.2f}s)")
            else:
                self.results["failed"] += 1
                self.log(f"❌ {feature_file.name} - FAILED ({result['duration']:.2f}s)")
                if self.config.get("verbose") and result.get("stderr"):
                    self.log(f"Error: {result['stderr']}")
            
            # Fail fast
            if not result["success"] and self.config.get("fail_fast"):
                self.log("🛑 Fail fast habilitado, deteniendo ejecución")
                break
        
        return results
    
    def run_features_parallel(self, feature_files: List[Path]) -> List[Dict[str, Any]]:
        """Ejecutar features en paralelo"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Enviar todas las tareas
            future_to_feature = {
                executor.submit(self.run_single_feature, feature_file): feature_file
                for feature_file in feature_files
            }
            
            # Procesar resultados conforme se completan
            for future in as_completed(future_to_feature):
                feature_file = future_to_feature[future]
                
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Actualizar estadísticas (thread-safe)
                    with threading.Lock():
                        self.results["total"] += 1
                        if result["success"]:
                            self.results["passed"] += 1
                            self.log(f"✅ {feature_file.name} - PASSED ({result['duration']:.2f}s)")
                        else:
                            self.results["failed"] += 1
                            self.log(f"❌ {feature_file.name} - FAILED ({result['duration']:.2f}s)")
                
                except Exception as e:
                    self.log(f"❌ Error ejecutando {feature_file.name}: {e}")
                    results.append({
                        "feature_file": str(feature_file),
                        "success": False,
                        "returncode": -1,
                        "stdout": "",
                        "stderr": str(e),
                        "duration": 0
                    })
        
        return results
    
    def run(self, tags: List[str] = None, exclude_tags: List[str] = None) -> Dict[str, Any]:
        """
        Ejecutar tests
        
        Args:
            tags: Tags a incluir
            exclude_tags: Tags a excluir
        """
        self.log("🥋 Iniciando ejecución de tests con Judo Framework")
        self.log(f"📁 Directorio de features: {self.features_dir}")
        self.log(f"📊 Directorio de reportes: {self.output_dir}")
        
        # Guardar tags para usarlos en run_behave_command
        self.current_tags = tags or []
        self.current_exclude_tags = exclude_tags or []
        
        # Inicializar tiempos
        self.results["start_time"] = time.time()
        
        # Callback before all
        if self.before_all_callback:
            self.before_all_callback()
        
        # Encontrar features
        feature_files = self.find_features(tags, exclude_tags)
        
        if not feature_files:
            self.log("⚠️ No se encontraron features para ejecutar")
            return self.results
        
        self.log(f"🎯 Encontrados {len(feature_files)} features para ejecutar")
        if tags:
            self.log(f"🏷️ Tags incluidos: {', '.join(tags)}")
        if exclude_tags:
            self.log(f"🚫 Tags excluidos: {', '.join(exclude_tags)}")
        
        # Ejecutar features
        if self.run_all_features_together and not self.parallel:
            # Ejecutar todos los features en una sola llamada a behave
            # Esto genera un solo reporte HTML con todos los features
            self.log("📝 Ejecutando todos los features juntos (un solo reporte)")
            single_result = self.run_all_features_in_one_execution(feature_files)
            execution_results = [single_result]
            
            # Actualizar estadísticas basadas en el resultado
            if single_result["success"]:
                self.results["passed"] = len(feature_files)
                self.log(f"✅ Todos los features - PASSED ({single_result['duration']:.2f}s)")
            else:
                self.results["failed"] = len(feature_files)
                self.log(f"❌ Ejecución - FAILED ({single_result['duration']:.2f}s)")
        elif self.parallel and len(feature_files) > 1:
            self.log(f"🚀 Ejecutando en paralelo con {self.max_workers} hilos")
            execution_results = self.run_features_parallel(feature_files)
        else:
            self.log("📝 Ejecutando secuencialmente (un feature a la vez)")
            execution_results = self.run_features_sequential(feature_files)
        
        # Finalizar
        self.results["end_time"] = time.time()
        self.results["duration"] = self.results["end_time"] - self.results["start_time"]
        
        # Callback after all
        if self.after_all_callback:
            self.after_all_callback(self.results)
        
        # Generar reporte
        self._generate_final_report(execution_results)
        
        # Consolidar Cucumber JSON si está habilitado
        if self.generate_cucumber_json and execution_results:
            self.consolidate_cucumber_json()
        
        return self.results
    
    def _generate_final_report(self, execution_results: List[Dict[str, Any]]):
        """Generar reporte final con datos de Behave"""
        try:
            # Recopilar archivos Cucumber JSON
            cucumber_json_files = []
            for result in execution_results:
                if result.get("cucumber_json"):
                    cucumber_json_files.append(result["cucumber_json"])
            
            # IMPORTANTE: El reporte HTML ya fue generado por los auto_hooks durante
            # la ejecución de behave (en after_all_judo). Los hooks capturan todos los 
            # datos de request/response en tiempo real.
            # NO necesitamos generar el reporte aquí.
            
            report_path = self.output_dir / "test_execution_report.html"
            if report_path.exists():
                self.log(f"📊 Reporte HTML generado: {report_path}")
            else:
                self.log(f"⚠️ Reporte HTML no encontrado en: {report_path}")
            
            # Mostrar información sobre archivos Cucumber JSON
            if cucumber_json_files:
                self.log(f"\n🥒 Cucumber JSON generados ({len(cucumber_json_files)} archivos):")
                self.log(f"📁 Directorio: {self.cucumber_json_dir}")
                for json_file in cucumber_json_files:
                    self.log(f"   - {Path(json_file).name}")
                self.log(f"\n💡 Estos archivos pueden ser usados con:")
                self.log(f"   • Xray (Jira)")
                self.log(f"   • Cucumber HTML Reporter")
                self.log(f"   • Allure")
                self.log(f"   • Cualquier herramienta compatible con Cucumber JSON")
        except Exception as e:
            self.log(f"⚠️ Error generando reporte: {e}")
    
    def _process_feature_data(self, feature_data: Dict[str, Any]):
        """Procesar datos de un feature para el reporte"""
        try:
            from ..reporting.report_data import StepStatus, ScenarioStatus
            
            feature_name = feature_data.get("name", "Unknown Feature")
            
            # Iniciar feature en el reporter
            # Procesar tags del feature
            feature_tags = []
            for tag in feature_data.get("tags", []):
                if isinstance(tag, dict):
                    feature_tags.append(tag.get("name", ""))
                elif isinstance(tag, str):
                    feature_tags.append(tag)
            
            self.reporter.start_feature(
                name=feature_name,
                description=feature_data.get("description", ""),
                file_path=feature_data.get("uri", ""),
                tags=feature_tags
            )
            
            # Procesar scenarios
            for scenario in feature_data.get("elements", []):
                scenario_name = scenario.get("name", "Unknown Scenario")
                scenario_type = scenario.get("type", "scenario")
                
                # Verificar si el scenario tiene steps con resultados (fue ejecutado)
                steps = scenario.get("steps", [])
                if not steps:
                    continue  # Skip scenarios sin steps
                
                # Verificar si algún step tiene resultado (indica que se ejecutó)
                has_results = any(step.get("result") is not None for step in steps)
                if not has_results:
                    continue  # Skip scenarios que no se ejecutaron
                
                # Procesar tags del scenario
                scenario_tags = []
                for tag in scenario.get("tags", []):
                    if isinstance(tag, dict):
                        scenario_tags.append(tag.get("name", ""))
                    elif isinstance(tag, str):
                        scenario_tags.append(tag)
                
                # Iniciar scenario
                self.reporter.start_scenario(
                    name=scenario_name,
                    tags=scenario_tags
                )
                
                # Procesar steps
                for step in steps:
                    step_keyword = step.get("keyword", "").strip()
                    step_name = step.get("name", "")
                    step_result = step.get("result", {})
                    
                    # Skip steps sin resultado
                    if not step_result:
                        continue
                    
                    step_status = step_result.get("status", "undefined")
                    
                    # Iniciar step
                    full_step = f"{step_keyword} {step_name}"
                    self.reporter.start_step(full_step, is_background=False)
                    
                    # Finalizar step con status apropiado
                    if step_status == "passed":
                        self.reporter.finish_step(StepStatus.PASSED)
                    elif step_status == "failed":
                        error_msg = step_result.get("error_message", "Step failed")
                        self.reporter.finish_step(StepStatus.FAILED, error_msg)
                    elif step_status == "skipped":
                        self.reporter.finish_step(StepStatus.SKIPPED)
                    else:
                        self.reporter.finish_step(StepStatus.PENDING)
                
                # Finalizar scenario
                scenario_status = ScenarioStatus.PASSED
                if any(s.get("result", {}).get("status") == "failed" for s in steps if s.get("result")):
                    scenario_status = ScenarioStatus.FAILED
                self.reporter.finish_scenario(scenario_status)
            
            # Finalizar feature
            self.reporter.finish_feature()
                        
        except Exception as e:
            self.log(f"⚠️ Error procesando datos de feature: {e}")
    
    def consolidate_cucumber_json(self, output_file: str = "cucumber-consolidated.json"):
        """
        Consolidar todos los archivos Cucumber JSON en uno solo
        Útil para herramientas como Xray que prefieren un solo archivo
        
        Args:
            output_file: Nombre del archivo consolidado
        """
        import json
        
        consolidated = []
        
        # Leer todos los archivos JSON en el directorio
        for json_file in self.cucumber_json_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        consolidated.extend(data)
                    else:
                        consolidated.append(data)
            except Exception as e:
                self.log(f"⚠️ Error leyendo {json_file.name}: {e}")
        
        # Guardar archivo consolidado
        if consolidated:
            output_path = self.cucumber_json_dir / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(consolidated, f, indent=2, ensure_ascii=False)
            
            self.log(f"📦 JSON consolidado generado: {output_path}")
            return str(output_path)
        
        return None
    
    def log(self, message: str):
        """Log mensaje (puede ser override por usuarios)"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def print_summary(self):
        """Imprimir resumen de ejecución"""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE EJECUCIÓN")
        print("=" * 60)
        print(f"⏱️  Duración total: {self.results['duration']:.2f}s")
        print(f"📋 Total features: {self.results['total']}")
        print(f"✅ Exitosos: {self.results['passed']}")
        print(f"❌ Fallidos: {self.results['failed']}")
        print(f"⏭️  Omitidos: {self.results['skipped']}")
        
        if self.results['total'] > 0:
            success_rate = (self.results['passed'] / self.results['total']) * 100
            print(f"📈 Tasa de éxito: {success_rate:.1f}%")
        
        print("=" * 60)
        
        if self.results['failed'] == 0:
            print("🎉 ¡Todos los tests pasaron!")
        else:
            print(f"⚠️ {self.results['failed']} test(s) fallaron")
        
        return self.results['failed'] == 0