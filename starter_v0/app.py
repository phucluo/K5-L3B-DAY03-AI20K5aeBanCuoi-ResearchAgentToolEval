"""Streamlit UI for Research Agent — 5aeBanCuoi.

Theme: Xanh tím than (Deep Navy & Indigo Glassmorphism).
Features:
- Multi-turn conversational research chat with live structured tool calling visualizer.
- Preset query shortcuts for quick showdown demo.
- Live tool execution inspection (expandable arguments and outputs).
- Automatic transcript logging to starter_v0/transcripts/.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"

from chat import run_model_tool_loop, write_transcript, trim_history
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import build_artifact_version, artifact_version_dict

load_lab_env(ROOT)

st.set_page_config(
    page_title="Research Agent — 5aeBanCuoi",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling: Xanh tím than (Deep Navy & Indigo)
st.markdown("""
<style>
    /* Global background */
    .stApp {
        background: linear-gradient(135deg, #070913 0%, #0d1224 50%, #151838 100%);
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Header banner */
    .navy-header {
        background: linear-gradient(90deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.6);
    }
    .navy-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .navy-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 6px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #090d1a !important;
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    /* Tool card badge */
    .tool-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.18);
        border: 1px solid #6366f1;
        color: #c7d2fe;
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 0.8rem;
        font-family: monospace;
        margin: 2px;
    }
    
    /* Chat message bubble styling */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 12px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #3730a3 0%, #4f46e5 100%);
        color: white;
        border: 1px solid #6366f1;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4338ca 0%, #6366f1 100%);
        border-color: #818cf8;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="navy-header">
    <div class="navy-title">🔬 AI Research Agent — Nhóm 5aeBanCuoi</div>
    <div class="navy-subtitle">Trợ lý nghiên cứu chuyên sâu: Tra cứu tin tức, trích xuất arXiv, tổng hợp digest và kiểm soát ranh giới gửi tin an toàn.</div>
</div>
""", unsafe_allow_html=True)

# Sidebar setup
with st.sidebar:
    st.markdown("### ⚙️ Cấu hình Agent")
    provider_name = st.selectbox("Provider", ["groq", "openrouter", "openai", "gemini"], index=0)
    model_name = st.text_input("Model ID", value="openai/gpt-oss-120b" if provider_name == "groq" else "")
    model_override = model_name.strip() if model_name.strip() else None

    st.markdown("---")
    st.markdown("### 🛠️ Bộ Công cụ tích hợp (CP3)")
    tool_names = [
        "clarify", "timeline", "social_search", "lookup", "fetch",
        "format", "send", "policy", "papers", "paper_text", "summarize_paper (Mới)"
    ]
    st.markdown("".join([f"<span class='tool-badge'>{t}</span>" for t in tool_names]), unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚡ Câu hỏi mẫu thử nhanh (A3)")
    sample_queries = [
        ("1. Tin tức Sam Altman", "Tweet mới nhất của Sam Altman là gì?"),
        ("2. Tin AI hôm nay", "Tin tức AI hôm nay có gì nổi bật?"),
        ("3. Đọc link bài viết", "Tóm tắt bài này giúp mình: https://openai.com/research/"),
        ("4. Tóm tắt Paper (CP3)", "Tóm tắt các phát hiện từ đoạn văn bản nghiên cứu này: We present DeepSeek-R1, an open-source reasoning model that achieves performance comparable to OpenAI-o1."),
        ("5. Gửi Telegram (Guardrail)", "Đăng bản tin này lên Telegram giúp mình"),
    ]
    
    preset_query = None
    for label, query_text in sample_queries:
        if st.button(label, use_container_width=True):
            preset_query = query_text

    st.markdown("---")
    if st.button("🗑️ Xóa lịch sử trò chuyện", use_container_width=True):
        st.session_state.messages = []
        st.session_state.raw_history = []
        st.session_state.transcript = None
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "raw_history" not in st.session_state:
    st.session_state.raw_history = []
if "transcript_path" not in st.session_state:
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    st.session_state.transcript_path = TRANSCRIPTS_DIR / f"ui_{ts}.transcript.json"

# Load artifacts
system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
tools_path = ARTIFACTS_DIR / "tools.yaml"
system_prompt = system_prompt_path.read_text(encoding="utf-8")
tool_declarations = load_tool_declarations(tools_path)
openai_tools = to_openai_tools(tool_declarations)

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "tool_events" in msg and msg["tool_events"]:
            with st.expander(f"🔍 Chi tiết {len(msg['tool_events'])} lượt gọi Tool", expanded=False):
                for ev in msg["tool_events"]:
                    st.code(f"Tool: {ev.get('tool')}\nArgs: {json.dumps(ev.get('args'), ensure_ascii=False, indent=2)}\nResult: {json.dumps(ev.get('result'), ensure_ascii=False, indent=2)}", language="json")

# Handle input
user_input = st.chat_input("Nhập câu hỏi hoặc yêu cầu nghiên cứu...") or preset_query

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare model loop
    provider = make_provider(provider_name)
    working_messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.raw_history, history_window=5),
        {"role": "user", "content": user_input},
    ]

    with st.chat_message("assistant"):
        with st.spinner("Agent đang phân tích và gọi công cụ..."):
            try:
                loop_result = run_model_tool_loop(
                    provider=provider,
                    messages=working_messages,
                    tools=openai_tools,
                    model=model_override,
                    max_tool_rounds=4,
                )
                assistant_text = loop_result.get("assistant_text") or "Đã hoàn thành."
                tool_events = loop_result.get("tool_events", [])

                # Render response
                st.markdown(assistant_text)
                if tool_events:
                    with st.expander(f"🔍 Chi tiết {len(tool_events)} lượt gọi Tool", expanded=True):
                        for ev in tool_events:
                            st.write(f"**🔧 {ev.get('tool')}**")
                            st.json(ev.get("args") or {})
                            st.caption("Kết quả trả về:")
                            st.json(ev.get("result") or {})

                # Update state
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_text,
                    "tool_events": tool_events,
                })
                st.session_state.raw_history.append({"role": "user", "content": user_input})
                st.session_state.raw_history.append({"role": "assistant", "content": assistant_text})

                # Write to transcript
                artifact_ver = build_artifact_version("v3", system_prompt_path, tools_path)
                transcript_data = {
                    "transcript_id": st.session_state.transcript_path.stem,
                    **artifact_version_dict(artifact_ver),
                    "provider": provider_name,
                    "model": model_override,
                    "created_at": datetime.now().isoformat(),
                    "turns": [
                        {
                            "turn_index": idx + 1,
                            "user": st.session_state.raw_history[idx * 2]["content"],
                            "assistant_text": st.session_state.raw_history[idx * 2 + 1]["content"],
                        }
                        for idx in range(len(st.session_state.raw_history) // 2)
                    ],
                }
                write_transcript(st.session_state.transcript_path, transcript_data)

            except Exception as exc:
                err_msg = f"⚠️ Lỗi hệ thống: {type(exc).__name__} — {str(exc)}"
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})

