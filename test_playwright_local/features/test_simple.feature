# Simple test that doesn't depend on external services

Feature: Simple Integration Test

  @api @simple
  Scenario: Variable management test
    Given I have a Judo API client
    When I set the variable "testVar" to "testValue"
    Then I should have variable "testVar" with value "testValue"
    
  @api @simple  
  Scenario: Variable storage test
    Given I have a Judo API client
    When I set the variable "name" to "John"
    And I set the variable "age" to "25"
    Then I should have variable "name" with value "John"
    And I should have variable "age" with value "25"