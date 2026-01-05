"""
Response Caching
Cache responses to improve test performance
"""

import hashlib
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class CacheEntry:
    """Single cache entry"""
    
    def __init__(self, response: Any, ttl: Optional[int] = None):
        """
        Initialize cache entry
        
        Args:
            response: Response to cache
            ttl: Time to live in seconds
        """
        self.response = response
        self.created_at = datetime.now()
        self.ttl = ttl
    
    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        if self.ttl is None:
            return False
        
        elapsed = (datetime.now() - self.created_at).total_seconds()
        return elapsed > self.ttl
    
    def get_age_seconds(self) -> float:
        """Get age of cache entry in seconds"""
        return (datetime.now() - self.created_at).total_seconds()


class ResponseCache:
    """Cache for HTTP responses"""
    
    def __init__(self, enabled: bool = True, default_ttl: Optional[int] = 300):
        """
        Initialize response cache
        
        Args:
            enabled: Whether caching is enabled
            default_ttl: Default time to live in seconds
        """
        self.enabled = enabled
        self.default_ttl = default_ttl
        self.cache: Dict[str, CacheEntry] = {}
    
    def _generate_key(self, method: str, url: str, params: Optional[Dict] = None) -> str:
        """Generate cache key from request details"""
        key_parts = [method, url]
        
        if params:
            params_str = json.dumps(params, sort_keys=True)
            key_parts.append(params_str)
        
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, method: str, url: str, params: Optional[Dict] = None) -> Optional[Any]:
        """
        Get cached response
        
        Args:
            method: HTTP method
            url: Request URL
            params: Query parameters
        
        Returns:
            Cached response or None
        """
        if not self.enabled:
            return None
        
        # Only cache GET requests
        if method.upper() != "GET":
            return None
        
        key = self._generate_key(method, url, params)
        
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        
        if entry.is_expired():
            del self.cache[key]
            return None
        
        return entry.response
    
    def set(self, method: str, url: str, response: Any, params: Optional[Dict] = None, ttl: Optional[int] = None):
        """
        Cache response
        
        Args:
            method: HTTP method
            url: Request URL
            response: Response to cache
            params: Query parameters
            ttl: Time to live in seconds (uses default if not specified)
        """
        if not self.enabled:
            return
        
        # Only cache GET requests
        if method.upper() != "GET":
            return
        
        key = self._generate_key(method, url, params)
        cache_ttl = ttl if ttl is not None else self.default_ttl
        
        self.cache[key] = CacheEntry(response, cache_ttl)
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
    
    def clear_expired(self):
        """Remove expired entries"""
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.is_expired()
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        self.clear_expired()
        
        total_entries = len(self.cache)
        total_size = sum(
            len(json.dumps(entry.response, default=str))
            for entry in self.cache.values()
        )
        
        return {
            "enabled": self.enabled,
            "total_entries": total_entries,
            "total_size_bytes": total_size,
            "default_ttl_seconds": self.default_ttl
        }
    
    def enable(self):
        """Enable caching"""
        self.enabled = True
    
    def disable(self):
        """Disable caching"""
        self.enabled = False
