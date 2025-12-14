# Test hybrid API + UI functionality

Feature: Hybrid API and UI Testing

  Background:
    Given I have a Judo API client
    And the base URL is "https://httpbin.org"

  @hybrid @smoke
  Scenario: API data used in UI form
    # Get data from API
    When I send a GET request to "/json"
    Then the response status should be 200
    And the response should contain "slideshow"
    And I extract "$.slideshow.author" from the API response and store it as "authorName"
    And I extract "$.slideshow.title" from the API response and store it as "slideTitle"
    
    # Use API data in UI
    Given I start a browser
    And I create a new page
    When I navigate to "https://httpbin.org/forms/post"
    And I fill "#custname" with "{authorName}"
    And I fill "#custemail" with "author@slideshow.com"
    And I fill "#custtel" with "555-0123"
    And I select "large" from "#size"
    
    # Verify the data was filled correctly
    Then the element "#custname" should have attribute "value" with value "{authorName}"
    
    # Take screenshot showing API data in UI
    And I take a screenshot named "api_data_in_ui"
    
    # Submit form and verify API data is in response
    When I click on "input[type='submit']"
    And I wait for element "pre" to be visible
    Then the element "pre" should contain "{authorName}"
    And the element "pre" should contain "author@slideshow.com"
    
    And I close the browser

  @hybrid @data-flow
  Scenario: UI data captured for API use
    # Start with UI interaction
    Given I start a browser
    And I create a new page
    When I navigate to "https://httpbin.org/forms/post"
    
    # Fill form with test data
    And I fill "#custname" with "John Doe"
    And I fill "#custemail" with "john@example.com"
    And I fill "#custtel" with "123-456-7890"
    And I select "medium" from "#size"
    
    # Capture UI data for API use
    When I capture text from element "#custname" and store it as "uiName"
    And I capture text from element "#custemail" and store it as "uiEmail"
    And I capture attribute "value" from element "#custtel" and store it as "uiPhone"
    
    # Verify captured data
    Then I should have variable "uiName" with value "John Doe"
    And I should have variable "uiEmail" with value "john@example.com"
    And I should have variable "uiPhone" with value "123-456-7890"
    
    # Use captured UI data in API call
    When I send a POST request to "/post" with JSON:
      """
      {
        "name": "{uiName}",
        "email": "{uiEmail}",
        "phone": "{uiPhone}",
        "source": "ui_capture",
        "timestamp": "2024-12-13"
      }
      """
    Then the response status should be 200
    And the response "$.json.name" should be "{uiName}"
    And the response "$.json.email" should be "{uiEmail}"
    And the response "$.json.phone" should be "{uiPhone}"
    And the response "$.json.source" should be "ui_capture"
    
    And I close the browser

  @hybrid @complex-workflow
  Scenario: Complex workflow with API validation and UI interaction
    # Step 1: Get initial data from API
    When I send a GET request to "/uuid"
    Then the response status should be 200
    And I extract "$.uuid" from the API response and store it as "sessionId"
    
    # Step 2: Start UI session with API data
    Given I start a browser
    And I create a new page
    When I navigate to "https://httpbin.org/forms/post"
    
    # Step 3: Fill form with mixed data (API + static)
    And I fill "#custname" with "Test Session {sessionId}"
    And I fill "#custemail" with "session@test.com"
    And I fill "#custtel" with "555-{sessionId}"
    And I select "large" from "#size"
    And I check the checkbox "#topping[value='bacon']"
    
    # Step 4: Take screenshot of filled form
    And I take a screenshot named "session_form_filled"
    
    # Step 5: Capture form data for validation
    When I capture text from element "#custname" and store it as "formName"
    And I capture text from element "#custemail" and store it as "formEmail"
    
    # Step 6: Validate form data via API before submission
    When I send a POST request to "/post" with JSON:
      """
      {
        "validation_request": true,
        "session_id": "{sessionId}",
        "form_data": {
          "name": "{formName}",
          "email": "{formEmail}"
        }
      }
      """
    Then the response status should be 200
    And the response should contain "validation_request"
    And the response "$.json.session_id" should be "{sessionId}"
    
    # Step 7: Submit form in UI
    When I click on "input[type='submit']"
    And I wait for element "pre" to be visible
    Then the element "pre" should contain "{sessionId}"
    And the element "pre" should contain "session@test.com"
    
    # Step 8: Final API call to log completion
    When I send a POST request to "/post" with JSON:
      """
      {
        "workflow_completed": true,
        "session_id": "{sessionId}",
        "status": "success"
      }
      """
    Then the response status should be 200
    And the response "$.json.workflow_completed" should be true
    
    # Step 9: Take final screenshot
    And I take a screenshot named "workflow_completed"
    
    And I close the browser

  @hybrid @multi-step-validation
  Scenario: Multi-step form with API validation at each step
    # Initialize session
    When I send a GET request to "/uuid"
    Then the response status should be 200
    And I extract "$.uuid" from the API response and store it as "formSessionId"
    
    # Start UI
    Given I start a browser
    And I create a new page
    When I navigate to "https://httpbin.org/forms/post"
    
    # Step 1: Fill name and validate via API
    When I fill "#custname" with "Multi Step User"
    And I capture text from element "#custname" and store it as "stepName"
    And I send a POST request to "/post" with JSON:
      """
      {
        "step": 1,
        "session_id": "{formSessionId}",
        "field": "name",
        "value": "{stepName}"
      }
      """
    Then the response status should be 200
    And the response "$.json.step" should be 1
    
    # Step 2: Fill email and validate via API
    When I fill "#custemail" with "multistep@validation.com"
    And I capture text from element "#custemail" and store it as "stepEmail"
    And I send a POST request to "/post" with JSON:
      """
      {
        "step": 2,
        "session_id": "{formSessionId}",
        "field": "email",
        "value": "{stepEmail}"
      }
      """
    Then the response status should be 200
    And the response "$.json.step" should be 2
    
    # Step 3: Complete form and final validation
    When I fill "#custtel" with "555-MULTI"
    And I select "medium" from "#size"
    And I capture text from element "#custtel" and store it as "stepPhone"
    
    # Final validation with all data
    When I send a POST request to "/post" with JSON:
      """
      {
        "step": "final",
        "session_id": "{formSessionId}",
        "complete_form": {
          "name": "{stepName}",
          "email": "{stepEmail}",
          "phone": "{stepPhone}"
        }
      }
      """
    Then the response status should be 200
    And the response "$.json.step" should be "final"
    
    # Submit UI form
    When I click on "input[type='submit']"
    And I wait for element "pre" to be visible
    Then the element "pre" should contain "Multi Step User"
    And the element "pre" should contain "multistep@validation.com"
    And the element "pre" should contain "555-MULTI"
    
    And I close the browser