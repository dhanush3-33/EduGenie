# Project Documentation Phase

> Index to EduGenie docs and code. Implementation lives in `05_Project_Development/`; the root `README.md` is the full guide.

## Setup

- `cd 05_Project_Development` → `pip install -r requirements.txt`.
- `copy .env.example .env` (Windows) or `cp .env.example .env` (macOS/Linux), then set `GEMINI_API_KEY` (https://aistudio.google.com/app/apikey).
- Run `uvicorn main:app --reload`; UI at http://127.0.0.1:8000, health at `/health`, docs at `/docs`.
- First Explain call downloads `MBZUAI/LaMini-Flan-T5-783M` (~3 GB); afterwards it runs CPU-only offline.

## API Reference

- `POST /qa` — req `{"question"}` → res `{"question", "answer"}` (Gemini `gemini-3.6-flash`).
- `POST /explain` — req `{"concept"}` → res `{"concept", "explanation"}` (local LaMini model).
- `POST /quiz` — req `{"passage"}` (≥30 chars) → res `{"passage", "quiz"}` (3 MCQs, strict JSON).
- `POST /summarize` — req `{"text"}` → res `{"summary"}` (3–6 sentences or short list).
- `POST /learn/recommendations` — req `{"topic"}` → res `{"topic", "learning_path"}` (staged plan + projects).
- Errors: blank input → 422/400; model/upstream failure or missing key → 502.

## Where to Find the Code

- `05_Project_Development/main.py` — routes, Pydantic models, error mapping.
- `qna.py`, `explanation_module.py`, `quiz_module.py`, `summary_module.py`, `learning_path.py` — one module per feature.
- `templates/index.html`, `static/style.css` — single-page UI.
- `requirements.txt`, `.env.example` — dependencies and key placeholder.
