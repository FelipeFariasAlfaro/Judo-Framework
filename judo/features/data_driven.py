"""
Data-Driven Testing
Support for CSV, JSON, Excel data sources
"""

import csv
import json
from typing import List, Dict, Any, Callable, Optional, Union
from pathlib import Path


class DataDrivenTesting:
    """Data-driven testing utilities"""
    
    @staticmethod
    def load_csv(file_path: str) -> List[Dict[str, str]]:
        """
        Load test data from CSV file
        
        Args:
            file_path: Path to CSV file
        
        Returns:
            List of dictionaries with row data
        """
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    
    @staticmethod
    def load_json(file_path: str) -> Union[List[Dict], Dict]:
        """
        Load test data from JSON file
        
        Args:
            file_path: Path to JSON file
        
        Returns:
            Parsed JSON data
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def load_excel(file_path: str, sheet_name: str = 0) -> List[Dict[str, Any]]:
        """
        Load test data from Excel file
        
        Args:
            file_path: Path to Excel file
            sheet_name: Sheet name or index
        
        Returns:
            List of dictionaries with row data
        """
        try:
            import openpyxl
        except ImportError:
            raise ImportError("openpyxl required: pip install openpyxl")
        
        workbook = openpyxl.load_workbook(file_path)
        worksheet = workbook[sheet_name] if isinstance(sheet_name, str) else workbook.worksheets[sheet_name]
        
        data = []
        headers = None
        
        for row_idx, row in enumerate(worksheet.iter_rows(values_only=True)):
            if row_idx == 0:
                headers = row
            else:
                if headers:
                    row_dict = {headers[i]: row[i] for i in range(len(headers))}
                    data.append(row_dict)
        
        return data
    
    @staticmethod
    def run_with_data_source(
        data_source: Union[str, List[Dict]],
        test_func: Callable,
        source_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Run test function with data from source
        
        Args:
            data_source: File path or list of data dictionaries
            test_func: Function to run for each data row
            source_type: Type of source ('csv', 'json', 'excel') - auto-detected if not provided
        
        Returns:
            List of results for each test run
        """
        # Load data
        if isinstance(data_source, str):
            if source_type is None:
                # Auto-detect from file extension
                ext = Path(data_source).suffix.lower()
                source_type = ext.lstrip('.')
            
            if source_type == 'csv':
                data = DataDrivenTesting.load_csv(data_source)
            elif source_type == 'json':
                data = DataDrivenTesting.load_json(data_source)
            elif source_type == 'excel' or source_type in ['xlsx', 'xls']:
                data = DataDrivenTesting.load_excel(data_source)
            else:
                raise ValueError(f"Unknown source type: {source_type}")
        else:
            data = data_source
        
        # Run tests
        results = []
        for idx, row_data in enumerate(data):
            try:
                result = test_func(row_data, idx)
                results.append({
                    "index": idx,
                    "data": row_data,
                    "result": result,
                    "status": "passed",
                    "error": None
                })
            except Exception as e:
                results.append({
                    "index": idx,
                    "data": row_data,
                    "result": None,
                    "status": "failed",
                    "error": str(e)
                })
        
        return results
    
    @staticmethod
    def generate_test_data(
        count: int,
        template: Dict[str, Callable],
        seed: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate test data using template with generators
        
        Args:
            count: Number of test cases to generate
            template: Dict with field names and generator functions
            seed: Random seed for reproducibility
        
        Returns:
            List of generated test data dictionaries
        """
        if seed is not None:
            import random
            random.seed(seed)
        
        data = []
        for _ in range(count):
            row = {}
            for field_name, generator in template.items():
                if callable(generator):
                    row[field_name] = generator()
                else:
                    row[field_name] = generator
            data.append(row)
        
        return data
    
    @staticmethod
    def save_results(results: List[Dict], output_file: str, format: str = 'json'):
        """
        Save test results to file
        
        Args:
            results: List of test results
            output_file: Output file path
            format: Output format ('json' or 'csv')
        """
        if format == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str)
        elif format == 'csv':
            if not results:
                return
            
            # Flatten results for CSV
            flattened = []
            for result in results:
                flat_row = {
                    'index': result['index'],
                    'status': result['status'],
                    'error': result['error'] or ''
                }
                # Add data fields
                if isinstance(result['data'], dict):
                    flat_row.update(result['data'])
                flattened.append(flat_row)
            
            # Write CSV
            if flattened:
                keys = flattened[0].keys()
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(flattened)
        else:
            raise ValueError(f"Unknown format: {format}")
    
    @staticmethod
    def get_summary(results: List[Dict]) -> Dict[str, Any]:
        """Get summary statistics from results"""
        total = len(results)
        passed = sum(1 for r in results if r['status'] == 'passed')
        failed = total - passed
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "fail_rate": (failed / total * 100) if total > 0 else 0
        }
