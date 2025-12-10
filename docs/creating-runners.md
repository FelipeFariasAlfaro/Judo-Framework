# 🏃‍♂️ Creando Runners Personalizados

Judo Framework permite crear runners personalizados para ejecutar tests con tags, ejecución paralela, y configuraciones específicas, similar a los runners de Karate Framework.

## 🎯 ¿Qué es un Runner?

Un runner es una clase que organiza y ejecuta tus tests de Behave con funcionalidades avanzadas:

- ✅ **Filtrado por tags**: Ejecutar solo tests con tags específicos
- ✅ **Ejecución paralela**: Ejecutar múltiples features simultáneamente
- ✅ **Test suites**: Organizar tests en suites reutilizables
- ✅ **Configuración flexible**: Timeouts, reintentos, fail-fast
- ✅ **Callbacks**: Hooks antes/después de ejecución
- ✅ **Reportes automáticos**: Generación de reportes HTML

## 🚀 Creando tu Primer Runner

### **1. Runner Básico**

Crea un archivo `my_runner.py` en tu proyecto:

```python
from judo.runner.base_runner import BaseRunner
import sys

class MyRunner(BaseRunner):
    def __init__(self):
        super().__init__(
            features_dir="features",      # Tu directorio de .feature files
            output_dir="test_reports",    # Donde guardar reportes
            parallel=False,               # Ejecución secuencial
            max_workers=4                 # Hilos si habilitas paralelo
        )
        
        # Configuración
        self.configure(
            timeout=300,      # 5 minutos por test
            fail_fast=False,  # Continuar aunque falle
            verbose=True      # Mostrar detalles
        )
    
    def run_smoke_tests(self):
        """Ejecutar solo smoke tests"""
        return self.run(tags=["@smoke"])
    
    def run_api_tests(self):
        """Ejecutar tests de API"""
        return self.run(tags=["@api"])

def main():
    runner = MyRunner()
    
    if len(sys.argv) > 1 and sys.argv[1] == "smoke":
        results = runner.run_smoke_tests()
    else:
        results = runner.run_api_tests()
    
    success = runner.print_summary()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

### **2. Ejecutar tu Runner**

```bash
# Ejecutar API tests
python my_runner.py

# Ejecutar smoke tests
python my_runner.py smoke
```

## 🔧 Configuración Avanzada

### **Ejecución Paralela**

```python
class MyParallelRunner(BaseRunner):
    def __init__(self):
        super().__init__(
            parallel=True,        # Habilitar paralelo
            max_workers=6         # 6 hilos simultáneos
        )
    
    def run_fast_tests(self):
        # Configurar para máxima velocidad
        self.set_parallel(True, max_workers=8)
        self.configure(timeout=120, fail_fast=False)
        
        return self.run(
            tags=["@fast", "@smoke"],
            exclude_tags=["@slow", "@manual"]
        )
```

### **Callbacks y Hooks**

```python
class MyAdvancedRunner(BaseRunner):
    def setup_environment(self):
        """Configurar antes de todos los tests"""
        print("🔧 Configurando entorno...")
        os.environ["API_BASE_URL"] = "https://api.example.com"
    
    def cleanup_environment(self):
        """Limpiar después de todos los tests"""
        print("🧹 Limpiando...")
    
    def __init__(self):
        super().__init__()
        
        # Configurar callbacks
        self.set_callbacks(
            before_all=self.setup_environment,
            after_all=lambda results: self.cleanup_environment()
        )
```

## 📋 Test Suites

### **Crear Suites Personalizadas**

```python
from judo.runner.test_suite import TestSuite

# Suite de smoke tests
smoke_suite = TestSuite(
    name="Smoke Tests",
    description="Tests críticos básicos"
).add_features_by_tag(["@smoke"]).set_config(
    parallel=True,
    max_workers=2,
    fail_fast=True
)

# Suite de regresión
regression_suite = TestSuite(
    name="Regression Tests", 
    description="Tests completos de regresión"
).add_features_by_tag(["@regression"]).exclude_by_tag(["@manual"]).set_config(
    parallel=True,
    max_workers=4,
    timeout=600
)

# Suite por features específicos
user_suite = TestSuite(
    name="User Management",
    description="Tests de gestión de usuarios"
).add_feature("features/user_api.feature").add_feature("features/user_auth.feature")
```

### **Runner con Suites**

```python
class MySuiteRunner(BaseRunner):
    def __init__(self):
        super().__init__()
        self.suites = {
            "smoke": smoke_suite,
            "regression": regression_suite,
            "user": user_suite
        }
    
    def run_suite(self, suite_name):
        if suite_name not in self.suites:
            print(f"❌ Suite desconocida: {suite_name}")
            return
        
        suite = self.suites[suite_name]
        
        # Aplicar configuración de la suite
        if suite.config.get("parallel"):
            self.set_parallel(True, suite.config.get("max_workers", 4))
        
        return self.run(
            tags=suite.get_tags(),
            exclude_tags=suite.get_exclude_tags()
        )
