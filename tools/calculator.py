"""
Tool: Calculator
Safely evaluates mathematical expressions.
Uses a restricted eval so users cannot inject harmful code.
"""

import math
import re


# Only these names are allowed inside expressions
SAFE_NAMES = {
    "abs": abs, "round": round, "min": min, "max": max,
    "pow": pow, "sum": sum,
    "sqrt": math.sqrt, "ceil": math.ceil, "floor": math.floor,
    "log": math.log, "log10": math.log10,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "pi": math.pi, "e": math.e,
}


def calculator(expression: str) -> dict:
    """
    Evaluate a mathematical expression safely.

    Args:
        expression: A math expression string e.g. "85000 * 0.18" or "sqrt(144)"

    Returns:
        dict with 'result', 'expression', and optional 'error'
    """
    original = expression.strip()

    # Basic sanitisation — reject anything that looks like code injection
    forbidden = ["import", "exec", "eval", "open", "__", "os.", "sys."]
    for bad in forbidden:
        if bad in original:
            return {
                "expression": original,
                "result":     None,
                "error":      f"Expression contains forbidden keyword: '{bad}'"
            }

    # Replace common plain-English patterns
    clean = original
    clean = re.sub(r'\bx\b', '*', clean)      # "5 x 3" → "5 * 3"
    clean = clean.replace("^", "**")           # "2^8" → "2**8"
    clean = clean.replace(",", "")             # "1,000" → "1000"
    clean = re.sub(r'[a-zA-Z]+\s*%', lambda m: str(float(m.group()[:-1]) / 100), clean)

    try:
        result = eval(clean, {"__builtins__": {}}, SAFE_NAMES)  # noqa: S307
        # Round floats to avoid floating point noise
        if isinstance(result, float):
            result = round(result, 6)
        return {
            "expression": original,
            "evaluated":  clean,
            "result":     result,
            "error":      None
        }
    except ZeroDivisionError:
        return {"expression": original, "result": None, "error": "Division by zero"}
    except Exception as e:
        return {"expression": original, "result": None, "error": str(e)}


def format_result_for_llm(calc_output: dict) -> str:
    """
    Convert calculator output to readable text for the LLM.
    """
    if calc_output.get("error"):
        return f"Calculation error: {calc_output['error']}"

    expr   = calc_output["expression"]
    result = calc_output["result"]
    return f"Calculation: {expr} = {result}"
