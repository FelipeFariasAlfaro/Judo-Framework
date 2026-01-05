"""
API Contract Testing
Validate against OpenAPI and AsyncAPI specs
"""

import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class ContractValidator:
    """Validate API responses against contracts"""
    
    def __init__(self, spec_file: str):
        """
        Initialize contract validator
        
        Args:
            spec_file: Path to OpenAPI or AsyncAPI spec file
        """
        self.spec_file = spec_file
        self.spec = self._load_spec(spec_file)
    
    @staticmethod
    def _load_spec(spec_file: str) -> Dict[str, Any]:
        """Load spec from file"""
        with open(spec_file, 'r', encoding='utf-8') as f:
            if spec_file.endswith('.json'):
                return json.load(f)
            elif spec_file.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            else:
                raise ValueError("Spec file must be JSON or YAML")
    
    def validate_openapi(self, method: str, path: str, response: Dict[str, Any], status_code: int) -> bool:
        """
        Validate response against OpenAPI spec
        
        Args:
            method: HTTP method
            path: Request path
            response: Response body
            status_code: Response status code
        
        Returns:
            True if valid
        """
        try:
            import jsonschema
        except ImportError:
            raise ImportError("jsonschema required: pip install jsonschema")
        
        # Find path in spec
        paths = self.spec.get("paths", {})
        path_spec = None
        
        for spec_path in paths:
            if self._match_path(spec_path, path):
                path_spec = paths[spec_path]
                break
        
        if not path_spec:
            raise ValueError(f"Path {path} not found in OpenAPI spec")
        
        # Find method in path
        method_spec = path_spec.get(method.lower())
        if not method_spec:
            raise ValueError(f"Method {method} not found for path {path}")
        
        # Find response schema
        responses = method_spec.get("responses", {})
        response_spec = responses.get(str(status_code))
        
        if not response_spec:
            raise ValueError(f"Status code {status_code} not found in spec")
        
        # Get schema
        content = response_spec.get("content", {})
        json_content = content.get("application/json", {})
        schema = json_content.get("schema", {})
        
        if not schema:
            return True  # No schema to validate
        
        # Validate
        try:
            jsonschema.validate(response, schema)
            return True
        except jsonschema.ValidationError as e:
            raise AssertionError(f"Response validation failed: {e.message}")
    
    def validate_asyncapi(self, channel: str, message: Dict[str, Any]) -> bool:
        """
        Validate message against AsyncAPI spec
        
        Args:
            channel: Channel name
            message: Message payload
        
        Returns:
            True if valid
        """
        try:
            import jsonschema
        except ImportError:
            raise ImportError("jsonschema required: pip install jsonschema")
        
        # Find channel in spec
        channels = self.spec.get("channels", {})
        channel_spec = channels.get(channel)
        
        if not channel_spec:
            raise ValueError(f"Channel {channel} not found in AsyncAPI spec")
        
        # Get message schema
        publish = channel_spec.get("publish", {})
        message_spec = publish.get("message", {})
        payload = message_spec.get("payload", {})
        
        if not payload:
            return True  # No schema to validate
        
        # Validate
        try:
            jsonschema.validate(message, payload)
            return True
        except jsonschema.ValidationError as e:
            raise AssertionError(f"Message validation failed: {e.message}")
    
    @staticmethod
    def _match_path(spec_path: str, actual_path: str) -> bool:
        """Check if spec path matches actual path"""
        # Simple path matching (doesn't handle all OpenAPI path patterns)
        spec_parts = spec_path.split('/')
        actual_parts = actual_path.split('/')
        
        if len(spec_parts) != len(actual_parts):
            return False
        
        for spec_part, actual_part in zip(spec_parts, actual_parts):
            if spec_part.startswith('{') and spec_part.endswith('}'):
                # Parameter - matches anything
                continue
            elif spec_part != actual_part:
                return False
        
        return True
    
    def get_endpoints(self) -> Dict[str, list]:
        """Get all endpoints from spec"""
        endpoints = {}
        paths = self.spec.get("paths", {})
        
        for path, path_spec in paths.items():
            methods = [m.upper() for m in path_spec.keys() if m in ['get', 'post', 'put', 'patch', 'delete']]
            endpoints[path] = methods
        
        return endpoints
    
    def get_schemas(self) -> Dict[str, Dict]:
        """Get all schemas from spec"""
        components = self.spec.get("components", {})
        schemas = components.get("schemas", {})
        return schemas
