"""Quiz generation module: 3 MCQs with 4 options each, strict JSON output."""

import json
import os
import re

from dotenv import load_dotenv
from google import genai

load_dotenv()

_MODEL_NAME = "gemini-3.6-flash"
_NUM_QUESTIONS = 3


def _get_client() -> genai.Client:
    """Create a Gemini client from the environment API key."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to your .env file."
        )
    return genai.Client(api_key=api_key)


def _build_prompt(passage: str) -> str:
    """Build a prompt that forces strict JSON quiz output."""
    return (
        "You are EduGenie, a quiz generator. "
        f"Create exactly {_NUM_QUESTIONS} multiple-choice questions "
        "from the passage below. Each question must have exactly 4 options "
        "and exactly one correct answer.\n\n"
        "Return ONLY a valid JSON array. No markdown, no code fences, "
        "no commentary. Use this exact schema:\n"
        '[{"question": "...", "options": ["A...", "B...", '
        '"C...", "D..."], "answer": "A..."}]\n'
        'The "answer" value must exactly match one of the 4 option strings.\n\n'
        f"Passage:\n{passage.strip()}"
    )


def _strip_code_fences(raw: str) -> str:
    """Remove ```json / ``` fences and surrounding whitespace."""
    text = (raw or "").strip()
    # Remove leading ```json or ``` and trailing ```
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```\s*$", "", text)
    return text.strip()


def _validate_quiz(data) -> list:
    """Validate parsed JSON matches the 3x4 MCQ schema."""
    if not isinstance(data, list):
        raise ValueError("Quiz JSON must be a list.")
    if len(data) != _NUM_QUESTIONS:
        raise ValueError(
            f"Quiz must contain exactly {_NUM_QUESTIONS} questions, "
            f"got {len(data)}."
        )
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Question {i + 1} must be an object.")
        for key in ("question", "options", "answer"):
            if key not in item:
                raise ValueError(f"Question {i + 1} is missing '{key}'.")
        if not isinstance(item["question"], str) or not item["question"].strip():
            raise ValueError(f"Question {i + 1} text must be non-empty.")
        options = item["options"]
        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(f"Question {i + 1} must have exactly 4 options.")
        if any(not isinstance(o, str) or not o.strip() for o in options):
            raise ValueError(f"Question {i + 1} has an empty option.")
        if item["answer"] not in options:
            raise ValueError(
                f"Question {i + 1} answer must exactly match one option."
            )
    return data


def _parse_quiz_json(raw: str) -> list:
    """Strip fences, json.loads, and validate. Raises ValueError on failure."""
    cleaned = _strip_code_fences(raw)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model did not return valid JSON: {exc}") from exc
    return _validate_quiz(data)


def generate_quiz(passage: str) -> list:
    """Generate 3 MCQs from a passage via Gemini.

    Strips markdown fences before parsing. Retries once on parse
    failure, then raises a clear error (never crashes the caller).

    Args:
        passage: Source text to quiz on (non-empty).

    Returns:
        List of 3 dicts with keys: question, options (4), answer.

    Raises:
        ValueError: If input is empty or a very short passage.
        RuntimeError: If the API key is missing, the API fails, or
            parsing fails after one retry.
    """
    cleaned = (passage or "").strip()
    if not cleaned:
        raise ValueError("Passage must not be empty.")
    if len(cleaned) < 30:
        raise ValueError("Passage is too short to generate a quiz (min 30 chars).")

    try:
        client = _get_client()
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Could not create Gemini client: {exc}") from exc

    prompt = _build_prompt(cleaned)
    last_error: Exception | None = None

    for _attempt in range(2):  # initial try + one retry
        try:
            response = client.models.generate_content(
                model=_MODEL_NAME,
                contents=prompt,
            )
            raw = (response.text or "").strip()
            if not raw:
                last_error = ValueError("Gemini returned an empty response.")
                continue
            return _parse_quiz_json(raw)
        except (ValueError, RuntimeError) as exc:
            last_error = exc
            continue
        except Exception as exc:
            last_error = RuntimeError(f"Gemini quiz request failed: {exc}")

    raise RuntimeError(
        f"Could not generate a valid quiz after retry: {last_error}"
    )
