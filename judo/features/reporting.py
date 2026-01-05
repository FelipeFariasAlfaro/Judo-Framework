"""
Advanced Report Generation
Multiple report formats (HTML, JSON, JUnit, Allure)
"""

import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """Generate reports in multiple formats"""
    
    def __init__(self, test_results: List[Dict[str, Any]]):
        """
        Initialize report generator
        
        Args:
            test_results: List of test result dictionaries
        """
        self.test_results = test_results
        self.timestamp = datetime.now()
    
    def generate_json(self, output_file: str):
        """Generate JSON report"""
        report = {
            "timestamp": self.timestamp.isoformat(),
            "total_tests": len(self.test_results),
            "passed": sum(1 for r in self.test_results if r.get("status") == "passed"),
            "failed": sum(1 for r in self.test_results if r.get("status") == "failed"),
            "skipped": sum(1 for r in self.test_results if r.get("status") == "skipped"),
            "tests": self.test_results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"✅ JSON report generated: {output_file}")
    
    def generate_junit(self, output_file: str):
        """Generate JUnit XML report"""
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r.get("status") == "passed")
        failed = total - passed
        
        testsuites = ET.Element("testsuites")
        testsuite = ET.SubElement(testsuites, "testsuite")
        testsuite.set("name", "Judo Framework Tests")
        testsuite.set("tests", str(total))
        testsuite.set("failures", str(failed))
        testsuite.set("timestamp", self.timestamp.isoformat())
        
        for result in self.test_results:
            testcase = ET.SubElement(testsuite, "testcase")
            testcase.set("name", result.get("name", "Unknown"))
            testcase.set("time", str(result.get("duration", 0)))
            
            if result.get("status") == "failed":
                failure = ET.SubElement(testcase, "failure")
                failure.set("message", result.get("error", "Test failed"))
                failure.text = result.get("error_details", "")
            elif result.get("status") == "skipped":
                ET.SubElement(testcase, "skipped")
        
        tree = ET.ElementTree(testsuites)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f"✅ JUnit report generated: {output_file}")
    
    def generate_allure(self, output_dir: str):
        """Generate Allure report structure"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Create allure-results directory
        results_dir = Path(output_dir) / "allure-results"
        results_dir.mkdir(exist_ok=True)
        
        # Generate test results
        for idx, result in enumerate(self.test_results):
            test_result = {
                "uuid": f"test-{idx}",
                "name": result.get("name", f"Test {idx}"),
                "status": result.get("status", "unknown"),
                "start": int(self.timestamp.timestamp() * 1000),
                "stop": int(self.timestamp.timestamp() * 1000) + int(result.get("duration", 0) * 1000),
                "duration": int(result.get("duration", 0) * 1000),
                "description": result.get("description", ""),
                "labels": [
                    {"name": "suite", "value": "API Tests"},
                    {"name": "severity", "value": "normal"}
                ]
            }
            
            if result.get("error"):
                test_result["statusDetails"] = {
                    "message": result.get("error"),
                    "trace": result.get("error_details", "")
                }
            
            # Write test result
            result_file = results_dir / f"test-result-{idx}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(test_result, f, indent=2)
        
        print(f"✅ Allure report structure generated: {output_dir}")
    
    def generate_html(self, output_file: str):
        """Generate HTML report"""
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r.get("status") == "passed")
        failed = total - passed
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Judo Framework Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
                .stat {{ padding: 15px; border-radius: 5px; color: white; }}
                .passed {{ background-color: #4CAF50; }}
                .failed {{ background-color: #f44336; }}
                .total {{ background-color: #2196F3; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f0f0f0; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .status-passed {{ color: #4CAF50; font-weight: bold; }}
                .status-failed {{ color: #f44336; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🥋 Judo Framework Test Report</h1>
                <p>Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <div class="stat total">
                    <h3>Total Tests</h3>
                    <p>{total}</p>
                </div>
                <div class="stat passed">
                    <h3>Passed</h3>
                    <p>{passed}</p>
                </div>
                <div class="stat failed">
                    <h3>Failed</h3>
                    <p>{failed}</p>
                </div>
                <div class="stat">
                    <h3 style="color: #333;">Pass Rate</h3>
                    <p style="color: #333;">{pass_rate:.1f}%</p>
                </div>
            </div>
            
            <table>
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Duration (ms)</th>
                    <th>Error</th>
                </tr>
        """
        
        for result in self.test_results:
            status = result.get("status", "unknown")
            status_class = f"status-{status}"
            error = result.get("error", "")
            duration = result.get("duration", 0) * 1000
            
            html += f"""
                <tr>
                    <td>{result.get("name", "Unknown")}</td>
                    <td class="{status_class}">{status.upper()}</td>
                    <td>{duration:.2f}</td>
                    <td>{error}</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ HTML report generated: {output_file}")
    
    def generate_all(self, output_dir: str):
        """Generate all report formats"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        self.generate_json(f"{output_dir}/report.json")
        self.generate_junit(f"{output_dir}/report.xml")
        self.generate_html(f"{output_dir}/report.html")
        self.generate_allure(output_dir)
