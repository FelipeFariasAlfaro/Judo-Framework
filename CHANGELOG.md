# Changelog

All notable changes to Judo Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.11] - 2024-12-11

### Added
- 🎨 Nuevo parámetro `console_format` en BaseRunner para controlar el formato de salida
- 📝 Opciones disponibles: 'progress', 'progress2', 'pretty', 'plain', 'none'

### Changed
- 🔧 Formato de consola por defecto cambiado de 'pretty' a 'progress'
- 📊 Salida más limpia y fácil de leer durante la ejecución de tests
- ✅ Formato 'progress' muestra solo puntos (.) por cada scenario exitoso
- ❌ Formato 'pretty' (anterior default) mostraba todos los detalles de cada step

## [1.2.10] - 2024-12-11

### Fixed
- 🐛 **Fixed duplicate report generation**: Reports are now generated only in the configured `output_dir`
- 📁 Previously, reports were created in both the custom directory AND the default `judo_reports` directory
- 🔧 Fixed global reporter initialization to respect the output directory from BaseRunner
- ✅ Now changing `output_dir` parameter correctly generates reports only in the specified location

## [1.2.9] - 2024-12-10

### Changed
- 📝 Updated repository URLs to official GitHub repository
- 🔗 Updated all documentation links to point to https://github.com/FelipeFariasAlfaro/Judo-Framework
- 📦 Updated package metadata with correct repository information

## [1.2.9] - 2024-12-10

### Added
- ✨ **New step for nested arrays**: Search items in nested arrays
- 🔍 English: `Then the response array "users" should contain an item with "name" equal to "John Doe"`
- 🇪🇸 Spanish: `Entonces el array "usuarios" debe contener un elemento con "nombre" igual a "Juan"`
- 📊 Supports dot notation for deep nesting: `data.users.active`
- 🥒 **Cucumber JSON export**: Automatic generation of Cucumber-compatible JSON reports
- 📦 **JSON consolidation**: Merge all feature JSONs into a single file for Xray/Allure
- 🎯 **Xray integration ready**: Export results directly to Jira Xray

### Cucumber JSON Features
- Automatic generation in `cucumber-json/` directory
- Individual JSON per feature execution
- Consolidated JSON file for easy upload to Xray
- Compatible with Cucumber HTML Reporter, Allure, and other tools
- Can be disabled with `generate_cucumber_json=False`

### Example
```python
# Enable Cucumber JSON (enabled by default)
runner = BaseRunner(
    features_dir="features",
    output_dir="judo_reports",
    generate_cucumber_json=True,  # Default: True
    cucumber_json_dir="custom/path"  # Optional: custom directory
)

# Run tests
runner.run(tags=["@api"])

# Files generated:
# - judo_reports/cucumber-json/feature1_20241210_120000.json
# - judo_reports/cucumber-json/feature2_20241210_120001.json
# - judo_reports/cucumber-json/cucumber-consolidated.json (all features)
```

## [1.2.8] - 2024-12-10

### Fixed
- 🔧 **Critical variable interpolation fix**: Variables now properly replaced in JSON request bodies
- 📝 Fixed `{variable}` syntax not working in POST/PUT/PATCH JSON bodies
- 🌐 Added variable interpolation to all HTTP request endpoints
- 🔑 Added variable interpolation to headers, query parameters, and auth tokens
- 🇪🇸 Applied same fixes to Spanish steps

### Changed
- All HTTP request steps now support `{variableName}` syntax in endpoints
- Headers and query parameters now support variable interpolation
- Bearer tokens now support variable interpolation
- Consistent variable handling across English and Spanish steps

### Example
```gherkin
Given I set the variable "userId" to "123"
When I send a GET request to "/users/{userId}"
And I set the header "X-User-Id" to "{userId}"
```

## [1.2.7] - 2024-12-10

