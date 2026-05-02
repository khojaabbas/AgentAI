"""
AgentAI — Main Streamlit App
=============================
Entry point. Run with: streamlit run app.py
"""

import time
import streamlit as st

from utils import keys_ready
from agent import run_agent
from ui import (
    STYLES, top_bar, welcome_screen, suggestion_chip,
    user_bubble, answer_card,
    trace_step, tool_pill, stat_row,
)


st.set_page_config(
    page_title="AgentAI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(STYLES, unsafe_allow_html=True)


def _init():
    defaults = {
        "question": "",
        "answer": None,
        "agent_steps": [],
        "tools_used": [],
        "tool_calls": 0,
        "elapsed": None,
        "status": "idle",
        "show_trace": False,
        "history": [],
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init()
ss = st.session_state


def submit_question(question: str):
    question = question.strip()

    if not question:
        return

    ok, missing = keys_ready()

    if not ok:
        st.error(
            f"App API keys are not configured. Missing: {', '.join(missing)}"
        )
        return

    ss.question = question
    ss.answer = None
    ss.agent_steps = []
    ss.tools_used = []
    ss.tool_calls = 0
    ss.elapsed = None
    ss.show_trace = False
    ss.status = "thinking"
    st.rerun()


with st.sidebar:
    st.markdown("### App Status")

    ok, missing = keys_ready()

    if ok:
        st.success("API keys configured", icon="✅")
    else:
        st.error(f"Missing secrets: {', '.join(missing)}")

    st.markdown("---")
    st.markdown("### Tools")

    used = ss.tools_used

    def _pill_state(name):
        if ss.status == "thinking" and ss.agent_steps:
            last = ss.agent_steps[-1]
            if last.get("tool") == name:
                return "active"

        if name in used:
            return "done"

        return "idle"

    def _pill_sub(name):
        count = sum(1 for s in ss.agent_steps if s.get("tool") == name)

        if _pill_state(name) == "active":
            return "running now..."

        if _pill_state(name) == "done":
            return f"{count} call{'s' if count != 1 else ''} made"

        return "standing by"

    st.markdown(
        tool_pill("Web search", "#6c63ff", _pill_sub("web_search"), _pill_state("web_search")),
        unsafe_allow_html=True
    )

    st.markdown(
        tool_pill("Calculator", "#1D9E75", _pill_sub("calculator"), _pill_state("calculator")),
        unsafe_allow_html=True
    )

    st.markdown(
        tool_pill("Summariser", "#BA7517", _pill_sub("summarise"), _pill_state("summarise")),
        unsafe_allow_html=True
    )

    if ss.agent_steps:
        st.markdown("---")
        st.markdown("### Stats")
        st.markdown(
            stat_row(len(ss.agent_steps), ss.tool_calls),
            unsafe_allow_html=True
        )

    if ss.history:
        st.markdown("---")
        st.markdown("### History")

        for i, (q, _) in enumerate(reversed(ss.history[-6:])):
            if st.button(f"↩ {q[:42]}{'…' if len(q) > 42 else ''}", key=f"hist_{i}"):
                _, a = ss.history[-(i + 1)]
                ss.answer = a
                ss.question = q
                ss.status = "done"
                st.rerun()

    if ss.status == "done":
        st.markdown("---")

        if st.button("＋ New question"):
            ss.status = "idle"
            ss.question = ""
            ss.answer = None
            ss.agent_steps = []
            ss.tools_used = []
            ss.tool_calls = 0
            ss.elapsed = None
            ss.show_trace = False
            st.rerun()


st.markdown(top_bar(ss.status, ss.elapsed), unsafe_allow_html=True)


if ss.status == "idle":
    st.markdown(welcome_screen(), unsafe_allow_html=True)

    suggestions = [
        ("What is the latest AI news this week?", "uses: web search → summariser"),
        ("What is 18% GST on PKR 85,000? Show working.", "uses: calculator"),
        ("Search LangGraph and summarise how it works.", "uses: web search → summariser"),
        ("What is 1 USD to PKR today?", "uses: web search"),
    ]

    st.markdown("---")

    cols = st.columns(2)

    for i, (q, tag) in enumerate(suggestions):
        with cols[i % 2]:
            st.markdown(suggestion_chip(q, tag), unsafe_allow_html=True)

            if st.button("Ask this ↗", key=f"sugg_{i}"):
                submit_question(q)

    st.markdown("---")


elif ss.status == "thinking":
    st.markdown(user_bubble(ss.question), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="thinking-card">
            <div class="thinking-header">◷ Reasoning steps</div>
            <div class="live-step ls-active">
                <div class="ls-icon">1</div>
                <div>Agent working...</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        t0 = time.time()

        result = run_agent(ss.question)

        ss.elapsed = round(time.time() - t0, 1)
        ss.agent_steps = result.get("steps", [])
        ss.tools_used = result.get("tools_used", [])
        ss.tool_calls = result.get("tool_calls", 0)
        ss.answer = result.get("final") or "I was unable to produce a final answer."

        ss.history.append((ss.question, ss.answer))

        ss.status = "done"
        st.rerun()

    except Exception as e:
        ss.status = "error"
        ss.answer = f"Something went wrong: {str(e)}"
        st.rerun()


elif ss.status in ("done", "error"):
    st.markdown(user_bubble(ss.question), unsafe_allow_html=True)

    toggle_label = "▼ Hide reasoning trace" if ss.show_trace else "▶ View reasoning trace"
    trace_cols = st.columns([6, 1])

    with trace_cols[0]:
        st.markdown(
            f"""
            <div class="trace-toggle">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M2 4h10M2 7h10M2 10h6"
                    stroke="#5a5a7a"
                    stroke-width="1"
                    stroke-linecap="round"/>
                </svg>
                {toggle_label}
            </div>
            """,
            unsafe_allow_html=True
        )

    with trace_cols[1]:
        if st.button("toggle", key="trace_toggle", help="Show/hide trace"):
            ss.show_trace = not ss.show_trace
            st.rerun()

    if ss.show_trace and ss.agent_steps:
        for i, step in enumerate(ss.agent_steps, 1):
            st.markdown(
                trace_step(i, step["kind"], step["content"]),
                unsafe_allow_html=True
            )

        st.markdown("---")

    st.markdown(
        answer_card(ss.answer, ss.elapsed),
        unsafe_allow_html=True
    )

    st.markdown("---")


if ss.status in ("idle", "done", "error"):
    placeholder = (
        "Ask anything — I'll figure out which tool to use..."
        if ss.status == "idle"
        else "Ask a follow-up question..."
    )

    chat_query = st.chat_input(
        placeholder,
        key="global_chat_input"
    )

    if chat_query and chat_query.strip():
        submit_question(chat_query)