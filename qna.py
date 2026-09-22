"""General question-answering module powered by Google Gemini."""

import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

_MODEL_NAME = "gemini-2.0-flash"


def _get_client() -> genai.Client:
    """Create a Gemini client from the environment API key."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to your .env file."
        )
    return genai.Client(api_key=api_key)


def answer_question(question: str) -> str:
    """Answer a general knowledge question using Gemini.

    Args:
        question: The user's question (non-empty string).

    Returns:
        The model's plain-text answer.

    Raises:
        ValueError: If the question is empty.
        RuntimeError: If the API key is missing or the API call fails.
    """
    cleaned = (question or "").strip()
    if not cleaned:
        raise ValueError("Question must not be empty.")

    try:
        client = _get_client()
        prompt = (
            "You are EduGenie, a helpful learning assistant. "
            "Answer the following question clearly and accurately.\n\n"
            f"Question: {cleaned}"
        )
        response = client.models.generate_content(
            model=_MODEL_NAME,
            contents=prompt,
        )
        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text
    except (ValueError, RuntimeError):
        raise
    except Exception as exc:
        raise RuntimeError(f"Gemini Q&A request failed: {exc}") from exc
