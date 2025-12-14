<div align="center">
  <img src="../assets/judo-framework-logo.png" alt="Judo Framework Logo" width="300"/>
</div>

# 🎯 Judo Framework Examples

This directory contains essential examples demonstrating Judo Framework capabilities.

## 📁 Files Overview

### 🎪 Complete Showcases
- **`complete_showcase.feature`** - Comprehensive English examples with 30+ scenarios
- **`showcase_completo.feature`** - Comprehensive Spanish examples with 30+ scenarios

These files demonstrate ALL Judo Framework features with detailed explanations.

### 💾 Request/Response Logging Examples
- **`logging_demo.feature`** - English demo of automatic request/response logging
- **`demo_logging_es.feature`** - Spanish demo of automatic request/response logging
- **`request_response_logging_example.py`** - Python configuration examples

### 🔐 Environment Variables Examples (.env)
- **`env_variables_example.feature`** - English examples using .env files
- **`env_variables_ejemplo_es.feature`** - Spanish examples using .env files
- **`.env.example`** - Template for environment variables configuration

### 📊 Test Data
- **`test_data/`** - Directory with sample JSON files and schemas
- **`output/`** - Directory for generated output files

## 🚀 Quick Start

### Run Complete Showcase
```bash
# English version
behave examples/complete_showcase.feature

# Spanish version  
behave examples/showcase_completo.feature
```

### Run with Tags
```bash
# Run only HTTP method examples
behave examples/complete_showcase.feature --tags=@http

# Run only file operation examples
behave examples/complete_showcase.feature --tags=@files

# Run environment variables examples
behave examples/complete_showcase.feature --tags=@env

# Run logging demos
behave examples/logging_demo.feature --tags=@demo
```

### Test Environment Variables Features
```bash
# 1. Copy the example .env file
cp examples/.env.example examples/.env

# 2. Edit examples/.env with your values (optional for showcase)
# The showcase works with the default example values

# 3. Run environment variable scenarios
behave examples/complete_showcase.feature --tags=@env

# Spanish version
behave examples/showcase_completo.feature --tags=@env
```

### Enable Request/Response Logging
```bash
# Set environment variables
export JUDO_SAVE_REQUESTS_RESPONSES=true
export JUDO_OUTPUT_DIRECTORY=api_logs

# Run examples with logging
behave examples/logging_demo.feature
```

## 📚 What You'll Learn

### From Complete Showcase Files
- ✅ All HTTP methods (GET, POST, PUT, PATCH, DELETE)
- ✅ Query parameters and headers
- ✅ Variables and data extraction
- ✅ Response validation techniques
- ✅ Array operations and validation
- ✅ Authentication workflows
- ✅ File operations (JSON, schema validation)
- ✅ Error handling
- ✅ Performance testing
- ✅ Complete CRUD workflows

### From Logging Examples
- ✅ How to enable/disable request/response logging
- ✅ Configuration options (environment variables, runner, feature files)
- ✅ File organization and naming conventions
- ✅ Debugging failed tests with logged data
- ✅ Using logs for API documentation

### From Environment Variables Examples
- ✅ How to use .env files for sensitive data
- ✅ Loading API tokens and keys from environment
- ✅ Setting headers from environment variables
- ✅ Managing different environments (dev, staging, prod)
- ✅ Keeping secrets out of version control

## 🎓 Learning Path

### 1. Beginners
Start with these scenarios:
```bash
behave examples/complete_showcase.feature --tags=@http
```

### 2. Intermediate
```bash
behave examples/complete_showcase.feature --tags=@variables,@validation
```

### 3. Advanced
```bash
behave examples/complete_showcase.feature --tags=@workflow,@complex
```

## 🔧 Configuration Examples

### Python Runner with Logging
```python
from judo.runner.base_runner import BaseRunner

runner = BaseRunner(
    features_dir="examples",
    save_requests_responses=True,
    requests_responses_dir="my_api_logs"
)

results = runner.run(tags=["@demo"])
```

### Environment Variables
```bash
export JUDO_SAVE_REQUESTS_RESPONSES=true
export JUDO_OUTPUT_DIRECTORY=custom_logs
export JUDO_LOG_SAVED_FILES=true
```

## 📖 Documentation

### 🌐 Official Documentation
**Complete documentation: [http://centyc.cl/judo-framework/](http://centyc.cl/judo-framework/)**

### 📚 Local Documentation
- [Request/Response Logging](../docs/request-response-logging.md)
- [Test Data Guide](test_data/README.md)
- [Main README](../README.md)

## 💡 Tips

1. **Use tags** to run specific types of examples
2. **Enable logging** to see request/response details
3. **Check test_data/** for sample files
4. **Read comments** in feature files for explanations
5. **Start simple** and gradually try more complex scenarios

---

**Made with ❤️ at CENTYC for API testing excellence** 🥋