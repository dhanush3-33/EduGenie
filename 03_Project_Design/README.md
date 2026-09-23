# Project Design Phase

> High-level architecture of EduGenie as implemented in `05_Project_Development/`.

## Components

- **FastAPI backend** (`main.py`, `EduGenie 1.0.0`) — 5 POST endpoints plus `GET /` and `GET /health`.
- **Single-page frontend** (`templates/index.html` + `static/style.css`) — dropdown mapped by `TASK_CONFIG`, `fetch()`, loading/error states.
- **5 feature modules** — `qna.py`, `explanation_module.py`, `quiz_module.py`, `summary_module.py`, `learning_path.py`, one per capability.

## Gemini vs Local Model

- **Gemini API** (`google-genai` SDK, `gemini-3.6-flash`) powers Q&A, Quiz, Summary, and Learning Path via `client.models.generate_content`.
- **Local pipeline** powers Explain only: `transformers` text2text with `MBZUAI/LaMini-Flan-T5-783M` (`max_new_tokens=256`, `device=-1` CPU-only).
- The local pipeline loads once via `lru_cache`, so repeats are fast and offline.

## Request/Response Flow

- UI trims input → `POST` JSON (`question` / `concept` / `passage` / `text` / `topic`).
- Pydantic non-blank check → module function → Gemini or local model.
- JSON response (`answer` / `explanation` / `quiz` / `summary` / `learning_path`) renders below the form, HTML-escaped.

## Pydantic Request Models (`main.py`)

- `QuestionRequest { question }` → `POST /qa`
- `ExplainRequest { concept }` → `POST /explain`
- `QuizRequest { passage }` → `POST /quiz`
- `SummarizeRequest { text }` → `POST /summarize`
- `LearnRequest { topic }` → `POST /learn/recommendations`
- All fields share the `_not_blank` validator; endpoints map `ValueError` → 400, `RuntimeError` → 502.
