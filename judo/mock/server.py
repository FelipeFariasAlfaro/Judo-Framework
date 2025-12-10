"""
Mock Server - Built-in mock server for testing
Provides Karate-like mock server functionality
"""

import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict, List, Optional, Callable
from urllib.parse import urlparse, parse_qs


class MockHandler(BaseHTTPRequestHandler):
    """HTTP request handler for mock server"""
    
    def __init__(self, mock_server, *args, **kwargs):
        self.mock_server = mock_server
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        self._handle_request('GET')
    
    def do_POST(self):
        self._handle_request('POST')
    
    def do_PUT(self):
        self._handle_request('PUT')
    
    def do_PATCH(self):
        self._handle_request('PATCH')
    
    def do_DELETE(self):
        self._handle_request('DELETE')
    
    def _handle_request(self, method: str):
        """Handle incoming request"""
        # Parse request
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        # Get request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ''
        
        # Find matching route
        response_data = self.mock_server.find_route(method, path, query_params, body, dict(self.headers))
        
        if response_data:
            # Send response
            self.send_response(response_data.get('status', 200))
            
            # Send headers
            headers = response_data.get('headers', {})
            for key, value in headers.items():
                self.send_header(key, value)
            self.end_headers()
            
            # Send body
            body = response_data.get('body', '')
            if isinstance(body, dict):
                body = json.dumps(body)
            self.wfile.write(body.encode('utf-8'))
        else:
            # Default 404 response
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Route not found'}).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to suppress default logging"""
        pass


class MockServer:
    """
    Mock server providing Karate-like mocking capabilities
    """
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.routes = []
        self.server = None
        self.server_thread = None
        self.running = False
    
    def start(self) -> None:
        """Start the mock server"""
        if self.running:
            return
        
        def handler(*args, **kwargs):
            return MockHandler(self, *args, **kwargs)
        
        self.server = HTTPServer(('localhost', self.port), handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.running = True
        print(f"Mock server started on http://localhost:{self.port}")
    
    def stop(self) -> None:
        """Stop the mock server"""
        if self.server and self.running:
            self.server.shutdown()
            self.server.server_close()
            self.running = False
            print("Mock server stopped")
    
    def add_route(self, method: str, path: str, response: Dict[str, Any], 
                  condition: Callable = None) -> None:
        """Add a mock route"""
        route = {
            'method': method.upper(),
            'path': path,
            'response': response,
            'condition': condition
        }
        self.routes.append(route)
    
    def get(self, path: str, response: Dict[str, Any], condition: Callable = None) -> None:
        """Add GET route"""
        self.add_route('GET', path, response, condition)
    
    def post(self, path: str, response: Dict[str, Any], condition: Callable = None) -> None:
        """Add POST route"""
        self.add_route('POST', path, response, condition)
    
    def put(self, path: str, response: Dict[str, Any], condition: Callable = None) -> None:
        """Add PUT route"""
        self.add_route('PUT', path, response, condition)
    
    def delete(self, path: str, response: Dict[str, Any], condition: Callable = None) -> None:
        """Add DELETE route"""
        self.add_route('DELETE', path, response, condition) 
   
    def find_route(self, method: str, path: str, query_params: Dict, 
                   body: str, headers: Dict) -> Optional[Dict]:
        """Find matching route for request"""
        for route in self.routes:
            if route['method'] == method and self._path_matches(route['path'], path):
                # Check condition if provided
                if route['condition']:
                    request_data = {
                        'method': method,
                        'path': path,
                        'query': query_params,
                        'body': body,
                        'headers': headers
                    }
                    if not route['condition'](request_data):
                        continue
                
                return route['response']
        
        return None
    
    def _path_matches(self, route_path: str, request_path: str) -> bool:
        """Check if route path matches request path (supports wildcards)"""
        if route_path == request_path:
            return True
        
        # Simple wildcard matching
        if '*' in route_path:
            import re
            pattern = route_path.replace('*', '.*')
            return bool(re.match(f'^{pattern}$', request_path))
        
        return False
    
    def clear_routes(self) -> None:
        """Clear all routes"""
        self.routes.clear()
    
    def get_url(self) -> str:
        """Get server URL"""
        return f"http://localhost:{self.port}"
    
    def is_running(self) -> bool:
        """Check if server is running"""
        return self.running