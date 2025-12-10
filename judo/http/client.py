"""
HTTP Client - Advanced HTTP client with Karate-like features
"""

import requests
from requests.auth import HTTPBasicAuth
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin
from ..core.response import JudoResponse


class HttpClient:
    """
    Advanced HTTP client providing Karate-like HTTP functionality
    """
    
    def __init__(self, judo_instance):
        self.judo = judo_instance
        self.session = requests.Session()
        self.default_headers = {}
        self.default_params = {}
        self.default_cookies = {}
        self.form_fields = {}
        self.multipart_fields = {}
        
    def _build_url(self, url: str) -> str:
        """Build complete URL"""
        if url.startswith(('http://', 'https://')):
            return url
        if self.judo.base_url:
            return urljoin(self.judo.base_url, url)
        return url
    
    def _prepare_request_kwargs(self, **kwargs) -> Dict:
        """Prepare request arguments"""
        # Merge headers
        headers = self.default_headers.copy()
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers
        
        # Merge params
        params = self.default_params.copy()
        params.update(kwargs.get('params', {}))
        if params:
            kwargs['params'] = params
        
        # Merge cookies
        cookies = self.default_cookies.copy()
        cookies.update(kwargs.get('cookies', {}))
        if cookies:
            kwargs['cookies'] = cookies
            
        return kwargs
    
    def get(self, url: str, **kwargs) -> JudoResponse:
        """HTTP GET request"""
        full_url = self._build_url(url)
        kwargs = self._prepare_request_kwargs(**kwargs)
        
        # Log request to reporter
        if self.judo.reporter:
            self.judo.reporter.log_request(
                method="GET",
                url=full_url,
                headers=kwargs.get('headers', {}),
                params=kwargs.get('params', {}),
                body=None
            )
        
        response = self.session.get(full_url, **kwargs)
        judo_response = JudoResponse(response)
        
        # Log response to reporter
        if self.judo.reporter:
            self.judo.reporter.log_response(
                status_code=response.status_code,
                headers=dict(response.headers),
                body=judo_response.json if judo_response.is_json() else response.text,
                body_type="json" if judo_response.is_json() else "text",
                elapsed_time=response.elapsed.total_seconds()
            )
        
        return judo_response
    
    def post(self, url: str, **kwargs) -> JudoResponse:
        """HTTP POST request"""
        full_url = self._build_url(url)
        kwargs = self._prepare_request_kwargs(**kwargs)
        
        # Handle form data
        if self.form_fields:
            kwargs['data'] = self.form_fields
            self.form_fields.clear()
        
        # Handle multipart data
        if self.multipart_fields:
            kwargs['files'] = self.multipart_fields
            self.multipart_fields.clear()
        
        # Determine body and body type for logging
        body = None
        body_type = "json"
        if 'json' in kwargs:
            body = kwargs['json']
            body_type = "json"
        elif 'data' in kwargs:
            body = kwargs['data']
            body_type = "form"
        elif 'files' in kwargs:
            body = kwargs['files']
            body_type = "multipart"
        
        # Log request to reporter
        if self.judo.reporter:
            self.judo.reporter.log_request(
                method="POST",
                url=full_url,
                headers=kwargs.get('headers', {}),
                params=kwargs.get('params', {}),
                body=body,
                body_type=body_type
            )
        
        response = self.session.post(full_url, **kwargs)
        judo_response = JudoResponse(response)
        
        # Log response to reporter
        if self.judo.reporter:
            self.judo.reporter.log_response(
                status_code=response.status_code,
                headers=dict(response.headers),
                body=judo_response.json if judo_response.is_json() else response.text,
                body_type="json" if judo_response.is_json() else "text",
                elapsed_time=response.elapsed.total_seconds()
            )
        
        return judo_response
    
    def put(self, url: str, **kwargs) -> JudoResponse:
        """HTTP PUT request"""
        full_url = self._build_url(url)
        kwargs = self._prepare_request_kwargs(**kwargs)
        response = self.session.put(full_url, **kwargs)
        return JudoResponse(response)
    
    def patch(self, url: str, **kwargs) -> JudoResponse:
        """HTTP PATCH request"""
        full_url = self._build_url(url)
        kwargs = self._prepare_request_kwargs(**kwargs)
        response = self.session.patch(full_url, **kwargs)
        return JudoResponse(response)
    
    def delete(self, url: str, **kwargs) -> JudoResponse:
        """HTTP DELETE request"""
        full_url = self._build_url(url)
        kwargs = self._prepare_request_kwargs(**kwargs)
        response = self.session.delete(full_url, **kwargs)
        return JudoResponse(response)
    
    def head(self, url: str, **kwargs) -> JudoResponse:
        """HTTP HEAD request"""
        full_url = self._build_url(url)
        kwargs = self._prepare_request_kwargs(**kwargs)
        response = self.session.head(full_url, **kwargs)
        return JudoResponse(response)
    
    def options(self, url: str, **kwargs) -> JudoResponse:
        """HTTP OPTIONS request"""
        full_url = self._build_url(url)
        kwargs = self._prepare_request_kwargs(**kwargs)
        response = self.session.options(full_url, **kwargs)
        return JudoResponse(response)
    
    # Configuration methods
    
    def set_header(self, name: str, value: str) -> None:
        """Set default header"""
        self.default_headers[name] = value
    
    def set_headers(self, headers: Dict[str, str]) -> None:
        """Set multiple default headers"""
        self.default_headers.update(headers)
    
    def set_param(self, name: str, value: Any) -> None:
        """Set default query parameter"""
        self.default_params[name] = value
    
    def set_params(self, params: Dict[str, Any]) -> None:
        """Set multiple default parameters"""
        self.default_params.update(params)
    
    def set_cookie(self, name: str, value: str) -> None:
        """Set default cookie"""
        self.default_cookies[name] = value
    
    def set_cookies(self, cookies: Dict[str, str]) -> None:
        """Set multiple default cookies"""
        self.default_cookies.update(cookies)
    
    def set_form_field(self, name: str, value: Any) -> None:
        """Set form field for next request"""
        self.form_fields[name] = value
    
    def set_multipart_field(self, name: str, value: Any, filename: str = None) -> None:
        """Set multipart form field for next request"""
        if filename:
            self.multipart_fields[name] = (filename, value)
        else:
            self.multipart_fields[name] = value
    
    def set_basic_auth(self, username: str, password: str) -> None:
        """Set basic authentication"""
        self.session.auth = HTTPBasicAuth(username, password)
    
    def set_bearer_token(self, token: str) -> None:
        """Set bearer token authentication"""
        self.set_header('Authorization', f'Bearer {token}')
    
    def clear_auth(self) -> None:
        """Clear authentication"""
        self.session.auth = None
        self.default_headers.pop('Authorization', None)
    
    def set_timeout(self, timeout: float) -> None:
        """Set request timeout"""
        self.session.timeout = timeout
    
    def set_verify_ssl(self, verify: bool) -> None:
        """Set SSL verification"""
        self.session.verify = verify
    
    def set_proxy(self, proxy_url: str) -> None:
        """Set proxy"""
        self.session.proxies = {'http': proxy_url, 'https': proxy_url}