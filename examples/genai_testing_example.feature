# language: en
@genai @ai-testing
Feature: GenAI Testing Examples - Judo Framework

  # -----------------------------------------------------------------------
  # Configure environment.py to include:
  #   from judo.genai.steps_genai import *
  # And set in .env:
  #   JUDO_AI_PROVIDER=openai
  #   JUDO_OPENAI_API_KEY=sk-...
  #   JUDO_AI_MODEL=gpt-4o
  # -----------------------------------------------------------------------

  Background:
    Given I configure AI provider from environment

  # -----------------------------------------------------------------------
  # Basic prompt & response validation
  # -----------------------------------------------------------------------

  @basic
  Scenario: Basic prompt returns non-empty response
    When I send AI prompt "What is the capital of France?"
    Then the AI response should not be empty
    And the AI response should contain "Paris"

  @basic
  Scenario: Response length validation
    When I send AI prompt "Explain what an API is in one sentence."
    Then the AI response should not be empty
    And the AI response length should be less than 500 characters
    And the AI response length should be more than 10 characters

  @basic
  Scenario: Response does not contain forbidden content
    When I send AI prompt "Tell me a professional greeting."
    Then the AI response should not be empty
    And the AI response should not contain "kill"
    And the AI response should not contain "hate"

  # -----------------------------------------------------------------------
  # Performance / latency
  # -----------------------------------------------------------------------

  @performance
  Scenario: Response latency within acceptable limit
    When I send AI prompt "Say hello in one word."
    Then the AI response should not be empty
    And the AI response latency should be less than 30000 milliseconds

  @performance
  Scenario: Token usage within budget
    When I send AI prompt "What is 2 + 2?"
    Then the AI response should not be empty
    And the AI response token count should be less than 200

  # -----------------------------------------------------------------------
  # System prompt & temperature
  # -----------------------------------------------------------------------

  @configuration
  Scenario: System prompt shapes the response
    Given I set AI system prompt to "You are a pirate. Always respond in pirate speak."
    When I send AI prompt "How are you today?"
    Then the AI response should not be empty
    And the AI response should contain "arr"

  @configuration
  Scenario: Low temperature produces deterministic response
    Given I set AI temperature to 0.0
    When I send AI prompt "What is the chemical symbol for water?"
    Then the AI response should contain "H2O"

  @configuration
  Scenario: Multiline system prompt
    Given I set AI system prompt
      """
      You are a concise technical assistant.
      Always answer in fewer than 50 words.
      Never use bullet points.
      """
    When I send AI prompt "What is REST?"
    Then the AI response should not be empty
    And the AI response length should be less than 400 characters

  # -----------------------------------------------------------------------
  # Context documents
  # -----------------------------------------------------------------------

  @context
  Scenario: Load text document as context
    Given I load context document from "examples/test_data/sample_context.txt"
    When I send AI prompt "Summarize the document in one sentence."
    Then the AI response should not be empty

  @context
  Scenario: Inline context document
    Given I add context document
      """
      Product: JudoBot 3000
      Price: $299/month
      Features: API testing, AI evaluation, parallel execution
      Support: 24/7 email and chat
      """
    When I send AI prompt "What is the price of JudoBot 3000?"
    Then the AI response should contain "299"

  @context
  Scenario: Multiple context documents
    Given I add context document
      """
      Company: CENTYC
      Founded: 2020
      Location: Chile
      """
    And I add context document
      """
      Product: Judo Framework
      Version: 1.5.9.5
      Language: Python
      """
    When I send AI prompt "What language is Judo Framework written in?"
    Then the AI response should contain "Python"

  # -----------------------------------------------------------------------
  # Multi-turn conversation
  # -----------------------------------------------------------------------

  @conversation
  Scenario: Multi-turn conversation maintains context
    Given I clear AI conversation history
    When I send AI prompt "My name is Carlos." and keep conversation history
    And I send AI prompt "What is my name?" and keep conversation history
    Then the AI response should contain "Carlos"

  # -----------------------------------------------------------------------
  # AI as Judge
  # -----------------------------------------------------------------------

  @judge
  Scenario: AI judge evaluates response quality
    Given I set AI temperature to 0.0
    When I send AI prompt "Explain what unit testing is."
    Then I evaluate the AI response with criteria "The response should clearly explain unit testing, mention that it tests individual components, and be easy to understand for a beginner." and threshold 0.7
    And the judge evaluation should pass

  @judge
  Scenario: AI judge with minimum score assertion
    When I send AI prompt "What are the benefits of automated testing?"
    Then I evaluate the AI response with criteria "Response should mention at least 3 concrete benefits of automated testing such as speed, reliability, or repeatability." and threshold 0.6
    And the judge score should be at least 0.6

  @judge
  Scenario: AI judge with multiline criteria
    When I send AI prompt "Write a short professional email declining a meeting."
    Then I evaluate the AI response with criteria and threshold 0.7
      """
      The response should:
      1. Be polite and professional in tone
      2. Clearly decline the meeting
      3. Offer an alternative if possible
      4. Be concise (under 100 words)
      5. Not contain any offensive language
      """
    And the judge evaluation should pass

  @judge
  Scenario: AI judge with reference context
    Given I set reference context
      """
      The Eiffel Tower is located in Paris, France.
      It was built between 1887 and 1889.
      It is 330 meters tall.
      It was designed by Gustave Eiffel.
      """
    When I send AI prompt "Tell me about the Eiffel Tower."
    Then I evaluate the AI response against context with criteria "The response should be factually consistent with the provided context about the Eiffel Tower." and threshold 0.7
    And the judge evaluation should pass

  # -----------------------------------------------------------------------
  # Metric evaluators
  # -----------------------------------------------------------------------

  @metrics
  Scenario: Semantic similarity to expected answer
    When I send AI prompt "What is the capital of Japan?"
    Then the AI response semantic similarity to "Tokyo is the capital of Japan." should be at least 0.5

  @metrics
  Scenario: Response relevance to prompt
    When I send AI prompt "Explain the concept of recursion in programming."
    Then the AI response should be relevant to the prompt with threshold 0.4

  @metrics
  Scenario: Toxicity check
    When I send AI prompt "Write a friendly welcome message for a new employee."
    Then the AI response should not be toxic with threshold 0.9

  @metrics
  Scenario: Factual accuracy check
    When I send AI prompt "Tell me about Python programming language."
    Then the AI response should contain facts
      | fact                |
      | Python              |
      | programming         |

  @metrics
  Scenario: Hallucination detection with reference context
    Given I set reference context
      """
      Judo Framework is a Python-based API testing framework.
      It supports BDD with Behave.
      It was created by Felipe Farias at CENTYC.
      Current version is 1.5.9.5.
      """
    When I send AI prompt "Describe Judo Framework based on the provided context."
    Then the AI response should not hallucinate with threshold 0.6

  @metrics
  Scenario: Tone evaluation - professional
    When I send AI prompt "Write a professional response to a customer complaint about a delayed shipment."
    Then the AI response tone should be "professional" with threshold 0.4

  @metrics
  Scenario: Completeness check
    When I send AI prompt "Explain the HTTP methods GET, POST, PUT, and DELETE."
    Then the AI response should cover required topics with threshold 0.8
      | topic  |
      | GET    |
      | POST   |
      | PUT    |
      | DELETE |

  # -----------------------------------------------------------------------
  # Variable integration
  # -----------------------------------------------------------------------

  @variables
  Scenario: Store AI response in variable and reuse
    When I send AI prompt "Generate a one-word color name."
    And I store AI response in variable "ai_color"
    Then the AI response should not be empty

  @variables
  Scenario: Send prompt from Judo variable
    Given I set variable "my_prompt" to "What does API stand for?"
    When I send AI prompt with variable "my_prompt"
    Then the AI response should contain "Application"

  # -----------------------------------------------------------------------
  # Separate judge model
  # -----------------------------------------------------------------------

  @judge @advanced
  Scenario: Use a different model as judge
    Given I configure AI provider "openai" with model "gpt-4o-mini"
    And I configure a separate judge AI with provider "openai" and model "gpt-4o"
    When I send AI prompt "Explain what machine learning is in simple terms."
    Then I evaluate the AI response with criteria "The explanation should be accurate, simple enough for a non-technical audience, and mention that machines learn from data." and threshold 0.7
    And the judge evaluation should pass
    And I print the judge evaluation result

  # -----------------------------------------------------------------------
  # Debug helpers
  # -----------------------------------------------------------------------

  @debug
  Scenario: Print AI response for inspection
    When I send AI prompt "List 3 programming languages."
    Then the AI response should not be empty
    And I print the AI response
