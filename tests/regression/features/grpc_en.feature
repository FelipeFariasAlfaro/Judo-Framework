@grpc
Feature: gRPC through server reflection

  Scenario: unary calls, status codes and metadata
    Given I connect to the gRPC server "__GRPC__"
    Then the gRPC server should expose the service "judo.test.Greeter"
    And the gRPC server should expose the method "judo.test.Greeter/SayHello"
    When I send the gRPC request "judo.test.Greeter/SayHello"
      """
      {"name": "Ana"}
      """
    Then the gRPC status should be "OK"
    And the gRPC response "message" should be "Hello Ana"
    And the gRPC response "count" should be "3"
    And the gRPC response should contain "message"
    And I save the gRPC response "message" as "greeting"
    And the variable "greeting" should be defined
    And the gRPC call should take less than 5000 milliseconds
    When I send the gRPC request "judo.test.Greeter.SayHello"
      """
      {"name": "missing"}
      """
    Then the gRPC status should be "NOT_FOUND"
    When I send the gRPC request "judo.test.Greeter/SayHello"
      """
      {"name": "secure"}
      """
    Then the gRPC status should be "UNAUTHENTICATED"
    Given I set the gRPC metadata "authorization" to "Bearer ok"
    When I send the gRPC request "judo.test.Greeter/SayHello"
      """
      {"name": "secure"}
      """
    Then the gRPC status should be "OK"
    And the gRPC response "message" should be "Hello secure"

  Scenario: server streaming
    Given I connect to the gRPC server "__GRPC__"
    When I send the gRPC streaming request "judo.test.Greeter/Countdown"
      """
      {"times": 3}
      """
    Then the gRPC status should be "OK"
    And the gRPC stream should return 3 messages
    And the gRPC stream message 0 "message" should be "T-3"
    And the gRPC stream message 2 "count" should be "1"

  Scenario: timeouts and closing
    Given I set the gRPC timeout to 0.05 seconds
    And I connect to the gRPC server "__GRPC__"
    When I send the gRPC request "judo.test.Greeter/SayHello"
      """
      {"name": "slow"}
      """
    Then the gRPC status should be "DEADLINE_EXCEEDED"
    When I close the gRPC connection
