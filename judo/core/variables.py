"""
Variable Manager - Handles variable storage and manipulation
Implements Karate's variable system with scoping and interpolation
"""

import os
import re
from typing import Any, Dict, Optional


class VariableManager:
    """
    Manages variables with Karate-like scoping and interpolation
    """
    
    def __init__(self):
        self.variables = {}
        self.global_variables = {}
        
    def set(self, name: str, value: Any) -> None:
        """Set variable value"""
        self.variables[name] = value
    
    def get(self, name: str, default: Any = None) -> Any:
        """Get variable value with fallback to global and environment"""
        # Check local variables first
        if name in self.variables:
            return self.variables[name]
        
        # Check global variables
        if name in self.global_variables:
            return self.global_variables[name]
        
        # Check environment variables
        env_value = os.getenv(name)
        if env_value is not None:
            return env_value
            
        return default
    
    def remove(self, name: str) -> None:
        """Remove variable"""
        self.variables.pop(name, None)
        self.global_variables.pop(name, None)
    
    def set_global(self, name: str, value: Any) -> None:
        """Set global variable"""
        self.global_variables[name] = value
    
    def clear(self) -> None:
        """Clear all local variables"""
        self.variables.clear()
    
    def clear_global(self) -> None:
        """Clear all global variables"""
        self.global_variables.clear()
    
    def interpolate(self, text: str) -> str:
        """
        Interpolate variables in text using #{variable} syntax
        Similar to Karate's embedded expressions
        """
        if not isinstance(text, str):
            return text
        
        # Pattern to match #{variable} or #{expression}
        pattern = r'#\{([^}]+)\}'
        
        def replace_var(match):
            var_name = match.group(1).strip()
            
            # Handle simple variable reference
            if var_name in self.variables:
                return str(self.variables[var_name])
            elif var_name in self.global_variables:
                return str(self.global_variables[var_name])
            else:
                # Try environment variable
                env_value = os.getenv(var_name)
                if env_value is not None:
                    return env_value
                
                # Return original if not found
                return match.group(0)
        
        return re.sub(pattern, replace_var, text)
    
    def evaluate_expression(self, expression: str) -> Any:
        """
        Evaluate simple expressions with variables
        Limited evaluation for security
        """
        # Replace variables in expression
        interpolated = self.interpolate(expression)
        
        # Simple arithmetic evaluation (be careful with eval!)
        try:
            # Only allow safe operations
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in interpolated):
                return eval(interpolated)
        except:
            pass
        
        return interpolated
    
    def get_all(self) -> Dict[str, Any]:
        """Get all variables (local + global)"""
        result = self.global_variables.copy()
        result.update(self.variables)
        return result
    
    def exists(self, name: str) -> bool:
        """Check if variable exists"""
        return (name in self.variables or 
                name in self.global_variables or 
                os.getenv(name) is not None)
    
    def copy_from(self, other: 'VariableManager') -> None:
        """Copy variables from another manager"""
        self.variables.update(other.variables)
        self.global_variables.update(other.global_variables)
    
    def __contains__(self, name: str) -> bool:
        """Support 'in' operator"""
        return self.exists(name)
    
    def __getitem__(self, name: str) -> Any:
        """Support dict-like access"""
        return self.get(name)
    
    def __setitem__(self, name: str, value: Any) -> None:
        """Support dict-like assignment"""
        self.set(name, value)
    
    def __str__(self) -> str:
        """String representation"""
        return f"Variables: {len(self.variables)} local, {len(self.global_variables)} global"