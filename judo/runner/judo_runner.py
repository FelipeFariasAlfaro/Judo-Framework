"""
Judo Runner - Main test runner implementation
"""

from typing import List, Dict, Any, Optional
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..core.judo import Judo


class JudoRunner:
    """
    Main Judo test runner for executing tests with tags and parallel execution
    """
    
    def __init__(self, parallel: bool = False, max_workers: int = 4):
        """
        Initialize Judo Runner
        
        Args:
            parallel: Enable parallel execution
            max_workers: Maximum number of parallel workers
        """
        self.parallel = parallel
        self.max_workers = max_workers
        self.judo = Judo()
        self.results = []
    
    def run_behave(self, tags: List[str] = None, exclude_tags: List[str] = None, 
                   features_path: str = "features") -> Dict[str, Any]:
        """
        Run Behave tests with specified tags
        
        Args:
            tags: List of tags to include (e.g., ["@smoke", "@api"])
            exclude_tags: List of tags to exclude
            features_path: Path to features directory
            
        Returns:
            Dict with execution results
        """
        cmd = ["behave", features_path]
        
        # Add tags
        if tags:
            for tag in tags:
                cmd.extend(["--tags", tag])
        
        # Add exclude tags
        if exclude_tags:
            for tag in exclude_tags:
                cmd.extend(["--tags", f"~{tag}"])
        
        # Add parallel execution if enabled
        if self.parallel:
            cmd.extend(["--processes", str(self.max_workers)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "returncode": -1
            }
    
    def set_parallel(self, enabled: bool, max_workers: int = None):
        """Set parallel execution settings"""
        self.parallel = enabled
        if max_workers:
            self.max_workers = max_workers