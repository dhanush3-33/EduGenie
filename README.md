# EduGenie — AI-Powered Learning Assistant

EduGenie is an AI-powered learning assistant with a FastAPI backend and a
single-page HTML/CSS/JS frontend. Four modules call Google Gemini
(`gemini-2.0-flash` via the official `google-genai` SDK); the Explain module
runs fully local on the LaMini-Flan-T5-783M model (CPU-only, offline after the
first download).

## Features

- **Q&A** (`qna.py` → `answer_question`) — answers general questions clearly
  and accurately via Gemini.
- **Explain** (`explanation_module.py` → `explain_concept`) — simplifies
  complex concepts with short sentences and an everyday example, using a local
  `MBZUAI/LaMini-Flan-T5-783M` text2text pipeline cached with `lru_cache`
  (loaded once, not per request).
- **Quiz** (`quiz_module.py` → `generate_quiz`) — generates exactly 3 MCQs
  with 4 options each from a passage (minimum 30 chars), returned as validated
  strict JSON where `answer` exactly matches one option string.
- **Summary** (`summary_module.py` → `summarize_text`) — summarizes long
  passages concisely in 3–6 sentences (or a short bulleted list) via Gemini.
- **Learning Path** (`learning_path.py` → `get_learning_recommendations`) —
  generates a structured beginner → intermediate → advanced plan with
  videos/articles/books per stage plus practice projects, via Gemini.

## Setup

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then edit `.env` and set your key (get one at
https://aistudio.google.com/app/apikey):

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Never commit `.env` — it is git-ignored. Only `.env.example` (placeholder) is
tracked.

Note: the Explain module downloads `MBZUAI/LaMini-Flan-T5-783M` (~3 GB) from
Hugging Face on first use, then runs on CPU offline.

## Run

```bash
uvicorn main:app --reload
```

- UI: http://127.0.0.1:8000 (task dropdown + textarea, results render below)
- Health: http://127.0.0.1:8000/health
- API docs: http://127.0.0.1:8000/docs

## Tech stack

- FastAPI (0.116.1) + Uvicorn (0.35.0) — REST API, Jinja2 templates, static files
- `google-genai` SDK (1.32.0), model `gemini-2.0-flash` — Q&A, Quiz, Summary,
  Learning Path
- `MBZUAI/LaMini-Flan-T5-783M` via `transformers` (4.55.0) + `torch` (2.8.0) +
  `sentencepiece` — local Explain module
- Jinja2 + vanilla JS `fetch()` — single-page frontend
- `python-dotenv` — `GEMINI_API_KEY` loaded from environment/`.env`, never
  hardcoded; Pydantic models validate every request; CORS open for local use

## Error handling

- Empty / whitespace-only input → rejected by Pydantic validators
  (HTTP 422), or HTTP 400 for failures raised inside module logic
  (e.g. quiz passage shorter than 30 chars).
- Missing `GEMINI_API_KEY` or failed model call → HTTP 502 with a clear
  `detail` message (missing key, empty model response, API failure).
- The app never returns 500 on bad user input; every endpoint wraps its module
  call in try/except and maps `ValueError` → 400, `RuntimeError` → 502.
- Quiz robustness: `quiz_module.py` strips ` ```json ` code fences before
  `json.loads()`, validates the 3-questions × 4-options schema (answer must
  match one option exactly), retries the Gemini call once on parse failure,
  then returns a clear error instead of crashing the endpoint.

## Endpoints

| Method | Path                    | Purpose                                              |
| ------ | ----------------------- | ---------------------------------------------------- |
| POST   | `/qa`                   | Answer a question (`{"question"}` → `answer`)        |
| POST   | `/explain`              | Simplify a concept (`{"concept"}` → `explanation`)   |
| POST   | `/quiz`                 | 3 MCQs from a passage (`{"passage"}` → `quiz` list)  |
| POST   | `/summarize`            | Summarize text (`{"text"}` → `summary`)              |
| POST   | `/learn/recommendations`| Learning plan (`{"topic"}` → `learning_path`)        |
| GET    | `/`                     | Serves `templates/index.html` via Jinja2Templates    |
| GET    | `/health`               | Health check (`{"status": "ok"}`)                    |

Example (Q&A):

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"What is photosynthesis?\"}"
```

## Project structure

```text
main.py               FastAPI app: 5 POST endpoints + UI + health + CORS
qna.py                answer_question() via Gemini
explanation_module.py explain_concept() via local LaMini-Flan-T5-783M
quiz_module.py        generate_quiz() via Gemini, fence-stripped + validated JSON
summary_module.py     summarize_text() via Gemini
learning_path.py      get_learning_recommendations() via Gemini
templates/index.html  single-page UI (task dropdown, textarea, live results)
static/style.css      clean responsive styling
requirements.txt      pinned dependencies
.env.example          GEMINI_API_KEY placeholder (tracked; real .env is not)
.gitignore            venvs, caches, .env, logs, OS + IDE files
```
