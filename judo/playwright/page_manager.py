"""
Page Manager for Playwright Integration
Manages multiple pages and provides utilities for complex UI testing scenarios
"""

from typing import Dict, List, Optional, Any
from . import PLAYWRIGHT_AVAILABLE

if PLAYWRIGHT_AVAILABLE:
    from playwright.sync_api import Page, BrowserContext


class PageManager:
    """
    Advanced page management for complex UI testing scenarios
    Provides utilities for multi-page testing, page state management, and coordination
    """
    
    def __init__(self, browser_context: 'BrowserContext'):
        """
        Initialize page manager
        
        Args:
            browser_context: Playwright browser context
        """
        self.browser_context = browser_context
        self.pages: Dict[str, 'Page'] = {}
        self.page_states: Dict[str, Dict[str, Any]] = {}
        self.current_page_name: Optional[str] = None
        
    def create_page(self, name: str, **options) -> 'Page':
        """
        Create a new page with advanced options
        
        Args:
            name: Name for the page
            **options: Page creation options
            
        Returns:
            Created page
        """
        if name in self.pages:
            raise ValueError(f"Page '{name}' already exists")
        
        page = self.browser_context.new_page(**options)
        self.pages[name] = page
        self.page_states[name] = {
            'created_at': self._get_timestamp(),
            'url_history': [],
            'screenshots': [],
            'errors': [],
            'console_messages': []
        }
        
        # Setup page event handlers
        self._setup_page_handlers(page, name)
        
        # Set as current if it's the first page
        if not self.current_page_name:
            self.current_page_name = name
        
        return page
    
    def get_page(self, name: str) -> 'Page':
        """Get a page by name"""
        if name not in self.pages:
            raise ValueError(f"Page '{name}' not found. Available pages: {list(self.pages.keys())}")
        return self.pages[name]
    
    def switch_to_page(self, name: str):
        """Switch to a specific page"""
        if name not in self.pages:
            raise ValueError(f"Page '{name}' not found. Available pages: {list(self.pages.keys())}")
        
        self.current_page_name = name
    
    def get_current_page(self) -> Optional['Page']:
        """Get the current active page"""
        if self.current_page_name and self.current_page_name in self.pages:
            return self.pages[self.current_page_name]
        return None
    
    def close_page(self, name: str):
        """Close a specific page"""
        if name not in self.pages:
            return
        
        page = self.pages[name]
        page.close()
        
        del self.pages[name]
        del self.page_states[name]
        
        # If we closed the current page, switch to another one
        if self.current_page_name == name:
            if self.pages:
                self.current_page_name = list(self.pages.keys())[0]
            else:
                self.current_page_name = None
    
    def close_all_pages(self):
        """Close all pages"""
        for name in list(self.pages.keys()):
            self.close_page(name)
    
    def list_pages(self) -> List[str]:
        """Get list of all page names"""
        return list(self.pages.keys())
    
    def get_page_state(self, name: str) -> Dict[str, Any]:
        """Get state information for a page"""
        if name not in self.page_states:
            raise ValueError(f"Page '{name}' not found")
        return self.page_states[name].copy()
    
    def get_all_page_states(self) -> Dict[str, Dict[str, Any]]:
        """Get state information for all pages"""
        return {name: state.copy() for name, state in self.page_states.items()}
    
    def take_screenshots_all_pages(self, prefix: str = "all_pages") -> Dict[str, str]:
        """
        Take screenshots of all pages
        
        Args:
            prefix: Prefix for screenshot filenames
            
        Returns:
            Dictionary mapping page names to screenshot file paths
        """
        import os
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = "judo_screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        screenshots = {}
        for name, page in self.pages.items():
            filename = f"{prefix}_{name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            try:
                page.screenshot(path=filepath)
                screenshots[name] = filepath
                
                # Update page state
                self.page_states[name]['screenshots'].append({
                    'timestamp': timestamp,
                    'filepath': filepath,
                    'url': page.url
                })
            except Exception as e:
                screenshots[name] = f"Error: {e}"
        
        return screenshots
    
    def wait_for_any_page_navigation(self, timeout: int = 30000) -> str:
        """
        Wait for navigation on any page
        
        Args:
            timeout: Timeout in milliseconds
            
        Returns:
            Name of the page that navigated
        """
        import asyncio
        from playwright.sync_api import expect
        
        # This is a simplified version - in practice, you'd want to use async/await
        # for proper multi-page event handling
        for name, page in self.pages.items():
            try:
                page.wait_for_load_state('networkidle', timeout=timeout)
                return name
            except:
                continue
        
        raise TimeoutError("No page navigation detected within timeout")
    
    def execute_on_all_pages(self, script: str) -> Dict[str, Any]:
        """
        Execute JavaScript on all pages
        
        Args:
            script: JavaScript code to execute
            
        Returns:
            Dictionary mapping page names to execution results
        """
        results = {}
        for name, page in self.pages.items():
            try:
                result = page.evaluate(script)
                results[name] = result
            except Exception as e:
                results[name] = f"Error: {e}"
        
        return results
    
    def find_element_across_pages(self, selector: str) -> List[Dict[str, Any]]:
        """
        Find elements matching selector across all pages
        
        Args:
            selector: CSS selector to search for
            
        Returns:
            List of dictionaries with page name and element info
        """
        results = []
        for name, page in self.pages.items():
            try:
                elements = page.locator(selector)
                count = elements.count()
                if count > 0:
                    results.append({
                        'page_name': name,
                        'page_url': page.url,
                        'element_count': count,
                        'selector': selector
                    })
            except Exception as e:
                results.append({
                    'page_name': name,
                    'page_url': page.url,
                    'error': str(e),
                    'selector': selector
                })
        
        return results
    
    def sync_cookies_across_pages(self):
        """Synchronize cookies across all pages"""
        if not self.pages:
            return
        
        # Get cookies from browser context (shared across all pages)
        cookies = self.browser_context.cookies()
        
        # Cookies are automatically shared in the same browser context
        # This method is here for completeness and future extensions
        return len(cookies)
    
    def get_performance_metrics_all_pages(self) -> Dict[str, Dict[str, Any]]:
        """
        Get performance metrics for all pages
        
        Returns:
            Dictionary mapping page names to performance metrics
        """
        metrics = {}
        for name, page in self.pages.items():
            try:
                # Get basic performance metrics via JavaScript
                perf_data = page.evaluate("""
                    () => {
                        const perf = performance.getEntriesByType('navigation')[0];
                        return {
                            loadTime: perf.loadEventEnd - perf.loadEventStart,
                            domContentLoaded: perf.domContentLoadedEventEnd - perf.domContentLoadedEventStart,
                            responseTime: perf.responseEnd - perf.responseStart,
                            url: window.location.href,
                            title: document.title
                        };
                    }
                """)
                metrics[name] = perf_data
            except Exception as e:
                metrics[name] = {'error': str(e)}
        
        return metrics
    
    def _setup_page_handlers(self, page: 'Page', page_name: str):
        """Setup event handlers for a page"""
        def handle_console(msg):
            self.page_states[page_name]['console_messages'].append({
                'timestamp': self._get_timestamp(),
                'type': msg.type,
                'text': msg.text,
                'url': page.url
            })
        
        def handle_page_error(error):
            self.page_states[page_name]['errors'].append({
                'timestamp': self._get_timestamp(),
                'error': str(error),
                'url': page.url
            })
        
        def handle_response(response):
            # Track URL changes
            current_url = page.url
            url_history = self.page_states[page_name]['url_history']
            if not url_history or url_history[-1] != current_url:
                url_history.append(current_url)
        
        page.on("console", handle_console)
        page.on("pageerror", handle_page_error)
        page.on("response", handle_response)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    # Context manager support
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_all_pages()


