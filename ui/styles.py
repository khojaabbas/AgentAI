"""
UI Styles
Clean light theme for the AgentAI Streamlit app.
Includes ChatGPT-style chat input, readable cards, and sidebar toggle support.
"""

STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer {
    visibility: hidden;
}

header {
    visibility: visible !important;
    background: transparent !important;
}

.stApp {
    background: #f7f7f3 !important;
    color: #111111 !important;
}

.block-container {
    padding: 1.2rem 1.5rem 6rem !important;
    max-width: 100% !important;
    background: #f7f7f3 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #f4f3ee !important;
    border-right: 1px solid #d8d6cc !important;
}

[data-testid="stSidebar"] * {
    color: #111111 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: .5px !important;
    text-transform: uppercase !important;
    margin-bottom: 10px !important;
}

[data-testid="stSidebar"] .stTextInput input {
    background: #ffffff !important;
    border: 1px solid #cfcfc7 !important;
    border-radius: 8px !important;
}

/* Top bar */
.top-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-bottom: 14px;
    margin-bottom: 16px;
    border-bottom: 1px solid #dedbd0;
}

.app-logo {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: #eee9ff;
    border: 1px solid #c8bfff;
    display: flex;
    align-items: center;
    justify-content: center;
}

.logo-ring {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    border: 2px solid #6c63ff;
}

.app-title {
    font-size: 17px;
    font-weight: 600;
    color: #111111;
    margin: 0;
}

.app-sub {
    font-size: 12px;
    color: #555555;
    margin: 0;
}

/* Status badge */
.status-badge {
    margin-left: auto;
    padding: 5px 12px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 500;
}

.status-idle {
    background: #ffffff;
    border: 1px solid #d8d6cc;
    color: #555555;
}

.status-think {
    background: #eee9ff;
    border: 1px solid #c8bfff;
    color: #4b3f9f;
}

.status-done {
    background: #eaf7ef;
    border: 1px solid #b8e5c5;
    color: #16803a;
}

.status-err {
    background: #fff0f0;
    border: 1px solid #f3b8b8;
    color: #c62828;
}

/* Welcome */
.welcome-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    text-align: center;
}

.welcome-icon {
    width: 52px;
    height: 52px;
    border-radius: 15px;
    background: #eee9ff;
    border: 1px solid #c8bfff;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
}

.welcome-title {
    font-size: 18px;
    font-weight: 600;
    color: #111111;
    margin-bottom: 8px;
}

.welcome-sub {
    font-size: 14px;
    color: #555555;
    line-height: 1.7;
    margin-bottom: 24px;
}

/* Suggestion chips */
.suggestion-chip {
    background: #ffffff;
    border: 1px solid #d8d6cc;
    border-radius: 10px;
    padding: 11px 16px;
    cursor: pointer;
    transition: border-color .15s, background .15s;
}

.suggestion-chip:hover {
    border-color: #8f7cff;
    background: #fbfaff;
}

.sugg-q {
    font-size: 13px;
    color: #111111;
}

.sugg-tag {
    font-size: 11px;
    color: #666666;
    margin-top: 3px;
}

/* Cards */
.answer-card,
.thinking-card {
    background: #ffffff;
    border: 1px solid #d8d6cc;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}

/* User bubble */
.user-bubble {
    background: #eee9ff;
    border: 1px solid #c8bfff;
    border-radius: 12px 12px 4px 12px;
    padding: 11px 16px;
    margin-bottom: 16px;
    max-width: 85%;
    margin-left: auto;
    color: #21125c;
    line-height: 1.6;
}

/* Answer card */
.answer-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e5e1d7;
}

.agent-dot {
    width: 26px;
    height: 26px;
    border-radius: 8px;
    background: #eee9ff;
    border: 1px solid #c8bfff;
    display: flex;
    align-items: center;
    justify-content: center;
}

.agent-name {
    font-size: 13px;
    font-weight: 600;
    color: #111111;
}

.time-tag {
    margin-left: auto;
    font-size: 11px;
    color: #666666;
}

.answer-body {
    font-size: 14px;
    line-height: 1.8;
    color: #111111;
}

