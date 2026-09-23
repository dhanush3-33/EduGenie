# Project Demonstration Phase

> Live-demo walkthrough. Run `uvicorn main:app --reload` from `05_Project_Development/` and open http://127.0.0.1:8000.

## Demo Script

- **1. Q&A (`POST /qa`)** — enter `{"question": "What is photosynthesis?"}` → clear plain-text `answer` about plants converting light to energy.
- **2. Explain (`POST /explain`)** — enter `{"concept": "gravity"}` → beginner-friendly `explanation` with short sentences and an everyday example (local model, works offline).
- **3. Quiz (`POST /quiz`)** — paste a 3+ sentence passage (≥30 chars) as `{"passage"}` → `quiz` with exactly 3 questions, 4 options each, correct option marked.
- **4. Summary (`POST /summarize`)** — paste a long paragraph as `{"text"}` → 3–6 sentence `summary` of the key points.
- **5. Learning Path (`POST /learn/recommendations`)** — enter `{"topic": "Python programming"}` → markdown `learning_path` with beginner/intermediate/advanced stages, resources, and projects.

## Tips for Recording

- Open with `GET /health` → `{"status": "ok"}` to prove the server is up.
- Show one failure case: empty input → validation error; mention the 502 path for a missing key.
- Close on `/docs` to show all 5 endpoints auto-documented.
- Keep each feature to ~1 minute: dropdown → paste → submit → result.
- Narrate the split: four features via Gemini `gemini-3.6-flash`, Explain via on-device LaMini.
- Point to the code map: routes in `main.py`, one module per feature in `05_Project_Development/`.