### Fixed
- 🎯 **Critical tag filtering fix**: BaseRunner now correctly passes tags to Behave command
- 🏷️ Fixed issue where all scenarios were executed even when specific tags were requested
- 📋 Tags are now properly filtered at execution time, not just at feature discovery

### Changed
- Added `current_tags` and `current_exclude_tags` attributes to BaseRunner
- Modified `run_behave_command` to include `--tags` arguments in the Behave command
- Improved tag handling throughout the execution pipeline

## [1.2.6] - 2024-12-10

### Fixed
- 🔍 **JSON validation fix**: Improved `is_json()` method to properly detect JSON responses
- 📝 Fixed "response should be valid JSON" step that was incorrectly failing
- 🎯 Better JSON detection by attempting to parse response when content-type is ambiguous

### Changed
- Enhanced `JudoResponse.is_json()` to try parsing JSON if content-type header is missing or unclear
- Added support for `application/javascript` content-type

## [1.2.5] - 2024-12-10

### Fixed
- 🖥️ **Output visibility fix**: BaseRunner now shows Behave output in real-time when verbose mode is enabled
- 📺 Fixed issue where STDOUT was captured but not displayed during test execution
- 🔧 Improved subprocess handling to show test execution progress
- 🎯 **Critical fix**: Skip non-executed scenarios when processing Behave JSON output
- 📊 Fixed error when running features with multiple scenarios but only executing some via tags

### Changed
- Modified `run_behave_command` to use `capture_output=False` in verbose mode
- Better console output for test execution monitoring
- Enhanced error message display
- Added validation to only process scenarios that were actually executed
- Improved step result validation before processing

## [1.2.4] - 2024-12-10

### Fixed
- 🐛 **Critical fix**: Resolved `'str' object has no attribute 'get'` error in BaseRunner
- 🏷️ Fixed tag processing to handle both dict and string formats from Behave JSON output
- 📊 Improved feature and scenario data processing in custom runners

### Changed
- Enhanced tag handling in `_process_feature_data` method
- Better error handling for different tag formats

## [1.2.3] - 2024-12-10

### Fixed
- 🔧 Fixed pyproject.toml configuration warnings
- 📦 Improved package build process
- 🛠️ Enhanced setuptools compatibility

### Changed
- Updated build configuration for better compatibility
- Improved package metadata

## [1.2.2] - 2024-12-10

### Fixed
- Minor bug fixes and improvements

## [1.2.1] - 2024-12-10

### Added
- 🇪🇸 **Full Spanish language support** for all Behave steps
- New file `judo/behave/steps_es.py` with complete Spanish step definitions
- Spanish examples in `examples/EJEMPLO_POST.feature`
- Support for bilingual projects (English and Spanish in same project)

### Changed
- Updated `judo/behave/__init__.py` to automatically load Spanish steps
- Enhanced README with comprehensive examples and documentation
- Improved project structure and organization

### Features
- All HTTP methods in Spanish (GET, POST, PUT, PATCH, DELETE)
- Spanish validation steps
- Spanish data extraction and variable management
- Spanish authentication steps
- Natural language syntax in Spanish

## [1.2.0] - 2024-12-10

### Added
- ✨ **Automatic report generation** with zero configuration
- 🎯 **Ultra-simple setup** - Only 10 lines in environment.py
- 📊 **Auto-hooks system** for automatic test tracking
- New file `judo/behave/auto_hooks.py` with pre-configured hooks
- Automatic capture of features, scenarios, and steps
- Detailed HTML reports with full test execution data

### Changed
- Simplified environment.py setup from 100+ lines to just 10 lines
- Improved user experience - "as simple as Karate"
- Enhanced reporting system with automatic data capture

### Fixed
- Report generation now works automatically without manual configuration
- Fixed issue where reports showed 0 features/scenarios/steps

## [1.1.1] - 2024-12-10

### Added
- Behave formatter for automatic report generation
- New file `judo/behave/formatter.py`
- Entry point registration for Behave formatters

