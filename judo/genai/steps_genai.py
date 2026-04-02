"""
Judo Framework - GenAI Evaluation Steps (English)

PURPOSE: Evaluate AI responses obtained via standard REST API steps.
The workflow is:
  1. Call your GenAI API endpoint using normal Judo REST steps
  2. Extract the AI response text into a variable
  3. Use these steps to evaluate that response

Three evaluation strategies:
  - RAG (Retrieval Augmented Generation): compare response against context
    from local documents or databases
  - Semantic Validation: measure similarity, relevance, toxicity, etc.
  - LLM as Judge: use an AI model to evaluate response quality

Import in environment.py:
    from judo.genai.steps_genai import *

.env configuration:
    JUDO_AI_PROVIDER=openai          # openai | claude | gemini (for judge only)
    JUDO_OPENAI_API_KEY=sk-...
    JUDO_AI_MODEL=gpt-4o
    JUDO_AI_TEMPERATURE=0.0
    JUDO_AI_TIMEOUT=60
"""

import os
from behave import step

from .judge import GenAIJudge
from .context_loader import ContextLoader
from .evaluators import (
    SemanticSimilarityEvaluator,
    RelevanceEvaluator,
    ToxicityEvaluator,
    FactualAccuracyEvaluator,
    HallucinationEvaluator,
    ToneEvaluator,
    CompletenessEvaluator,
)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_judge(context) -> GenAIJudge:
    """Get or lazily create the LLM judge client."""
    if not hasattr(context, "_judo_ai_judge") or context._judo_ai_judge is None:
        from .client import GenAIClient
        judge_client = getattr(context, "_judo_ai_judge_client", None) or GenAIClient()
        context._judo_ai_judge = GenAIJudge(judge_client)
    return context._judo_ai_judge


def _get_loader(context) -> ContextLoader:
    if not hasattr(context, "_judo_ctx_loader"):
        context._judo_ctx_loader = ContextLoader()
    return context._judo_ctx_loader


def _get_response_text(context) -> str:
    """
    Resolve the AI response text from context.
    Looks for _judo_eval_text (set explicitly) or falls back to
    the last HTTP response body field set via 'I use response field'.
    """
    text = getattr(context, "_judo_eval_text", None)
    assert text, (
        "No AI response text to evaluate. "
        "Use 'I use response field \"<field>\" as AI response' first."
    )
    return text


def _get_rag_context(context) -> str:
    ctx = getattr(context, "_judo_rag_context", None)
    assert ctx, (
        "No RAG context loaded. "
        "Use 'I load RAG context from ...' first."
    )
    return ctx


# ===========================================================================
# STEP 0 — Wire the response to evaluate
# ===========================================================================

@step('I use response field "{field}" as AI response')
def step_use_response_field(context, field):
    """
    Extract a field from the last HTTP response and set it as the text
    to be evaluated by subsequent GenAI steps.

    Example:
        When I send GET request to "/chat/answer"
        Then the response status should be 200
        And I use response field "answer" as AI response
    """
    assert hasattr(context, "judo_context") and context.judo_context.response, \
        "No HTTP response available. Make a REST call first."
    resp = context.judo_context.response
    data = resp.json if resp.json else {}
    # Support dot-notation: "data.choices[0].message.content" -> simple key for now
    parts = field.split(".")
    val = data
    for part in parts:
        if isinstance(val, dict):
            val = val.get(part)
        elif isinstance(val, list):
            try:
                val = val[int(part)]
            except (ValueError, IndexError):
                val = None
        else:
            val = None
        if val is None:
            break
    assert val is not None, f"Field '{field}' not found in response: {data}"
    context._judo_eval_text = str(val)


@step('I use response field "{field}" as AI response with fallback "{fallback}"')
def step_use_response_field_fallback(context, field, fallback):
    """Same as above but uses fallback value if field is missing."""
    try:
        step_use_response_field(context, field)
    except AssertionError:
        context._judo_eval_text = fallback


@step('I set AI response text to "{text}"')
def step_set_response_text(context, text):
    """Manually set the text to evaluate (useful for testing or inline values)."""
    context._judo_eval_text = text


