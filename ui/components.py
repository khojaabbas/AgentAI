"""
UI Components
Reusable HTML snippets for the AgentAI Streamlit app.
"""

import html
import re


def clean_answer_text(text: str) -> str:
    """
    Prevent raw internal tool-call messages from showing in the UI.
    """
    if not text:
        return ""

    cleaned = str(text).strip()

    cleaned = re.sub(
        r"\[Calling tool:\s*.*?\]\s*\{.*?\}",
        "",
        cleaned,
        flags=re.DOTALL
    )

    cleaned = re.sub(
        r"\[Calling tool:\s*.*?\]",
        "",
        cleaned,
        flags=re.DOTALL
    )

    return cleaned.strip()


def top_bar(status: str = "idle", elapsed: float | None = None) -> str:
    if status == "thinking":
        badge = '<div class="status-badge status-think"><div class="pulse pulse-purple"></div>Agent thinking...</div>'
    elif status == "done":
        t = f" · {elapsed:.1f}s" if elapsed else ""
        badge = f'<div class="status-badge status-done"><div class="pulse pulse-green"></div>Done{t}</div>'
    elif status == "error":
        badge = '<div class="status-badge status-err">Error occurred</div>'
    else:
        badge = '<div class="status-badge status-idle"><div class="pulse pulse-gray"></div>Ready</div>'

    return f"""
    <div class="top-bar">
      <div class="app-logo"><div class="logo-ring"></div></div>
      <div>
        <p class="app-title">AgentAI</p>
        <p class="app-sub">LangGraph · Groq · Tavily</p>
      </div>
      {badge}
    </div>
    """


def welcome_screen() -> str:
    return """
    <div class="welcome-wrap">
      <div class="welcome-icon">
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
          <circle cx="11" cy="11" r="9" stroke="#6c63ff" stroke-width="1.5"/>
          <circle cx="11" cy="11" r="4" fill="#6c63ff" opacity=".3"/>
          <circle cx="11" cy="11" r="1.5" fill="#6c63ff"/>
        </svg>
      </div>
      <p class="welcome-title">Ask me anything</p>
      <p class="welcome-sub">
        I can search the internet, solve maths,<br>
        and summarise information for you.
      </p>
    </div>
    """


def suggestion_chip(question: str, tag: str) -> str:
    q = html.escape(question)
    t = html.escape(tag)
    return f"""
    <div class="suggestion-chip">
      <div class="sugg-q">{q}</div>
      <div class="sugg-tag">{t}</div>
    </div>
    """


def user_bubble(question: str) -> str:
    q = html.escape(question)
    return f'<div class="user-bubble">{q}</div>'


def thinking_card(steps: list) -> str:
    rows = ""

    for i, s in enumerate(steps, 1):
        status = s.get("status", "wait")
        content = html.escape(str(s.get("content", "")))
        css = f"ls-{status}"

        dots = (
            '<div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>'
            if status == "active"
            else ""
        )

        rows += f"""
        <div class="live-step {css}">
          <div class="ls-icon">{i}</div>
          <div>{content}{dots}</div>
        </div>
        """

    return f"""
    <div class="thinking-card">
      <div class="thinking-header">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <circle cx="7" cy="7" r="5.5" stroke="#5a5a7a" stroke-width="1"/>
          <path d="M7 4.5v3l1.5 1" stroke="#5a5a7a" stroke-width="1" stroke-linecap="round"/>
        </svg>
        Reasoning steps
      </div>
      {rows}
    </div>
    """


def answer_card(answer_text: str, elapsed: float | None = None) -> str:
    t_tag = f'<span class="time-tag">{elapsed:.1f}s</span>' if elapsed else ""

    cleaned = clean_answer_text(answer_text)

    if not cleaned:
        cleaned = "I processed your request, but the final answer was empty. Please try again."

    safe = html.escape(cleaned).replace("\n", "<br>")

    return f"""
    <div class="answer-card">
      <div class="answer-header">
        <div class="agent-dot">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <circle cx="6" cy="6" r="4.5" stroke="#6c63ff" stroke-width="1"/>
            <circle cx="6" cy="6" r="1.5" fill="#6c63ff"/>
          </svg>
        </div>
        <span class="agent-name">AgentAI</span>
        {t_tag}
      </div>
      <div class="answer-body">{safe}</div>
    </div>
    """


def trace_step(num: int, kind: str, content: str) -> str:
    kind_label = {
        "think": ("THOUGHT", "step-think"),
        "tool_call": ("TOOL CALL", "step-tool"),
        "tool_result": ("RESULT", "step-result"),
        "answer": ("ANSWER", "step-answer"),
    }

    label, css = kind_label.get(kind, ("STEP", "step-think"))
    safe = html.escape(str(content))

    return f"""
    <div class="trace-step {css}" data-num="{num}">
      <div class="step-label">{label}</div>
      {safe}
    </div>
    """


def tool_pill(name: str, color: str, subtitle: str, state: str = "idle") -> str:
    css = {
        "active": "tool-pill-active",
        "done": "tool-pill-done"
    }.get(state, "")

    return f"""
    <div class="tool-pill {css}">
      <div class="tp-dot" style="background:{html.escape(color)};"></div>
      <div>
        <div class="tp-name">{html.escape(name)}</div>
        <div class="tp-sub">{html.escape(subtitle)}</div>
      </div>
    </div>
    """


def stat_row(steps: int, tool_calls: int) -> str:
    return f"""
    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-label">Steps</div>
        <div class="stat-val">{steps}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Tool calls</div>
        <div class="stat-val">{tool_calls}</div>
      </div>
    </div>
    """