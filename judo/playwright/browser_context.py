"""
Browser Context Integration for Judo Framework
Extends JudoContext with Playwright browser capabilities
"""

import os
from typing import Any, Dict, Optional, Union
from ..behave.context import JudoContext

# Check Playwright availability
try:
    import playwright
    from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class JudoBrowserContext(JudoContext):
    """
    Enhanced Judo context with Playwright browser capabilities
    Maintains full compatibility with API testing while adding UI testing
    """
    
    def __init__(self, behave_context=None):
        """Initialize Judo browser context"""
        super().__init__(behave_context)
        
        # Browser-related attributes
        self.playwright: Optional['Playwright'] = None
        self.browser: Optional['Browser'] = None
        self.browser_context: Optional['BrowserContext'] = None
        self.page: Optional['Page'] = None
        self.pages: Dict[str, 'Page'] = {}  # Named pages for multi-page scenarios
        
        # Browser configuration
        self.browser_type = 'chromium'  # Default browser
        self.headless = True  # Default to headless
        self.browser_options = {}
        self.context_options = {}
        
        # UI testing state
        self.current_page_name = 'main'
        self.screenshots_enabled = False
        self.screenshot_on_failure = True
        self.screenshot_directory = None
        
        # Initialize browser configuration from environment
        self._setup_browser_defaults()
    
    def _setup_browser_defaults(self):
        """Setup default browser configuration from environment variables"""
        # Browser type
        self.browser_type = os.getenv('JUDO_BROWSER', 'chromium').lower()
        
        # Headless mode
        self.headless = os.getenv('JUDO_HEADLESS', 'true').lower() == 'true'
        
        # Screenshots
        self.screenshots_enabled = os.getenv('JUDO_SCREENSHOTS', 'false').lower() == 'true'
        self.screenshot_on_failure = os.getenv('JUDO_SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
        self.screenshot_directory = os.getenv('JUDO_SCREENSHOT_DIR', 'judo_screenshots')
        
        # Browser options from environment
        if os.getenv('JUDO_BROWSER_ARGS'):
            args = os.getenv('JUDO_BROWSER_ARGS').split(',')
            self.browser_options['args'] = [arg.strip() for arg in args]
        
        # Viewport size
        viewport_width = os.getenv('JUDO_VIEWPORT_WIDTH', '1280')
        viewport_height = os.getenv('JUDO_VIEWPORT_HEIGHT', '720')
        self.context_options['viewport'] = {
            'width': int(viewport_width),
            'height': int(viewport_height)
        }
        
        # User agent
        if os.getenv('JUDO_USER_AGENT'):
            self.context_options['user_agent'] = os.getenv('JUDO_USER_AGENT')
    
    # Browser Lifecycle Management
    def start_browser(self, browser_type: str = None, headless: bool = None, **options):
        """
        Start Playwright browser
        
        Args:
            browser_type: 'chromium', 'firefox', or 'webkit'
            headless: True for headless mode, False for headed
            **options: Additional browser options
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright is not installed. Install it with:\n"
                "pip install 'judo-framework[browser]' or pip install playwright\n"
                "Then run: playwright install"
            )
        
        if self.playwright is None:
            self.playwright = sync_playwright().start()
        
        # Use provided values or defaults
        browser_type = browser_type or self.browser_type
        headless = headless if headless is not None else self.headless
        
        # Merge options
        browser_options = {**self.browser_options, **options}
        browser_options['headless'] = headless
        
        # Get browser launcher
        if browser_type == 'chromium':
            browser_launcher = self.playwright.chromium
        elif browser_type == 'firefox':
            browser_launcher = self.playwright.firefox
        elif browser_type == 'webkit':
            browser_launcher = self.playwright.webkit
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        
        # Launch browser
        self.browser = browser_launcher.launch(**browser_options)
        self.browser_type = browser_type
        
        # Log browser start
        self.log(f"Started {browser_type} browser (headless={headless})")
    
    def create_browser_context(self, **options):
        """
        Create new browser context
        
        Args:
            **options: Browser context options (viewport, user_agent, etc.)
        """
        if not self.browser:
            self.start_browser()
        
        # Merge context options
        context_options = {**self.context_options, **options}
        
        # Create context
        self.browser_context = self.browser.new_context(**context_options)
        
        # Enable request/response interception if API logging is enabled
        if self.save_requests_responses:
            self._setup_network_interception()
        
        self.log("Created new browser context")
    
    def new_page(self, name: str = None) -> 'Page':
        """
        Create new page
        
        Args:
            name: Optional name for the page (default: 'main')
            
        Returns:
            Playwright Page object
        """
        if not self.browser_context:
            self.create_browser_context()
        
        page = self.browser_context.new_page()
        page_name = name or self.current_page_name
        
        # Store page reference
        self.pages[page_name] = page
        self.page = page  # Set as current page
        self.current_page_name = page_name
        
        # Setup page event handlers
        self._setup_page_handlers(page)
        
        self.log(f"Created new page: {page_name}")
        return page
    
    def switch_to_page(self, name: str):
        """Switch to a named page"""
        if name not in self.pages:
            raise ValueError(f"Page '{name}' not found. Available pages: {list(self.pages.keys())}")
        
        self.page = self.pages[name]
        self.current_page_name = name
        self.log(f"Switched to page: {name}")
    
    def close_page(self, name: str = None):
        """Close a page"""
        page_name = name or self.current_page_name
        
        if page_name in self.pages:
            self.pages[page_name].close()
            del self.pages[page_name]
            
            # If we closed the current page, switch to another one or clear
            if page_name == self.current_page_name:
                if self.pages:
                    # Switch to first available page
                    first_page_name = list(self.pages.keys())[0]
                    self.switch_to_page(first_page_name)
                else:
                    self.page = None
                    self.current_page_name = None
            
            self.log(f"Closed page: {page_name}")
    
    def close_browser(self):
        """Close browser and cleanup"""
        if self.browser_context:
            self.browser_context.close()
            self.browser_context = None
        
        if self.browser:
            self.browser.close()
            self.browser = None
        
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
        
        # Clear page references
        self.pages.clear()
        self.page = None
        self.current_page_name = None
        
        self.log("Closed browser")
    
    def _setup_page_handlers(self, page: 'Page'):
        """Setup event handlers for a page"""
        # Console message handler
        def handle_console(msg):
            if os.getenv('JUDO_LOG_CONSOLE', 'false').lower() == 'true':
                self.log(f"Browser Console [{msg.type}]: {msg.text}", "DEBUG")
        
        page.on("console", handle_console)
        
        # Page error handler
        def handle_page_error(error):
            self.log(f"Page Error: {error}", "ERROR")
        
        page.on("pageerror", handle_page_error)
        
        # Request/Response handlers for API integration
        if self.save_requests_responses:
            def handle_request(request):
                # Log browser requests if enabled
                if os.getenv('JUDO_LOG_BROWSER_REQUESTS', 'false').lower() == 'true':
                    self.log(f"Browser Request: {request.method} {request.url}", "DEBUG")
            
            def handle_response(response):
                # Log browser responses if enabled
                if os.getenv('JUDO_LOG_BROWSER_RESPONSES', 'false').lower() == 'true':
                    self.log(f"Browser Response: {response.status} {response.url}", "DEBUG")
            
            page.on("request", handle_request)
            page.on("response", handle_response)
    
    def _setup_network_interception(self):
        """Setup network interception for API request logging"""
        # This could be extended to capture browser API calls
        # and integrate them with the existing request/response logging
        pass
    
    # Page Navigation
    def navigate_to(self, url: str, **options):
        """
        Navigate to URL
        
        Args:
            url: URL to navigate to
            **options: Navigation options (wait_until, timeout, etc.)
        """
        if not self.page:
            self.new_page()
        
        # Interpolate URL with variables
        url = self.interpolate_string(url)
        
        # Default options
        nav_options = {'wait_until': 'domcontentloaded', **options}
        
        # Navigate
        response = self.page.goto(url, **nav_options)
        
        # Log navigation
        self.log(f"Navigated to: {url}")
        
        # Take screenshot if enabled
        if self.screenshots_enabled:
            self.take_screenshot(f"navigate_to_{self._sanitize_filename(url)}")
        
        return response
    
    def reload_page(self, **options):
        """Reload current page"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        response = self.page.reload(**options)
        self.log("Page reloaded")
        return response
    
    def go_back(self, **options):
        """Go back in browser history"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        response = self.page.go_back(**options)
        self.log("Navigated back")
        return response
    
    def go_forward(self, **options):
        """Go forward in browser history"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        response = self.page.go_forward(**options)
        self.log("Navigated forward")
        return response
    
    # Element Interaction
    def click_element(self, selector: str, **options):
        """Click an element"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        # Interpolate selector with variables
        selector = self.interpolate_string(selector)
        
        # Click element
        self.page.click(selector, **options)
        self.log(f"Clicked element: {selector}")
        
        # Take screenshot if enabled
        if self.screenshots_enabled:
            self.take_screenshot(f"click_{self._sanitize_filename(selector)}")
    
    def fill_input(self, selector: str, value: str, **options):
        """Fill an input field"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        # Interpolate selector and value with variables
        selector = self.interpolate_string(selector)
        value = self.interpolate_string(value)
        
        # Fill input
        self.page.fill(selector, value, **options)
        self.log(f"Filled input {selector} with: {value}")
    
    def type_text(self, selector: str, text: str, **options):
        """Type text into an element"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        # Interpolate selector and text with variables
        selector = self.interpolate_string(selector)
        text = self.interpolate_string(text)
        
        # Type text
        self.page.type(selector, text, **options)
        self.log(f"Typed text in {selector}: {text}")
    
    def select_option(self, selector: str, value: Union[str, list], **options):
        """Select option(s) in a select element"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        # Interpolate selector with variables
        selector = self.interpolate_string(selector)
        
        # Handle single value or list of values
        if isinstance(value, str):
            value = self.interpolate_string(value)
        elif isinstance(value, list):
            value = [self.interpolate_string(v) for v in value]
        
        # Select option(s)
        self.page.select_option(selector, value, **options)
        self.log(f"Selected option in {selector}: {value}")
    
    def check_checkbox(self, selector: str, **options):
        """Check a checkbox"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        selector = self.interpolate_string(selector)
        self.page.check(selector, **options)
        self.log(f"Checked checkbox: {selector}")
    
    def uncheck_checkbox(self, selector: str, **options):
        """Uncheck a checkbox"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        selector = self.interpolate_string(selector)
        self.page.uncheck(selector, **options)
        self.log(f"Unchecked checkbox: {selector}")
    
    # Element Queries and Validation
    def get_element_text(self, selector: str, **options) -> str:
        """Get text content of an element"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        selector = self.interpolate_string(selector)
        text = self.page.text_content(selector, **options)
        self.log(f"Got text from {selector}: {text}")
        return text or ""
    
    def get_element_attribute(self, selector: str, attribute: str, **options) -> Optional[str]:
        """Get attribute value of an element"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        selector = self.interpolate_string(selector)
        attribute = self.interpolate_string(attribute)
        
        value = self.page.get_attribute(selector, attribute, **options)
        self.log(f"Got attribute {attribute} from {selector}: {value}")
        return value
    
    def is_element_visible(self, selector: str, **options) -> bool:
        """Check if element is visible"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        selector = self.interpolate_string(selector)
        visible = self.page.is_visible(selector, **options)
        self.log(f"Element {selector} visible: {visible}")
        return visible
    
    def is_element_enabled(self, selector: str, **options) -> bool:
        """Check if element is enabled"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        selector = self.interpolate_string(selector)
        enabled = self.page.is_enabled(selector, **options)
        self.log(f"Element {selector} enabled: {enabled}")
        return enabled
    
    def wait_for_element(self, selector: str, state: str = 'visible', **options):
        """Wait for element to reach specified state"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        selector = self.interpolate_string(selector)
        self.page.wait_for_selector(selector, state=state, **options)
        self.log(f"Waited for element {selector} to be {state}")
    
    def wait_for_url(self, url_pattern: str, **options):
        """Wait for URL to match pattern"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        url_pattern = self.interpolate_string(url_pattern)
        self.page.wait_for_url(url_pattern, **options)
        self.log(f"Waited for URL pattern: {url_pattern}")
    
    # Screenshots and Visual Testing
    def take_screenshot(self, name: str = None, attach_to_report: bool = True, **options):
        """
        Take a screenshot
        
        Args:
            name: Screenshot name (auto-generated if not provided)
            attach_to_report: If True, automatically attach to HTML report
            **options: Additional Playwright screenshot options
        
        Returns:
            str: Path to the screenshot file
        """
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        # Generate filename
        if not name:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}"
        
        # Ensure screenshot directory exists
        screenshot_dir = self.screenshot_directory or 'judo_screenshots'
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # Create full path
        filename = f"{name}.png"
        filepath = os.path.join(screenshot_dir, filename)
        
        # Take screenshot
        self.page.screenshot(path=filepath, **options)
        self.log(f"Screenshot saved: {filepath}")
        
        # Attach to reporter if enabled
        if attach_to_report:
            try:
                from ..reporting.reporter import get_reporter
                reporter = get_reporter()
                if reporter and reporter.current_step:
                    reporter.attach_screenshot(filepath)
                    self.log(f"Screenshot attached to report")
            except Exception as e:
                self.log(f"Warning: Could not attach screenshot to report: {e}")
        
        return filepath
    
    def take_element_screenshot(self, selector: str, name: str = None, **options):
        """Take screenshot of specific element"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        selector = self.interpolate_string(selector)
        
        # Generate filename
        if not name:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"element_{self._sanitize_filename(selector)}_{timestamp}"
        
        # Ensure screenshot directory exists
        screenshot_dir = self.screenshot_directory or 'judo_screenshots'
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # Create full path
        filename = f"{name}.png"
        filepath = os.path.join(screenshot_dir, filename)
        
        # Take element screenshot
        element = self.page.locator(selector)
        element.screenshot(path=filepath, **options)
        self.log(f"Element screenshot saved: {filepath}")
        
        return filepath
    
    # JavaScript Execution
    def execute_javascript(self, script: str, *args):
        """Execute JavaScript in the page"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        script = self.interpolate_string(script)
        result = self.page.evaluate(script, *args)
        self.log(f"Executed JavaScript: {script[:100]}...")
        return result
    
    # Cookie Management
    def get_cookies(self) -> list:
        """Get all cookies"""
        if not self.browser_context:
            raise RuntimeError("No browser context available.")
        
        cookies = self.browser_context.cookies()
        self.log(f"Retrieved {len(cookies)} cookies")
        return cookies
    
    def add_cookie(self, cookie: dict):
        """Add a cookie"""
        if not self.browser_context:
            raise RuntimeError("No browser context available.")
        
        self.browser_context.add_cookies([cookie])
        self.log(f"Added cookie: {cookie.get('name', 'unknown')}")
    
    def clear_cookies(self):
        """Clear all cookies"""
        if not self.browser_context:
            raise RuntimeError("No browser context available.")
        
        self.browser_context.clear_cookies()
        self.log("Cleared all cookies")
    
    # Local Storage and Session Storage
    def set_local_storage(self, key: str, value: str):
        """Set local storage item"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        key = self.interpolate_string(key)
        value = self.interpolate_string(value)
        
        self.page.evaluate(f"localStorage.setItem('{key}', '{value}')")
        self.log(f"Set localStorage[{key}] = {value}")
    
    def get_local_storage(self, key: str) -> Optional[str]:
        """Get local storage item"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        key = self.interpolate_string(key)
        value = self.page.evaluate(f"localStorage.getItem('{key}')")
        self.log(f"Got localStorage[{key}] = {value}")
        return value
    
    def clear_local_storage(self):
        """Clear local storage"""
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        self.page.evaluate("localStorage.clear()")
        self.log("Cleared localStorage")
    
    # Override reset method to include browser cleanup
    def reset(self):
        """Reset context including browser state"""
        # Close browser if it's open
        if self.browser:
            self.close_browser()
        
        # Call parent reset
        super().reset()
        
        # Re-setup browser defaults
        self._setup_browser_defaults()
    
    # Hybrid API + UI Methods
    def extract_api_data_to_ui(self, json_path: str, variable_name: str):
        """
        Extract data from last API response and make it available for UI testing
        This enables hybrid scenarios where API data is used in UI interactions
        """
        if not self.response:
            raise RuntimeError("No API response available. Make an API request first.")
        
        # Extract data using JSONPath
        from jsonpath_ng import parse
        jsonpath_expr = parse(json_path)
        matches = jsonpath_expr.find(self.response.json)
        
        if not matches:
            raise ValueError(f"JSONPath '{json_path}' not found in API response")
        
        # Store the extracted value
        extracted_value = matches[0].value
        self.set_variable(variable_name, extracted_value)
        
        self.log(f"Extracted API data {json_path} -> {variable_name}: {extracted_value}")
        return extracted_value
    
    def capture_ui_data_for_api(self, selector: str, variable_name: str, attribute: str = None):
        """
        Capture data from UI element and make it available for API testing
        This enables hybrid scenarios where UI data is used in API calls
        """
        if not self.page:
            raise RuntimeError("No page available. Create a page first.")
        
        selector = self.interpolate_string(selector)
        
        if attribute:
            # Get attribute value
            value = self.get_element_attribute(selector, attribute)
        else:
            # Get text content
            value = self.get_element_text(selector)
        
        # Store the captured value
        self.set_variable(variable_name, value)
        
        self.log(f"Captured UI data from {selector} -> {variable_name}: {value}")
        return value