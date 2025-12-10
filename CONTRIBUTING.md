# Contributing to Judo Framework

First off, thank you for considering contributing to Judo Framework! 🥋

It's people like you that make Judo Framework such a great tool for the API testing community.

## 🌟 Ways to Contribute

There are many ways to contribute to Judo Framework:

- 🐛 **Report bugs** - Help us identify and fix issues
- ✨ **Suggest features** - Share your ideas for improvements
- 📝 **Improve documentation** - Help others understand and use Judo
- 🌍 **Add translations** - Make Judo accessible in more languages
- 🧪 **Write tests** - Improve code quality and coverage
- 💻 **Submit code** - Fix bugs or implement new features
- 🎨 **Improve UI** - Enhance the HTML reports design
- 📚 **Create examples** - Show others how to use Judo effectively

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/judo.git
cd judo
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install development dependencies
pip install -e .[dev]
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Development Guidelines

### Code Style

We follow PEP 8 with some modifications:

```bash
# Format code with Black
black judo/

# Check linting with flake8
flake8 judo/

# Type checking with mypy
mypy judo/
```

### Writing Tests

All new features should include tests:

```python
# tests/test_your_feature.py
import pytest
from judo import Judo

def test_your_feature():
    """Test description"""
    judo = Judo()
    # Your test code here
    assert result == expected
```

Run tests:
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_your_feature.py

# Run with coverage
pytest --cov=judo tests/
```

### Documentation

- Update docstrings for all public functions
- Add examples in docstrings
- Update README.md if adding major features
- Add entries to CHANGELOG.md

Example docstring:
```python
def your_function(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Example:
        >>> your_function("test", 42)
        True
    """
    # Implementation
```

## 🐛 Reporting Bugs

### Before Submitting

1. Check if the bug has already been reported in [Issues](https://github.com/judo-framework/judo/issues)
2. Try to reproduce with the latest version
3. Collect relevant information

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python version: [e.g., 3.9.7]
- Judo version: [e.g., 1.2.1]

**Additional context**
Any other relevant information.

**Code sample**
```python
# Minimal code to reproduce the issue
```
```

## ✨ Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Any other relevant information.

**Example usage**
```python
# How you envision using this feature
```
```

## 💻 Submitting Code

### Pull Request Process

1. **Update your fork**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow the code style guidelines
   - Add tests for new features
   - Update documentation

3. **Test your changes**
   ```bash
   pytest tests/
   flake8 judo/
   black judo/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   **Commit message format:**
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes (formatting, etc.)
   - `refactor:` Code refactoring
   - `test:` Adding or updating tests
   - `chore:` Maintenance tasks

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

### Pull Request Template

```markdown
**Description**
Brief description of changes.

**Type of change**
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

**How Has This Been Tested?**
Describe the tests you ran.

**Checklist:**
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
- [ ] I have updated CHANGELOG.md
```

## 🌍 Adding Translations

We welcome translations to make Judo accessible worldwide!

### Adding a New Language

1. **Create step definitions file**
   ```bash
   # Example for French
   touch judo/behave/steps_fr.py
   ```

2. **Translate steps**
   ```python
   # judo/behave/steps_fr.py
   from behave import given, when, then
   
   @given('que l\'URL de base est "{url}"')
   def step_url_base_fr(context, url):
       # Implementation
   ```

3. **Update imports**
   ```python
   # judo/behave/__init__.py
   from . import steps_fr  # Add this line
   ```

4. **Add documentation**
   - Create `docs/getting-started_FR.md`
   - Update README.md with French link

5. **Add examples**
   - Create example feature files in French
   - Add to `examples/` directory

## 📚 Documentation

### Documentation Structure

```
docs/
├── getting-started.md       # English
├── getting-started_ES.md    # Spanish
├── getting-started_FR.md    # French (example)
├── dsl-reference.md
├── behave-integration.md
└── ...
```

### Writing Documentation

- Use clear, simple language
- Include code examples
- Add screenshots where helpful
- Keep formatting consistent
- Test all code examples

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── test_core/
│   ├── test_judo.py
│   ├── test_matcher.py
│   └── test_response.py
├── test_behave/
│   ├── test_steps.py
│   ├── test_steps_es.py
│   └── test_context.py
├── test_http/
│   └── test_client.py
└── test_reporting/
    ├── test_reporter.py
    └── test_html_reporter.py
```

### Writing Good Tests

```python
def test_feature_name():
    """
    Test should:
    1. Have a clear name
    2. Test one thing
    3. Be independent
    4. Be repeatable
    5. Be fast
    """
    # Arrange
    judo = Judo()
    
    # Act
    result = judo.some_method()
    
    # Assert
    assert result == expected
```

## 🎨 UI/UX Contributions

### HTML Reports

The HTML reports are generated from templates in `judo/reporting/`.

To improve the UI:

1. Edit `judo/reporting/html_reporter.py`
2. Update CSS/JavaScript inline or in templates
3. Test with various scenarios
4. Ensure responsive design
5. Check browser compatibility

## 📊 Performance Considerations

- Profile code before optimizing
- Use appropriate data structures
- Avoid unnecessary computations
- Cache when appropriate
- Consider memory usage

## 🔒 Security

- Never commit sensitive data
- Use environment variables for secrets
- Validate all inputs
- Follow security best practices
- Report security issues privately

## 📞 Getting Help

- 💬 [GitHub Discussions](https://github.com/judo-framework/judo/discussions)
- 📧 Email: felipe.farias@centyc.cl
- 🐛 [Issues](https://github.com/judo-framework/judo/issues)

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

**Positive behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behavior:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation
- Part of the Judo community

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Thank You! 🙏

Your contributions make Judo Framework better for everyone. We appreciate your time and effort!

**Made with ❤️ by the Judo Framework community**
