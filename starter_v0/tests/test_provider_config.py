from __future__ import annotations

from providers import make_provider


def test_groq_provider_uses_groq_credentials_and_endpoint(monkeypatch) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "test-groq-key")
    monkeypatch.delenv("GROQ_BASE_URL", raising=False)
    monkeypatch.delenv("GROQ_MODEL", raising=False)

    provider = make_provider("groq")

    assert provider.api_key_env == "GROQ_API_KEY"
    assert provider.base_url == "https://api.groq.com/openai/v1"
    assert provider.default_model == "openai/gpt-oss-20b"


def test_groq_provider_allows_endpoint_and_model_overrides(monkeypatch) -> None:
    monkeypatch.setenv("GROQ_BASE_URL", "https://groq.example/v1")
    monkeypatch.setenv("GROQ_MODEL", "custom-model")

    provider = make_provider("groq")

    assert provider.base_url == "https://groq.example/v1"
    assert provider.default_model == "custom-model"
