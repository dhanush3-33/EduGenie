# Project Testing Phase

> Testing plan/checklist for EduGenie (code under test lives in `05_Project_Development/`).

## Endpoint Checklist

- **POST /qa `{"question"}`** — valid → 200 with non-empty `answer`; empty → 422/400; missing key or API failure → 502.
- **POST /explain `{"concept"}`** — valid → 200 with `explanation` (first call downloads the model, later calls offline); empty → 422/400.
- **POST /quiz `{"passage"}`** — passage ≥ 30 chars → 200 with 3 questions × 4 options, `answer` matching one option.
- **Quiz robustness** — short/empty passage → 400/422; malformed model JSON → fence-strip + validate + one retry, then a clear 502.
- **POST /summarize `{"text"}`** — long passage → 200 with 3–6 sentence `summary`; empty → 422/400; Gemini failure → 502.
- **POST /learn/recommendations `{"topic"}`** — topic → 200 with staged `learning_path`; empty → 422/400; failure → 502.
- **GET /health** → `{"status": "ok"}`; **GET /** → 200 HTML; interactive docs at `/docs`.

## Manual Frontend Steps

- Run `uvicorn main:app --reload` from `05_Project_Development/`, open http://127.0.0.1:8000.
- For each dropdown task (Q&A, Explain, Quiz, Summary, Recommend Path), submit a valid input and confirm the rendered result.
- Submit empty input per task and confirm the inline error message.
- Remove the API key / go offline to confirm Gemini-backed tasks surface the 502 detail.
- For Quiz, confirm 3 questions render with the correct option marked.
