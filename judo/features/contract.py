"""
API Contract Testing
Validate against OpenAPI and AsyncAPI specs
"""

import json
import yaml
import re
from typing import Dict, Any, Optional, List
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
        
        # Resolve schema references
        schema = self._resolve_schema_refs(schema)
        
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
        
        # Resolve schema references
        payload = self._resolve_schema_refs(payload)
        
        # Validate
        try:
            jsonschema.validate(message, payload)
            return True
        except jsonschema.ValidationError as e:
            raise AssertionError(f"Message validation failed: {e.message}")
    
    def _resolve_schema_refs(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve $ref references in schema"""
        if isinstance(schema, dict):
            if "$ref" in schema:
                ref_path = schema["$ref"]
                if ref_path.startswith("#/"):
                    # Internal reference
                    parts = ref_path[2:].split("/")
                    resolved = self.spec
                    for part in parts:
                        resolved = resolved.get(part, {})
                    return self._resolve_schema_refs(resolved)
                else:
                    # External reference - not supported yet
                    return schema
            else:
                # Recursively resolve refs in nested objects
                resolved = {}
                for key, value in schema.items():
                    resolved[key] = self._resolve_schema_refs(value)
                return resolved
        elif isinstance(schema, list):
            return [self._resolve_schema_refs(item) for item in schema]
        else:
            return schema
    
    @staticmethod
    def _match_path(spec_path: str, actual_path: str) -> bool:
        """Check if spec path matches actual path"""
        # Enhanced path matching with parameter support
        spec_parts = spec_path.split('/')
        actual_parts = actual_path.split('/')
        
        if len(spec_parts) != len(actual_parts):
            return False
        
        for spec_part, actual_part in zip(spec_parts, actual_parts):
            if spec_part.startswith('{') and spec_part.endswith('}'):
                # Parameter - matches anything non-empty
                if not actual_part:
                    return False
                continue
            elif spec_part != actual_part:
                return False
        
        return True
    
    def get_endpoints(self) -> Dict[str, List[str]]:
        """Get all endpoints from spec"""
        endpoints = {}
        paths = self.spec.get("paths", {})
        
        for path, path_spec in paths.items():
            methods = [m.upper() for m in path_spec.keys() if m in ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']]
            if methods:
                endpoints[path] = methods
        
        return endpoints
    
    def get_schemas(self) -> Dict[str, Dict]:
        """Get all schemas from spec"""
        components = self.spec.get("components", {})
        schemas = components.get("schemas", {})
        return schemas
    
    def get_security_schemes(self) -> Dict[str, Dict]:
        """Get security schemes from spec"""
        components = self.spec.get("components", {})
        security_schemes = components.get("securitySchemes", {})
        return security_schemes
    
    def validate_request_body(self, method: str, path: str, request_body: Dict[str, Any]) -> bool:
        """
        Validate request body against OpenAPI spec
        
        Args:
            method: HTTP method
            path: Request path
            request_body: Request body data
        
        Returns:
            True if valid
        """
        try:
            import jsonschema
        except ImportError:
            raise ImportError("jsonschema required: pip install jsonschema")
        
        # Find path and method in spec
        paths = self.spec.get("paths", {})
        path_spec = None
        
        for spec_path in paths:
            if self._match_path(spec_path, path):
                path_spec = paths[spec_path]
                break
        
        if not path_spec:
            raise ValueError(f"Path {path} not found in OpenAPI spec")
        
        method_spec = path_spec.get(method.lower())
        if not method_spec:
            raise ValueError(f"Method {method} not found for path {path}")
        
        # Get request body schema
        request_body_spec = method_spec.get("requestBody", {})
        if not request_body_spec:
            return True  # No request body expected
        
        content = request_body_spec.get("content", {})
        json_content = content.get("application/json", {})
        schema = json_content.get("schema", {})
        
        if not schema:
            return True  # No schema to validate
        
        # Resolve schema references
        schema = self._resolve_schema_refs(schema)
        
        # Validate
        try:
            jsonschema.validate(request_body, schema)
            return True
        except jsonschema.ValidationError as e:
            raise AssertionError(f"Request body validation failed: {e.message}")
    
    def validate_headers(self, method: str, path: str, headers: Dict[str, str], status_code: int) -> bool:
        """
        Validate response headers against OpenAPI spec
        
        Args:
            method: HTTP method
            path: Request path
            headers: Response headers
            status_code: Response status code
        
        Returns:
            True if valid
        """
        # Find path and method in spec
        paths = self.spec.get("paths", {})
        path_spec = None
        
        for spec_path in paths:
            if self._match_path(spec_path, path):
                path_spec = paths[spec_path]
                break
        
        if not path_spec:
            return True  # Path not in spec, skip validation
        
        method_spec = path_spec.get(method.lower())
        if not method_spec:
            return True  # Method not in spec, skip validation
        
        # Get response spec
        responses = method_spec.get("responses", {})
        response_spec = responses.get(str(status_code))
        
        if not response_spec:
            return True  # Status code not in spec, skip validation
        
        # Check required headers
        headers_spec = response_spec.get("headers", {})
        for header_name, header_spec in headers_spec.items():
            required = header_spec.get("required", False)
            if required and header_name.lower() not in [h.lower() for h in headers.keys()]:
                raise AssertionError(f"Required header '{header_name}' is missing")
        
        return True
    
    def get_operation_info(self, method: str, path: str) -> Dict[str, Any]:
        """
        Get operation information from spec
        
        Args:
            method: HTTP method
            path: Request path
        
        Returns:
            Operation information
        """
        paths = self.spec.get("paths", {})
        
        for spec_path in paths:
            if self._match_path(spec_path, path):
                path_spec = paths[spec_path]
                method_spec = path_spec.get(method.lower(), {})
                return {
                    "operationId": method_spec.get("operationId"),
                    "summary": method_spec.get("summary"),
                    "description": method_spec.get("description"),
                    "tags": method_spec.get("tags", []),
                    "parameters": method_spec.get("parameters", []),
                    "requestBody": method_spec.get("requestBody"),
                    "responses": method_spec.get("responses", {}),
                    "security": method_spec.get("security", [])
                }
        
        return {}


class DataTypeValidator:
    """Advanced data type validation utilities"""
    
    @staticmethod
    def validate_email_format(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_url_format(url: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def validate_uuid_format(uuid_str: str) -> bool:
        """Validate UUID format"""
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
        return bool(re.match(pattern, uuid_str.lower()))
    
    @staticmethod
    def validate_iso_date_format(date_str: str) -> bool:
        """Validate ISO date format"""
        pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?(?:Z|[+-]\d{2}:\d{2})$'
        return bool(re.match(pattern, date_str))
    
    @staticmethod
    def validate_phone_format(phone: str) -> bool:
        """Validate phone number format"""
        # Basic international phone format
        pattern = r'^\+?[1-9]\d{1,14}$'
        return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))
    
    @staticmethod
    def validate_credit_card_format(card: str) -> bool:
        """Validate credit card format (Luhn algorithm)"""
        # Remove spaces and dashes
        card = card.replace(' ', '').replace('-', '')
        
        # Check if all digits
        if not card.isdigit():
            return False
        
        # Luhn algorithm
        def luhn_check(card_num):
            def digits_of(n):
                return [int(d) for d in str(n)]
            
            digits = digits_of(card_num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10 == 0
        
        return luhn_check(card)


class StructureValidator:
    """Validate complex data structures"""
    
    @staticmethod
    def validate_nested_structure(data: Any, expected_structure: Dict[str, Any]) -> List[str]:
        """
        Validate nested data structure
        
        Args:
            data: Data to validate
            expected_structure: Expected structure definition
        
        Returns:
            List of validation errors
        """
        errors = []
        
        def validate_recursive(current_data, current_structure, path=""):
            if isinstance(current_structure, dict):
                if not isinstance(current_data, dict):
                    errors.append(f"Path '{path}': expected object, got {type(current_data).__name__}")
                    return
                
                for key, expected_value in current_structure.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    if key not in current_data:
                        errors.append(f"Path '{current_path}': missing required field")
                        continue
                    
                    validate_recursive(current_data[key], expected_value, current_path)
            
            elif isinstance(current_structure, list):
                if not isinstance(current_data, list):
                    errors.append(f"Path '{path}': expected array, got {type(current_data).__name__}")
                    return
                
                if len(current_structure) > 0:
                    # Validate each item against first structure element
                    expected_item_structure = current_structure[0]
                    for i, item in enumerate(current_data):
                        validate_recursive(item, expected_item_structure, f"{path}[{i}]")
            
            elif isinstance(current_structure, type):
                if not isinstance(current_data, current_structure):
                    errors.append(f"Path '{path}': expected {current_structure.__name__}, got {type(current_data).__name__}")
            
            elif isinstance(current_structure, str):
                # Type name as string
                type_mapping = {
                    'string': str,
                    'number': (int, float),
                    'integer': int,
                    'boolean': bool,
                    'array': list,
                    'object': dict,
                    'null': type(None)
                }
                
                expected_type = type_mapping.get(current_structure.lower())
                if expected_type and not isinstance(current_data, expected_type):
                    errors.append(f"Path '{path}': expected {current_structure}, got {type(current_data).__name__}")
        
        validate_recursive(data, expected_structure)
        return errors
