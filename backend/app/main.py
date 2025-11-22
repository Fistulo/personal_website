from dotenv import load_dotenv
load_dotenv()
import os
import logging

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .llm import answer_question
from .database import init_db, log_qa_interaction, get_recent_logs

logger = logging.getLogger(__name__)

app = FastAPI()

DOMAIN = os.getenv("DOMAIN", "localhost")

if DOMAIN == "localhost":
    ALLOWED_ORIGINS = ["http://localhost"]
else:
    ALLOWED_ORIGINS = [f"https://{DOMAIN}"]

# CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    language: str

class Answer(BaseModel):
    answer: str

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully!")

@app.post("/api/ask", response_model=Answer)
async def ask_question(body: QuestionRequest, request: Request):
    answer = await answer_question(body.question, body.language)
    log_qa_interaction(
        question=body.question,
        answer=answer,
        language=body.language,
        user_ip=request.client.host
    )
    return Answer(answer=answer)

@app.get("/api/health")
async def health():
    return {"status": "ok"}

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request, token: str = None):
    if token != ADMIN_TOKEN:
        return HTMLResponse("<h1>Unauthorized</h1>", status_code=401)

    logs = get_recent_logs(100)  # ← Use the new function

    html = """
    <html>
    <head><title>Admin - Question Logs</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
    </style>
    </head>
    <body>
        <h1>Question Logs</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Timestamp</th>
                <th>Language</th>
                <th>Question</th>
                <th>Answer</th>
                <th>IP</th>
            </tr>
    """

    for log in logs:
        html += f"""
            <tr>
                <td>{log['id']}</td>
                <td>{log['timestamp']}</td>
                <td>{log['language']}</td>
                <td>{log['question']}</td>
                <td>{log['answer'][:100]}...</td>
                <td>{log['user_ip']}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """
    return html