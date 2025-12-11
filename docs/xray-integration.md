# 🎯 Xray Integration Guide

Judo Framework automatically generates Cucumber JSON reports that can be imported directly into Jira Xray for test management and reporting.

## 📋 Overview

When you run tests with Judo's `BaseRunner`, it automatically generates:
- Individual JSON files per feature execution
- A consolidated JSON file with all results
- Compatible with Xray's Cucumber JSON import format

## 🚀 Quick Start

### 1. Run Your Tests

```python
from judo.runner.base_runner import BaseRunner

runner = BaseRunner(
    features_dir="features",
    output_dir="judo_reports",
    generate_cucumber_json=True  # Enabled by default
)

results = runner.run(tags=["@api"])
```

### 2. Generated Files

After execution, you'll find:

```
judo_reports/
├── cucumber-json/
│   ├── feature1_20241210_120000.json
│   ├── feature2_20241210_120001.json
│   └── cucumber-consolidated.json  ← Upload this to Xray
├── test_execution_report.html
└── ...
```

## 📤 Uploading to Xray

### Option 1: Manual Upload via Jira UI

1. Go to your Jira project
2. Navigate to **Xray** → **Import Execution Results**
3. Select **Cucumber JSON** as format
4. Upload `cucumber-consolidated.json`
5. Map to your Test Execution (or create new one)

### Option 2: Xray REST API

```python
import requests

# Xray Cloud
url = "https://xray.cloud.getxray.app/api/v2/import/execution/cucumber"
headers = {
    "Authorization": f"Bearer {xray_token}",
    "Content-Type": "application/json"
}

with open("judo_reports/cucumber-json/cucumber-consolidated.json", "rb") as f:
    response = requests.post(url, headers=headers, files={"file": f})
    
print(f"Test Execution Key: {response.json()['key']}")
```

### Option 3: Xray Server/Data Center

```python
import requests

url = "https://your-jira.com/rest/raven/2.0/import/execution/cucumber"
auth = ("username", "password")

with open("judo_reports/cucumber-json/cucumber-consolidated.json", "rb") as f:
    response = requests.post(url, auth=auth, files={"file": f})
    
print(f"Test Execution Key: {response.json()['testExecIssue']['key']}")
```

## 🏷️ Mapping Tests to Xray

### Using Tags

Tag your scenarios with Xray test keys:

```gherkin
@TEST-123
Scenario: User login
  Given the base URL is "https://api.example.com"
  When I send a POST request to "/login" with JSON:
    """
    {"username": "user", "password": "pass"}
    """
  Then the response status should be 200
```

Xray will automatically link results to `TEST-123`.

### Using Scenario Names

If you don't use tags, Xray will match by scenario name:

```gherkin
Scenario: TEST-123 User login
  # Xray will match this to TEST-123
```

## 🔧 Advanced Configuration

### Custom JSON Directory

```python
runner = BaseRunner(
    features_dir="features",
    cucumber_json_dir="xray-reports"  # Custom directory
)
```

### Disable Cucumber JSON

```python
runner = BaseRunner(
    features_dir="features",
    generate_cucumber_json=False  # Disable if not needed
)
```

### Manual Consolidation

```python
# Run tests
runner.run(tags=["@smoke"])

# Manually consolidate later
consolidated_path = runner.consolidate_cucumber_json("my-report.json")
print(f"Consolidated JSON: {consolidated_path}")
```

## 📊 JSON Format Example

```json
[
  {
    "id": "user-login",
    "name": "User Authentication",
    "description": "Test user login functionality",
    "keyword": "Feature",
    "uri": "features/auth.feature",
    "tags": [
      {
        "name": "@TEST-123",
        "line": 1
      }
    ],
    "elements": [
      {
        "id": "user-login;successful-login",
        "name": "Successful login",
        "keyword": "Scenario",
        "type": "scenario",
        "tags": [
          {
            "name": "@TEST-123",
            "line": 3
          }
        ],
        "steps": [
          {
            "keyword": "Given ",
            "name": "the base URL is \"https://api.example.com\"",
            "line": 5,
            "result": {
              "status": "passed",
              "duration": 123456789
            }
          }
        ]
      }
    ]
  }
]
```

## 🎯 Best Practices

### 1. Use Consistent Tags

```gherkin
@TEST-123 @api @smoke
Scenario: Critical API test
```

### 2. One Feature = One Test Set

Organize features by test sets in Xray:

```
features/
├── auth/          # TEST-SET-1
│   └── login.feature
├── users/         # TEST-SET-2
│   └── crud.feature
```

### 3. Include Test Plan Tags

```gherkin
@TESTPLAN-456 @TEST-123
Scenario: Part of sprint test plan
```

### 4. Use Descriptive Names

```gherkin
# Good
Scenario: TEST-123 User can login with valid credentials

# Avoid
Scenario: Test 1
```

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
name: API Tests

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run Judo Tests
        run: |
          pip install judo-framework
          python runner.py
      
      - name: Upload to Xray
        env:
          XRAY_TOKEN: ${{ secrets.XRAY_TOKEN }}
        run: |
          curl -X POST \
            -H "Authorization: Bearer $XRAY_TOKEN" \
            -F "file=@judo_reports/cucumber-json/cucumber-consolidated.json" \
            https://xray.cloud.getxray.app/api/v2/import/execution/cucumber
```

### Jenkins

```groovy
pipeline {
    agent any
    
    stages {
        stage('Test') {
            steps {
                sh 'python runner.py'
            }
        }
        
        stage('Upload to Xray') {
            steps {
                script {
                    def response = sh(
                        script: """
                            curl -X POST \
                              -H "Authorization: Bearer ${XRAY_TOKEN}" \
                              -F "file=@judo_reports/cucumber-json/cucumber-consolidated.json" \
                              https://xray.cloud.getxray.app/api/v2/import/execution/cucumber
                        """,
                        returnStdout: true
                    )
                    echo "Test Execution: ${response}"
                }
            }
        }
    }
}
```

## 📚 Additional Resources

- [Xray Cucumber Integration](https://docs.getxray.app/display/XRAY/Cucumber+JSON+results+import)
- [Xray REST API](https://docs.getxray.app/display/XRAY/Import+Execution+Results+-+REST)
- [Cucumber JSON Format](https://github.com/cucumber/cucumber-json-schema)

## 🆘 Troubleshooting

### Issue: Tests not linking to Xray

**Solution**: Ensure tags match exactly:
```gherkin
@TEST-123  # Correct
@test-123  # Wrong - case sensitive
```

### Issue: Duplicate test executions

**Solution**: Use unique Test Execution keys or let Xray create new ones.

### Issue: JSON format error

**Solution**: Validate JSON format:
```bash
python -m json.tool cucumber-consolidated.json
```

## 💡 Tips

1. **Run tests before important meetings** - Have fresh results in Xray
2. **Tag by priority** - `@critical`, `@high`, `@medium`, `@low`
3. **Use test plans** - Group related tests with `@TESTPLAN-XXX`
4. **Archive old JSONs** - Keep history for trend analysis
5. **Automate uploads** - Integrate with CI/CD for continuous reporting

---

**Made with ❤️ by Judo Framework**
