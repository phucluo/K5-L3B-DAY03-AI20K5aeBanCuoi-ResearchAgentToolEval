from __future__ import annotations

import os
from typing import Any

from providers.base import ModelResponse
from providers.openai_provider import OpenAIProvider


class GroqProvider(OpenAIProvider):
    """Groq uses an OpenAI-compatible Chat Completions surface with automatic rate limit fallback."""

    def __init__(self) -> None:
        super().__init__(
            api_key_env="GROQ_API_KEY",
            base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
            default_model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        )

    def complete(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.0,
        tool_choice: Any | None = None,
    ) -> ModelResponse:
        target_model = model or self.default_model
        try:
            return super().complete(
                messages,
                tools,
                model=target_model,
                temperature=temperature,
                tool_choice=tool_choice,
            )
        except Exception as exc:
            if "429" in str(exc) and "gpt-oss-20b" not in target_model:
                return super().complete(
                    messages,
                    tools,
                    model="openai/gpt-oss-20b",
                    temperature=temperature,
                    tool_choice=tool_choice,
                )
            raise

