"""EduGenie FastAPI application: mounts routes, templates, and static files."""

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="EduGenie", version="1.0.0")

# Allow any frontend origin (local UI, curl, other clients).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def _not_blank(value: str, field_name: str) -> str:
    """Validate that a string field is non-empty after stripping."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must not be empty.")
    return value.strip()


class QuestionRequest(BaseModel):
    """Request body for POST /qa."""

    question: str

    @field_validator("question")
    @classmethod
    def _check_question(cls, value: str) -> str:
        return _not_blank(value, "question")


class ExplainRequest(BaseModel):
    """Request body for POST /explain."""

    concept: str

    @field_validator("concept")
    @classmethod
    def _check_concept(cls, value: str) -> str:
        return _not_blank(value, "concept")


class QuizRequest(BaseModel):
    """Request body for POST /quiz."""

    passage: str

    @field_validator("passage")
    @classmethod
    def _check_passage(cls, value: str) -> str:
        return _not_blank(value, "passage")


class SummarizeRequest(BaseModel):
    """Request body for POST /summarize."""

    text: str

    @field_validator("text")
    @classmethod
    def _check_text(cls, value: str) -> str:
        return _not_blank(value, "text")


class LearnRequest(BaseModel):
    """Request body for POST /learn/recommendations."""

    topic: str

    @field_validator("topic")
    @classmethod
    def _check_topic(cls, value: str) -> str:
        return _not_blank(value, "topic")


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    """Serve the single-page frontend."""
    return templates.TemplateResponse(request, "index.html")


@app.get("/health")
def health() -> dict:
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.post("/qa")
def qa_endpoint(payload: QuestionRequest) -> dict:
    """Answer a general question via Gemini."""
    try:
        return {"question": payload.question, "answer": answer_question(payload.question)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain")
def explain_endpoint(payload: ExplainRequest) -> dict:
    """Simplify a concept via the local Hugging Face model."""
    try:
        return {
            "concept": payload.concept,
            "explanation": explain_concept(payload.concept),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz")
def quiz_endpoint(payload: QuizRequest) -> dict:
    """Generate 3 MCQs from a passage via Gemini (strict JSON)."""
    try:
        return {"passage": payload.passage, "quiz": generate_quiz(payload.passage)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/summarize")
def summarize_endpoint(payload: SummarizeRequest) -> dict:
    """Summarize a long passage via Gemini."""
    try:
        return {"summary": summarize_text(payload.text)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/learn/recommendations")
def learn_endpoint(payload: LearnRequest) -> dict:
    """Generate a beginner-to-advanced learning path via Gemini."""
    try:
        return {
            "topic": payload.topic,
            "learning_path": get_learning_recommendations(payload.topic),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
