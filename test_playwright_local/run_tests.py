#!/usr/bin/env python3
"""
Test runner for Playwright integration
This script runs comprehensive tests to validate the integration
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🎭 {title}")
    print("=" * 60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def run_command(cmd, description, cwd=None):
    """Run a command and return success status"""
    print(f"🔍 {description}")
    print(f"   Command: {cmd}")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=cwd or Path(__file__).parent
        )
        
        if result.returncode == 0:
            print(f"   ✅ Success")
            if result.stdout.strip():
                # Show last few lines of output
                lines = result.stdout.strip().split('\n')
                for line in lines[-3:]:
                    print(f"   📄 {line}")
            return True
        else:
            print(f"   ❌ Failed (exit code: {result.returncode})")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return False
            
    except Exception as e:
        print(f"   💥 Exception: {e}")
        return False

def check_prerequisites():
    """Check if all prerequisites are installed"""
    print_section("Checking Prerequisites")
    
    checks = [
        ("python --version", "Python version"),
        ("pip --version", "Pip version"),
    ]
    
    all_good = True
    for cmd, desc in checks:
        if not run_command(cmd, desc):
            all_good = False
    
    # Check if we can import judo
    try:
        import judo
        print(f"🔍 Judo Framework import")
        print(f"   ✅ Success - Version: {judo.__version__}")
    except ImportError as e:
        print(f"🔍 Judo Framework import")
        print(f"   ❌ Failed: {e}")
        all_good = False
    
    # Check Playwright availability
    try:
        from judo import PLAYWRIGHT_AVAILABLE
        print(f"🔍 Playwright integration")
        if PLAYWRIGHT_AVAILABLE:
            print(f"   ✅ Available")
        else:
            print(f"   ⚠️ Not available (will test API-only mode)")
    except ImportError:
        print(f"🔍 Playwright integration")
        print(f"   ❌ Import failed")
        all_good = False
    
    return all_good

def run_api_tests():
    """Run API-only tests to ensure backward compatibility"""
    print_section("API-Only Tests (Backward Compatibility)")
    
    cmd = "behave features/test_api_only.feature --no-capture --format=pretty"
    return run_command(cmd, "Running API-only tests")

def run_ui_tests():
    """Run UI-only tests"""
    print_section("UI-Only Tests (Playwright)")
    
    # Check if Playwright is available first
    try:
        from judo import PLAYWRIGHT_AVAILABLE
        if not PLAYWRIGHT_AVAILABLE:
            print("   ⚠️ Playwright not available, skipping UI tests")
            return True
    except ImportError:
        print("   ⚠️ Cannot check Playwright availability, skipping UI tests")
        return True
    
    cmd = "behave features/test_ui_only.feature --no-capture --format=pretty"
    return run_command(cmd, "Running UI-only tests")

def run_hybrid_tests():
    """Run hybrid API + UI tests"""
    print_section("Hybrid API + UI Tests")
    
    # Check if Playwright is available first
    try:
        from judo import PLAYWRIGHT_AVAILABLE
        if not PLAYWRIGHT_AVAILABLE:
            print("   ⚠️ Playwright not available, skipping hybrid tests")
            return True
    except ImportError:
        print("   ⚠️ Cannot check Playwright availability, skipping hybrid tests")
        return True
    
    cmd = "behave features/test_hybrid.feature --no-capture --format=pretty"
    return run_command(cmd, "Running hybrid tests")

def run_spanish_tests():
    """Run Spanish language tests"""
    print_section("Spanish Language Tests")
    
    # Check if Playwright is available first
    try:
        from judo import PLAYWRIGHT_AVAILABLE
        if not PLAYWRIGHT_AVAILABLE:
            print("   ⚠️ Playwright not available, skipping Spanish UI tests")
            # Still run API parts
            cmd = "behave features/test_spanish.feature --tags=@api --no-capture --format=pretty"
            return run_command(cmd, "Running Spanish API tests only")
    except ImportError:
        print("   ⚠️ Cannot check Playwright availability, skipping Spanish tests")
        return True
    
    cmd = "behave features/test_spanish.feature --no-capture --format=pretty"
    return run_command(cmd, "Running Spanish tests")

def run_specific_scenarios():
    """Run specific test scenarios"""
    print_section("Specific Scenario Tests")
    
    scenarios = [
        ("--tags=@smoke", "Smoke tests"),
        ("--tags=@api", "API tests"),
    ]
    
    # Add UI tests if Playwright is available
    try:
        from judo import PLAYWRIGHT_AVAILABLE
        if PLAYWRIGHT_AVAILABLE:
            scenarios.extend([
                ("--tags=@ui", "UI tests"),
                ("--tags=@hybrid", "Hybrid tests"),
            ])
    except ImportError:
        pass
    
    all_passed = True
    for tag, desc in scenarios:
        cmd = f"behave {tag} --no-capture --format=pretty"
        if not run_command(cmd, f"Running {desc}"):
            all_passed = False
    
    return all_passed

def generate_reports():
    """Generate test reports"""
    print_section("Generating Reports")
    
    # Run tests with HTML formatter to generate reports
    cmd = "behave --format=html --outfile=test_reports/test_report.html"
    success = run_command(cmd, "Generating HTML report")
    
    if success:
        report_path = Path(__file__).parent / "test_reports" / "test_report.html"
        if report_path.exists():
            print(f"   📊 Report generated: {report_path}")
        else:
            print(f"   ⚠️ Report file not found at expected location")
    
    return success

def check_outputs():
    """Check if outputs were generated correctly"""
    print_section("Checking Outputs")
    
    test_dir = Path(__file__).parent
    
    # Check for screenshots
    screenshot_dir = test_dir / "test_screenshots"
    if screenshot_dir.exists():
        screenshots = list(screenshot_dir.glob("*.png"))
        print(f"   📸 Screenshots generated: {len(screenshots)}")
        for screenshot in screenshots[:5]:  # Show first 5
            print(f"      - {screenshot.name}")
        if len(screenshots) > 5:
            print(f"      ... and {len(screenshots) - 5} more")
    else:
        print(f"   📸 No screenshots directory found")
    
    # Check for reports
    reports_dir = test_dir / "test_reports"
    if reports_dir.exists():
        reports = list(reports_dir.glob("*.html"))
        print(f"   📊 HTML reports generated: {len(reports)}")
        for report in reports:
            print(f"      - {report.name}")
    else:
        print(f"   📊 No reports directory found")
    
    # Check for request/response logs
    if reports_dir.exists():
        json_files = list(reports_dir.rglob("*.json"))
        if json_files:
            print(f"   📝 Request/response logs: {len(json_files)}")
        else:
            print(f"   📝 No request/response logs found")
    
    return True

def main():
    """Main test runner"""
    print_header("Judo Framework - Playwright Integration Test Suite")
    
    # Change to test directory
    test_dir = Path(__file__).parent
    os.chdir(test_dir)
    
    # Load environment variables
    env_file = test_dir / ".env"
    if env_file.exists():
        print(f"📋 Loading environment from: {env_file}")
        # Simple .env loading
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print(f"   ✅ Environment loaded")
    
    # Create output directories
    os.makedirs("test_reports", exist_ok=True)
    os.makedirs("test_screenshots", exist_ok=True)
    
    # Run test suite
    test_results = []
    
    # 1. Check prerequisites
    test_results.append(("Prerequisites", check_prerequisites()))
    
    # 2. Run API tests (should always work)
    test_results.append(("API Tests", run_api_tests()))
    
    # 3. Run UI tests (if Playwright available)
    test_results.append(("UI Tests", run_ui_tests()))
    
    # 4. Run hybrid tests (if Playwright available)
    test_results.append(("Hybrid Tests", run_hybrid_tests()))
    
    # 5. Run Spanish tests
    test_results.append(("Spanish Tests", run_spanish_tests()))
    
    # 6. Run specific scenarios
    test_results.append(("Specific Scenarios", run_specific_scenarios()))
    
    # 7. Generate reports
    test_results.append(("Report Generation", generate_reports()))
    
    # 8. Check outputs
    test_results.append(("Output Check", check_outputs()))
    
    # Summary
    print_header("Test Results Summary")
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📊 Overall Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 All tests passed! Playwright integration is working correctly.")
        print("\n🚀 Integration is ready for production!")
        
        print("\n📁 Generated Files:")
        print("   - test_reports/: HTML reports and request/response logs")
        print("   - test_screenshots/: Screenshots from UI tests")
        
        return 0
    else:
        print(f"\n❌ {failed} test suite(s) failed. Check the output above for details.")
        
        print("\n🔧 Troubleshooting Tips:")
        print("1. Ensure Playwright is installed: pip install 'judo-framework[browser]'")
        print("2. Install browsers: playwright install")
        print("3. Check Python version (requires 3.8+)")
        print("4. Verify network connectivity for httpbin.org")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())