@step('I set AI response text')
def step_set_response_text_multiline(context):
    """Set the AI response text from a multiline docstring."""
    context._judo_eval_text = context.text.strip()


@step('I use variable "{variable_name}" as AI response')
def step_use_variable_as_response(context, variable_name):
    """Use a Judo variable value as the AI response text to evaluate."""
    val = context.judo_context.get_variable(variable_name)
    assert val, f"Variable '{variable_name}' is empty or not set."
    context._judo_eval_text = str(val)


@step('I store AI response text in variable "{variable_name}"')
def step_store_eval_text(context, variable_name):
    """Store the current AI response text in a Judo variable."""
    text = _get_response_text(context)
    context.judo_context.set_variable(variable_name, text)


# ===========================================================================
# STRATEGY 1 — RAG (Retrieval Augmented Generation)
# ===========================================================================

@step('I load RAG context from file "{file_path}"')
def step_rag_load_file(context, file_path):
    """
    Load a local document as RAG context.
    Supports: .txt, .md, .json, .yaml, .csv, .pdf, .docx

    Example:
        Given I load RAG context from file "docs/product_manual.pdf"
    """
    loader = _get_loader(context)
    context._judo_rag_context = loader.load(file_path)


@step('I load RAG context from URL "{url}"')
def step_rag_load_url(context, url):
    """
    Fetch content from a URL and use it as RAG context.

    Example:
        Given I load RAG context from URL "https://docs.myapi.com/faq"
    """
    loader = _get_loader(context)
    context._judo_rag_context = loader.load_url(url)


@step('I load RAG context from multiple files')
def step_rag_load_multiple(context):
    """
    Load multiple files as RAG context (table with column 'file').

    Example:
        Given I load RAG context from multiple files
          | file                    |
          | docs/manual.pdf         |
          | docs/faq.txt            |
    """
    loader = _get_loader(context)
    files = [row["file"] for row in context.table]
    context._judo_rag_context = loader.load_multiple(files)


@step('I set RAG context')
def step_rag_set_inline(context):
    """
    Set RAG context from an inline multiline docstring.

    Example:
        Given I set RAG context
          \"\"\"
          Product: MyApp v2.0
          Price: $99/month
          Support: 24/7
          \"\"\"
    """
    context._judo_rag_context = context.text.strip()


@step('I set RAG context "{text}"')
def step_rag_set_inline_single(context, text):
    """Set RAG context from a single-line string."""
    context._judo_rag_context = text


@step('the AI response should be grounded in RAG context with threshold {threshold:f}')
def step_rag_grounded(context, threshold):
    """
    Assert that the AI response is factually grounded in the loaded RAG context.
    Detects hallucinations — content not supported by the context.
    Threshold: 0.0-1.0 (recommended: 0.6-0.8)

    Example:
        Then the AI response should be grounded in RAG context with threshold 0.7
    """
    text = _get_response_text(context)
    rag_ctx = _get_rag_context(context)
    evaluator = HallucinationEvaluator()
    result = evaluator.evaluate(response=text, context=rag_ctx, threshold=threshold)
    assert result.passed, (
        f"RAG grounding check FAILED: {result.reason}\n"
        f"Score: {result.score:.2%} (threshold: {threshold:.0%})"
    )


@step('the AI response should contain RAG facts with threshold {threshold:f}')
def step_rag_facts(context, threshold):
    """
    Assert that the AI response contains key facts from the RAG context.
    Uses keyword overlap between context and response.
    Threshold: 0.0-1.0 (recommended: 0.5-0.8)

    Example:
        Then the AI response should contain RAG facts with threshold 0.6
    """
    text = _get_response_text(context)
    rag_ctx = _get_rag_context(context)
    # Extract key terms from context as "facts"
    import re
    words = re.findall(r'\b[A-Za-z0-9][A-Za-z0-9\-_\.]{3,}\b', rag_ctx)
    # Deduplicate, keep most significant (longer words)
    facts = list(dict.fromkeys(w for w in words if len(w) > 4))[:30]
    evaluator = FactualAccuracyEvaluator()
    result = evaluator.evaluate(response=text, facts=facts, threshold=threshold)
    assert result.passed, (
        f"RAG facts check FAILED: {result.reason}\n"
        f"Missing terms: {result.details.get('missing', [])[:10]}"
    )


