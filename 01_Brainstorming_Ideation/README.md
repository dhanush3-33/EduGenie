# Brainstorming and Ideation Phase

> Initial ideas behind EduGenie — a quick, free AI study helper for students.

## Problem

- Students need fast help while studying: answers, simpler explanations, self-quizzes, summaries, and study plans.
- That help is usually scattered across tools, tabs, or paywalled services.
- Goal: one lightweight page combining all five study aids, free to run locally.

## Core Idea

- A FastAPI backend (`05_Project_Development/main.py`) with a single-page UI (`templates/index.html`).
- Pick a task from a dropdown, paste text, get a result — no accounts, no setup beyond an API key.
- Keep each capability in its own Python module so ideas can be prototyped independently.

## Brainstormed Features (initial ideas)

- **Q&A** — ask anything and get a clear answer via the Gemini API (`qna.py` → `answer_question`).
- **Concept Explanation** — simplify tough topics with short sentences and an everyday example, fully local (`explanation_module.py`, `MBZUAI/LaMini-Flan-T5-783M`).
- **Quiz Generation** — paste a passage, get exactly 3 MCQs with 4 options each as strict validated JSON (`quiz_module.py`).
- **Text Summarization** — condense long readings into 3–6 sentences or a short list (`summary_module.py`).
- **Learning Path Recommendations** — enter a topic, get a beginner → advanced plan with resources and projects (`learning_path.py`).

## Why These Five

- Together they cover the full study loop: understand, simplify, test, condense, and plan what to learn next.
