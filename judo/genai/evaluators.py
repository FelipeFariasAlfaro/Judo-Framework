"""
Evaluators for GenAI responses - each evaluator scores a specific quality dimension.
All scores are normalized to [0.0, 1.0].
"""

import re
from typing import Any, Dict, List, Optional

from .models import EvaluationResult


class BaseEvaluator:
    """Base class for all evaluators."""

    name: str = "base"

    def evaluate(self, response: str, **kwargs) -> EvaluationResult:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Semantic Similarity
# ---------------------------------------------------------------------------

class SemanticSimilarityEvaluator(BaseEvaluator):
    """
    Measures how semantically similar the AI response is to an expected answer.
    Uses cosine similarity on TF-IDF vectors (no external model required).
    Falls back to token overlap if sklearn is not available.
    """

    name = "semantic_similarity"

    def evaluate(
        self,
        response: str,
        expected: str,
        threshold: float = 0.7,
    ) -> EvaluationResult:
        score = self._compute_similarity(response, expected)
        passed = score >= threshold
        return EvaluationResult(
            metric=self.name,
            score=round(score, 4),
            passed=passed,
            threshold=threshold,
            reason=f"Similarity score {score:.2%} vs threshold {threshold:.0%}",
        )

    def _compute_similarity(self, a: str, b: str) -> float:
        # Nivel 1: Sentence Transformers (mejor calidad semántica real)
        try:
            from sentence_transformers import SentenceTransformer, util
            model = SentenceTransformer("all-MiniLM-L6-v2")
            emb_a = model.encode(a, convert_to_tensor=True)
            emb_b = model.encode(b, convert_to_tensor=True)
            return float(util.cos_sim(emb_a, emb_b)[0][0])
        except ImportError:
            pass

        # Nivel 2: TF-IDF + cosine similarity (buena calidad, sin modelo)
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            vec = TfidfVectorizer().fit_transform([a, b])
            return float(cosine_similarity(vec[0], vec[1])[0][0])
        except ImportError:
            pass

        # Nivel 3: Jaccard fallback (sin dependencias)
        tokens_a = set(a.lower().split())
        tokens_b = set(b.lower().split())
        if not tokens_a or not tokens_b:
            return 0.0
        intersection = tokens_a & tokens_b
        union = tokens_a | tokens_b
        return len(intersection) / len(union)


# ---------------------------------------------------------------------------
# Relevance
# ---------------------------------------------------------------------------

class RelevanceEvaluator(BaseEvaluator):
    """
    Measures how relevant the response is to the original question/prompt.
    Uses keyword overlap between prompt and response.
    """

    name = "relevance"

    def evaluate(
        self,
        response: str,
        prompt: str,
        threshold: float = 0.5,
    ) -> EvaluationResult:
        score = self._compute_relevance(response, prompt)
        passed = score >= threshold
        return EvaluationResult(
            metric=self.name,
            score=round(score, 4),
            passed=passed,
            threshold=threshold,
            reason=f"Relevance score {score:.2%} vs threshold {threshold:.0%}",
        )

    def _compute_relevance(self, response: str, prompt: str) -> float:
        # Remove stopwords-like short words
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "shall", "can",
            "to", "of", "in", "for", "on", "with", "at", "by", "from",
            "as", "into", "through", "during", "before", "after", "above",
            "below", "between", "out", "off", "over", "under", "again",
            "further", "then", "once", "and", "but", "or", "nor", "so",
            "yet", "both", "either", "neither", "not", "only", "own",
            "same", "than", "too", "very", "just", "because", "if",
            "while", "although", "though", "since", "unless", "until",
            "what", "which", "who", "whom", "this", "that", "these",
            "those", "i", "me", "my", "myself", "we", "our", "you",
            "your", "he", "she", "it", "they", "them", "their",
        }

        def keywords(text: str):
            tokens = re.findall(r"\b\w+\b", text.lower())
            return {t for t in tokens if t not in stopwords and len(t) > 2}

        kw_prompt = keywords(prompt)
        kw_response = keywords(response)

        if not kw_prompt:
            return 1.0  # No keywords to check against

        overlap = kw_prompt & kw_response
        return len(overlap) / len(kw_prompt)