@step('the AI response semantic similarity to RAG context should be at least {threshold:f}')
def step_rag_semantic_similarity(context, threshold):
    """
    Assert that the AI response is semantically similar to the RAG context.
    Useful to verify the response stays on topic with the provided documents.
    Threshold: 0.0-1.0 (recommended: 0.4-0.7)

    Example:
        Then the AI response semantic similarity to RAG context should be at least 0.5
    """
    text = _get_response_text(context)
    rag_ctx = _get_rag_context(context)
    evaluator = SemanticSimilarityEvaluator()
    result = evaluator.evaluate(response=text, expected=rag_ctx, threshold=threshold)
    assert result.passed, (
        f"RAG semantic similarity FAILED: {result.reason}"
    )


# ===========================================================================
# STRATEGY 2 — Semantic Validations
# ===========================================================================

@step('the AI response should not be empty')
def step_not_empty(context):
    """Assert the AI response text is not empty."""
    text = _get_response_text(context)
    assert text.strip(), "AI response is empty."


@step('the AI response should contain "{text}"')
def step_contains(context, text):
    """Assert the AI response contains a specific string (case-insensitive)."""
    resp = _get_response_text(context)
    assert text.lower() in resp.lower(), (
        f"AI response does not contain '{text}'.\nResponse: {resp[:300]}"
    )


@step('the AI response should not contain "{text}"')
def step_not_contains(context, text):
    """Assert the AI response does NOT contain a specific string."""
    resp = _get_response_text(context)
    assert text.lower() not in resp.lower(), (
        f"AI response should not contain '{text}' but it does."
    )


@step('the AI response length should be less than {max_chars:d} characters')
def step_max_length(context, max_chars):
    """Assert the AI response is shorter than max_chars."""
    resp = _get_response_text(context)
    assert len(resp) < max_chars, (
        f"Response is {len(resp)} chars, expected < {max_chars}."
    )


@step('the AI response length should be more than {min_chars:d} characters')
def step_min_length(context, min_chars):
    """Assert the AI response is longer than min_chars."""
    resp = _get_response_text(context)
    assert len(resp) > min_chars, (
        f"Response is {len(resp)} chars, expected > {min_chars}."
    )


@step('the AI response semantic similarity to "{expected}" should be at least {threshold:f}')
def step_semantic_similarity(context, expected, threshold):
    """
    Assert semantic similarity between AI response and an expected answer.
    Uses TF-IDF cosine similarity (requires scikit-learn) or Jaccard fallback.
    Threshold: 0.0-1.0

    Example:
        Then the AI response semantic similarity to "Paris is the capital of France." should be at least 0.6
    """
    text = _get_response_text(context)
    evaluator = SemanticSimilarityEvaluator()
    result = evaluator.evaluate(response=text, expected=expected, threshold=threshold)
    assert result.passed, f"Semantic similarity FAILED: {result.reason}"


@step('the AI response should be relevant to "{prompt}" with threshold {threshold:f}')
def step_relevance(context, prompt, threshold):
    """
    Assert the AI response is relevant to a given prompt/question.
    Uses keyword overlap between prompt and response.
    Threshold: 0.0-1.0 (recommended: 0.3-0.6)

    Example:
        Then the AI response should be relevant to "What is machine learning?" with threshold 0.4
    """
    text = _get_response_text(context)
    evaluator = RelevanceEvaluator()
    result = evaluator.evaluate(response=text, prompt=prompt, threshold=threshold)
    assert result.passed, f"Relevance check FAILED: {result.reason}"


@step('the AI response should not be toxic with threshold {threshold:f}')
def step_toxicity(context, threshold):
    """
    Assert the AI response does not contain toxic content.
    Score 1.0 = clean, 0.0 = highly toxic.
    Threshold: 0.0-1.0 (recommended: 0.8-0.95)

    Example:
        Then the AI response should not be toxic with threshold 0.9
    """
    text = _get_response_text(context)
    evaluator = ToxicityEvaluator()
    result = evaluator.evaluate(response=text, threshold=threshold)
    assert result.passed, f"Toxicity check FAILED: {result.reason}"


