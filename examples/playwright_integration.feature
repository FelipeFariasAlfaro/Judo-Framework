# Playwright Integration Example - Hybrid API + UI Testing
# This example demonstrates how to combine API testing with UI testing in the same scenario

Feature: Hybrid API and UI Testing with Playwright Integration

  Background:
    Given I have a Judo API client
    And the base URL is "https://jsonplaceholder.typicode.com"

  @ui @api @hybrid
  Scenario: Create user via API and verify in UI
    # API Testing - Create a user
    When I send a POST request to "/users" with JSON:
      """
      {
        "name": "John Doe",
        "username": "johndoe",
        "email": "john@example.com",
        "phone": "1-770-736-8031 x56442",
        "website": "hildegard.org"
      }
      """
    Then the response status should be 201
    And the response should contain "id"
    And I extract "$.id" from the API response and store it as "userId"
    And I extract "$.name" from the API response and store it as "userName"
    
    # UI Testing - Navigate to a demo site and use the API data
    Given I start a browser
    And I create a new page
    When I navigate to "https://httpbin.org/forms/post"
    And I fill "#custname" with "{userName}"
    And I fill "#custtel" with "123-456-7890"
    And I fill "#custemail" with "john@example.com"
    And I select "large" from "#size"
    And I check the checkbox "#topping[value='bacon']"
    And I take a screenshot named "form_filled"
    
    # Capture UI data for API use
    When I capture text from "#custname" and store it as "uiName"
    Then I should have variable "uiName" with value "{userName}"
    
    # Submit form and verify
    When I click on "input[type='submit']"
    Then I wait for element "pre" to be visible
    And the element "pre" should contain "john@example.com"
    And I take a screenshot named "form_submitted"

  @ui @browser
  Scenario: Pure UI Testing - Form Validation
    Given I start a headed browser
    And I create a new page
    When I navigate to "https://httpbin.org/forms/post"
    
    # Test form validation
    When I click on "input[type='submit']"
    Then the element "#custname:invalid" should be visible
    
    # Fill form step by step
    When I fill "#custname" with "Test User"
    And I fill "#custtel" with "555-0123"
    And I fill "#custemail" with "test@example.com"
    And I select "medium" from "#size"
    And I check the checkbox "#topping[value='cheese']"
    And I check the checkbox "#topping[value='onion']"
    
    # Verify form state
    Then the element "#custname" should have attribute "value" with value "Test User"
    And the element "#size" should have attribute "value" with value "medium"
    
    # Submit and verify
    When I click on "input[type='submit']"
    And I wait for element "pre" to be visible
    Then the element "pre" should contain "Test User"
    And the element "pre" should contain "test@example.com"
    And the element "pre" should contain "cheese"
    And the element "pre" should contain "onion"

  @api @ui @multi-page
  Scenario: Multi-page UI with API data synchronization
    # Get user data from API
    When I send a GET request to "/users/1"
    Then the response status should be 200
    And I extract "$.name" from the API response and store it as "apiUserName"
    And I extract "$.email" from the API response and store it as "apiUserEmail"
    
    # Start browser with multiple pages
    Given I start a browser
    And I create a new page named "form_page"
    And I create a new page named "result_page"
    
    # Fill form in first page
    When I switch to page "form_page"
    And I navigate to "https://httpbin.org/forms/post"
    And I fill "#custname" with "{apiUserName}"
    And I fill "#custemail" with "{apiUserEmail}"
    And I fill "#custtel" with "123-456-7890"
    And I select "large" from "#size"
    And I take a screenshot named "multi_page_form"
    
    # Submit form
    When I click on "input[type='submit']"
    And I wait for element "pre" to be visible
    
    # Switch to result page and verify
    When I switch to page "result_page"
    And I navigate to "https://httpbin.org/get"
    Then the element "pre" should be visible
    
    # Take screenshots of both pages
    When I switch to page "form_page"
    And I take a screenshot named "form_page_final"
    And I switch to page "result_page"
    And I take a screenshot named "result_page_final"

  @ui @javascript
  Scenario: JavaScript execution and local storage
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
    
    # Execute complex JavaScript and store result
    When I execute JavaScript and store result in "pageInfo":
      """
      return {
        title: document.title,
        url: window.location.href,
        userAgent: navigator.userAgent.substring(0, 50),
        timestamp: new Date().toISOString()
      };
      """
    Then I should have variable "pageInfo"
    
    # Clear storage
    When I clear localStorage
    Then localStorage "testKey" should be "null"

  @ui @screenshots
  Scenario: Screenshot testing and visual verification
    Given I start a browser
    And I create a new page
    When I navigate to "https://httpbin.org"
    
    # Take full page screenshot
    And I take a screenshot named "httpbin_homepage"
    
    # Navigate and take element screenshot
    When I navigate to "https://httpbin.org/forms/post"
    And I take a screenshot of element "form" named "contact_form"
    
    # Fill form and take another screenshot
    When I fill "#custname" with "Screenshot Test"
    And I fill "#custemail" with "test@screenshot.com"
    And I take a screenshot of element "form" named "form_filled"
    
    # Take final full page screenshot
    And I take a screenshot named "form_page_complete"

  @ui @wait @timing
  Scenario: Advanced waiting and timing
    Given I start a browser
    And I create a new page
    When I navigate to "https://httpbin.org/delay/2"
    
    # Wait for page load
    And I wait for element "pre" to be visible
    Then the element "pre" should contain "origin"
    
    # Navigate to form and wait for elements
    When I navigate to "https://httpbin.org/forms/post"
    And I wait for element "#custname" to be visible
    And I wait for element "#size" to be visible
    
    # Test timing
    When I fill "#custname" with "Timing Test"
    And I wait 1 seconds
    And I fill "#custemail" with "timing@test.com"
    And I wait 2 seconds
    
    # Verify elements are ready
    Then the element "#custname" should be enabled
    And the element "#custemail" should be enabled
    And the element "input[type='submit']" should be enabled