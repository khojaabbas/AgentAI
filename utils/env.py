import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_secret(key: str):
    """
    Reads key from:
    1. Streamlit secrets on deployed app
    2. .env / environment variables locally
    """
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    return os.getenv(key)


def keys_ready():
    missing = []

    groq_key = get_secret("GROQ_API_KEY")
    tavily_key = get_secret("TAVILY_API_KEY")

    if not groq_key:
        missing.append("GROQ_API_KEY")

    if not tavily_key:
        missing.append("TAVILY_API_KEY")

    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key

    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key

    return len(missing) == 0, missing


def set_keys(groq_key=None, tavily_key=None):
    """
    Optional fallback for local/manual sidebar input.
    """
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key

    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key

    return keys_ready()