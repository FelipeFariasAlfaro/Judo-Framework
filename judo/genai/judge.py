"""
GenAI Judge - Uses an AI model to evaluate another AI's response.
Implements the LLM-as-a-Judge pattern.
"""

import json
import re
from typing import Any, Dict, List, Optional

from .client import GenAIClient
from .models import GenAIConfig, JudgeResult


_JUDGE_PROMPT_TEMPLATE = """You are an expert AI evaluator. Your task is to evaluate an AI response based on specific criteria.

## Evaluation Criteria
{criteria}

## Original Prompt / Question
{prompt}

## AI Response to Evaluate
{response}

{context_section}

## Instructions
Evaluate the response strictly based on the criteria above.
Respond ONLY with a valid JSON object in this exact format:
{{
  "score": <float between 0.0 and 1.0>,
  "verdict": "<PASS or FAIL>",
  "reasoning": "<detailed explanation of your evaluation>",
  "strengths": ["<strength 1>", "<strength 2>"],
  "weaknesses": ["<weakness 1>", "<weakness 2>"]
}}

Do not include any text outside the JSON object.
"""

_CONTEXT_SECTION_TEMPLATE = """## Reference Context / Ground Truth
{context}
"""


class GenAIJudge:
    """
    Uses an AI model as a judge to evaluate another AI's response.
    The judge model can be the same or different from the model under test.
    """

    def __init__(self, judge_client: Optional[GenAIClient] = None):
        """
        Args:
            judge_client: The GenAIClient to use as judge.
                          If None, creates one from environment variables.
                          You can use a different provider/model for the judge.
        """
        self._client = judge_client or GenAIClient()

    def evaluate(
        self,
        prompt: str,
        response: str,
        criteria: str,
        threshold: float = 0.7,
        context: Optional[str] = None,
    ) -> JudgeResult:
        """
        Ask the judge model to evaluate a response.

        Args:
            prompt: The original question/prompt sent to the AI under test.
            response: The AI response to evaluate.
            criteria: Natural language description of what makes a good response.
            threshold: Minimum score (0.0-1.0) to consider the evaluation passed.
            context: Optional reference context or ground truth.

        Returns:
            JudgeResult with score, verdict, and reasoning.
        """
        context_section = (
            _CONTEXT_SECTION_TEMPLATE.format(context=context) if context else ""
        )

        judge_prompt = _JUDGE_PROMPT_TEMPLATE.format(
            criteria=criteria,
            prompt=prompt,
            response=response,
            context_section=context_section,
        )

        judge_response = self._client.send(judge_prompt)
        return self._parse_judge_response(
            judge_response.text, criteria, threshold
        )

    def evaluate_batch(
        self,
        evaluations: List[Dict[str, Any]],
        threshold: float = 0.7,
    ) -> List[JudgeResult]:
        """
        Evaluate multiple prompt/response pairs.

        Args:
            evaluations: List of dicts with keys: prompt, response, criteria,
                         and optionally context and threshold.
            threshold: Default threshold if not specified per evaluation.

        Returns:
            List of JudgeResult objects.
        """
        results = []
        for item in evaluations:
            result = self.evaluate(
                prompt=item["prompt"],
                response=item["response"],
                criteria=item["criteria"],
                threshold=item.get("threshold", threshold),
                context=item.get("context"),
            )
            results.append(result)
        return results

    def _parse_judge_response(
        self, raw: str, criteria: str, threshold: float
    ) -> JudgeResult:
        """Parse the judge's JSON response into a JudgeResult."""
        # Extract JSON from the response (handle markdown code blocks)
        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not json_match:
            # Fallback: judge response was not parseable
            return JudgeResult(
                passed=False,
                score=0.0,
                threshold=threshold,
                verdict="FAIL",
                reasoning=f"Judge response could not be parsed: {raw[:200]}",
                criteria=criteria,
                raw_judge_response=raw,
            )

        try:
            data = json.loads(json_match.group())
        except json.JSONDecodeError as e:
            return JudgeResult(
                passed=False,
                score=0.0,
                threshold=threshold,
                verdict="FAIL",
                reasoning=f"JSON parse error: {e}. Raw: {raw[:200]}",
                criteria=criteria,
                raw_judge_response=raw,
            )

        score = float(data.get("score", 0.0))
        verdict = data.get("verdict", "FAIL").upper()
        reasoning = data.get("reasoning", "")

        # Normalize: if verdict says PASS but score < threshold, use score
        passed = score >= threshold

        return JudgeResult(
            passed=passed,
            score=round(score, 4),
            threshold=threshold,
            verdict="PASS" if passed else "FAIL",
            reasoning=reasoning,
            criteria=criteria,
            raw_judge_response=raw,
        )
