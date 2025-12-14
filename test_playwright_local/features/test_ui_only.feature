# Test UI-only functionality with Playwright integration

Feature: UI Testing with Playwright

  @ui @smoke
  Scenario: Basic browser startup and navigation
    Given I start a browser
    And I create a new page
    When I navigate to "https://httpbin.org"
    Then the element "h1" should be visible
    And the element "h1" should contain "httpbin"
    And I take a screenshot named "httpbin_homepage"
    And I close the browser

  @ui @forms
  Scenario: Form interaction testing
    Given I start a browser
    And I create a new page
    When I navigate to "https://httpbin.org/forms/post"
    
    # Test form validation
    When I click on "input[type='submit']"
    Then the element "#custname:invalid" should be visible
    
    # Fill form properly
    When I fill "#custname" with "Test User"
    And I fill "#custtel" with "555-0123"
    And I fill "#custemail" with "test@example.com"
    And I select "medium" from "#size"
    And I check the checkbox "#topping[value='cheese']"
    And I check the checkbox "#topping[value='onion']"
    
    # Verify form state
    Then the element "#custname" should have attribute "value" with value "Test User"
    And the element "#size" should have attribute "value" with value "medium"
    
    # Take screenshot before submit
    And I take a screenshot named "form_filled"
    
    # Submit and verify
    When I click on "input[type='submit']"
    And I wait for element "pre" to be visible
    Then the element "pre" should contain "Test User"
    And the element "pre" should contain "test@example.com"
    And the element "pre" should contain "cheese"
    And the element "pre" should contain "onion"
    
    # Take final screenshot
    And I take a screenshot named "form_submitted"
    And I close the browser

  @ui @javascript
  Scenario: JavaScript execution and storage
    Given I start a browser
    And I create a new page
    When I navigate to "https://httpbin.org"
    
    # Set local storage
    And I set localStorage "testKey" to "testValue"
    And I set localStorage "userPrefs" to "dark_mode"
    
    # Verify local storage
    Then localStorage "testKey" should be "testValue"
    And localStorage "userPrefs" should be "dark_mode"
    
    # Execute JavaScript
    When I execute JavaScript "return document.title"
    Then I should have variable "js_result" with value "httpbin.org"
    
    # Execute complex JavaScript
    When I execute JavaScript and store result in "pageInfo":
      """
      return {
        title: document.title,
        url: window.location.href,
        hasForm: document.forms.length > 0,
        linkCount: document.links.length
      };
      """
    Then I should have variable "pageInfo"
    
    # Clear storage
    When I clear localStorage
    Then localStorage "testKey" should be "null"
    
    And I close the browser

  @ui @multi-page
  Scenario: Multi-page management
    Given I start a browser
    And I create a new page named "main_page"
    And I create a new page named "form_page"
    
    # Use main page
    When I switch to page "main_page"
    And I navigate to "https://httpbin.org"
    Then the element "h1" should contain "httpbin"
    
    # Use form page
    When I switch to page "form_page"
    And I navigate to "https://httpbin.org/forms/post"
    Then the element "form" should be visible
    
    # Fill form in form page
    When I fill "#custname" with "Multi Page Test"
    And I fill "#custemail" with "multipage@test.com"
    
    # Switch back to main page
    When I switch to page "main_page"
    Then the element "h1" should contain "httpbin"
    
    # Switch back to form page and verify data is still there
    When I switch to page "form_page"
    Then the element "#custname" should have attribute "value" with value "Multi Page Test"
    
    # Take screenshots of both pages
    When I take a screenshot named "form_page_filled"
    And I switch to page "main_page"
    And I take a screenshot named "main_page_final"
    
    And I close the browser

  @ui @waiting
  Scenario: Advanced waiting and timing
    Given I start a browser
    And I create a new page
    When I navigate to "https://httpbin.org/delay/1"
    
    # Wait for delayed response
    And I wait for element "pre" to be visible
    Then the element "pre" should contain "origin"
    
    # Navigate to form and wait for elements
    When I navigate to "https://httpbin.org/forms/post"
    And I wait for element "#custname" to be visible
    And I wait for element "#size" to be visible
    
    # Test timing with waits
    When I fill "#custname" with "Timing Test"
    And I wait 1 seconds
    And I fill "#custemail" with "timing@test.com"
    
    # Verify elements are ready
    Then the element "#custname" should be enabled
    And the element "#custemail" should be enabled
    And the element "input[type='submit']" should be enabled
    
    And I close the browser

  @ui @screenshots
  Scenario: Screenshot testing
    Given I start a browser
    And I create a new page
    When I navigate to "https://httpbin.org"
    
    # Take full page screenshot
    And I take a screenshot named "httpbin_homepage"
    
    # Navigate to form
    When I navigate to "https://httpbin.org/forms/post"
    And I take a screenshot of element "form" with name "contact_form"
    
    # Fill form and take element screenshot
    When I fill "#custname" with "Screenshot Test"
    And I fill "#custemail" with "test@screenshot.com"
    And I take a screenshot of element "form" with name "form_filled"
    
    # Take final screenshot
    And I take a screenshot named "form_page_complete"
    
    And I close the browser