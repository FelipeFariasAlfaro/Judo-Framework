"""
Behave integration module - Gherkin DSL support for Judo Framework
Provides step definitions and utilities for BDD testing with Behave
"""

# Import all steps to register them automatically
from . import steps
from . import steps_es  # Steps en español
from .context import JudoContext
from .hooks import *

# Import auto hooks for easy access
from .auto_hooks import (
    before_all_judo,
    before_feature_judo,
    after_feature_judo,
    before_scenario_judo,
    after_scenario_judo,
    before_step_judo,
    after_step_judo,
    after_all_judo
)

# Force import of all step definitions
import sys
import importlib

def _ensure_steps_loaded():
    """Ensure all step definitions are loaded and registered"""
    try:
        # Force reload of steps module to ensure registration
        if 'judo.behave.steps' in sys.modules:
            importlib.reload(sys.modules['judo.behave.steps'])
        else:
            from . import steps
    except Exception as e:
        print(f"Warning: Could not load Judo steps: {e}")

# Load steps immediately
_ensure_steps_loaded()

__all__ = [
    'JudoContext',
    'before_all',
    'before_scenario', 
    'after_scenario',
    'after_all',
    'setup_judo_context',
    # Auto hooks
    'before_all_judo',
    'before_feature_judo',
    'after_feature_judo',
    'before_scenario_judo',
    'after_scenario_judo',
    'before_step_judo',
    'after_step_judo',
    'after_all_judo',
    # Convenience function
    'install_judo_hooks'
]

def setup_judo_context(context):
    """
    Setup Judo Framework context for Behave
    
    Args:
        context: Behave context object
    """
    from ..core.judo import Judo
    
    # Ensure steps are loaded
    _ensure_steps_loaded()
    
    # Initialize Judo context
    context.judo_context = JudoContext(context)
    
    # Initialize Judo instance (for backward compatibility)
    context.judo = context.judo_context.judo
    
    # Add helper methods to context
    context.get_last_response = lambda: getattr(context.judo_context, 'response', None)
    context.set_base_url = lambda url: context.judo_context.set_base_url(url)
    
    return context


def install_judo_hooks():
    """
    Instala automáticamente todos los hooks de Judo para captura de reportes.
    
    El usuario solo necesita llamar esta función en su environment.py:
    
    ```python
    from judo.behave import install_judo_hooks
    
    # Instalar hooks automáticamente
    before_all, before_feature, after_feature, before_scenario, after_scenario, before_step, after_step, after_all = install_judo_hooks()
    ```
    
    O más simple:
    
    ```python
    from judo.behave import *
    
    # Los hooks ya están disponibles como:
    # before_all_judo, before_feature_judo, after_feature_judo, etc.
    ```
    """
    return (
        before_all_judo,
        before_feature_judo,
        after_feature_judo,
        before_scenario_judo,
        after_scenario_judo,
        before_step_judo,
        after_step_judo,
        after_all_judo
    )