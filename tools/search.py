"""
Tool: Web Search
Uses Tavily API to search the internet for current information.
Returns clean, structured results ready for the LLM to read.
"""

import os
from tavily import TavilyClient


def web_search(query: str, max_results: int = 4) -> dict:
    """
    Search the web for current information.
    
    Args:
        query: The search query string
        max_results: How many results to return (default 4)
    
    Returns:
        dict with 'results' (list of dicts) and 'query' used
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {
            "error": "TAVILY_API_KEY not set",
            "results": [],
            "query": query
        }

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="basic"
        )

        results = []
        for item in response.get("results", []):
            results.append({
                "title":   item.get("title", ""),
                "url":     item.get("url", ""),
                "content": item.get("content", "")[:600],  # cap length
            })

        return {
            "query":   query,
            "results": results,
            "count":   len(results)
        }

    except Exception as e:
        return {
            "error":   str(e),
            "results": [],
            "query":   query
        }


def format_results_for_llm(search_output: dict) -> str:
    """
    Convert raw search output into readable text for the LLM.
    """
    if search_output.get("error"):
        return f"Search failed: {search_output['error']}"

    results = search_output.get("results", [])
    if not results:
        return "No results found."

    lines = [f"Search results for: '{search_output['query']}'\n"]
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']}")
        lines.append(f"    Source: {r['url']}")
        lines.append(f"    {r['content']}\n")

    return "\n".join(lines)
