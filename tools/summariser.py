"""
Tool: Summariser
Takes long text and returns a clean, concise summary.
Uses Groq LLM internally — AI using AI as a tool.
"""

import os
from groq import Groq


def summarise(text: str, style: str = "bullets", max_points: int = 3) -> dict:
    """
    Summarise a long piece of text into clean bullet points.

    Args:
        text:       The text to summarise
        style:      'bullets' or 'paragraph'
        max_points: How many bullet points (if style='bullets')

    Returns:
        dict with 'summary' and optional 'error'
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"summary": None, "error": "GROQ_API_KEY not set"}

    if not text or not text.strip():
        return {"summary": None, "error": "No text provided to summarise"}

    # Truncate very long inputs to avoid token limits
    truncated = text[:4000] if len(text) > 4000 else text

    if style == "bullets":
        instruction = (
            f"Summarise the following text into exactly {max_points} clear, "
            f"concise bullet points. Each bullet should be one sentence. "
            f"Start each bullet with '• '. Return only the bullets, nothing else."
        )
    else:
        instruction = (
            "Summarise the following text into one clear, concise paragraph "
            "of 3-4 sentences. Return only the paragraph, nothing else."
        )

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user",   "content": truncated}
            ],
            max_tokens=512,
            temperature=0.3,
        )
        summary = response.choices[0].message.content.strip()
        return {"summary": summary, "error": None}

    except Exception as e:
        return {"summary": None, "error": str(e)}


def format_summary_for_llm(summarise_output: dict) -> str:
    """
    Convert summariser output to readable text for the LLM.
    """
    if summarise_output.get("error"):
        return f"Summarisation failed: {summarise_output['error']}"
    return summarise_output.get("summary", "No summary produced.")
