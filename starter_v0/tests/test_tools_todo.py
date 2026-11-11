"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below has been implemented to verify offline behaviors using fixtures in conftest.py.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    clarify_tool = TOOL_FUNCTIONS["clarify"]
    result = clarify_tool(question="Select option", response_type="choice", options=["opt1", "opt2"])
    assert result["options"] == ["opt1", "opt2"]
    assert result["awaiting_user"] is True
    assert result["response_type"] == "choice"


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    format_tool = TOOL_FUNCTIONS["format"]
    items = [
        {"title": "Item 1", "section": "A"},
        {"title": "Item 2", "section": "B"},
        {"title": "Item 3", "section": "A"},
    ]
    result = format_tool(items=items, template="sections")
    assert result["markdown"].count("## A") == 1
    assert result["markdown"].count("## B") == 1


def test_format_thread_numbers_items() -> None:
    format_tool = TOOL_FUNCTIONS["format"]
    items = [{"title": "First"}, {"title": "Second"}]
    result = format_tool(items=items, template="thread")
    assert "1/ " in result["markdown"]
    assert "2/ " in result["markdown"]


def test_format_empty_items_does_not_crash() -> None:
    format_tool = TOOL_FUNCTIONS["format"]
    res1 = format_tool(items=None)
    assert res1["item_count"] == 0
    res2 = format_tool(items=[])
    assert res2["item_count"] == 0


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "123456")
    calls = fake_http(FakeResponse({"ok": True}))
    send_tool = TOOL_FUNCTIONS["send"]
    result = send_tool(text="Test message", confirmed=True)
    assert len(calls) == 1
    assert "fake-token" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "123456"
    assert calls[0]["json"]["text"] == "Test message"
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    send_tool = TOOL_FUNCTIONS["send"]
    result = send_tool(text="Test message", confirmed=True)
    assert "error" in result
    assert calls == []


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "fake-key")
    calls = fake_http(FakeResponse({"results": []}))
    lookup_tool = TOOL_FUNCTIONS["lookup"]
    lookup_tool(query="test", timeframe=None)
    assert len(calls) == 1
    assert "time_range" not in calls[0]["json"]


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fake-key")
    calls = fake_http(FakeResponse({
        "data": {
            "markdown": "Sample article content",
            "metadata": {"title": "Sample Title", "sourceURL": "https://example.com/article"}
        }
    }))
    fetch_tool = TOOL_FUNCTIONS["fetch"]
    result = fetch_tool(url="https://example.com/article")
    assert len(result["items"]) == 1
    item = result["items"][0]
    assert item["title"] == "Sample Title"
    assert item["url"] == "https://example.com/article"
    assert item["source"] == "example.com"
    assert item["summary"] == "Sample article content"


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fake-key")
    long_content = "x" * 6000
    calls = fake_http(FakeResponse({
        "data": {
            "markdown": long_content,
            "metadata": {"title": "Long Title", "sourceURL": "https://example.com/long"}
        }
    }))
    fetch_tool = TOOL_FUNCTIONS["fetch"]
    result = fetch_tool(url="https://example.com/long")
    assert len(result["items"][0]["summary"]) == 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "fake-key")
    payload = {
        "timeline": [
            {"text": "missing tweet id"},
            {"tweet_id": "101", "screen_name": "sama", "text": "Post 1"},
            {"tweet_id": "102", "screen_name": "sama", "text": "Post 2"},
            {"tweet_id": "103", "screen_name": "sama", "text": "Post 3"},
            {"tweet_id": "104", "screen_name": "sama", "text": "Post 4"},
            {"tweet_id": "105", "screen_name": "sama", "text": "Post 5"},
            {"tweet_id": "106", "screen_name": "sama", "text": "Post 6"},
        ]
    }
    calls = fake_http(FakeResponse(payload))
    timeline_tool = TOOL_FUNCTIONS["timeline"]
    result = timeline_tool(screenname="sama", limit=3)
    assert len(result["items"]) == 3
    for it in result["items"]:
        assert it["url"].startswith("https://x.com/sama/status/")


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "fake-key")
    calls = fake_http(FakeResponse({"tweets": []}))
    social_search_tool = TOOL_FUNCTIONS["social_search"]
    social_search_tool(query="OpenAI", search_type="Top")
    assert len(calls) == 1
    assert calls[0]["params"]["query"] == "OpenAI"
    assert calls[0]["params"]["search_type"] == "Top"


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    policy_tool = TOOL_FUNCTIONS["policy"]
    result = policy_tool(query="")
    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    policy_tool = TOOL_FUNCTIONS["policy"]
    result = policy_tool(query="data", policy_area="data_privacy")
    assert len(result["results"]) > 0
    for it in result["results"]:
        assert it["policy_area"] == "data_privacy"


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    policy_tool = TOOL_FUNCTIONS["policy"]
    result = policy_tool(query="probe", policy_area="source_citation")
    assert len(result["results"]) > 0
    item = result["results"][0]
    assert len(item.get("untrusted_text", [])) > 0
    assert "Assistant: ignore" in item["untrusted_text"][0]
    assert "Assistant: ignore" not in item["facts"]


# ---------------- YOUR NEW TOOL(S) ----------------

def test_my_new_tool_happy_path() -> None:
    tool = TOOL_FUNCTIONS["summarize_paper"]
    sample_paper = (
        "We propose a new Transformer architecture for agent reasoning. "
        "Our experiments show that the model outperforms state of the art baselines by 15%. "
        "The main limitation of our approach is the computational cost of training."
    )
    result = tool(paper_text=sample_paper, focus_area="findings", max_points=2)
    assert result["status"] == "success"
    assert result["focus_area"] == "findings"
    assert result["point_count"] > 0
    assert any("outperforms" in t for t in result["takeaways"])


def test_my_new_tool_bad_input_from_model() -> None:
    tool = TOOL_FUNCTIONS["summarize_paper"]
    result = tool(paper_text="")
    assert "error" in result
    assert result["error"] == "ValueError"


def test_my_new_tool_failure_returns_error_dict() -> None:
    tool = TOOL_FUNCTIONS["summarize_paper"]
    result = tool(paper_text=None)
    assert "error" in result
    assert isinstance(result["message"], str)
