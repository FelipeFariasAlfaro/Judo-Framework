"""
Playwright Integration for Judo Framework
Optional browser automation capabilities
"""

# Check if Playwright is available
try:
    import playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# Import steps to register them with behave
if PLAYWRIGHT_AVAILABLE:
    try:
        from . import steps
        from . import steps_es
    except ImportError:
        pass

__all__ = ['PLAYWRIGHT_AVAILABLE']