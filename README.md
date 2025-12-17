# 🎓 Smart Course Platform

**Online Learning Platform with Progress Tracking & AI Tutor**

## 📋 Описание

Умная платформа для онлайн-обучения с отслеживанием прогресса и встроенным AI-помощником. Проект демонстрирует современную backend-архитектуру с использованием FastAPI, PostgreSQL, JWT аутентификации и интеграцией с OpenAI API.

## 🚀 Основные возможности

- ✅ Регистрация и аутентификация пользователей (JWT)
- ✅ Роли: User (студент) и Admin
- ✅ Управление курсами и уроками (CRUD)
- ✅ Отслеживание прогресса обучения
- ✅ AI Tutor для помощи студентам
- ✅ REST API с автоматической документацией (Swagger)

## 🛠 Технологический стек

- **Framework**: FastAPI
- **Database**: PostgreSQL + SQLAlchemy 2.0
- **Auth**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **AI**: OpenAI API (gpt-4o-mini)
- **Validation**: Pydantic v2
- **Environment**: python-decouple

## 📦 Установка

### 1. Клонирование и настройка окружения

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt
```

### 2. Настройка базы данных

Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE course;
```

### 3. Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/course
JWT_SECRET=your-secret-key-change-in-production-min-32-chars
JWT_ALGORITHM=HS256
OPENAI_API_KEY=your-openai-api-key-here
```

### 4. Инициализация базы данных

```bash
python -m app.util.init_db
```

### 5. Запуск приложения

```bash
uvicorn main:app --reload
```

Приложение будет доступно по адресу: `http://localhost:8000`

## 📚 API Документация

После запуска приложения доступна автоматическая документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 API Endpoints

### Auth
- `POST /auth/register` - Регистрация нового пользователя
- `POST /auth/login` - Вход и получение JWT токена

### Courses
- `GET /courses` - Получить все курсы с прогрессом (требует авторизации)
- `GET /courses/{course_id}` - Получить курс по ID
- `POST /courses` - Создать курс (только Admin)
- `PUT /courses/{course_id}` - Обновить курс (только Admin)
- `DELETE /courses/{course_id}` - Удалить курс (только Admin)

### Lessons
- `GET /lessons/courses/{course_id}/lessons` - Получить уроки курса с прогрессом
- `GET /lessons/{lesson_id}` - Получить урок по ID
- `POST /lessons` - Создать урок (только Admin)
- `PUT /lessons/{lesson_id}` - Обновить урок (только Admin)
- `DELETE /lessons/{lesson_id}` - Удалить урок (только Admin)

### Progress
- `POST /progress/complete` - Отметить урок как завершенный
- `GET /progress/my` - Получить прогресс по всем курсам
- `GET /progress/recommended` - Получить рекомендованный курс

### AI Tutor
- `POST /api/ai/chat` - Задать вопрос AI-помощнику

## 📊 Структура базы данных

### User
- `id` - Primary Key
- `name` - Имя пользователя
- `email` - Email (уникальный)
- `hashed_password` - Хешированный пароль
- `role` - Роль (user/admin)

### Course
- `id` - Primary Key
- `title` - Название курса
- `description` - Описание
- `created_at` - Дата создания
- `updated_at` - Дата обновления

### Lesson
- `id` - Primary Key
- `course_id` - Foreign Key к Course
- `title` - Название урока
- `content` - Содержание урока
- `created_at` - Дата создания
- `updated_at` - Дата обновления

### Progress
- `id` - Primary Key
- `user_id` - Foreign Key к User
- `lesson_id` - Foreign Key к Lesson
- `course_id` - Foreign Key к Course
- `completed` - Статус завершения
- `completed_at` - Дата завершения

## 🧮 Расчет прогресса

Прогресс рассчитывается по формуле:
```
progress = (completed_lessons / total_lessons) * 100
```

## 🤖 AI Tutor

AI Tutor использует OpenAI API (gpt-4o-mini) для помощи студентам в понимании материала урока.

**Пример запроса:**
```json
{
  "course_title": "Python Basics",
  "lesson_title": "Loops",
  "question": "Explain for loop"
}
```

## 👤 Создание Admin пользователя

Для создания администратора используйте скрипт:

```bash
python scripts/create_admin.py
```

Или создайте пользователя через API и вручную измените роль в базе данных:

```sql
UPDATE "Users" SET role = 'admin' WHERE email = 'admin@example.com';
```

## 🏗 Архитектура проекта

```
Back/
├── app/
│   ├── core/
│   │   ├── database.py          # Настройка БД
│   │   └── security/
│   │       ├── authHandler.py   # JWT аутентификация
│   │       └── hashHelper.py    # Хеширование паролей
│   ├── db/
│   │   ├── models/              # SQLAlchemy модели
│   │   ├── schemas/             # Pydantic схемы
│   │   └── repository/          # Репозитории (доступ к БД)
│   ├── routers/                 # API endpoints
│   ├── service/                 # Бизнес-логика
│   └── util/
│       └── init_db.py           # Инициализация БД
├── main.py                      # Точка входа
├── requirements.txt             # Зависимости
└── .env                         # Переменные окружения
```

## 🔒 Безопасность

- Пароли хешируются с использованием bcrypt
- JWT токены для аутентификации
- Role-based access control (RBAC)
- Защита эндпоинтов через middleware

## 📝 Примеры использования

### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword"
  }'
```

### Вход

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword"
  }'
```

### Получение курсов (с токеном)

```bash
curl -X GET "http://localhost:8000/courses" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🐳 Docker (опционально)

Для запуска с Docker создайте `docker-compose.yml`:

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: course
    ports:
      - "5432:5432"
  
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/course
    depends_on:
      - db
```

## 📄 Лицензия

Этот проект создан для образовательных целей.

## 👨‍💻 Автор

Backend Final Project - Smart Course Platform

