"""
Скрипт для создания 6 коротких курсов
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.db.models import Course, Lesson, Assignment
from app.db.repository.courseRepo import CourseRepository
from app.db.repository.lessonRepo import LessonRepository
from app.db.repository.assignmentRepo import AssignmentRepository
from app.db.schemas.course import CourseCreate
from app.db.schemas.lesson import LessonCreate
from app.db.schemas.assignment import AssignmentCreate

COURSES_DATA = [
    {
        "title": "Java для начинающих",
        "description": "Изучите основы Java программирования. Создавайте приложения, работайте с классами и объектами.",
        "lessons": [
            {
                "title": "Введение в Java",
                "content": """# Введение в Java

Java - один из самых популярных языков программирования в мире.

## Что такое Java?

Java - это объектно-ориентированный язык программирования, созданный компанией Sun Microsystems в 1995 году.

## Особенности Java:

- Кроссплатформенность (Write Once, Run Anywhere)
- Автоматическое управление памятью
- Богатая стандартная библиотека
- Безопасность

## Первая программа

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

Это классическая программа Hello World на Java.""",
                "assignment": {
                    "title": "Первая программа на Java",
                    "description": "Создайте свою первую программу",
                    "instructions": "Создайте класс HelloWorld с методом main, который выводит ваше имя на экран."
                }
            },
            {
                "title": "Переменные и типы данных",
                "content": """# Переменные и типы данных в Java

## Примитивные типы

```java
int age = 25;
double price = 99.99;
boolean isActive = true;
char grade = 'A';
```

## Строки

```java
String name = "Иван";
String message = "Привет, " + name;
```

## Массивы

```java
int[] numbers = {1, 2, 3, 4, 5};
String[] names = new String[3];
```""",
                "assignment": {
                    "title": "Работа с переменными",
                    "description": "Практика с типами данных",
                    "instructions": "Создайте программу, которая объявляет переменные разных типов (int, double, String, boolean) и выводит их значения."
                }
            },
            {
                "title": "Условные операторы и циклы",
                "content": """# Условные операторы и циклы

## Условные операторы

```java
if (age >= 18) {
    System.out.println("Совершеннолетний");
} else {
    System.out.println("Несовершеннолетний");
}
```

## Циклы

```java
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

while (count < 5) {
    System.out.println(count);
    count++;
}
```""",
                "assignment": {
                    "title": "Калькулятор с условиями",
                    "description": "Создайте программу с условиями",
                    "instructions": "Напишите программу, которая проверяет число: если оно положительное, выводит 'Положительное', если отрицательное - 'Отрицательное', если ноль - 'Ноль'."
                }
            }
        ]
    },
    {
        "title": "Node.js разработка",
        "description": "Изучите серверную разработку на Node.js. Создавайте веб-серверы и API.",
        "lessons": [
            {
                "title": "Введение в Node.js",
                "content": """# Введение в Node.js

Node.js - это среда выполнения JavaScript на стороне сервера.

## Что такое Node.js?

Node.js позволяет запускать JavaScript вне браузера, на сервере.

## Установка

```bash
npm install
```

## Первый сервер

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('Hello, Node.js!');
});

server.listen(3000, () => {
    console.log('Server running on port 3000');
});
```""",
                "assignment": {
                    "title": "Первый Node.js сервер",
                    "description": "Создайте простой сервер",
                    "instructions": "Создайте Node.js сервер, который отвечает на запросы сообщением 'Welcome to Node.js!' на порту 3000."
                }
            },
            {
                "title": "Express.js основы",
                "content": """# Express.js основы

Express - популярный фреймворк для Node.js.

## Установка

```bash
npm install express
```

## Простое приложение

```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hello Express!');
});

app.listen(3000, () => {
    console.log('Server started');
});
```""",
                "assignment": {
                    "title": "Express приложение",
                    "description": "Создайте Express сервер",
                    "instructions": "Создайте Express приложение с маршрутом GET /api/hello, который возвращает JSON: {message: 'Hello from Express!'}"
                }
            }
        ]
    },
    {
        "title": "Django веб-разработка",
        "description": "Изучите Django - мощный Python фреймворк для создания веб-приложений.",
        "lessons": [
            {
                "title": "Введение в Django",
                "content": """# Введение в Django

Django - это высокоуровневый Python веб-фреймворк.

## Установка

```bash
pip install django
django-admin startproject myproject
```

## Структура проекта

```
myproject/
    manage.py
    myproject/
        settings.py
        urls.py
        wsgi.py
