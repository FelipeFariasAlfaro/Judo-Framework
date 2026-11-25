@new
Feature: New steps (v1.7.0) in English

  Background:
    Given I have a Judo API client
    And the base URL is "__BASE__"

  Scenario: Interpolation engine
    Given I set the variable "who" to "Ana"
    When I send a GET request to "/echo?a=${who}&b=${missing:-fallback}&c={who}&n=${uuid()}"
    Then the response "$.query.a" should be "Ana"
    And the response "$.query.b" should be "fallback"
    And the response "$.query.c" should be "Ana"
    And the response field "query.n" should match pattern "^[0-9a-f-]{36}$"

  Scenario: Nested variable access
    When I send a GET request to "/users/1"
    And I extract "$.address" from the response as "addr"
    And I send a GET request to "/echo?city=${addr.city}"
    Then the response "$.query.city" should be "Santiago"

  Scenario: Timeout, TLS and proxy settings are accepted
    Given I set the timeout to 10 seconds
    And I disable SSL verification
    When I send a GET request to "/health"
    Then the response status should be 200

  Scenario: Response headers and security headers
    When I send a GET request to "/secure"
    Then the response header "X-Frame-Options" should be "DENY"
    And the response header "strict-transport-security" should exist
    And the response should include security headers

  Scenario: XML and SOAP
    When I send a GET request to "/xml"
    Then the response XML "//user[@id='2']/name" should be "Luis"
    And the response XML "//user" should select 2 nodes
    And the response XML "/root/user/@id" should be "1"
    And I extract the XML "//user[@id='1']/name" as "first"
    And I should have variable "first" with value "Ana"
    When I send a SOAP request to "/echo" with action "urn:test"
      """
      <Envelope><Body>hi</Body></Envelope>
      """
    Then the response "$.headers.soapaction" should be "urn:test"
    And the response "$.headers.content-type" should be "text/xml; charset=utf-8"

  Scenario: JSON compare ignoring volatile fields
    When I send a GET request to "/users/1"
    Then the response should equal the JSON ignoring "created,uuid"
      """
      {"id": 1, "name": "Ana", "email": "ana@example.com", "active": true, "nickname": null,
       "website": "https://example.com", "created": "whatever", "age": 30,
       "address": {"city": "Santiago", "zip": "8320000"}, "tags": ["a", "b"]}
      """

  Scenario: Upload and download hash
    When I upload the file "data/hello.txt" as "file" to "/upload"
    Then the response should contain "content_type"
    And the response should contain "sha256"
    When I send a GET request to "/download"
    Then the response SHA-256 should be "__SHA__"

  Scenario: Polling and pagination and SQL (extra steps)
    When I poll "/job" until the response "$.state" equals "done" within 10 seconds
    And I collect all pages from "/pages" using the "page" parameter up to 10 pages as "all"
    Then the response status should be 200
    Given I connect to the database "sqlite:///:memory:"
    And I execute the SQL "create table t(x integer)"
    And I execute the SQL "insert into t values (7)"
    Then the SQL query "select x from t" should return the value "7"