/* Thinking */
.thinking-header {
    font-size: 13px;
    color: #555555;
    margin-bottom: 12px;
}

.live-step {
    display: flex;
    gap: 10px;
    align-items: center;
    padding: 10px 12px;
    border-radius: 10px;
    font-size: 13px;
}

.ls-active {
    background: #eee9ff;
    color: #4b3f9f;
}

.ls-icon {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #ddd7ff;
    color: #4b3f9f;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 600;
}

/* Trace */
.trace-toggle {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: #ffffff;
    border: 1px solid #d8d6cc;
    border-radius: 8px;
    margin-bottom: 12px;
    font-size: 12px;
    color: #555555;
    cursor: pointer;
}

.trace-step {
    padding: 10px 14px 10px 38px;
    position: relative;
    margin-bottom: 4px;
    border-radius: 8px;
    font-size: 13px;
    line-height: 1.6;
}

.trace-step::before {
    content: attr(data-num);
    position: absolute;
    left: 10px;
    top: 10px;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: block;
    line-height: 20px;
    text-align: center;
    font-size: 10px;
    font-weight: 600;
}

.step-think {
    background: #f3f0ff;
    color: #3f348f;
}

.step-think::before {
    background: #ddd7ff;
    color: #4b3f9f;
}

.step-tool {
    background: #ecfdf3;
    color: #166534;
}

.step-tool::before {
    background: #bbf7d0;
    color: #166534;
}

.step-result {
    background: #fff7e6;
    color: #8a5a00;
}

.step-result::before {
    background: #ffe3a3;
    color: #8a5a00;
}

.step-answer {
    background: #ecfdf3;
    color: #166534;
}

.step-answer::before {
    background: #bbf7d0;
    color: #166534;
}

.step-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: .5px;
    text-transform: uppercase;
    margin-bottom: 3px;
}

/* Tool pills */
.tool-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 10px;
    border-radius: 8px;
    margin-bottom: 6px;
    border: 1px solid #d8d6cc;
    background: #ffffff;
}

.tool-pill-active {
    border-color: #8f7cff !important;
    background: #eee9ff !important;
}

.tool-pill-done {
    border-color: #b8e5c5 !important;
    background: #eaf7ef !important;
}

.tp-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.tp-name {
    font-size: 12px;
    font-weight: 600;
    color: #111111;
}

.tp-sub {
    font-size: 11px;
    color: #666666;
}

/* Stats */
.stat-row {
    display: flex;
    gap: 8px;
    margin-top: 12px;
}

.stat-card {
    flex: 1;
    background: #ffffff;
    border: 1px solid #d8d6cc;
    border-radius: 8px;
    padding: 10px;
}

.stat-label {
    font-size: 10px;
    color: #666666;
    text-transform: uppercase;
    letter-spacing: .4px;
}

.stat-val {
    font-size: 18px;
    font-weight: 600;
    color: #111111;
    margin-top: 2px;
}

/* Buttons */
.stButton > button {
    background: #eee9ff !important;
    border: 1px solid #c8bfff !important;
    border-radius: 10px !important;
    color: #21125c !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background: #dfd7ff !important;
    border-color: #8f7cff !important;
}

/* Text input */
.stTextInput input {
    background: #ffffff !important;
    border: 1px solid #cfcfc7 !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    color: #111111 !important;
}

/* ChatGPT-style Streamlit chat input */
[data-testid="stChatInput"] {
    background: transparent !important;
}

[data-testid="stChatInput"] > div {
    
    border: 1px solid #d8d6cc !important;
    border-radius: 18px !important;
    box-shadow: 0 6px 22px rgba(20, 20, 20, 0.05) !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    border: none !important;
    color: #111111 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    padding: 18px 56px 18px 18px !important;
    min-height: 64px !important;
    max-height: 180px !important;
    line-height: 1.5 !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] textarea:focus {
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #777777 !important;
}

[data-testid="stChatInput"] button {
    background: #c96b45 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: none !important;
    width: 38px !important;
    height: 38px !important;
    margin-right: 8px !important;
}

[data-testid="stChatInput"] button:hover {
    background: #b85e3d !important;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #d8d6cc !important;
}

</style>
"""