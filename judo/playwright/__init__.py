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

# Only expose classes if Playwright is available
if PLAYWRIGHT_AVAILABLE:
    from .browser_context import JudoBrowserContext
    from .steps import *  # Import all Playwright steps
    from .page_manager import PageManager
    
    __all__ = ['JudoBrowserContext', 'PageManager', 'PLAYWRIGHT_AVAILABLE']
else:
    __all__ = ['PLAYWRIGHT_AVAILABLE']

def check_playwright_availability():
    """Check if Playwright is available and properly installed"""
    if not PLAYWRIGHT_AVAILABLE:
        raise ImportError(
            "Playwright is not installed. Install it with:\n"
            "pip install 'judo-framework[browser]' or pip install playwright\n"
            "Then run: playwright install"
        )
    
    # Check if browsers are installed
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # Try to get browser info - this will fail if browsers aren't installed
            browsers = []
            try:
                browsers.append(p.chromium.name)
            except:
                pass
            try:
                browsers.append(p.firefox.name)
            except:
                pass
            try:
                browsers.append(p.webkit.name)
            except:
                pass
            
            if not browsers:
                raise RuntimeError(
                    "No Playwright browsers are installed. Run:\n"
                    "playwright install"
                )
                
    except Exception as e:
        raise RuntimeError(
            f"Playwright installation issue: {e}\n"
            "Try running: playwright install"
        )