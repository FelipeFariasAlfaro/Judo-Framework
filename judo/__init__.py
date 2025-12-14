"""
Judo Framework - Complete API Testing Framework for Python
Inspired by Karate Framework with full DSL implementation

Created by Felipe Farias at CENTYC - Centro Latinoamericano de Testing y Calidad del Software
https://www.centyc.cl
"""

from .core.judo import Judo
from .core.response import JudoResponse
from .core.matcher import Matcher
from .core.variables import VariableManager
from .http.client import HttpClient
from .mock.server import MockServer
from .reporting.reporter import JudoReporter
from .reporting.html_reporter import HTMLReporter
from .runner.base_runner import BaseRunner
from .runner.test_suite import TestSuite, CommonSuites
from .utils.helpers import *

# Optional Playwright integration
try:
    from .playwright import PLAYWRIGHT_AVAILABLE
    if PLAYWRIGHT_AVAILABLE:
        from .playwright.browser_context import JudoBrowserContext
        from .playwright.page_manager import PageManager, PagePool
        __all__.extend(["JudoBrowserContext", "PageManager", "PagePool", "PLAYWRIGHT_AVAILABLE"])
    else:
        __all__.append("PLAYWRIGHT_AVAILABLE")
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    __all__.append("PLAYWRIGHT_AVAILABLE")

__version__ = "1.3.37"
__author__ = "Judo Framework Team"

# Main exports
__all__ = [
    "Judo",
    "JudoResponse", 
    "Matcher",
    "VariableManager",
    "HttpClient",
    "MockServer",
    "JudoReporter",
    "HTMLReporter",
    "BaseRunner",
    "TestSuite",
    "CommonSuites"
]

# Behave integration is available via judo.behave module
# Reporting is available via judo.reporting module
# Runners are available via judo.runner module