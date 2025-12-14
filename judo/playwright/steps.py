"""
Playwright Steps for Judo Framework (English)
Browser automation steps that integrate seamlessly with API testing
"""

from behave import step
# Check Playwright availability
try:
    import playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

if not PLAYWRIGHT_AVAILABLE:
    # If Playwright is not available, create dummy steps that raise helpful errors
    def _playwright_not_available(*args, **kwargs):
        raise ImportError(
            "Playwright is not installed. Install it with:\n"
            "pip install 'judo-framework[browser]' or pip install playwright\n"
            "Then run: playwright install"
        )
    
    # Create dummy steps
    step = lambda pattern: lambda func: _playwright_not_available

# Browser Lifecycle Steps
@step('I start a "{browser_type}" browser')
def step_start_browser(context, browser_type):
    """Start a specific browser type"""
    if not hasattr(context, 'judo_context') or not hasattr(context.judo_context, 'start_browser'):
        raise RuntimeError("Browser context not available. Use JudoBrowserContext in environment.py")
    
    context.judo_context.start_browser(browser_type=browser_type.lower())

@step('I start a browser')
def step_start_default_browser(context):
    """Start default browser (chromium)"""
    if not hasattr(context, 'judo_context') or not hasattr(context.judo_context, 'start_browser'):
        raise RuntimeError("Browser context not available. Use JudoBrowserContext in environment.py")
    
    context.judo_context.start_browser()

@step('I start a headless browser')
def step_start_headless_browser(context):
    """Start browser in headless mode"""
    if not hasattr(context, 'judo_context') or not hasattr(context.judo_context, 'start_browser'):
        raise RuntimeError("Browser context not available. Use JudoBrowserContext in environment.py")
    
    context.judo_context.start_browser(headless=True)

@step('I start a headed browser')
def step_start_headed_browser(context):
    """Start browser in headed mode (visible)"""
    if not hasattr(context, 'judo_context') or not hasattr(context.judo_context, 'start_browser'):
        raise RuntimeError("Browser context not available. Use JudoBrowserContext in environment.py")
    
    context.judo_context.start_browser(headless=False)

@step('I create a new page')
def step_create_new_page(context):
    """Create a new page"""
    if not hasattr(context, 'judo_context') or not hasattr(context.judo_context, 'new_page'):
        raise RuntimeError("Browser context not available. Use JudoBrowserContext in environment.py")
    
    context.judo_context.new_page()

@step('I create a new page named "{page_name}"')
def step_create_named_page(context, page_name):
    """Create a new page with a specific name"""
    if not hasattr(context, 'judo_context') or not hasattr(context.judo_context, 'new_page'):
        raise RuntimeError("Browser context not available. Use JudoBrowserContext in environment.py")
    
    context.judo_context.new_page(name=page_name)

@step('I switch to page "{page_name}"')
def step_switch_to_page(context, page_name):
    """Switch to a named page"""
    context.judo_context.switch_to_page(page_name)

@step('I close the current page')
def step_close_current_page(context):
    """Close the current page"""
    context.judo_context.close_page()

@step('I close page "{page_name}"')
def step_close_named_page(context, page_name):
    """Close a named page"""
    context.judo_context.close_page(page_name)

@step('I close the browser')
def step_close_browser(context):
    """Close the browser"""
    context.judo_context.close_browser()

# Navigation Steps
@step('I navigate to "{url}"')
def step_navigate_to_url(context, url):
    """Navigate to a URL"""
    context.judo_context.navigate_to(url)

@step('I go to "{url}"')
def step_go_to_url(context, url):
    """Navigate to a URL (alias)"""
    context.judo_context.navigate_to(url)

@step('I reload the page')
def step_reload_page(context):
    """Reload the current page"""
    context.judo_context.reload_page()

@step('I go back')
def step_go_back(context):
    """Go back in browser history"""
    context.judo_context.go_back()

@step('I go forward')
def step_go_forward(context):
    """Go forward in browser history"""
    context.judo_context.go_forward()

# Element Interaction Steps
@step('I click on "{selector}"')
def step_click_element(context, selector):
    """Click on an element"""
    context.judo_context.click_element(selector)

@step('I click the "{selector}" element')
def step_click_element_alt(context, selector):
    """Click on an element (alternative phrasing)"""
    context.judo_context.click_element(selector)

