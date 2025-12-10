"""
Core module - Main framework components
"""

from .judo import Judo
from .response import JudoResponse
from .matcher import Matcher
from .variables import VariableManager

__all__ = ['Judo', 'JudoResponse', 'Matcher', 'VariableManager']