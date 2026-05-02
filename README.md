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

## Tech stack
LLM --> Groq — llama-3.1-8b-instant (free) ||
||Agent --> LangGraph StateGraph 
||Search --> Tavily API (free tier) 
||Math --> Python safe eval 
||UI --> Streamlit + custom CSS

