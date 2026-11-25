@protocols
Feature: Non-JSON services and GraphQL

  Background:
    Given I have a Judo API client
    And the base URL is "__BASE__"

  Scenario: XML assertions
    When I send a GET request to "/xml"
    Then the response should be valid XML
    And the response XML "//user[@id='1']/name" should exist
    And the response XML "//user[@id='9']/name" should not exist
    And the response XML "//user[@id='2']/name" should contain "ui"
    And the response XML "//user[@id='1']/name" should match "^A.a$"
    And the response content type should be "application/xml"
    And the response XML should conform to the XSD "data/users.xsd"

  Scenario: SOAP 1.1, 1.2, file and faults
    When I send a SOAP request to "/soap" with action "urn:op"
      """
      <Envelope><Body>go</Body></Envelope>
      """
    Then the SOAP response should not be a fault
    And the response XML "//Result/Message" should be "ok"
    And the response header "X-Seen-Action" should be "urn:op"
    When I send a SOAP 1.2 request to "/soap" with action "urn:v12"
      """
      <Envelope><Body>go</Body></Envelope>
      """
    Then the response header "X-Seen-Type" should be "application/soap+xml"
    And the response header "X-Seen-Params" should be "charset=utf-8; action='urn:v12'"
    When I send the SOAP envelope file "data/envelope.xml" to "/soap" with action "urn:file"
    Then the SOAP response should not be a fault
    When I send a SOAP request to "/soap" with action "urn:f"
      """
      <Envelope><Body>FAULT</Body></Envelope>
      """
    Then the SOAP fault code should be "Server"
    And the SOAP fault message should contain "Boom"
    And the response status should be a server error

  Scenario: XML POST
    When I send an XML POST to "/xml-post"
      """
      <note><to>Ana</to></note>
      """
    Then the response XML "//to" should be "Ana"
    And the response content type should be "application/xml"

  Scenario: Forms
    When I send a form POST to "/form"
      | field | value |
      | user  | ana   |
      | pass  | s3    |
    Then the response "$.fields.user" should be "ana"
    And the response "$.content_type" should be "application/x-www-form-urlencoded"
    Given I set the form field "a" to "1"
    And I set the form field "b" to "two"
    When I submit the form to "/form"
    Then the response "$.fields.b" should be "two"

  Scenario: Text, CSV and binary
    When I send a GET request to "/text"
    Then the response text should contain "hello"
    And the response text should not contain "nope"
    And the response text should match "^hello,.*line$"
    And the response content type should be "text/plain"
    And the response size should be less than 100 bytes
    And I save the response text as "txt"
    When I send a GET request to "/csv"
    Then the response should be a CSV with 2 rows
    And the CSV column "name" should contain "Luis"
    When I download "/file" to the file "out/report.txt"
    Then the response should have the download filename "report.txt"
    And the response bytes should equal the file "out/report.txt"

  Scenario: Server-Sent Events
    When I open the SSE stream "/sse"
    Then I should receive an SSE event "tick" within 5 seconds
    And I should receive an SSE event with data containing "hello 2" within 5 seconds
    And I should receive 4 SSE events within 5 seconds
    And I should receive an SSE event "done" within 5 seconds
    And the last SSE event data "$.n" should be "4"
    And I close the SSE stream

  Scenario: GraphQL
    When I send the GraphQL query to "/graphql"
      """
      query { users { id name } }
      """
    Then the GraphQL response should not have errors
    And the GraphQL data "users[0].name" should be "Ana"
    And the GraphQL data "users" should have 2 items
    And the GraphQL data "users[1].email" should exist
    Given I set the GraphQL variables
      """
      {"name": "Zoe"}
      """
    When I send the GraphQL mutation to "/graphql"
      """
      mutation($name: String!) { createUser(name: $name) { id name } }
      """
    Then the GraphQL data "createUser.name" should be "Zoe"
    And I save the GraphQL data "createUser.id" as "newId"
    And the variable "newId" should be defined
    When I send the GraphQL query to "/graphql"
      """
      query { boom }
      """
    Then the GraphQL response should have an error containing "Cannot query"
    When I introspect the GraphQL schema at "/graphql"
    Then the GraphQL schema should have the type "User"
