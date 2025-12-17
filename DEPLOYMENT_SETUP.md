# Инструкция по настройке деплоя

## Текущие деплои

- **Backend (Render)**: https://smartcourse-backend.onrender.com/
- **Frontend (Vercel)**: https://vercel.com/detriots-projects/smart-course-u4nn/9gtELvpruzBxEK3K4zQeST37jSVc

## Настройка переменных окружения

### 1. Render (Backend) - Настройка переменных окружения

Перейдите в панель управления Render для вашего сервиса `smart-course-platform-api`:

1. Откройте: https://dashboard.render.com
2. Выберите ваш сервис `smart-course-platform-api`
3. Перейдите в раздел **Environment**
4. Добавьте/обновите следующие переменные:

#### Обязательные переменные:

- **DATABASE_URL**: URL вашей PostgreSQL базы данных
  ```
  postgresql://user:password@host:port/database
  ```

- **OPENAI_API_KEY**: Ваш OpenAI API ключ
  ```
  sk-proj-...
  ```

- **JWT_SECRET**: Секретный ключ для JWT (генерируется автоматически, но можно задать вручную)
  ```
  ваш-секретный-ключ-минимум-32-символа
  ```

- **JWT_ALGORITHM**: Алгоритм для JWT (по умолчанию HS256)
  ```
  HS256
  ```

- **CORS_ORIGINS**: URL вашего Vercel frontend (важно для работы API)
  ```
  https://smart-course-u4nn.vercel.app
  ```
  Или если у вас несколько доменов, разделите запятыми:
  ```
  https://smart-course-u4nn.vercel.app,https://your-custom-domain.com
  ```
  
  ⚠️ **Важно**: Замените на реальный URL вашего Vercel deployment!

### 2. Vercel (Frontend) - Настройка переменных окружения

Перейдите в панель управления Vercel:

1. Откройте: https://vercel.com/detriots-projects/smart-course-u4nn
2. Перейдите в **Settings** → **Environment Variables**
3. Добавьте следующую переменную:

#### Обязательная переменная:

- **VITE_API_URL**: URL вашего Render backend
  ```
  https://smartcourse-backend.onrender.com
  ```

⚠️ **Важно**: После добавления переменных окружения в Vercel, нужно **пересобрать deployment**:
- Перейдите в **Deployments**
- Нажмите на три точки рядом с последним deployment
- Выберите **Redeploy**

## Проверка работы

### Проверка Backend:
1. Откройте: https://smartcourse-backend.onrender.com/
2. Должно отобразиться: "Welcome to Smart Course Platform!"

### Проверка API:
```bash
curl https://smartcourse-backend.onrender.com/courses
```

### Проверка Frontend:
1. Откройте ваш Vercel deployment URL
2. Попробуйте зарегистрироваться или войти
3. Проверьте консоль браузера (F12) на наличие ошибок CORS

## Устранение проблем

### Проблема: CORS ошибки в браузере

**Решение**: 
1. Убедитесь, что в Render установлена переменная `CORS_ORIGINS` с правильным URL вашего Vercel deployment
2. URL должен точно совпадать (включая протокол https://)
3. После изменения переменных, перезапустите сервис в Render

### Проблема: Frontend не может подключиться к API

**Решение**:
1. Проверьте, что в Vercel установлена переменная `VITE_API_URL`
2. Убедитесь, что значение правильное: `https://smartcourse-backend.onrender.com`
3. Пересоберите deployment в Vercel после изменения переменных

### Проблема: 401 Unauthorized

**Решение**:
1. Проверьте, что `JWT_SECRET` установлен в Render
2. Убедитесь, что токены сохраняются в localStorage браузера

## Безопасность

⚠️ **Важные напоминания**:
- Никогда не коммитьте `.env` файлы в Git
- Используйте разные `JWT_SECRET` для production и development
- Регулярно обновляйте зависимости
- Используйте HTTPS для всех production deployments

