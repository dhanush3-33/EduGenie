"""Learning-path recommendation module powered by Google Gemini."""

import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

_MODEL_NAME = "gemini-3.6-flash"


def _get_client() -> genai.Client:
    """Create a Gemini client from the environment API key."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to your .env file."
        )
    return genai.Client(api_key=api_key)


def get_learning_recommendations(topic: str) -> str:
    """Generate a structured beginner-to-advanced learning plan.

    Args:
        topic: The subject the user wants to learn (non-empty).

    Returns:
        A markdown-formatted learning path with stages and resources
        (videos, articles, books) for each stage.

    Raises:
        ValueError: If the topic is empty.
        RuntimeError: If the API key is missing or the API call fails.
    """
    cleaned = (topic or "").strip()
    if not cleaned:
        raise ValueError("Topic must not be empty.")

    try:
        client = _get_client()
        prompt = (
            "You are EduGenie, a curriculum designer. "
            "Create a structured learning path for the topic below, "
            "ordered from beginner to advanced.\n\n"
            "Include these sections:\n"
            "1. Beginner stage — key concepts + 1-2 resources\n"
            "2. Intermediate stage — key concepts + 1-2 resources\n"
            "3. Advanced stage — key concepts + 1-2 resources\n"
            "4. Suggested practice projects\n\n"
            "For resources, name specific videos, articles, or books "
            "(with authors/platforms where known). "
            "Keep it concise and use markdown headings and bullets.\n\n"
            f"Topic: {cleaned}"
        )
        response = client.models.generate_content(
            model=_MODEL_NAME,
            contents=prompt,
        )
        plan = (response.text or "").strip()
        if not plan:
            raise RuntimeError("Gemini returned an empty response.")
        return plan
    except (ValueError, RuntimeError):
        raise
    except Exception as exc:
        raise RuntimeError(
            f"Gemini learning-path request failed: {exc}"
        ) from exc