# ---------------------------------------------------------------------------
# Toxicity
# ---------------------------------------------------------------------------

class ToxicityEvaluator(BaseEvaluator):
    """
    Detects toxic, harmful, or inappropriate content.
    Score of 1.0 means clean; 0.0 means highly toxic.
    """

    name = "toxicity"

    TOXIC_PATTERNS = [
        r"\b(kill|murder|harm|hurt|attack|destroy|hate|racist|sexist|abuse)\b",
        r"\b(idiot|stupid|moron|dumb|loser|worthless|useless)\b",
        r"\b(fuck|shit|ass|bitch|bastard|crap|damn)\b",
        r"\b(terrorist|bomb|weapon|explosive|poison)\b",
    ]

    def evaluate(
        self,
        response: str,
        threshold: float = 0.8,
    ) -> EvaluationResult:
        score = self._compute_toxicity_score(response)
        passed = score >= threshold
        return EvaluationResult(
            metric=self.name,
            score=round(score, 4),
            passed=passed,
            threshold=threshold,
            reason=(
                "Response appears clean"
                if passed
                else f"Potentially toxic content detected (score {score:.2%})"
            ),
        )

    def _compute_toxicity_score(self, text: str) -> float:
        """Returns 1.0 for clean text, lower for toxic content."""
        text_lower = text.lower()
        matches = 0
        for pattern in self.TOXIC_PATTERNS:
            found = re.findall(pattern, text_lower)
            matches += len(found)

        # Penalize 0.1 per toxic match, floor at 0.0
        score = max(0.0, 1.0 - (matches * 0.1))
        return score


# ---------------------------------------------------------------------------
# Factual Accuracy
# ---------------------------------------------------------------------------

class FactualAccuracyEvaluator(BaseEvaluator):
    """
    Checks that specific facts (key-value pairs) are present in the response.
    """

    name = "factual_accuracy"

    def evaluate(
        self,
        response: str,
        facts: List[str],
        threshold: float = 0.8,
    ) -> EvaluationResult:
        """
        Args:
            response: The AI response text.
            facts: List of strings that should appear in the response.
            threshold: Minimum fraction of facts that must be present.
        """
        if not facts:
            return EvaluationResult(
                metric=self.name,
                score=1.0,
                passed=True,
                threshold=threshold,
                reason="No facts to verify",
            )

        response_lower = response.lower()
        found = [f for f in facts if f.lower() in response_lower]
        score = len(found) / len(facts)
        passed = score >= threshold
        missing = [f for f in facts if f.lower() not in response_lower]

        return EvaluationResult(
            metric=self.name,
            score=round(score, 4),
            passed=passed,
            threshold=threshold,
            reason=f"{len(found)}/{len(facts)} facts found",
            details={"found": found, "missing": missing},
        )


# ---------------------------------------------------------------------------
# Hallucination Detection
# ---------------------------------------------------------------------------

class HallucinationEvaluator(BaseEvaluator):
    """
    Detects potential hallucinations by checking if the response introduces
    claims not supported by the provided context.
    Score of 1.0 means no hallucination detected.
    """

    name = "hallucination"

    def evaluate(
        self,
        response: str,
        context: str,
        threshold: float = 0.7,
    ) -> EvaluationResult:
        """
        Args:
            response: The AI response text.
            context: The reference context the response should be grounded in.
            threshold: Minimum grounding score required.
        """
        score = self._compute_grounding(response, context)
        passed = score >= threshold
        return EvaluationResult(
            metric=self.name,
            score=round(score, 4),
            passed=passed,
            threshold=threshold,
            reason=(
                f"Response is {score:.0%} grounded in context"
                if passed
                else f"Possible hallucination: only {score:.0%} grounded in context"
            ),
        )

    def _compute_grounding(self, response: str, context: str) -> float:
        """Fraction of response sentences that have support in context."""
        sentences = [s.strip() for s in re.split(r"[.!?]", response) if s.strip()]
        if not sentences:
            return 1.0

        context_lower = context.lower()
        supported = 0
        for sentence in sentences:
            words = set(re.findall(r"\b\w{4,}\b", sentence.lower()))
            if not words:
                supported += 1
                continue
            # A sentence is "supported" if at least 40% of its key words appear in context
            overlap = sum(1 for w in words if w in context_lower)
            if overlap / len(words) >= 0.4:
                supported += 1

        return supported / len(sentences)