@step('the AI response should contain required facts')
def step_factual_accuracy(context):
    """
    Assert the AI response contains all facts listed in the table.
    Table columns: fact, (optional) threshold

    Example:
        Then the AI response should contain required facts
          | fact        |
          | Python      |
          | open source |
    """
    text = _get_response_text(context)
    facts = [row["fact"] for row in context.table]
    threshold = float(context.table[0].get("threshold", 0.8)) if context.table else 0.8
    evaluator = FactualAccuracyEvaluator()
    result = evaluator.evaluate(response=text, facts=facts, threshold=threshold)
    assert result.passed, (
        f"Factual accuracy FAILED: {result.reason}\n"
        f"Missing: {result.details.get('missing', [])}"
    )


@step('the AI response tone should be "{expected_tone}" with threshold {threshold:f}')
def step_tone(context, expected_tone, threshold):
    """
    Assert the AI response matches an expected tone.
    Supported: professional, friendly, formal, concise, empathetic
    Threshold: 0.0-1.0 (recommended: 0.4-0.6)

    Example:
        Then the AI response tone should be "professional" with threshold 0.4
    """
    text = _get_response_text(context)
    evaluator = ToneEvaluator()
    result = evaluator.evaluate(response=text, expected_tone=expected_tone, threshold=threshold)
    assert result.passed, f"Tone check FAILED: {result.reason}"


@step('the AI response should cover required topics with threshold {threshold:f}')
def step_completeness(context, threshold):
    """
    Assert the AI response covers all required topics listed in the table.
    Table column: topic
    Threshold: 0.0-1.0 (recommended: 0.7-0.9)

    Example:
        Then the AI response should cover required topics with threshold 0.8
          | topic  |
          | GET    |
          | POST   |
          | DELETE |
    """
    text = _get_response_text(context)
    topics = [row["topic"] for row in context.table]
    evaluator = CompletenessEvaluator()
    result = evaluator.evaluate(response=text, required_topics=topics, threshold=threshold)
    assert result.passed, (
        f"Completeness FAILED: {result.reason}\n"
        f"Missing topics: {result.details.get('missing', [])}"
    )


# ===========================================================================
# STRATEGY 3 — LLM as Judge
# ===========================================================================

@step('I configure judge AI with provider "{provider}" and model "{model}"')
def step_configure_judge(context, provider, model):
    """
    Configure a specific AI model to act as judge.
    If not called, the judge uses JUDO_AI_PROVIDER from .env.

    Example:
        Given I configure judge AI with provider "openai" and model "gpt-4o"
    """
    from .client import GenAIClient
    from .models import GenAIConfig
    key_map = {
        "openai": "JUDO_OPENAI_API_KEY",
        "claude": "JUDO_CLAUDE_API_KEY",
        "gemini": "JUDO_GEMINI_API_KEY",
    }
    api_key = os.getenv(key_map.get(provider.lower(), "JUDO_AI_API_KEY"), "")
    config = GenAIConfig(provider=provider.lower(), api_key=api_key, model=model)
    context._judo_ai_judge_client = GenAIClient(config)
    context._judo_ai_judge = GenAIJudge(context._judo_ai_judge_client)


@step('I set judge criteria "{criteria}"')
def step_set_judge_criteria(context, criteria):
    """Store evaluation criteria for use in subsequent judge steps."""
    context._judo_judge_criteria = criteria


@step('I set judge criteria')
def step_set_judge_criteria_multiline(context):
    """Store multiline evaluation criteria."""
    context._judo_judge_criteria = context.text.strip()


@step('I set judge prompt "{prompt}"')
def step_set_judge_prompt(context, prompt):
    """Store the original prompt/question for judge context."""
    context._judo_judge_prompt = prompt


@step('I evaluate the AI response as judge with criteria "{criteria}" and threshold {threshold:f}')
def step_judge_evaluate(context, criteria, threshold):
    """
    Use an LLM judge to evaluate the AI response against given criteria.
    The judge returns a score (0.0-1.0), verdict (PASS/FAIL) and reasoning.

    Example:
        Then I evaluate the AI response as judge with criteria "The response should clearly explain REST APIs and mention HTTP methods." and threshold 0.7
    """
    text = _get_response_text(context)
    prompt = getattr(context, "_judo_judge_prompt", "")
    judge = _get_judge(context)
    context._judo_judge_result = judge.evaluate(
        prompt=prompt,
        response=text,
        criteria=criteria,
        threshold=threshold,
    )


