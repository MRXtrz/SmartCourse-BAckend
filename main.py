from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers import auth, courses, lessons, progress, ai, assignments, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="Smart Course Platform API",
    lifespan=lifespan
)

from decouple import config

origins = [
    "https://smart-course-u4nn.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth.authRouter, tags=["Auth"], prefix="/auth")
app.include_router(router=courses.coursesRouter, tags=["Courses"], prefix="/courses")
app.include_router(router=lessons.lessonsRouter, tags=["Lessons"], prefix="/lessons")
app.include_router(router=progress.progressRouter, tags=["Progress"], prefix="/progress")
app.include_router(router=ai.aiRouter, tags=["AI Tutor"], prefix="/api/ai")
app.include_router(router=assignments.assignmentsRouter, tags=["Assignments"], prefix="/assignments")
app.include_router(router=admin.adminRouter, tags=["Admin"], prefix="/admin")


@app.get("/", response_class=HTMLResponse)
async def main():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Главная страница</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(to right, #74ebd5, #ACB6E5);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            h1 {
                color: white;
                font-size: 3rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
        </style>
    </head>
    <body>
        <h1>Welcome to Smart Course Platform!</h1>
    </body>
    </html>
    """
    return html_content
