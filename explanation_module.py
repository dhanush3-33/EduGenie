"""Local explanation module using a small Hugging Face model.

Uses MBZUAI/LaMini-Flan-T5-783M via a transformers text2text pipeline.
The pipeline is loaded once and cached so repeated requests are fast
and work offline/CPU-only after the first download.
"""

from functools import lru_cache

from transformers import pipeline

_MODEL_ID = "MBZUAI/LaMini-Flan-T5-783M"


@lru_cache(maxsize=1)
def _get_pipeline():
    """Load and cache the text2text generation pipeline (once per process)."""
    return pipeline(
        "text2text-generation",
        model=_MODEL_ID,
        max_new_tokens=256,
        device=-1,  # CPU-only for maximum compatibility
    )


def explain_concept(concept: str) -> str:
    """Explain a concept in simple, beginner-friendly terms.

    Args:
        concept: The concept or question to simplify.

    Returns:
        A plain-text simplified explanation.

    Raises:
        ValueError: If the input is empty.
        RuntimeError: If local generation fails.
    """
    cleaned = (concept or "").strip()
    if not cleaned:
        raise ValueError("Concept must not be empty.")

    prompt = (
        "Explain the following concept in simple terms that a beginner "
        "can understand. Use short sentences and an everyday example.\n\n"
        f"Concept: {cleaned}\nExplanation:"
    )
    try:
        generator = _get_pipeline()
        outputs = generator(prompt)
        if not outputs or "generated_text" not in outputs[0]:
            raise RuntimeError("Explanation model returned no output.")
        text = str(outputs[0]["generated_text"]).strip()
        if not text:
            raise RuntimeError("Explanation model returned an empty result.")
        return text
    except (ValueError, RuntimeError):
        raise
    except Exception as exc:
        raise RuntimeError(f"Local explanation failed: {exc}") from exc
