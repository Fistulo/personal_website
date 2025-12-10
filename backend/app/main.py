import os
from dotenv import load_dotenv

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

from .llm import answer_question
from .database import init_db, log_qa_interaction, get_recent_logs

load_dotenv()
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
DOMAIN = os.getenv("DOMAIN", "localhost")

# initializes database on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan,
              docs_url="/api/docs", #change doc urls since caddy sends only /api/* requests to the backend
              redoc_url="/api/redoc",
              openapi_url="/api/openapi.json")  
    

# CORS configuration
if DOMAIN == "localhost":
    ALLOWED_ORIGINS = ["http://localhost"]
else:
    ALLOWED_ORIGINS = [f"https://{DOMAIN}"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QuestionRequest(BaseModel):
    question: str = Field(max_length= 150)
    language: str = Field(max_length= 50)

@app.post("/api/ask")
async def ask_question(body: QuestionRequest, request: Request, background_tasks: BackgroundTasks)-> str:

    answer = await answer_question(body.question, body.language)
    background_tasks.add_task(log_qa_interaction, body.question, answer, body.language, request.client.host)
    return answer

@app.get("/api/admin", response_class=HTMLResponse)
async def admin_panel(token: str = None):
    if token != ADMIN_TOKEN:
        return HTMLResponse("<h1>Unauthorized</h1>", status_code=401)

    logs = get_recent_logs(100)

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