@step('I fill "{selector}" with "{value}"')
def step_fill_input(context, selector, value):
    """Fill an input field with a value"""
    context.judo_context.fill_input(selector, value)

@step('I type "{text}" in "{selector}"')
def step_type_text(context, selector, text):
    """Type text into an element"""
    context.judo_context.type_text(selector, text)

@step('I select "{value}" from "{selector}"')
def step_select_option(context, selector, value):
    """Select an option from a select element"""
    context.judo_context.select_option(selector, value)

@step('I check the checkbox "{selector}"')
def step_check_checkbox(context, selector):
    """Check a checkbox"""
    context.judo_context.check_checkbox(selector)

@step('I uncheck the checkbox "{selector}"')
def step_uncheck_checkbox(context, selector):
    """Uncheck a checkbox"""
    context.judo_context.uncheck_checkbox(selector)

# Element Validation Steps
@step('the element "{selector}" should be visible')
def step_element_should_be_visible(context, selector):
    """Verify that an element is visible"""
    assert context.judo_context.is_element_visible(selector), f"Element '{selector}' is not visible"

@step('the element "{selector}" should not be visible')
def step_element_should_not_be_visible(context, selector):
    """Verify that an element is not visible"""
    assert not context.judo_context.is_element_visible(selector), f"Element '{selector}' is visible"

@step('the element "{selector}" should be enabled')
def step_element_should_be_enabled(context, selector):
    """Verify that an element is enabled"""
    assert context.judo_context.is_element_enabled(selector), f"Element '{selector}' is not enabled"

@step('the element "{selector}" should be disabled')
def step_element_should_be_disabled(context, selector):
    """Verify that an element is disabled"""
    assert not context.judo_context.is_element_enabled(selector), f"Element '{selector}' is enabled"

@step('the element "{selector}" should contain "{text}"')
def step_element_should_contain_text(context, selector, text):
    """Verify that an element contains specific text"""
    actual_text = context.judo_context.get_element_text(selector)
    text = context.judo_context.interpolate_string(text)
    assert text in actual_text, f"Element '{selector}' does not contain '{text}'. Actual text: '{actual_text}'"

@step('the element "{selector}" should have text "{text}"')
def step_element_should_have_exact_text(context, selector, text):
    """Verify that an element has exact text"""
    actual_text = context.judo_context.get_element_text(selector)
    text = context.judo_context.interpolate_string(text)
    assert actual_text == text, f"Element '{selector}' text mismatch. Expected: '{text}', Actual: '{actual_text}'"

@step('the element "{selector}" should have attribute "{attribute}" with value "{value}"')
def step_element_should_have_attribute(context, selector, attribute, value):
    """Verify that an element has a specific attribute value"""
    actual_value = context.judo_context.get_element_attribute(selector, attribute)
    value = context.judo_context.interpolate_string(value)
    assert actual_value == value, f"Element '{selector}' attribute '{attribute}' mismatch. Expected: '{value}', Actual: '{actual_value}'"

# Wait Steps
@step('I wait for element "{selector}" to be visible')
def step_wait_for_element_visible(context, selector):
    """Wait for an element to become visible"""
    context.judo_context.wait_for_element(selector, state='visible')

@step('I wait for element "{selector}" to be hidden')
def step_wait_for_element_hidden(context, selector):
    """Wait for an element to become hidden"""
    context.judo_context.wait_for_element(selector, state='hidden')

@step('I wait for element "{selector}" to be attached')
def step_wait_for_element_attached(context, selector):
    """Wait for an element to be attached to DOM"""
    context.judo_context.wait_for_element(selector, state='attached')

@step('I wait for element "{selector}" to be detached')
def step_wait_for_element_detached(context, selector):
    """Wait for an element to be detached from DOM"""
    context.judo_context.wait_for_element(selector, state='detached')

@step('I wait for URL to contain "{url_pattern}"')
def step_wait_for_url_pattern(context, url_pattern):
    """Wait for URL to match a pattern"""
    context.judo_context.wait_for_url(f"**{url_pattern}**")

@step('I wait for URL to be "{url}"')
def step_wait_for_exact_url(context, url):
    """Wait for exact URL"""
    context.judo_context.wait_for_url(url)

@step('I wait {seconds:d} seconds')
def step_wait_seconds(context, seconds):
    """Wait for a specific number of seconds"""
    context.judo_context.wait(seconds)

