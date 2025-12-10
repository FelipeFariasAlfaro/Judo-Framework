"""
Command Line Interface for Judo Framework
"""

import argparse
import sys
import os
from typing import List


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Judo Framework - API Testing Framework for Python',
        prog='judo'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run test files')
    run_parser.add_argument('files', nargs='*', help='Test files to run')
    run_parser.add_argument('--env', '-e', help='Environment to use')
    run_parser.add_argument('--parallel', '-p', action='store_true', help='Run tests in parallel')
    run_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize new Judo project')
    init_parser.add_argument('name', help='Project name')
    
    # Mock command
    mock_parser = subparsers.add_parser('mock', help='Start mock server')
    mock_parser.add_argument('--port', '-p', type=int, default=8080, help='Port to run on')
    mock_parser.add_argument('--config', '-c', help='Mock configuration file')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Show version')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        run_tests(args.files, args.env, args.parallel, args.verbose)
    elif args.command == 'init':
        init_project(args.name)
    elif args.command == 'mock':
        start_mock_server(args.port, args.config)
    elif args.command == 'version':
        show_version()
    else:
        parser.print_help()


def run_tests(files: List[str], env: str, parallel: bool, verbose: bool):
    """Run test files"""
    print("Running Judo tests...")
    
    if not files:
        # Find all test files
        files = find_test_files()
    
    if env:
        os.environ['KARATE_ENV'] = env
    
    print(f"Found {len(files)} test files")
    
    for file in files:
        print(f"Running: {file}")
        # Here you would implement the test runner
        # For now, just print the file name


def find_test_files() -> List[str]:
    """Find all test files in current directory"""
    test_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py') and ('test' in file.lower() or 'spec' in file.lower()):
                test_files.append(os.path.join(root, file))
    return test_files


def init_project(name: str):
    """Initialize new Judo project"""
    print(f"Initializing Judo project: {name}")
    
    # Create project structure
    os.makedirs(name, exist_ok=True)
    os.makedirs(f"{name}/tests", exist_ok=True)
    os.makedirs(f"{name}/config", exist_ok=True)
    
    # Create sample test file
    sample_test = '''"""
Sample Judo test
"""

from judo import Judo

def test_sample_api():
    # Create Judo instance
    judo = Judo()
    
    # Configure base URL
    judo.url = "https://jsonplaceholder.typicode.com"
    
    # Make GET request
    response = judo.get("/posts/1")
    
    # Validate response
    judo.match(response.status, 200)
    judo.match(response.json.userId, 1)
    judo.match(response.json.title, "##string")
    
    print("Test passed!")

if __name__ == "__main__":
    test_sample_api()
'''
    
    with open(f"{name}/tests/test_sample.py", 'w') as f:
        f.write(sample_test)
    
    # Create config file
    config = '''# Judo Framework Configuration

environments:
  dev:
    baseUrl: "https://api-dev.example.com"
  test:
    baseUrl: "https://api-test.example.com"
  prod:
    baseUrl: "https://api.example.com"
'''
    
    with open(f"{name}/config/judo.yaml", 'w') as f:
        f.write(config)
    
    print(f"Project '{name}' created successfully!")
    print(f"Run 'cd {name} && python tests/test_sample.py' to test")


def start_mock_server(port: int, config_file: str):
    """Start mock server"""
    from judo.mock.server import MockServer
    
    print(f"Starting mock server on port {port}")
    
    server = MockServer(port)
    
    if config_file:
        # Load mock configuration
        print(f"Loading config from: {config_file}")
        # Implementation would load routes from config file
    else:
        # Add some default routes for demo
        server.get("/health", {"status": 200, "body": {"status": "ok"}})
        server.get("/users/*", {"status": 200, "body": {"id": 1, "name": "John Doe"}})
    
    try:
        server.start()
        print("Mock server running. Press Ctrl+C to stop.")
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
        print("\nMock server stopped.")


def show_version():
    """Show version information"""
    from judo import __version__
    print(f"Judo Framework v{__version__}")


if __name__ == '__main__':
    main()