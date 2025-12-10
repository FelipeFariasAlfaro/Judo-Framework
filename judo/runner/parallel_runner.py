"""
Parallel Runner - Execute tests in parallel
"""

from typing import List, Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class ParallelRunner:
    """
    Runner for executing tests in parallel
    """
    
    def __init__(self, max_workers: int = 4):
        """
        Initialize Parallel Runner
        
        Args:
            max_workers: Maximum number of parallel workers
        """
        self.max_workers = max_workers
        self.results = []
    
    def run_parallel(self, test_functions: List[Callable], *args, **kwargs) -> List[Dict[str, Any]]:
        """
        Run test functions in parallel
        
        Args:
            test_functions: List of test functions to execute
            
        Returns:
            List of results from each test function
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all test functions
            future_to_test = {
                executor.submit(test_func, *args, **kwargs): test_func 
                for test_func in test_functions
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_test):
                test_func = future_to_test[future]
                try:
                    result = future.result()
                    results.append({
                        "test_function": test_func.__name__,
                        "success": True,
                        "result": result,
                        "timestamp": time.time()
                    })
                except Exception as e:
                    results.append({
                        "test_function": test_func.__name__,
                        "success": False,
                        "error": str(e),
                        "timestamp": time.time()
                    })
        
        self.results.extend(results)
        return results