# Screenshot Steps
@step('I take a screenshot')
def step_take_screenshot(context):
    """Take a screenshot of the current page"""
    context.judo_context.take_screenshot()

@step('I take a screenshot named "{name}"')
def step_take_named_screenshot(context, name):
    """Take a screenshot with a specific name"""
    context.judo_context.take_screenshot(name)

@step('I take a screenshot of element "{selector}"')
def step_take_element_screenshot(context, selector):
    """Take a screenshot of a specific element"""
    context.judo_context.take_element_screenshot(selector)

@step('I take an element screenshot of "{selector}" named "{name}"')
def step_take_named_element_screenshot(context, selector, name):
    """Take a screenshot of a specific element with a name"""
    context.judo_context.take_element_screenshot(selector, name)

# JavaScript Steps
@step('I execute JavaScript')
def step_execute_javascript(context):
    """Execute JavaScript code from step text"""
    script = context.text
    result = context.judo_context.execute_javascript(script)
    context.judo_context.set_variable('js_result', result)

@step('I execute JavaScript "{script}"')
def step_execute_javascript_inline(context, script):
    """Execute inline JavaScript code"""
    result = context.judo_context.execute_javascript(script)
    context.judo_context.set_variable('js_result', result)

@step('I execute JavaScript and store result in "{variable_name}"')
def step_execute_javascript_store_result(context, variable_name):
    """Execute JavaScript and store result in a variable"""
    script = context.text
    result = context.judo_context.execute_javascript(script)
    context.judo_context.set_variable(variable_name, result)

# Cookie Steps
@step('I clear all cookies')
def step_clear_cookies(context):
    """Clear all cookies"""
    context.judo_context.clear_cookies()

@step('I add cookie with name "{name}" and value "{value}"')
def step_add_cookie(context, name, value):
    """Add a cookie"""
    name = context.judo_context.interpolate_string(name)
    value = context.judo_context.interpolate_string(value)
    
    cookie = {
        'name': name,
        'value': value,
        'url': context.judo_context.page.url if context.judo_context.page else 'http://localhost'
    }
    context.judo_context.add_cookie(cookie)

# Local Storage Steps
@step('I set localStorage "{key}" to "{value}"')
def step_set_local_storage(context, key, value):
    """Set a localStorage item"""
    context.judo_context.set_local_storage(key, value)

@step('I clear localStorage')
def step_clear_local_storage(context):
    """Clear localStorage"""
    context.judo_context.clear_local_storage()

@step('localStorage "{key}" should be "{value}"')
def step_local_storage_should_be(context, key, value):
    """Verify localStorage value"""
    actual_value = context.judo_context.get_local_storage(key)
    value = context.judo_context.interpolate_string(value)
    assert actual_value == value, f"localStorage[{key}] mismatch. Expected: '{value}', Actual: '{actual_value}'"

# Variable Extraction Steps (Hybrid API + UI)
@step('I extract "{json_path}" from the API response and store it as "{variable_name}"')
def step_extract_api_data_for_ui(context, json_path, variable_name):
    """Extract data from API response for use in UI testing"""
    context.judo_context.extract_api_data_to_ui(json_path, variable_name)

@step('I capture text from element "{selector}" and store it as "{variable_name}"')
def step_capture_ui_text_for_api(context, selector, variable_name):
    """Capture text from UI element for use in API testing"""
    context.judo_context.capture_ui_data_for_api(selector, variable_name)

@step('I capture attribute "{attribute}" from element "{selector}" and store it as "{variable_name}"')
def step_capture_ui_attribute_for_api(context, selector, attribute, variable_name):
    """Capture attribute from UI element for use in API testing"""
    context.judo_context.capture_ui_data_for_api(selector, variable_name, attribute)

# Form Steps
@step('I submit the form "{selector}"')
def step_submit_form(context, selector):
    """Submit a form"""
    # Use JavaScript to submit the form
    selector = context.judo_context.interpolate_string(selector)
    script = f"document.querySelector('{selector}').submit()"
    context.judo_context.execute_javascript(script)

@step('I fill the form')
def step_fill_form_from_table(context):
    """Fill form fields from a data table"""
    if not context.table:
        raise ValueError("This step requires a data table with field and value columns")
    
    for row in context.table:
        field = row['field']
        value = row['value']
        context.judo_context.fill_input(field, value)

