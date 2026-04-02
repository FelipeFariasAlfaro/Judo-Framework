"""
GenAI Client - Unified client for OpenAI, Anthropic Claude, and Google Gemini
"""

import os
import time
from typing import Any, Dict, List, Optional

from .models import GenAIConfig, GenAIResponse


class GenAIClient:
    """
    Unified client for interacting with GenAI providers.
    Supports OpenAI, Anthropic Claude, and Google Gemini.
    Configuration is loaded from environment variables or passed directly.
    """

    SUPPORTED_PROVIDERS = ("openai", "claude", "gemini")

    def __init__(self, config: Optional[GenAIConfig] = None):
        """
        Initialize the client. If no config is provided, loads from environment.
        """
        if config:
            self.config = config
        else:
            self.config = self._load_from_env()

        self._validate_config()
        self._context_documents: List[str] = []
        self._system_prompt: Optional[str] = None
        self._conversation_history: List[Dict[str, str]] = []

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def _load_from_env(self) -> GenAIConfig:
        """Load configuration from environment variables."""
        provider = os.getenv("JUDO_AI_PROVIDER", "").lower().strip()
        if not provider:
            raise ValueError(
                "JUDO_AI_PROVIDER not set. "
                "Set it to 'openai', 'claude', or 'gemini' in your .env file."
            )

        # Resolve API key and default model per provider
        if provider == "openai":
            api_key = os.getenv("JUDO_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY", "")
            model = os.getenv("JUDO_AI_MODEL", "gpt-4o")
        elif provider == "claude":
            api_key = os.getenv("JUDO_CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY", "")
            model = os.getenv("JUDO_AI_MODEL", "claude-3-5-sonnet-20241022")
        elif provider == "gemini":
            api_key = os.getenv("JUDO_GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
            model = os.getenv("JUDO_AI_MODEL", "gemini-1.5-pro")
        else:
            raise ValueError(
                f"Unsupported provider '{provider}'. "
                f"Choose from: {self.SUPPORTED_PROVIDERS}"
            )

        return GenAIConfig(
            provider=provider,
            api_key=api_key,
            model=model,
            temperature=float(os.getenv("JUDO_AI_TEMPERATURE", "0.0")),
            max_tokens=int(os.getenv("JUDO_AI_MAX_TOKENS", "2048")),
            timeout=int(os.getenv("JUDO_AI_TIMEOUT", "60")),
        )

    def _validate_config(self):
        """Validate that the configuration is complete."""
        if self.config.provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported provider '{self.config.provider}'. "
                f"Choose from: {self.SUPPORTED_PROVIDERS}"
            )
        if not self.config.api_key:
            raise ValueError(
                f"API key for provider '{self.config.provider}' is not set. "
                f"Check your .env file."
            )

    # ------------------------------------------------------------------
    # Context & System Prompt
    # ------------------------------------------------------------------

    def set_system_prompt(self, prompt: str):
        """Set a system-level prompt for all subsequent calls."""
        self._system_prompt = prompt

    def add_context_document(self, content: str):
        """Add a document as context (appended to system prompt)."""
        self._context_documents.append(content)

    def clear_context(self):
        """Clear all context documents."""
        self._context_documents.clear()

    def clear_history(self):
        """Clear conversation history."""
        self._conversation_history.clear()

    def _build_system_prompt(self) -> str:
        """Build the full system prompt including context documents."""
        parts = []
        if self._system_prompt:
            parts.append(self._system_prompt)
        if self._context_documents:
            parts.append("\n\n--- CONTEXT DOCUMENTS ---")
            for i, doc in enumerate(self._context_documents, 1):
                parts.append(f"\n[Document {i}]:\n{doc}")
            parts.append("\n--- END CONTEXT ---")
        return "\n".join(parts) if parts else ""

    # ------------------------------------------------------------------
    # Core send method
    # ------------------------------------------------------------------

    def send(self, prompt: str, keep_history: bool = False) -> GenAIResponse:
        """
        Send a prompt to the configured AI provider and return the response.

        Args:
            prompt: The user message/prompt to send.
            keep_history: If True, maintains conversation history across calls.

        Returns:
            GenAIResponse with the model's reply and metadata.
        """
        if keep_history:
            self._conversation_history.append({"role": "user", "content": prompt})

        start = time.time()

        if self.config.provider == "openai":
            response = self._send_openai(prompt, keep_history)
        elif self.config.provider == "claude":
            response = self._send_claude(prompt, keep_history)
        elif self.config.provider == "gemini":
            response = self._send_gemini(prompt, keep_history)
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

        response.latency_ms = (time.time() - start) * 1000

        if keep_history:
            self._conversation_history.append(
                {"role": "assistant", "content": response.text}
            )

        return response

    # ------------------------------------------------------------------
    # Provider implementations
    # ------------------------------------------------------------------

    def _send_openai(self, prompt: str, keep_history: bool) -> GenAIResponse:
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "openai package not installed. Run: pip install openai"
            )

        client = OpenAI(api_key=self.config.api_key)
        system_prompt = self._build_system_prompt()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if keep_history and self._conversation_history:
            # Add history except the last user message (already added)
            messages.extend(self._conversation_history[:-1])

        messages.append({"role": "user", "content": prompt})

        resp = client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            timeout=self.config.timeout,
            **self.config.extra_params,
        )

        return GenAIResponse(
            text=resp.choices[0].message.content,
            provider="openai",
            model=self.config.model,
            prompt_tokens=resp.usage.prompt_tokens,
            completion_tokens=resp.usage.completion_tokens,
            total_tokens=resp.usage.total_tokens,
            raw=resp,
        )

    def _send_claude(self, prompt: str, keep_history: bool) -> GenAIResponse:
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "anthropic package not installed. Run: pip install anthropic"
            )

        client = anthropic.Anthropic(api_key=self.config.api_key)
        system_prompt = self._build_system_prompt()

        messages = []
        if keep_history and self._conversation_history:
            messages.extend(self._conversation_history[:-1])
        messages.append({"role": "user", "content": prompt})

        kwargs: Dict[str, Any] = dict(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            messages=messages,
            **self.config.extra_params,
        )
        if system_prompt:
            kwargs["system"] = system_prompt

        resp = client.messages.create(**kwargs)

        text = resp.content[0].text if resp.content else ""
        return GenAIResponse(
            text=text,
            provider="claude",
            model=self.config.model,
            prompt_tokens=resp.usage.input_tokens,
            completion_tokens=resp.usage.output_tokens,
            total_tokens=resp.usage.input_tokens + resp.usage.output_tokens,
            raw=resp,
        )

    def _send_gemini(self, prompt: str, keep_history: bool) -> GenAIResponse:
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError(
                "google-generativeai package not installed. "
                "Run: pip install google-generativeai"
            )

        genai.configure(api_key=self.config.api_key)
        system_prompt = self._build_system_prompt()

        generation_config = genai.GenerationConfig(
            temperature=self.config.temperature,
            max_output_tokens=self.config.max_tokens,
        )

        model_kwargs: Dict[str, Any] = {"generation_config": generation_config}
        if system_prompt:
            model_kwargs["system_instruction"] = system_prompt

        model = genai.GenerativeModel(self.config.model, **model_kwargs)

        if keep_history and self._conversation_history:
            history = [
                {"role": m["role"], "parts": [m["content"]]}
                for m in self._conversation_history[:-1]
            ]
            chat = model.start_chat(history=history)
            resp = chat.send_message(prompt)
        else:
            resp = model.generate_content(prompt)

        text = resp.text if hasattr(resp, "text") else ""
        usage = getattr(resp, "usage_metadata", None)
        prompt_tokens = getattr(usage, "prompt_token_count", 0) if usage else 0
        completion_tokens = getattr(usage, "candidates_token_count", 0) if usage else 0

        return GenAIResponse(
            text=text,
            provider="gemini",
            model=self.config.model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            raw=resp,
        )
