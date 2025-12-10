# HTML Reporting - Comprehensive Test Reports

Judo Framework incluye un sistema completo de reportes HTML que captura automáticamente todos los detalles de la ejecución de pruebas, incluyendo requests, responses, headers, variables, assertions y más.

## 🎯 Características del Sistema de Reportes

### ✅ **Captura Automática**
- **HTTP Requests/Responses**: Método, URL, headers, parámetros, body
- **Assertions**: Resultados esperados vs actuales
- **Variables**: Asignación y uso de variables
- **Timing**: Tiempo de ejecución de cada paso
- **Errores**: Mensajes de error y stack traces completos

### ✅ **Reporte HTML Interactivo**
- **Navegación colapsible**: Features, scenarios y steps expandibles
- **Syntax highlighting**: JSON y código con colores
- **Responsive design**: Funciona en desktop y móvil
- **Búsqueda visual**: Fácil identificación de errores

### ✅ **Información Detallada**
- **Environment info**: Versión Python, plataforma, configuración
- **Performance metrics**: Tiempos de respuesta y estadísticas
- **Success rates**: Porcentajes de éxito por feature/scenario
- **Request/Response data**: Headers, body, status codes

## 🚀 Uso Básico

### **1. Automático con Behave**

Los reportes se generan automáticamente cuando usas Behave:

```bash
behave features/
```

El reporte HTML se genera automáticamente en `reports/judo_report_YYYYMMDD_HHMMSS.html`

### **2. Programático con DSL**

```python
from judo import Judo

# Crear instancia con reporting habilitado (por defecto)
judo = Judo()
judo.url = "https://api.example.com"

# Iniciar scenario para reporting
judo.start_scenario("Test API Endpoint")

# Ejecutar pasos con captura automática
judo.start_step("Make GET request")
response = judo.get("/users/1")
judo.finish_step(response.status == 200)

judo.start_step("Validate response")
judo.match(response.status, 200)
judo.match(response.json["name"], "##string")
judo.finish_step(True)

judo.finish_scenario(True)

# Generar reporte HTML
report_path = judo.generate_html_report("my_test_report.html")
print(f"Report generated: {report_path}")
```

### **3. Reporter Personalizado**

```python
from judo import JudoReporter, Judo

# Crear reporter personalizado
reporter = JudoReporter("My Custom Test Report")

# Configurar Judo con el reporter
judo = Judo(enable_reporting=True)
judo.reporter = reporter

# Agregar información de entorno
reporter.report_data.environment.update({
    "test_environment": "staging",
    "api_version": "v2.1",
    "test_suite": "integration_tests"
})

# Ejecutar tests...
feature = reporter.start_feature("User API", "Testing user operations")
scenario = reporter.start_scenario("Create user", ["post", "user"])

# ... ejecutar pasos ...

# Generar reporte
report_path = reporter.generate_html_report("custom_report.html")
```

## 📊 Estructura del Reporte HTML

### **1. Header Section**
- Título del reporte
- Fecha y hora de ejecución
- Duración total
- Estado general (PASSED/FAILED)

### **2. Summary Section**
- Número total de features, scenarios, steps
- Breakdown por estado (passed/failed/skipped)
- Porcentaje de éxito
- Métricas de rendimiento

### **3. Features Section**
Cada feature incluye:
- Nombre y descripción
- Tags asociados
- Duración de ejecución
- Lista de scenarios

### **4. Scenarios Section**
Cada scenario incluye:
- Nombre y tags
- Estado (passed/failed/skipped)
- Duración
- Lista de steps (incluyendo background steps)

### **5. Steps Section**
Cada step incluye:
- Texto del step
- Estado y duración
- **Request Details** (si aplica):
  - Método HTTP (GET, POST, etc.)
  - URL completa
  - Headers de request
  - Query parameters
  - Request body (JSON/form/multipart)
- **Response Details** (si aplica):
  - Status code
  - Response headers
  - Response body (JSON/text)
  - Tiempo de respuesta
- **Variables**:
  - Variables utilizadas
  - Variables asignadas
- **Assertions**:
  - Descripción de la assertion
  - Valor esperado vs actual
  - Estado (passed/failed)
- **Errores** (si aplica):
  - Mensaje de error
  - Stack trace completo

## 🎨 Características Visuales

### **Color Coding**
- 🟢 **Verde**: Steps/scenarios/features exitosos
- 🔴 **Rojo**: Fallos y errores
- 🟡 **Amarillo**: Steps omitidos
- 🔵 **Azul**: Información general

### **HTTP Method Colors**
- 🟢 **GET**: Verde
- 🔵 **POST**: Azul
- 🟠 **PUT**: Naranja
- 🟣 **PATCH**: Púrpura
- 🔴 **DELETE**: Rojo

