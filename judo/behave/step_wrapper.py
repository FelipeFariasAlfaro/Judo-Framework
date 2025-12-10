"""
Step Wrapper - Automatically capture step execution for reporting
"""

import functools
import traceback
from ..reporting.reporter import get_reporter
from ..reporting.report_data import StepStatus


def capture_step(step_func):
    """Decorator to capture step execution for reporting"""
    
    @functools.wraps(step_func)
    def wrapper(context, *args, **kwargs):
        reporter = get_reporter()
        
        # Extract step text from the function and arguments
        step_text = _build_step_text(step_func, args)
        
        # Start step in reporter
        reporter.start_step(step_text)
        
        try:
            # Execute the step
            result = step_func(context, *args, **kwargs)
            
            # Mark step as passed
            reporter.finish_step(StepStatus.PASSED)
            
            return result
            
        except Exception as e:
            # Mark step as failed
            error_message = str(e)
            error_traceback = traceback.format_exc()
            reporter.finish_step(StepStatus.FAILED, error_message, error_traceback)
            
            # Re-raise the exception
            raise
    
    return wrapper


def _build_step_text(step_func, args):
    """Build step text from function name and arguments"""
    # Get the step pattern from the function's step decorator
    if hasattr(step_func, 'pattern'):
        pattern = step_func.pattern
        # Try to substitute arguments into the pattern
        try:
            return pattern.format(*args)
        except:
            return f"{step_func.__name__}({', '.join(map(str, args))})"
    else:
        return f"{step_func.__name__}({', '.join(map(str, args))})"