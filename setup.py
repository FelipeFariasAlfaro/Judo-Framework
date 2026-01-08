from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="judo-framework",
    version="1.5.9.5",
    author="Felipe Farias - CENTYC",
    author_email="felipe.farias@centyc.cl",
    description="A comprehensive API testing framework for Python, inspired by Karate Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FelipeFariasAlfaro/Judo-Framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "jsonpath-ng>=1.5.3",
        "pyyaml>=6.0",
        "jsonschema>=4.17.0",
        "faker>=18.0.0",
        "pytest>=7.0.0",
        "behave>=1.2.6",
        "jinja2>=3.1.0",
        "websocket-client>=1.5.0",
        "beautifulsoup4>=4.12.0",
        "python-dotenv>=1.0.0",
        "PyJWT>=2.6.0",
    ],
    extras_require={
        "dev": [
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "crypto": [
            "cryptography>=40.0.0",
        ],
        "xml": [
            "lxml>=4.9.0",
        ],
        "excel": [
            "openpyxl>=3.0.0",
        ],
        "websocket": [
            "websockets>=10.0",
        ],
        "graphql": [
            "graphql-core>=3.2.0",
        ],
        "full": [
            "cryptography>=40.0.0",
            "lxml>=4.9.0",
            "openpyxl>=3.0.0",
            "websockets>=10.0",
            "graphql-core>=3.2.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "judo=judo.cli:main",
        ],
        "behave.formatters": [
            "judo = judo.behave.formatter:JudoFormatter",
        ],
    },
)