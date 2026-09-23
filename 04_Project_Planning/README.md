# Project Planning Phase

> How the 8 SDLC phases map to EduGenie milestones, and why the stack was chosen.

## Phase → Milestone Map

- **01 Brainstorming/Ideation** — problem framing and the 5-feature shortlist.
- **02 Requirement Analysis** — endpoint contract, API-key dependency, offline-Explain and quiz-validation constraints.
- **03 Project Design** — FastAPI + module-per-feature layout, Gemini-vs-local split, Pydantic models, UI mapping.
- **04 Project Planning** — this plan: stack choices and build sequencing.
- **05 Project Development** — implementation in `05_Project_Development/` (modules, `main.py`, UI, `requirements.txt`).
- **06 Project Testing** — endpoint checklist plus manual UI passes.
- **07 Project Documentation** — root README plus endpoint/setup reference.
- **08 Project Demonstration** — scripted walkthrough with sample inputs per feature.

## Build Sequence

- First: Gemini-backed modules (Q&A, Summary, Learning Path) plus local Explain.
- Next: strict-JSON Quiz module with fence-strip/validate/retry hardening.
- Then: `main.py` wiring (routes, Pydantic models, error mapping) and the single-page UI.

## Tech Stack Decisions

- **FastAPI + Uvicorn** — minimal boilerplate for 5 JSON endpoints, `/docs` for free, Jinja2/static support.
- **Gemini API (`google-genai`, `gemini-3.6-flash`)** — one hosted LLM for four features; no GPU, keyed via `.env`.
- **`transformers` + `torch` + `sentencepiece`** — local LaMini model on CPU so Explain is offline and free per call.
- **Jinja2 + vanilla JS** — no frontend build; `fetch()` to the same origin, one `uvicorn main:app --reload` to run.
