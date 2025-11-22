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

class QuestionRequest(BaseModel):
    question: str
    language: str
class Answer(BaseModel):
    answer: str

@app.post("/api/ask", response_model=Answer)
async def ask_question(request: QuestionRequest):
    answer = await answer_question(request.question, request.language)
    return Answer(answer=answer)

@app.get("/api/health")
async def health():
    return {"status": "ok"}
