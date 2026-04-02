"""
Data models for GenAI testing module
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class GenAIConfig:
    """Configuration for a GenAI provider"""
    provider: str           # "openai", "claude", "gemini"
    api_key: str
    model: str
    temperature: float = 0.0
    max_tokens: int = 2048
    timeout: int = 60
    extra_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GenAIResponse:
    """Response from a GenAI provider"""
    text: str
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0
    raw: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """Result of a single evaluation metric"""
    metric: str
    score: float            # 0.0 to 1.0
    passed: bool
    threshold: float
    reason: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JudgeResult:
    """Result from the AI judge evaluation"""
    passed: bool
    score: float            # 0.0 to 1.0
    threshold: float
    verdict: str            # "PASS" / "FAIL"
    reasoning: str
    criteria: str
    evaluations: List[EvaluationResult] = field(default_factory=list)
    raw_judge_response: str = ""
