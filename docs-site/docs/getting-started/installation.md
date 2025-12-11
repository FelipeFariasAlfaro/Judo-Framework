# Installation

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## Install from PyPI

The easiest way to install Judo Framework is using pip:

```bash
pip install judo-framework
```

This will install Judo Framework and all its dependencies.

## Verify Installation

Check that Judo Framework is installed correctly:

```bash
python -c "import judo; print(judo.__version__)"
```

You should see the version number printed.

## Install Specific Version

To install a specific version:

```bash
pip install judo-framework==1.2.11
```

## Upgrade to Latest Version

To upgrade to the latest version:

```bash
pip install --upgrade judo-framework
```

## Install from Source

If you want to install from source (for development):

```bash
git clone https://github.com/FelipeFariasAlfaro/Judo-Framework.git
cd Judo-Framework
pip install -e .
```

## Dependencies

Judo Framework automatically installs these dependencies:

- `requests` - HTTP client
- `behave` - BDD framework
- `jsonpath-ng` - JSON path expressions
- `pyyaml` - YAML support
- `jsonschema` - Schema validation
- `jinja2` - Template engine

## Optional Dependencies

For additional features, install optional dependencies:

### Cryptography Support

```bash
pip install judo-framework[crypto]
```

### XML Support

```bash
pip install judo-framework[xml]
```

### Browser Automation

```bash
pip install judo-framework[browser]
```

### All Features

```bash
pip install judo-framework[full]
```

## Virtual Environment (Recommended)

It's recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install Judo Framework
pip install judo-framework
```

## Troubleshooting

### Permission Errors

If you get permission errors, try:

```bash
pip install --user judo-framework
```

### SSL Certificate Errors

If you have SSL certificate issues:

```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org judo-framework
```

### Behind a Proxy

If you're behind a proxy:

```bash
pip install --proxy http://user:password@proxy:port judo-framework
```

## Next Steps

Now that you have Judo Framework installed, let's create your first test!

[Quick Start →](quick-start.md){ .md-button .md-button--primary }
