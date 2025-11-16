from dotenv import load_dotenv
load_dotenv()  # Load .env file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .llm import answer_question

app = FastAPI()

# CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lennart-lais.ch"],  # Your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str

@app.post("/api/ask", response_model=Answer)
async def ask_question(question: Question):
    answer = await answer_question(question.question)
    return Answer(answer=answer)

@app.get("/health")
async def health():
    return {"status": "ok"}
