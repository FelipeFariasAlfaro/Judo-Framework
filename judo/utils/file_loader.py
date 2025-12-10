"""
File Loader - Load JSON, YAML and other data files
Provides Karate-like file loading capabilities
"""

import json
import yaml
import os
from typing import Any, Dict, List, Union
from pathlib import Path


class FileLoader:
    """
    File loader for JSON, YAML and other data files
    Similar to Karate's file loading capabilities
    """
    
    def __init__(self, base_path: str = None):
        """Initialize file loader with optional base path"""
        self.base_path = Path(base_path) if base_path else Path.cwd()
    
    def load_json(self, file_path: str) -> Union[Dict, List, Any]:
        """
        Load JSON file
        Similar to Karate's read('file.json')
        """
        full_path = self._resolve_path(file_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {full_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {full_path}: {e}")
    
    def load_yaml(self, file_path: str) -> Union[Dict, List, Any]:
        """
        Load YAML file
        Similar to Karate's read('file.yaml')
        """
        full_path = self._resolve_path(file_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"YAML file not found: {full_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in file {full_path}: {e}")
    
    def load_text(self, file_path: str) -> str:
        """
        Load text file
        Similar to Karate's read('file.txt')
        """
        full_path = self._resolve_path(file_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Text file not found: {full_path}")
    
    def load_csv(self, file_path: str) -> List[Dict]:
        """
        Load CSV file as list of dictionaries
        Similar to Karate's read('file.csv')
        """
        import csv
        full_path = self._resolve_path(file_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {full_path}")
    
    def load_binary(self, file_path: str) -> bytes:
        """
        Load binary file
        For file uploads, images, etc.
        """
        full_path = self._resolve_path(file_path)
        
        try:
            with open(full_path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Binary file not found: {full_path}")
    
    def save_json(self, data: Any, file_path: str, pretty: bool = True) -> None:
        """Save data to JSON file"""
        full_path = self._resolve_path(file_path)
        
        # Create directory if it doesn't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)
    
    def save_yaml(self, data: Any, file_path: str) -> None:
        """Save data to YAML file"""
        full_path = self._resolve_path(file_path)
        
        # Create directory if it doesn't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    
    def save_text(self, content: str, file_path: str) -> None:
        """Save text to file"""
        full_path = self._resolve_path(file_path)
        
        # Create directory if it doesn't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists"""
        full_path = self._resolve_path(file_path)
        return full_path.exists()
    
    def _resolve_path(self, file_path: str) -> Path:
        """Resolve file path relative to base path"""
        path = Path(file_path)
        
        if path.is_absolute():
            return path
        else:
            return self.base_path / path
    
    def set_base_path(self, base_path: str) -> None:
        """Set new base path for file operations"""
        self.base_path = Path(base_path)
    
    def get_base_path(self) -> str:
        """Get current base path"""
        return str(self.base_path)


# Global file loader instance
_file_loader = FileLoader()

# Convenience functions (Karate-style)
def read(file_path: str) -> Any:
    """
    Read file and auto-detect format based on extension
    Similar to Karate's read() function
    """
    path = Path(file_path)
    extension = path.suffix.lower()
    
    if extension == '.json':
        return _file_loader.load_json(file_path)
    elif extension in ['.yaml', '.yml']:
        return _file_loader.load_yaml(file_path)
    elif extension == '.csv':
        return _file_loader.load_csv(file_path)
    else:
        return _file_loader.load_text(file_path)

def read_json(file_path: str) -> Union[Dict, List, Any]:
    """Read JSON file"""
    return _file_loader.load_json(file_path)

def read_yaml(file_path: str) -> Union[Dict, List, Any]:
    """Read YAML file"""
    return _file_loader.load_yaml(file_path)

def read_text(file_path: str) -> str:
    """Read text file"""
    return _file_loader.load_text(file_path)

def read_csv(file_path: str) -> List[Dict]:
    """Read CSV file"""
    return _file_loader.load_csv(file_path)

def read_binary(file_path: str) -> bytes:
    """Read binary file"""
    return _file_loader.load_binary(file_path)

def write_json(data: Any, file_path: str, pretty: bool = True) -> None:
    """Write data to JSON file"""
    _file_loader.save_json(data, file_path, pretty)

def write_yaml(data: Any, file_path: str) -> None:
    """Write data to YAML file"""
    _file_loader.save_yaml(data, file_path)

def write_text(content: str, file_path: str) -> None:
    """Write text to file"""
    _file_loader.save_text(content, file_path)

def file_exists(file_path: str) -> bool:
    """Check if file exists"""
    return _file_loader.file_exists(file_path)

def set_base_path(base_path: str) -> None:
    """Set base path for file operations"""
    _file_loader.set_base_path(base_path)