# Test Data Files

This directory contains sample data files used by the Judo Framework examples.

## 📁 Files

### JSON Request Data

**`simple_post.json`**
```json
{
  "title": "Simple Post from File",
  "body": "This is a simple post created from a JSON file",
  "userId": 1
}
```
Used for: POST and PATCH requests

**`update_post.json`**
```json
{
  "id": 1,
  "title": "Updated Post Title", 
  "body": "This post was updated using data from a file",
  "userId": 1
}
```
Used for: PUT requests (complete updates)

### Schema Files

**`simple_schema.json`**
JSON Schema for validating post responses:
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "number"},
    "title": {"type": "string"},
    "body": {"type": "string"},
    "userId": {"type": "number"}
  },
  "required": ["id", "title", "body", "userId"]
}
```

### Complex Examples (Advanced)

**`create_post.json`** - More detailed post data
**`update_user.json`** - Complete user update data
**`user_schema.json`** - Full user schema validation
**`expected_user.json`** - Expected user response data
**`multiple_posts.json`** - Array of posts for batch operations
**`config.yaml`** - YAML configuration example

## 🚀 How to Use

### In English Features
```gherkin
# POST with JSON file
When I POST to "/posts" with JSON file "examples/test_data/simple_post.json"

# Validate against schema
And the response should match schema file "examples/test_data/simple_schema.json"
```

### In Spanish Features
```gherkin
# POST con archivo JSON
Cuando hago una petición POST a "/posts" con archivo JSON "examples/test_data/simple_post.json"

# Validar contra esquema
Y la respuesta debe coincidir con el esquema del archivo "examples/test_data/simple_schema.json"
```

## 📝 Creating Your Own Files

### 1. JSON Request Data
Create `.json` files with the data you want to send:
```json
{
  "field1": "value1",
  "field2": "value2"
}
```

### 2. JSON Schema Files
Create schema files to validate responses:
```json
{
  "type": "object",
  "properties": {
    "field1": {"type": "string"},
    "field2": {"type": "number"}
  },
  "required": ["field1"]
}
```

### 3. Expected Response Files
Save expected responses for exact matching:
```json
{
  "id": 1,
  "status": "success",
  "data": {...}
}
```

## 🎯 Best Practices

### File Organization
```
test_data/
├── requests/          # Request data
│   ├── create_user.json
│   └── update_user.json
├── schemas/           # Validation schemas
│   ├── user_schema.json
│   └── post_schema.json
└── expected/          # Expected responses
    ├── user_response.json
    └── post_response.json
```

### Naming Conventions
- **Requests**: `create_*.json`, `update_*.json`
- **Schemas**: `*_schema.json`
- **Expected**: `expected_*.json`

### File Paths
Always use relative paths from the project root:
```gherkin
"examples/test_data/simple_post.json"
```

## 🔧 Tips

### 1. Keep Files Simple
Start with simple JSON structures and add complexity as needed.

### 2. Use Descriptive Names
File names should clearly indicate their purpose:
- `create_user.json` ✅
- `data.json` ❌

### 3. Validate Your JSON
Ensure your JSON files are valid before using them:
```bash
# Check JSON validity
python -m json.tool examples/test_data/simple_post.json
```

### 4. Version Control
Include test data files in version control so all team members have the same data.

### 5. Environment-Specific Data
Create different data files for different environments:
- `user_dev.json`
- `user_staging.json`
- `user_prod.json`

## 📚 Related Examples

See these scenarios in the showcase files:
- `@files` tagged scenarios in `complete_showcase.feature`
- `@archivos` tagged scenarios in `showcase_completo.feature`

## 💡 Advanced Usage

### Dynamic File Paths
Use variables in file paths:
```gherkin
Given I set the variable "env" to "dev"
When I POST to "/users" with JSON file "examples/test_data/user_{env}.json"
```

### File Validation
Validate files before using them:
```gherkin
Given I load test data "userData" from file "examples/test_data/user.json"
# The file is automatically validated when loaded
```

## 🌐 More Information

**📖 Official Documentation**: [http://centyc.cl/judo-framework/](http://centyc.cl/judo-framework/)

---

**Made with ❤️ at CENTYC for API testing excellence** 🥋