@flow
Feature: Conditional and control-flow steps

  Background:
    Given I have a Judo API client
    And the base URL is "__BASE__"

  Scenario: if / otherwise on status
    When I send a GET request to "/status?code=404"
    And if the response status is 404 then run
      """
      When I send a GET request to "/health"
      Then the response status should be 200
      And I set the variable "branch" to "not-found"
      """
    And otherwise run
      """
      Then I fail the test with the message "must not run"
      """
    Then I should have variable "branch" with value "not-found"

  Scenario: otherwise branch runs when the condition is false
    When I send a GET request to "/health"
    And if the response "$.status" equals "nope" then run
      """
      Then I fail the test with the message "must not run"
      """
    And otherwise run
      """
      And I set the variable "branch" to "else"
      """
    Then I should have variable "branch" with value "else"

  Scenario: JSON conditions
    When I send a GET request to "/users/1"
    And if the response "$.age" is greater than 18 then run
      """
      And I set the variable "adult" to "yes"
      """
    And if the response "$.age" is less than 18 then run
      """
      Then I fail the test with the message "must not run"
      """
    And if the response "$.nickname" does not exist then run
      """
      Then I fail the test with the message "nickname is null but present: must not run"
      """
    And if the response "$.tags" contains "b" then run
      """
      And I set the variable "has_b" to "yes"
      """
    And if the response "$.address.city" exists then run
      """
      And I set the variable "has_city" to "yes"
      """
    And if the response header "content-type" exists then run
      """
      And I set the variable "has_ct" to "yes"
      """
    And if the response body contains "Santiago" then run
      """
      And I set the variable "has_body" to "yes"
      """
    Then the variable "adult" should be defined
    And the variable "has_b" should be defined
    And the variable "has_city" should be defined
    And the variable "has_ct" should be defined
    And the variable "has_body" should be defined
    And the variable "nothing" should not be defined

  Scenario: variable and environment conditions
    Given I set the variable "mode" to "fast"
    When if the variable "mode" equals "fast" then run
      """
      And I set the variable "r1" to "ok"
      """
    And if the variable "mode" is defined then run
      """
      And I set the variable "r2" to "ok"
      """
    And if the variable "ghost" is not defined then run
      """
      And I set the variable "r3" to "ok"
      """
    And if the variable "ghost" is empty then run
      """
      And I set the variable "r4" to "ok"
      """
    And if the environment is "never-set" then run
      """
      Then I fail the test with the message "must not run"
      """
    And if the environment variable "JUDO_DEFINITELY_UNSET_X" is set then run
      """
      Then I fail the test with the message "must not run"
      """
    Then the variable "r1" should be defined
    And the variable "r2" should be defined
    And the variable "r3" should be defined
    And the variable "r4" should be defined
    And the variable "ghost" should be empty

  @flowtag
  Scenario: tag and file conditions
    When if the scenario has the tag "flowtag" then run
      """
      And I set the variable "tagged" to "yes"
      """
    And if the file "data/exists.txt" exists then run
      """
      And I set the variable "filed" to "yes"
      """
    And if the file "data/missing.txt" exists then run
      """
      Then I fail the test with the message "must not run"
      """
    Then the variable "tagged" should be defined
    And the variable "filed" should be defined

  Scenario: repeat, for each and iteration variable
    When I send a GET request to "/users"
    And for each item in the response "$" run
      """
      When I send a GET request to "/echo?id=${item.id}&i=${index}"
      Then the response "$.query.id" should be "${item.id}"
      """
    And I repeat 3 times
      """
      When I send a GET request to "/echo?n=${iteration}"
      Then the response "$.query.n" should be "${iteration}"
      """
    Then the variable "iteration" should be defined

  Scenario: repeat until and retry
    Given I send a GET request to "/reset"
    When I repeat until the response "$.state" equals "done" up to 5 times
      """
      When I send a GET request to "/job"
      """
    Then the response "$.state" should be "done"
    Given I send a GET request to "/reset"
    When I retry the following steps up to 5 times with 0.05 seconds delay
      """
      When I send a GET request to "/flaky"
      Then the response status should be 200
      """

  Scenario: nested docstring inside a block
    When if the variable "never" is not defined then run
      """
      When I send a POST request to "/users" with JSON
        '''
        {"name": "Nested"}
        '''
      Then the response status should be 201
      And the response "$.name" should be "Nested"
      """

  Scenario: soft assertions report every failure
    When I send a GET request to "/health"
    Then I verify all of the following
      """
      Then the response status should be 200
      And the response "$.status" should be "ok"
      """

  Scenario: skip the scenario
    Given I set the variable "mode" to "skipme"
    When I skip the scenario if the variable "mode" equals "skipme"
    Then I fail the test with the message "skipped scenarios must not reach this step"
