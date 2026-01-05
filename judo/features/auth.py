"""
Authentication Handlers
OAuth2, JWT, and other auth mechanisms
"""

import json
import time
import jwt
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import requests


class OAuth2Handler:
    """OAuth2 authentication handler"""
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_url: str,
        scope: str = "",
        grant_type: str = "client_credentials"
    ):
        """
        Initialize OAuth2 handler
        
        Args:
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret
            token_url: Token endpoint URL
            scope: OAuth2 scope
            grant_type: Grant type (default: client_credentials)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.scope = scope
        self.grant_type = grant_type
        
        self.access_token = None
        self.token_expiry = None
    
    def get_token(self, force_refresh: bool = False) -> str:
        """
        Get access token (with automatic refresh)
        
        Args:
            force_refresh: Force token refresh
        
        Returns:
            Access token
        """
        # Check if token is still valid
        if self.access_token and self.token_expiry and not force_refresh:
            if datetime.now() < self.token_expiry:
                return self.access_token
        
        # Request new token
        payload = {
            "grant_type": self.grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        if self.scope:
            payload["scope"] = self.scope
        
        try:
            response = requests.post(self.token_url, data=payload)
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data.get("access_token")
            
            # Calculate expiry time
            expires_in = data.get("expires_in", 3600)
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in - 60)
            
            return self.access_token
        except Exception as e:
            raise Exception(f"Failed to get OAuth2 token: {e}")
    
    def get_authorization_header(self) -> Dict[str, str]:
        """Get authorization header"""
        token = self.get_token()
        return {"Authorization": f"Bearer {token}"}


class JWTHandler:
    """JWT authentication handler"""
    
    def __init__(
        self,
        secret: str,
        algorithm: str = "HS256",
        auto_refresh: bool = True,
        expiry_seconds: int = 3600
    ):
        """
        Initialize JWT handler
        
        Args:
            secret: JWT secret key
            algorithm: JWT algorithm
            auto_refresh: Automatically refresh expired tokens
            expiry_seconds: Token expiry time in seconds
        """
        self.secret = secret
        self.algorithm = algorithm
        self.auto_refresh = auto_refresh
        self.expiry_seconds = expiry_seconds
        
        self.token = None
        self.token_expiry = None
    
    def create_token(self, payload: Dict[str, Any]) -> str:
        """
        Create JWT token
        
        Args:
            payload: Token payload
        
        Returns:
            JWT token
        """
        # Add expiry
        payload["exp"] = datetime.utcnow() + timedelta(seconds=self.expiry_seconds)
        payload["iat"] = datetime.utcnow()
        
        self.token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        self.token_expiry = datetime.now() + timedelta(seconds=self.expiry_seconds - 60)
        
        return self.token
    
    def get_token(self, payload: Optional[Dict[str, Any]] = None) -> str:
        """
        Get JWT token (with automatic refresh)
        
        Args:
            payload: Token payload (for creating new token)
        
        Returns:
            JWT token
        """
        # Check if token is still valid
        if self.token and self.token_expiry:
            if datetime.now() < self.token_expiry:
                return self.token
        
        # Create new token
        if payload is None:
            payload = {}
        
        return self.create_token(payload)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify JWT token
        
        Args:
            token: JWT token to verify
        
        Returns:
            Decoded token payload
        """
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.InvalidTokenError as e:
            raise Exception(f"Invalid JWT token: {e}")
    
    def get_authorization_header(self, payload: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Get authorization header"""
        token = self.get_token(payload)
        return {"Authorization": f"Bearer {token}"}


class BasicAuthHandler:
    """Basic authentication handler"""
    
    def __init__(self, username: str, password: str):
        """
        Initialize basic auth handler
        
        Args:
            username: Username
            password: Password
        """
        self.username = username
        self.password = password
    
    def get_authorization_header(self) -> Dict[str, str]:
        """Get authorization header"""
        import base64
        
        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        
        return {"Authorization": f"Basic {encoded}"}


class APIKeyHandler:
    """API Key authentication handler"""
    
    def __init__(self, key: str, header_name: str = "X-API-Key"):
        """
        Initialize API key handler
        
        Args:
            key: API key
            header_name: Header name for API key
        """
        self.key = key
        self.header_name = header_name
    
    def get_authorization_header(self) -> Dict[str, str]:
        """Get authorization header"""
        return {self.header_name: self.key}