@step('I evaluate the AI response as judge with threshold {threshold:f}')
def step_judge_evaluate_multiline(context, threshold):
    """
    Use an LLM judge with multiline criteria from a docstring.

    Example:
        Then I evaluate the AI response as judge with threshold 0.7
          \"\"\"
          The response must:
          1. Be accurate and factual
          2. Be concise (under 200 words)
          3. Use professional language
          \"\"\"
    """
    text = _get_response_text(context)
    prompt = getattr(context, "_judo_judge_prompt", "")
    criteria = context.text.strip()
    judge = _get_judge(context)
    context._judo_judge_result = judge.evaluate(
        prompt=prompt,
        response=text,
        criteria=criteria,
        threshold=threshold,
    )


@step('I evaluate the AI response as judge against RAG context with criteria "{criteria}" and threshold {threshold:f}')
def step_judge_evaluate_rag(context, criteria, threshold):
    """
    Use an LLM judge to evaluate the response against RAG context.
    The judge receives the context as ground truth for factual evaluation.

    Example:
        Then I evaluate the AI response as judge against RAG context with criteria "Response must be consistent with the provided documentation." and threshold 0.7
    """
    text = _get_response_text(context)
    rag_ctx = _get_rag_context(context)
    prompt = getattr(context, "_judo_judge_prompt", "")
    judge = _get_judge(context)
    context._judo_judge_result = judge.evaluate(
        prompt=prompt,
        response=text,
        criteria=criteria,
        threshold=threshold,
        context=rag_ctx,
    )


@step('I evaluate the AI response as judge against RAG context with threshold {threshold:f}')
def step_judge_evaluate_rag_multiline(context, threshold):
    """
    LLM judge against RAG context with multiline criteria.

    Example:
        Then I evaluate the AI response as judge against RAG context with threshold 0.7
          \"\"\"
          The response must be factually consistent with the provided context.
          It should not introduce information not present in the context.
          \"\"\"
    """
    text = _get_response_text(context)
    rag_ctx = _get_rag_context(context)
    prompt = getattr(context, "_judo_judge_prompt", "")
    criteria = context.text.strip()
    judge = _get_judge(context)
    context._judo_judge_result = judge.evaluate(
        prompt=prompt,
        response=text,
        criteria=criteria,
        threshold=threshold,
        context=rag_ctx,
    )


@step('the judge evaluation should pass')
def step_judge_pass(context):
    """Assert that the LLM judge evaluation passed."""
    result = getattr(context, "_judo_judge_result", None)
    assert result, "No judge evaluation available. Run an 'I evaluate...' step first."
    assert result.passed, (
        f"Judge evaluation FAILED.\n"
        f"Score: {result.score:.2%} (threshold: {result.threshold:.0%})\n"
        f"Reasoning: {result.reasoning}"
    )


@step('the judge score should be at least {min_score:f}')
def step_judge_min_score(context, min_score):
    """Assert the judge score meets a minimum value."""
    result = getattr(context, "_judo_judge_result", None)
    assert result, "No judge evaluation available."
    assert result.score >= min_score, (
        f"Judge score {result.score:.2%} < minimum {min_score:.0%}.\n"
        f"Reasoning: {result.reasoning}"
    )


@step('I print the AI response text')
def step_print_response(context):
    """Print the current AI response text for debugging."""
    text = getattr(context, "_judo_eval_text", None)
    if text:
        print(f"\n=== AI Response Text ===\n{text}\n========================\n")
    else:
        print("No AI response text set.")


@step('I print the judge evaluation result')
def step_print_judge(context):
    """Print the judge evaluation result for debugging."""
    result = getattr(context, "_judo_judge_result", None)
    if result:
        print(f"\n=== Judge Evaluation ===")
        print(f"Verdict   : {result.verdict}")
        print(f"Score     : {result.score:.2%}")
        print(f"Threshold : {result.threshold:.0%}")
        print(f"Reasoning : {result.reasoning}")
        print(f"========================\n")
    else:
        print("No judge evaluation available.")
