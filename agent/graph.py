"""
Agent Core — LangGraph implementation
======================================
Flow:
  think → tool → final answer
"""

import os
import json
from typing import TypedDict, Literal
from datetime import datetime

from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

from tools import (
    web_search, format_results_for_llm,
    calculator, format_result_for_llm,
    summarise, format_summary_for_llm,
)


class Step(TypedDict):
    kind: Literal["think", "tool_call", "tool_result", "answer"]
    content: str
    tool: str | None
    ts: str


class AgentState(TypedDict):
    messages: list
    steps: list[Step]
    tool_calls: int
    tools_used: list[str]
    final: str | None


TOOLS_SPEC = [
    {
        "name": "web_search",
        "description": (
            "Search the internet for current, real-time information. "
            "Use this for news, events, prices, exchange rates, weather, or anything recent."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A clear, specific search query."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculator",
        "description": (
            "Evaluate mathematical expressions accurately. "
            "Use this for arithmetic, percentages, conversions, or calculations."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A math expression, for example: 85000 * 0.18"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "summarise",
        "description": (
            "Summarise long text into clear bullet points. "
            "Use this after web_search when results are long."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The long text to summarise."
                },
                "max_points": {
                    "type": "string",
                    "description": "Number of bullet points to produce, for example: 3 or 5."
                }
            },
            "required": ["text"]
        }
    }
]


SYSTEM_PROMPT = """
You are AgentAI — a helpful AI assistant with access to tools.

Available tools:
- web_search: search the internet for current information.
- calculator: evaluate mathematical expressions.
- summarise: condense long text into bullet points.

Rules:
1. Use calculator for any math question.
2. Use web_search for latest news, current events, prices, exchange rates, or recent facts.
3. Use summarise only when long text needs condensing.
4. Never show internal tool calls to the user.
5. Never answer with text like [Calling tool: calculator].
6. After using tools, always convert the result into a clean, readable final answer.
7. The final answer must be plain English, not JSON, not raw tool output.
8. Be clear, concise, and helpful.
"""


def _now() -> str:
    return datetime.now().strftime("%H:%M:%S")


def _add_step(
    state: AgentState,
    kind: Literal["think", "tool_call", "tool_result", "answer"],
    content: str,
    tool: str | None = None
) -> None:
    state["steps"].append({
        "kind": kind,
        "content": content,
        "tool": tool,
        "ts": _now()
    })


def think_node(state: AgentState) -> AgentState:
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-8b-instant",
        temperature=0.2,
    )

    lc_messages = [SystemMessage(content=SYSTEM_PROMPT)]

    for m in state["messages"]:
        role = m.get("role")

        if role == "user":
            lc_messages.append(HumanMessage(content=m["content"]))

        elif role == "assistant":
            content = m.get("content") or ""
            lc_messages.append(AIMessage(content=content))

        elif role == "tool":
            lc_messages.append(
                ToolMessage(
                    content=m.get("content", ""),
                    tool_call_id=m.get("tool_call_id", "0")
                )
            )

    response = llm.bind_tools(
        TOOLS_SPEC,
        tool_choice="auto"
    ).invoke(lc_messages)

    if getattr(response, "tool_calls", None):
        tool_call = response.tool_calls[0]
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        tool_id = tool_call.get("id", "0")

        _add_step(
            state,
            "think",
            f"I need to use the {tool_name} tool.",
            tool=tool_name
        )

        state["messages"].append({
            "role": "assistant",
            "content": "",
            "tool_call": {
                "name": tool_name,
                "args": tool_args,
                "id": tool_id
            }
        })

        return state

    answer = response.content

    if isinstance(answer, list):
        answer = " ".join(str(item) for item in answer)

    if not isinstance(answer, str):
        answer = str(answer)

    if answer.strip().startswith("[Calling tool:"):
        answer = "I processed your request, but the model returned an internal tool message. Please try again."

    _add_step(state, "answer", answer)
    state["messages"].append({"role": "assistant", "content": answer})
    state["final"] = answer

    return state


def tool_node(state: AgentState) -> AgentState:
    last_msg = state["messages"][-1]
    tool_info = last_msg.get("tool_call")

    if not tool_info:
        return state

    tool_name = tool_info["name"]
    tool_args = tool_info.get("args", {})
    call_id = tool_info.get("id", "0")

    _add_step(
        state,
        "tool_call",
        f"Running {tool_name}",
        tool=tool_name
    )

    state["tool_calls"] += 1

    if tool_name not in state["tools_used"]:
        state["tools_used"].append(tool_name)

    try:
        if tool_name == "web_search":
            raw = web_search(tool_args.get("query", ""))
            result = format_results_for_llm(raw)

        elif tool_name == "calculator":
            raw = calculator(tool_args.get("expression", ""))
            result = format_result_for_llm(raw)

        elif tool_name == "summarise":
            max_points = tool_args.get("max_points", 3)

            try:
                max_points = int(max_points)
            except Exception:
                max_points = 3

            raw = summarise(
                tool_args.get("text", ""),
                max_points=max_points
            )
            result = format_summary_for_llm(raw)

        else:
            result = f"Unknown tool: {tool_name}"

    except Exception as e:
        result = f"Tool error in {tool_name}: {str(e)}"

    _add_step(state, "tool_result", result, tool=tool_name)

    state["messages"].append({
        "role": "tool",
        "content": result,
        "tool_call_id": call_id
    })

    return state


def final_node(state: AgentState) -> AgentState:
    """
    After a tool runs, force the LLM to write a clean final answer.
    This prevents infinite tool-calling loops.
    """
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-8b-instant",
        temperature=0.2,
    )

    user_question = state["messages"][0]["content"]

    last_tool_result = ""
    for m in reversed(state["messages"]):
        if m.get("role") == "tool":
            last_tool_result = m.get("content", "")
            break

    prompt = f"""
User question:
{user_question}

Tool result:
{last_tool_result}

Now write the final answer for the user.

Rules:
- Do not mention internal tool calls.
- Do not return JSON.
- Do not say "tool result".
- Use plain English.
- If this is a calculation, show the final number clearly.
- If this is a search/news/current information answer, summarize the result clearly.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    answer = response.content

    if isinstance(answer, list):
        answer = " ".join(str(item) for item in answer)

    if not isinstance(answer, str):
        answer = str(answer)

    state["final"] = answer
    state["messages"].append({"role": "assistant", "content": answer})
    _add_step(state, "answer", answer)

    return state


def route(state: AgentState) -> Literal["tool", "end"]:
    if state.get("final"):
        return "end"

    last = state["messages"][-1]

    if last.get("tool_call"):
        return "tool"

    return "end"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("think", think_node)
    graph.add_node("tool", tool_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("think")

    graph.add_conditional_edges(
        "think",
        route,
        {
            "tool": "tool",
            "end": END
        }
    )

    graph.add_edge("tool", "final")
    graph.add_edge("final", END)

    return graph.compile()


def run_agent(user_question: str) -> AgentState:
    graph = build_graph()

    initial_state: AgentState = {
        "messages": [
            {
                "role": "user",
                "content": user_question
            }
        ],
        "steps": [],
        "tool_calls": 0,
        "tools_used": [],
        "final": None,
    }

    result = graph.invoke(
        initial_state,
        {
            "recursion_limit": 20
        }
    )

    return result