### Changed
- Improved formatter callbacks for better data capture
- Enhanced step tracking and status reporting

## [1.1.0] - 2024-12-10

### Added
- Automatic Behave formatter integration
- Simplified configuration with behave.ini support
- Format option: `format = judo` in behave.ini

### Changed
- Reduced configuration complexity
- Improved formatter event handling

## [1.0.9] - 2024-12-10

### Added
- Enhanced environment.py with full reporting hooks
- Detailed step-by-step data capture
- Error tracking with stack traces

### Changed
- Improved report data structure
- Better scenario and feature tracking

## [1.0.8] - 2024-12-10

### Added
- Cross-platform support (Windows, macOS, Linux)
- Improved JSON data capture from Behave
- Robust temporary file handling

### Fixed
- File permission issues on different platforms
- JSON data parsing improvements

## [1.0.7] - 2024-12-10

### Added
- HTML reporting system
- Report data models and structures
- Automatic report generation

### Changed
- Enhanced reporting capabilities
- Improved data collection

## [1.0.6] - 2024-12-09

### Added
- Parallel test execution support
- Custom test runners
- Performance improvements

## [1.0.5] - 2024-12-09

### Added
- Behave integration
- Predefined Gherkin steps
- BDD testing support

## [1.0.0] - 2024-12-08

### Added
- Initial release
- Core Judo DSL
- HTTP client
- Basic matching capabilities
- File loading support (JSON, YAML, CSV)
- Mock server
- Schema validation
- Authentication support (Bearer, Basic)

---

## Version Comparison

| Version | Key Feature | Status |
|---------|-------------|--------|
| 1.2.1 | 🇪🇸 Spanish Support | Current |
| 1.2.0 | ✨ Auto Reports (10 lines setup) | Stable |
| 1.1.1 | 🔧 Behave Formatter | Stable |
| 1.1.0 | 📝 Simplified Config | Stable |
| 1.0.9 | 📊 Enhanced Reporting | Stable |
| 1.0.8 | 🌍 Cross-platform | Stable |
| 1.0.7 | 📄 HTML Reports | Stable |
| 1.0.0 | 🚀 Initial Release | Stable |

---

## Upgrade Guide

### From 1.2.0 to 1.2.1

No breaking changes. Spanish steps are automatically available.

**To use Spanish:**
```gherkin
# language: es
Característica: Mi Feature

  Escenario: Mi Escenario
    Dado que la URL base es "https://api.example.com"
    Cuando hago una petición GET a "/users"
    Entonces el código de respuesta debe ser 200
```

### From 1.1.x to 1.2.0

**Old way (1.1.x):**
```python
# environment.py - 100+ lines with manual hooks
from judo.behave import setup_judo_context
from judo.reporting.reporter import get_reporter
# ... many more lines
```

**New way (1.2.0+):**
```python
# environment.py - Just 10 lines!
from judo.behave import *

before_all = before_all_judo
before_feature = before_feature_judo
after_feature = after_feature_judo
before_scenario = before_scenario_judo
after_scenario = after_scenario_judo
before_step = before_step_judo
after_step = after_step_judo
after_all = after_all_judo
```

### From 1.0.x to 1.1.x

Update your environment.py to use the new simplified setup.

---

## Roadmap

### Planned for 1.3.0
- [ ] GraphQL support
- [ ] WebSocket testing
- [ ] Database assertions
- [ ] More language support (Portuguese, French)
- [ ] VS Code extension
- [ ] CI/CD integration templates

### Planned for 1.4.0
- [ ] Performance testing capabilities
- [ ] Load testing integration
- [ ] Advanced mocking scenarios
- [ ] Contract testing support

### Planned for 2.0.0
- [ ] Plugin system
- [ ] Custom reporters
- [ ] Advanced parallel execution
- [ ] Distributed testing

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## License

MIT License - See [LICENSE](LICENSE) for details.
