# AgentAI — Multi-Tool AI Agent

A production-grade AI agent that can search the web, solve maths, and summarise information.
Built with LangGraph, Groq (free tier), and Streamlit.

## Features
- **Web search** — searches the internet via Tavily API for current info
- **Calculator** — evaluates any mathematical expression accurately  
- **Summariser** — condenses long text into clean bullet points
- **Live reasoning trace** — shows every step the agent takes
- **Follow-up questions** — maintains context across turns
- **Chat history** — access previous conversations from sidebar

## Project Structure
```
agentai/
├── app.py              ← Streamlit entry point (run this)
├── requirements.txt
├── .env.example        ← copy to .env and fill in your keys
│
├── agent/
│   └── graph.py        ← LangGraph agent: state, nodes, routing
│
├── tools/
│   ├── search.py       ← Tavily web search tool
│   ├── calculator.py   ← safe math evaluator
│   └── summariser.py   ← Groq-powered summariser
│
├── ui/
│   ├── styles.py       ← all CSS
│   └── components.py   ← reusable HTML component functions
│
└── utils/
    └── env.py          ← API key loading helpers
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get free API keys
- **Groq**: https://console.groq.com → Create API key (completely free)
- **Tavily**: https://tavily.com → Sign up → Get API key (1000 searches/month free)

### 3. Set up environment
```bash
cp .env.example .env
# Edit .env and paste your keys
```
Or enter them directly in the app sidebar — no .env file needed.

### 4. Run
```bash
streamlit run app.py
```
Opens at http://localhost:8501

## How it works (LangGraph loop)
```
User question
     ↓
  [think] ← LLM decides: answer or use a tool?
     ↓
  [tool]  ← tool runs (search / calculator / summarise)
     ↓
  [think] ← LLM sees result, decides what to do next
     ↓
  ...loops until LLM has enough to answer...
     ↓
  Final answer shown to user
```

## Tech stack
| Layer | Technology |
|-------|-----------|
| LLM   | Groq — llama-3.1-8b-instant (free) |
| Agent | LangGraph StateGraph |
| Search | Tavily API (free tier) |
| Math  | Python safe eval |
| UI    | Streamlit + custom CSS |

## Skills demonstrated (for CV)
- LangGraph agentic loops and state management  
- Tool calling / function calling with LLMs
- Multi-step reasoning and tool chaining
- API integration (Groq, Tavily)
- Production Streamlit app with custom design
- Clean Python project structure