### **Status Code Colors**
- 🟢 **2xx**: Verde (éxito)
- 🔴 **4xx/5xx**: Rojo (error)

## 📁 Ejemplos de Uso

### **Ejemplo 1: Test Básico con Reporte**

```python
from judo import Judo

def test_user_api():
    judo = Judo()
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # Scenario automático
    judo.start_scenario("User API Test")
    
    # Step 1
    judo.start_step("Get user data")
    response = judo.get("/users/1")
    judo.finish_step(response.status == 200)
    
    # Step 2
    judo.start_step("Validate user data")
    judo.match(response.status, 200)
    judo.match(response.json["name"], "##string")
    judo.match(response.json["email"], "##email")
    judo.finish_step(True)
    
    judo.finish_scenario(True)
    
    # Generar reporte
    return judo.generate_html_report()

if __name__ == "__main__":
    report = test_user_api()
    print(f"Report: {report}")
```

### **Ejemplo 2: Test con Datos de Archivo**

```python
from judo import Judo

def test_with_file_data():
    judo = Judo()
    judo.url = "https://api.example.com"
    
    judo.start_scenario("Create User from File")
    
    # Cargar datos desde archivo
    judo.start_step("Load user data from file")
    user_data = judo.read("test_data/user.json")
    judo.set("userData", user_data)
    judo.finish_step(True)
    
    # Crear usuario
    judo.start_step("Create new user")
    response = judo.post("/users", json=user_data)
    judo.finish_step(response.status == 201)
    
    # Validar creación
    judo.start_step("Validate user creation")
    judo.match(response.status, 201)
    judo.match(response.json["name"], user_data["name"])
    judo.finish_step(True)
    
    judo.finish_scenario(True)
    return judo.generate_html_report("file_data_test.html")
```

### **Ejemplo 3: Test con Behave (Automático)**

```gherkin
# features/user_api.feature
Feature: User API Testing
  Scenario: Get user information
    Given I have a Judo API client
    And the base URL is "https://api.example.com"
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And the response should contain "name"
    And the response "$.email" should be a valid email
```

```bash
# Ejecutar con reporte automático
behave features/user_api.feature
# Genera: reports/judo_report_YYYYMMDD_HHMMSS.html
```

## ⚙️ Configuración Avanzada

### **Personalizar Directorio de Reportes**

```python
from judo.reporting import HTMLReporter

# Crear reporter con directorio personalizado
html_reporter = HTMLReporter(output_dir="custom_reports")

# Usar con JudoReporter
reporter = JudoReporter("Custom Report")
reporter.html_reporter = html_reporter
```

### **Agregar Información de Entorno**

```python
reporter = JudoReporter("Production Tests")

# Agregar info de entorno
reporter.report_data.environment.update({
    "environment": "production",
    "api_version": "v2.1",
    "database": "postgresql-prod",
    "test_runner": "jenkins",
    "build_number": "123"
})

# Agregar configuración
reporter.report_data.configuration = {
    "timeout": 30,
    "retries": 3,
    "parallel": True,
    "verify_ssl": True
}
```

### **Deshabilitar Reporting**

```python
# Deshabilitar reporting para performance
judo = Judo(enable_reporting=False)

# O deshabilitar temporalmente
judo.enable_reporting = False
```

## 🎯 Casos de Uso

### **1. Debugging de Tests**
- Ver requests/responses exactos
- Identificar qué assertions fallan
- Revisar variables y su estado
- Analizar timing de requests

### **2. Documentación de API**
- Generar documentación automática
- Mostrar ejemplos de uso
- Validar contratos de API

### **3. Reportes para Stakeholders**
- Reportes ejecutivos con métricas
- Evidencia de testing completo
- Análisis de cobertura

### **4. CI/CD Integration**
- Reportes automáticos en pipelines
- Archivos HTML como artifacts
- Métricas de calidad

## 📈 Métricas Incluidas

- **Execution Time**: Tiempo total y por step
- **Success Rate**: Porcentaje de éxito
- **Response Times**: Tiempos de respuesta de API
- **Request Count**: Número de requests por método
- **Error Rate**: Porcentaje de errores
- **Coverage**: Cobertura de endpoints

## 🌐 Visualización

Los reportes HTML son completamente interactivos:

- **Collapsible Sections**: Click para expandir/colapsar
- **Syntax Highlighting**: JSON y código con colores
- **Responsive Design**: Funciona en móvil y desktop
- **Search Friendly**: Fácil navegación y búsqueda
- **Print Friendly**: Optimizado para impresión

¡El sistema de reportes de Judo Framework proporciona la visibilidad completa que necesitas para tus tests de API! 🎉