```

## Запуск сервера

```bash
python manage.py runserver
```""",
                "assignment": {
                    "title": "Первый Django проект",
                    "description": "Создайте Django проект",
                    "instructions": "Создайте новый Django проект и запустите сервер разработки. Убедитесь, что видите страницу приветствия Django."
                }
            },
            {
                "title": "Создание приложений",
                "content": """# Создание приложений в Django

## Создание приложения

```bash
python manage.py startapp myapp
```

## Модели

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

## Миграции

```bash
python manage.py makemigrations
python manage.py migrate
```""",
                "assignment": {
                    "title": "Модель в Django",
                    "description": "Создайте модель",
                    "instructions": "Создайте Django приложение с моделью Product (name, price, description) и выполните миграции."
                }
            }
        ]
    },
    {
        "title": "FastAPI современный API",
        "description": "Изучите FastAPI - современный фреймворк для создания быстрых API на Python.",
        "lessons": [
            {
                "title": "Введение в FastAPI",
                "content": """# Введение в FastAPI

FastAPI - современный, быстрый веб-фреймворк для создания API.

## Установка

```bash
pip install fastapi uvicorn
```

## Первое приложение

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

## Запуск

```bash
uvicorn main:app --reload
```""",
                "assignment": {
                    "title": "Первый FastAPI endpoint",
                    "description": "Создайте API endpoint",
                    "instructions": "Создайте FastAPI приложение с endpoint GET /api/users, который возвращает список пользователей в формате JSON."
                }
            },
            {
                "title": "Pydantic модели",
                "content": """# Pydantic модели

Pydantic обеспечивает валидацию данных.

## Определение модели

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users/")
def create_user(user: User):
    return {"message": f"User {user.name} created"}
```""",
                "assignment": {
                    "title": "API с валидацией",
                    "description": "Создайте POST endpoint",
                    "instructions": "Создайте POST endpoint /api/products, который принимает данные продукта (name, price, description) и возвращает созданный продукт."
                }
            }
        ]
    },
    {
        "title": "PHP разработка",
        "description": "Изучите PHP - популярный язык для веб-разработки. Создавайте динамические веб-сайты.",
        "lessons": [
            {
                "title": "Введение в PHP",
                "content": """# Введение в PHP

PHP - серверный язык программирования.

## Первая программа

```php
<?php
echo "Hello, PHP!";
?>
```

## Переменные

```php
$name = "Иван";
$age = 25;
$price = 99.99;
```

## Массивы

```php
$fruits = ["яблоко", "банан", "апельсин"];
$person = ["name" => "Иван", "age" => 25];
```""",
                "assignment": {
                    "title": "Первая PHP программа",
                    "description": "Создайте PHP скрипт",
                    "instructions": "Создайте PHP файл, который выводит информацию о себе: имя, возраст, город в красивом формате."
                }
            },
            {
                "title": "Работа с формами",
                "content": """# Работа с формами в PHP

## HTML форма

```html
<form method="POST" action="process.php">
    <input type="text" name="username">
    <input type="submit" value="Отправить">
</form>
```

## Обработка данных

```php
<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    echo "Привет, " . $username;
}
?>
```""",
                "assignment": {
                    "title": "Обработка формы",
                    "description": "Создайте форму с обработкой",
                    "instructions": "Создайте HTML форму с полями имя и email, и PHP скрипт для обработки этой формы."
                }
            }
        ]
    },
    {
        "title": "Bootstrap дизайн",
        "description": "Изучите Bootstrap - популярный CSS фреймворк для создания красивых и адаптивных интерфейсов.",
        "lessons": [
            {
                "title": "Введение в Bootstrap",
                "content": """# Введение в Bootstrap

Bootstrap - популярный CSS фреймворк.

## Подключение

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

## Сетка

```html
<div class="container">
    <div class="row">
        <div class="col-md-6">Колонка 1</div>
        <div class="col-md-6">Колонка 2</div>
    </div>
</div>
```""",
                "assignment": {
                    "title": "Первая Bootstrap страница",
                    "description": "Создайте страницу с Bootstrap",
                    "instructions": "Создайте HTML страницу с использованием Bootstrap: header, контент в 2 колонки, footer."
                }
            },
            {
                "title": "Компоненты Bootstrap",
                "content": """# Компоненты Bootstrap

## Кнопки

```html
<button class="btn btn-primary">Основная</button>
<button class="btn btn-secondary">Вторичная</button>
```

## Карточки

```html
<div class="card">
    <div class="card-body">
        <h5 class="card-title">Заголовок</h5>
        <p class="card-text">Текст карточки</p>
    </div>
</div>
```

## Навигация

```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">Logo</a>
</nav>
```""",
                "assignment": {
                    "title": "Страница с компонентами",
                    "description": "Используйте компоненты Bootstrap",
                    "instructions": "Создайте страницу с навигацией, карточками товаров и кнопками используя компоненты Bootstrap."
                }
            }
        ]
    }
]

def create_courses():
    db = SessionLocal()
    try:
        course_repo = CourseRepository(db)
        lesson_repo = LessonRepository(db)
        assignment_repo = AssignmentRepository(db)
        
        for course_data in COURSES_DATA:
            existing_course = db.query(Course).filter(Course.title == course_data["title"]).first()
            
            if existing_course:
                print(f"[SKIP] Course '{course_data['title']}' already exists!")
                continue
            
            course_create = CourseCreate(
                title=course_data["title"],
                description=course_data["description"]
            )
            course = course_repo.create_course(course_create)
            print(f"[OK] Created course: {course.title}")
            
            for i, lesson_data in enumerate(course_data["lessons"], 1):
                lesson_create = LessonCreate(
                    course_id=course.id,
                    title=lesson_data["title"],
                    content=lesson_data["content"]
                )
                lesson = lesson_repo.create_lesson(lesson_create)
                print(f"  [OK] Lesson {i}: {lesson.title}")
                
                assignment_data = AssignmentCreate(
                    lesson_id=lesson.id,
                    title=lesson_data["assignment"]["title"],
                    description=lesson_data["assignment"]["description"],
                    instructions=lesson_data["assignment"]["instructions"]
                )
                assignment = assignment_repo.create_assignment(assignment_data)
                print(f"    [OK] Assignment: {assignment.title}")
        
        print(f"\n[SUCCESS] All courses created!")
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_courses()