```

## 🎯 Ejemplos de Uso Avanzado

### **Runner por Entornos**

```python
class MyEnvironmentRunner(BaseRunner):
    def run_for_environment(self, env):
        """Ejecutar tests para un entorno específico"""
        env_configs = {
            "dev": {
                "API_BASE_URL": "https://api-dev.example.com",
                "tags": ["@dev", "@smoke"]
            },
            "test": {
                "API_BASE_URL": "https://api-test.example.com", 
                "tags": ["@test", "@regression"]
            },
            "prod": {
                "API_BASE_URL": "https://api.example.com",
                "tags": ["@prod", "@smoke"]
            }
        }
        
        if env in env_configs:
            config = env_configs[env]
            os.environ["API_BASE_URL"] = config["API_BASE_URL"]
            return self.run(tags=config["tags"])

# Uso
runner = MyEnvironmentRunner()
runner.run_for_environment("test")
```

### **Runner con Reintentos**

```python
class MyRetryRunner(BaseRunner):
    def run_with_retry(self, max_retries=2):
        """Ejecutar con reintentos automáticos"""
        for attempt in range(max_retries + 1):
            if attempt > 0:
                self.log(f"🔁 Intento {attempt + 1}")
            
            results = self.run(exclude_tags=["@manual"])
            
            if results["failed"] == 0:
                return results
            
            if attempt < max_retries:
                self.log("⚠️ Reintentando tests fallidos...")
                # Reset para siguiente intento
                self._reset_results()
        
        return results
```

### **Runner de Performance**

```python
class MyPerformanceRunner(BaseRunner):
    def run_load_test(self, concurrent_users=10):
        """Simular carga con múltiples usuarios"""
        self.log(f"🏋️ Load test con {concurrent_users} usuarios")
        
        self.set_parallel(True, max_workers=concurrent_users)
        self.configure(timeout=60, fail_fast=False)
        
        return self.run(tags=["@load", "@performance"])
```

## 📁 Estructura de Proyecto Recomendada

```
mi_proyecto/
├── features/                    # Archivos .feature
│   ├── api/
│   │   ├── users.feature
│   │   └── posts.feature
│   └── integration/
│       └── workflow.feature
├── runners/                     # Tus runners personalizados
│   ├── basic_runner.py
│   ├── parallel_runner.py
│   └── suite_runner.py
├── test_data/                   # Datos de prueba
│   ├── users.json
│   └── schemas/
├── test_reports/                # Reportes generados
└── suites/                      # Configuraciones de suites
    ├── smoke_suite.json
    └── regression_suite.json
```

## 🎮 Comandos de Ejemplo

```bash
# Runner básico
python runners/basic_runner.py smoke
python runners/basic_runner.py api
python runners/basic_runner.py all

# Runner paralelo
python runners/parallel_runner.py fast
python runners/parallel_runner.py comprehensive
python runners/parallel_runner.py env:test

# Runner con suites
python runners/suite_runner.py smoke
python runners/suite_runner.py multiple smoke api regression
python runners/suite_runner.py list
```

## 🔧 Configuración por Archivo

### **Guardar Suite en JSON**

```python
# Crear y guardar suite
suite = TestSuite("My Suite", "Descripción").add_features_by_tag(["@api"])
suite.save_to_file("suites/my_suite.json")

# Cargar suite desde archivo
loaded_suite = TestSuite.load_from_file("suites/my_suite.json")
```

### **Archivo de Suite JSON**

```json
{
  "name": "API Tests",
  "description": "Tests completos de API",
  "tags": ["@api", "@smoke"],
  "exclude_tags": ["@manual", "@slow"],
  "config": {
    "parallel": true,
    "max_workers": 4,
    "timeout": 300,
    "fail_fast": false
  },
  "environments": {
    "test": {
      "API_BASE_URL": "https://api-test.example.com"
    }
  }
}
```

## 📊 Reportes Automáticos

Todos los runners generan automáticamente:

- ✅ **Reportes HTML** en el directorio `test_reports/`
- ✅ **Estadísticas detalladas** de ejecución
- ✅ **Información de timing** y performance
- ✅ **Detalles de errores** con stack traces

Los reportes se guardan en tu proyecto, no en la instalación de Judo Framework.

## 🎯 Mejores Prácticas

1. **Organiza por funcionalidad**: Crea runners específicos para diferentes tipos de tests
2. **Usa tags consistentes**: Define una estrategia de tags clara (@smoke, @api, @regression)
3. **Configura timeouts apropiados**: Tests de integración necesitan más tiempo
4. **Aprovecha el paralelismo**: Para tests independientes, usa ejecución paralela
5. **Implementa callbacks**: Para setup/cleanup de entorno
6. **Guarda configuraciones**: Usa archivos JSON para suites reutilizables

¡Con estos runners personalizados tendrás el control completo sobre la ejecución de tus tests! 🚀