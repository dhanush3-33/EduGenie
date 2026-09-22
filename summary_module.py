"""Passage summarization module powered by Google Gemini."""

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


def summarize_text(text: str) -> str:
    """Summarize a long passage concisely using Gemini.

    Args:
        text: The passage to summarize (non-empty).

    Returns:
        A concise plain-text summary.

    Raises:
        ValueError: If the input is empty.
        RuntimeError: If the API key is missing or the API call fails.
    """
    cleaned = (text or "").strip()
    if not cleaned:
        raise ValueError("Text to summarize must not be empty.")

    try:
        client = _get_client()
        prompt = (
            "You are EduGenie, a study assistant. "
            "Summarize the following passage concisely. "
            "Capture the key points in 3-6 sentences or a short "
            "bulleted list if that is clearer.\n\n"
            f"Passage:\n{cleaned}"
        )
        response = client.models.generate_content(
            model=_MODEL_NAME,
            contents=prompt,
        )
        summary = (response.text or "").strip()
        if not summary:
            raise RuntimeError("Gemini returned an empty response.")
        return summary
    except (ValueError, RuntimeError):
        raise
    except Exception as exc:
        raise RuntimeError(f"Gemini summarize request failed: {exc}") from exc
