# Requirement Analysis Phase

> What EduGenie must do, who it serves, and the constraints it operates under.

## Target Users

- **Students** — the primary audience, studying coursework across subjects.
- They need quick answers, simpler explanations, self-testing, summaries, and study plans from one page with no login.

## Functional Requirements

- `POST /qa` accepts `{"question"}` → returns `{"question", "answer"}` via Gemini (`gemini-3.6-flash`).
- `POST /explain` accepts `{"concept"}` → returns `{"concept", "explanation"}` via the local LaMini model.
- `POST /quiz` accepts `{"passage"}` (min 30 chars) → returns exactly 3 questions, 4 options each, `answer` matching one option.
- `POST /summarize` accepts `{"text"}` → returns `{"summary"}` in 3–6 sentences or a short bulleted list.
- `POST /learn/recommendations` accepts `{"topic"}` → returns a staged beginner → advanced plan plus practice projects.
- `GET /` serves the single-page UI; `GET /health` returns `{"status": "ok"}`.

## Non-Functional Requirements

- **Gemini API key** — `GEMINI_API_KEY` in `05_Project_Development/.env` required for Q&A, Quiz, Summary, Learning Path (missing key → 502).
- **Offline Explain** — works offline/CPU-only after the first ~3 GB model download; pipeline cached with `lru_cache`.
- **Validated quiz output** — fence-stripped, `json.loads`-parsed, schema-validated, retried once before a clear error.
- **Input/error contract** — blank input rejected (422 via Pydantic, 400 from module logic); upstream failures → 502, never 500 on bad input.
- **Single-origin UI** — frontend served by the same FastAPI app; vanilla JS `fetch()`, no build step.