class PagePool:
    """
    Page pool for efficient page reuse in test scenarios
    Useful for performance testing or scenarios with many page creations
    """
    
    def __init__(self, browser_context: 'BrowserContext', pool_size: int = 5):
        """
        Initialize page pool
        
        Args:
            browser_context: Playwright browser context
            pool_size: Maximum number of pages to keep in pool
        """
        self.browser_context = browser_context
        self.pool_size = pool_size
        self.available_pages: List['Page'] = []
        self.in_use_pages: Dict[str, 'Page'] = {}
        
        # Pre-create pages
        self._populate_pool()
    
    def _populate_pool(self):
        """Create initial pages for the pool"""
        for i in range(self.pool_size):
            page = self.browser_context.new_page()
            self.available_pages.append(page)
    
    def get_page(self, name: str) -> 'Page':
        """
        Get a page from the pool
        
        Args:
            name: Name to assign to the page
            
        Returns:
            Page from pool
        """
        if name in self.in_use_pages:
            return self.in_use_pages[name]
        
        if not self.available_pages:
            # Create new page if pool is empty
            page = self.browser_context.new_page()
        else:
            page = self.available_pages.pop()
        
        self.in_use_pages[name] = page
        return page
    
    def return_page(self, name: str):
        """
        Return a page to the pool
        
        Args:
            name: Name of the page to return
        """
        if name not in self.in_use_pages:
            return
        
        page = self.in_use_pages[name]
        del self.in_use_pages[name]
        
        # Reset page state
        try:
            page.goto('about:blank')
            page.evaluate('localStorage.clear(); sessionStorage.clear();')
        except:
            # If reset fails, close the page and create a new one
            page.close()
            page = self.browser_context.new_page()
        
        if len(self.available_pages) < self.pool_size:
            self.available_pages.append(page)
        else:
            page.close()
    
    def close_all(self):
        """Close all pages in the pool"""
        for page in self.available_pages:
            page.close()
        
        for page in self.in_use_pages.values():
            page.close()
        
        self.available_pages.clear()
        self.in_use_pages.clear()