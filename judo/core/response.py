"""
JudoResponse class - Enhanced response object with Karate-like features
"""

import json
from typing import Any, Dict, List, Optional, Union
from urllib.parse import parse_qs, urlparse


class JudoResponse:
    """
    Enhanced response object providing Karate-like response handling
    """
    
    def __init__(self, response):
        """Initialize with requests.Response object"""
        self._response = response
        self._json_cache = None
        self._xml_cache = None
    
    @property
    def status(self) -> int:
        """HTTP status code"""
        return self._response.status_code
    
    @property
    def status_code(self) -> int:
        """HTTP status code (alias)"""
        return self.status
    
    @property
    def headers(self) -> Dict[str, str]:
        """Response headers"""
        return dict(self._response.headers)
    
    @property
    def cookies(self) -> Dict[str, str]:
        """Response cookies"""
        return dict(self._response.cookies)
    
    @property
    def text(self) -> str:
        """Response text content"""
        return self._response.text
    
    @property
    def content(self) -> bytes:
        """Response binary content"""
        return self._response.content
    
    @property
    def json(self) -> Any:
        """Parse response as JSON"""
        if self._json_cache is None:
            try:
                self._json_cache = self._response.json()
            except (json.JSONDecodeError, ValueError):
                self._json_cache = {}
        return self._json_cache
    
    @property
    def xml(self) -> Any:
        """Parse response as XML"""
        if self._xml_cache is None:
            try:
                from lxml import etree
                self._xml_cache = etree.fromstring(self.content)
            except Exception:
                self._xml_cache = None
        return self._xml_cache
    
    @property
    def url(self) -> str:
        """Response URL"""
        return self._response.url
    
    @property
    def elapsed(self) -> float:
        """Response time in seconds"""
        return self._response.elapsed.total_seconds()
    
    @property
    def encoding(self) -> str:
        """Response encoding"""
        return self._response.encoding or 'utf-8'
    
    def header(self, name: str, default: str = None) -> str:
        """Get specific header value"""
        return self.headers.get(name, default)
    
    def cookie(self, name: str, default: str = None) -> str:
        """Get specific cookie value"""
        return self.cookies.get(name, default)
    
    def json_path(self, path: str) -> Any:
        """Extract value using JSONPath"""
        from jsonpath_ng import parse
        jsonpath_expr = parse(path)
        matches = [match.value for match in jsonpath_expr.find(self.json)]
        return matches[0] if len(matches) == 1 else matches
    
    def xpath(self, xpath: str) -> Any:
        """Extract value using XPath"""
        if self.xml is not None:
            results = self.xml.xpath(xpath)
            return results[0] if len(results) == 1 else results
        return None
    
    def contains(self, text: str) -> bool:
        """Check if response text contains specified text"""
        return text in self.text
    
    def contains_json(self, key: str) -> bool:
        """Check if JSON response contains key"""
        if isinstance(self.json, dict):
            return key in self.json
        return False
    
    def is_json(self) -> bool:
        """Check if response is JSON"""
        # Check content-type header first
        content_type = self.header('content-type', '').lower()
        if 'application/json' in content_type or 'application/javascript' in content_type:
            return True
        
        # If already cached, it's JSON
        if self._json_cache is not None:
            return True
        
        # Try to parse as JSON
        try:
            self._response.json()
            return True
        except (json.JSONDecodeError, ValueError):
            return False
    
    def is_xml(self) -> bool:
        """Check if response is XML"""
        content_type = self.header('content-type', '').lower()
        return any(xml_type in content_type for xml_type in ['application/xml', 'text/xml'])
    
    def is_html(self) -> bool:
        """Check if response is HTML"""
        content_type = self.header('content-type', '').lower()
        return 'text/html' in content_type
    
    def is_success(self) -> bool:
        """Check if response is successful (2xx status)"""
        return 200 <= self.status < 300
    
    def is_redirect(self) -> bool:
        """Check if response is redirect (3xx status)"""
        return 300 <= self.status < 400
    
    def is_client_error(self) -> bool:
        """Check if response is client error (4xx status)"""
        return 400 <= self.status < 500
    
    def is_server_error(self) -> bool:
        """Check if response is server error (5xx status)"""
        return 500 <= self.status < 600
    
    def pretty_print(self) -> str:
        """Pretty print response for debugging"""
        lines = [
            f"Status: {self.status}",
            f"URL: {self.url}",
            f"Time: {self.elapsed:.3f}s",
            "Headers:"
        ]
        
        for key, value in self.headers.items():
            lines.append(f"  {key}: {value}")
        
        if self.is_json():
            lines.append("JSON Body:")
            lines.append(json.dumps(self.json, indent=2))
        elif self.text:
            lines.append("Text Body:")
            lines.append(self.text[:1000] + ("..." if len(self.text) > 1000 else ""))
        
        return "\n".join(lines)
    
    def __str__(self) -> str:
        """String representation"""
        return f"JudoResponse(status={self.status}, url='{self.url}')"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return self.__str__()