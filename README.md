# SmartCourse Backend (FastAPI)

Backend‑часть платформы SmartCourse: авторизация, курсы, уроки, задания, прогресс и AI‑репетитор.

## Технологии

- **Python 3.12**, **FastAPI**
- **SQLAlchemy** (ORM)
- **PostgreSQL** (или другая БД по URL)
- **OpenAI API** для AI‑туторинга и проверки заданий

## Установка и запуск локально

```bash
cd SmartCourse-BAckend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Создайте файл `.env` в корне backend‑проекта, например:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/smartcourse
OPENAI_API_KEY=sk-...
```

Запуск сервера:

```bash
uvicorn main:app --reload
```

По умолчанию API будет доступно на `http://localhost:8000`.

## Основные модули

- `app/routers` — FastAPI‑роутеры:
  - `auth.py` — регистрация, логин, JWT‑аутентификация
  - `courses.py`, `lessons.py`, `progress.py` — работа с курсами, уроками и прогрессом
  - `assignments.py` — задания и отправка решений
  - `ai.py` — AI‑репетитор и проверка заданий
- `app/service` — бизнес‑логика:
  - `userService.py`, `courseService.py`, `lessonService.py`, `progressService.py`
  - `assignmentService.py` — создание/получение заданий и отправка ответов
  - `aiService.py` — обёртка над OpenAI для чата и проверки заданий
- `app/db/models` и `app/db/schemas` — SQLAlchemy‑модели и Pydantic‑схемы

## AI‑функции

### 1. AI‑репетитор по урокам

Маршрут: `POST /api/ai/chat`  
Принимает `course_title`, `lesson_title`, `question` и возвращает развёрнутый ответ от AI‑тютора.

### 2. Проверка заданий с помощью AI

Маршрут: `POST /api/ai/assignment/check`  
Тело запроса (схема `AIAssignmentCheckRequest`):

- `course_title`
- `lesson_title`
- `assignment_title`
- `assignment_instructions`
- `user_answer`

Ответ (`AIAssignmentCheckResponse`):

- `is_correct: bool` — оценка правильности ответа
- `explanation: str` — подробное объяснение/разбор
- `suggested_answer?: str` — зарезервировано на будущее под эталонный ответ

Фронтенд вызывает этот эндпоинт со страницы курса (`CoursePage.tsx`), чтобы:

- проверить текущий ответ студента («Проверить ответ с ИИ»);
- помочь, если студент не знает, как решать («Помоги решить»).

## Краткое описание проекта для GitHub

SmartCourse — учебная платформа, где пользователь проходит курсы и уроки, выполняет задания и получает обратную связь от AI‑репетитора.  
Backend на FastAPI управляет пользователями, курсами, прогрессом и заданиями, а также интегрируется с OpenAI для объяснения материалов и проверки решений. Frontend на React/Vite отображает личный кабинет, курсы и AI‑чат, подключаясь к этому API.