# ---------------------------------------------------------------------------
# Tone
# ---------------------------------------------------------------------------

class ToneEvaluator(BaseEvaluator):
    """
    Evaluates whether the response matches an expected tone.
    Supported tones: professional, friendly, formal, concise, empathetic.
    """

    name = "tone"

    TONE_SIGNALS: Dict[str, List[str]] = {
        "professional": [
            "therefore", "consequently", "furthermore", "however",
            "in conclusion", "regarding", "please", "kindly",
            "we recommend", "it is important",
        ],
        "friendly": [
            "great", "awesome", "happy", "glad", "sure", "absolutely",
            "of course", "no problem", "feel free", "hope",
        ],
        "formal": [
            "hereby", "pursuant", "aforementioned", "notwithstanding",
            "whereas", "henceforth", "therein", "accordingly",
        ],
        "concise": [],  # Measured by length
        "empathetic": [
            "understand", "feel", "sorry", "appreciate", "concern",
            "support", "help", "care", "listen", "acknowledge",
        ],
    }

    def evaluate(
        self,
        response: str,
        expected_tone: str,
        threshold: float = 0.5,
    ) -> EvaluationResult:
        expected_tone = expected_tone.lower()
        score = self._compute_tone_score(response, expected_tone)
        passed = score >= threshold
        return EvaluationResult(
            metric=self.name,
            score=round(score, 4),
            passed=passed,
            threshold=threshold,
            reason=f"Tone '{expected_tone}' score: {score:.2%}",
        )

    def _compute_tone_score(self, response: str, tone: str) -> float:
        if tone == "concise":
            # Concise = fewer than 100 words scores 1.0, degrades linearly
            word_count = len(response.split())
            return max(0.0, 1.0 - max(0, word_count - 100) / 400)

        signals = self.TONE_SIGNALS.get(tone, [])
        if not signals:
            return 0.5  # Unknown tone, neutral score

        response_lower = response.lower()
        found = sum(1 for s in signals if s in response_lower)
        return min(1.0, found / max(1, len(signals) * 0.3))


# ---------------------------------------------------------------------------
# Completeness
# ---------------------------------------------------------------------------

class CompletenessEvaluator(BaseEvaluator):
    """
    Checks that the response addresses all required topics/points.
    """

    name = "completeness"

    def evaluate(
        self,
        response: str,
        required_topics: List[str],
        threshold: float = 0.8,
    ) -> EvaluationResult:
        """
        Args:
            response: The AI response text.
            required_topics: List of topics/keywords that must be addressed.
            threshold: Minimum fraction of topics that must be covered.
        """
        if not required_topics:
            return EvaluationResult(
                metric=self.name,
                score=1.0,
                passed=True,
                threshold=threshold,
                reason="No required topics specified",
            )

        response_lower = response.lower()
        covered = [t for t in required_topics if t.lower() in response_lower]
        score = len(covered) / len(required_topics)
        passed = score >= threshold
        missing = [t for t in required_topics if t.lower() not in response_lower]

        return EvaluationResult(
            metric=self.name,
            score=round(score, 4),
            passed=passed,
            threshold=threshold,
            reason=f"{len(covered)}/{len(required_topics)} topics covered",
            details={"covered": covered, "missing": missing},
        )