# Advanced Interaction Steps
@step('I hover over "{selector}"')
def step_hover_element(context, selector):
    """Hover over an element"""
    if not context.judo_context.page:
        raise RuntimeError("No page available. Create a page first.")
    
    selector = context.judo_context.interpolate_string(selector)
    context.judo_context.page.hover(selector)
    context.judo_context.log(f"Hovered over element: {selector}")

@step('I double-click on "{selector}"')
def step_double_click_element(context, selector):
    """Double-click on an element"""
    if not context.judo_context.page:
        raise RuntimeError("No page available. Create a page first.")
    
    selector = context.judo_context.interpolate_string(selector)
    context.judo_context.page.dblclick(selector)
    context.judo_context.log(f"Double-clicked element: {selector}")

@step('I right-click on "{selector}"')
def step_right_click_element(context, selector):
    """Right-click on an element"""
    if not context.judo_context.page:
        raise RuntimeError("No page available. Create a page first.")
    
    selector = context.judo_context.interpolate_string(selector)
    context.judo_context.page.click(selector, button='right')
    context.judo_context.log(f"Right-clicked element: {selector}")

@step('I drag "{source_selector}" to "{target_selector}"')
def step_drag_and_drop(context, source_selector, target_selector):
    """Drag and drop from source to target"""
    if not context.judo_context.page:
        raise RuntimeError("No page available. Create a page first.")
    
    source_selector = context.judo_context.interpolate_string(source_selector)
    target_selector = context.judo_context.interpolate_string(target_selector)
    
    source = context.judo_context.page.locator(source_selector)
    target = context.judo_context.page.locator(target_selector)
    
    source.drag_to(target)
    context.judo_context.log(f"Dragged {source_selector} to {target_selector}")

# File Upload Steps
@step('I upload file "{file_path}" to "{selector}"')
def step_upload_file(context, file_path, selector):
    """Upload a file to a file input"""
    if not context.judo_context.page:
        raise RuntimeError("No page available. Create a page first.")
    
    file_path = context.judo_context.interpolate_string(file_path)
    selector = context.judo_context.interpolate_string(selector)
    
    context.judo_context.page.set_input_files(selector, file_path)
    context.judo_context.log(f"Uploaded file {file_path} to {selector}")

# Alert/Dialog Steps
@step('I accept the alert')
def step_accept_alert(context):
    """Accept an alert dialog"""
    if not context.judo_context.page:
        raise RuntimeError("No page available. Create a page first.")
    
    # Set up dialog handler to accept
    context.judo_context.page.on("dialog", lambda dialog: dialog.accept())
    context.judo_context.log("Set up alert acceptance")

@step('I dismiss the alert')
def step_dismiss_alert(context):
    """Dismiss an alert dialog"""
    if not context.judo_context.page:
        raise RuntimeError("No page available. Create a page first.")
    
    # Set up dialog handler to dismiss
    context.judo_context.page.on("dialog", lambda dialog: dialog.dismiss())
    context.judo_context.log("Set up alert dismissal")

@step('I accept the alert with text "{text}"')
def step_accept_alert_with_text(context, text):
    """Accept an alert dialog and enter text (for prompt dialogs)"""
    if not context.judo_context.page:
        raise RuntimeError("No page available. Create a page first.")
    
    text = context.judo_context.interpolate_string(text)
    
    # Set up dialog handler to accept with text
    context.judo_context.page.on("dialog", lambda dialog: dialog.accept(text))
    context.judo_context.log(f"Set up alert acceptance with text: {text}")

# Window/Tab Management Steps
@step('I switch to new tab')
def step_switch_to_new_tab(context):
    """Switch to the newest tab/window"""
    if not context.judo_context.browser_context:
        raise RuntimeError("No browser context available.")
    
    pages = context.judo_context.browser_context.pages
    if len(pages) > 1:
        # Switch to the last (newest) page
        newest_page = pages[-1]
        context.judo_context.page = newest_page
        context.judo_context.log("Switched to new tab")
    else:
        raise RuntimeError("No new tab available")

@step('I close the current tab')
def step_close_current_tab(context):
    """Close the current tab"""
    if not context.judo_context.page:
        raise RuntimeError("No page available.")
    
    context.judo_context.page.close()
    
    # Switch to another available page if exists
    if context.judo_context.browser_context:
        pages = context.judo_context.browser_context.pages
        if pages:
            context.judo_context.page = pages[0]
        else:
            context.judo_context.page = None
    
    context.judo_context.log("Closed current tab")