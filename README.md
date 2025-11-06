# Проект для изучения Python
Тренировочный проект для обучения Пайтону, фреймворку и прочим инструментам.

## Клонирование и настройка проекта

- git clone https://github.com/Kunilin/python-education.git

- cd python-education

- Создай виртуальное окружение: python -m venv .venv

- Активируй виртуальное окружение:
  * Windows: .venv\Scripts\activate
  * Linux/Mac: source .venv/bin/activate

## Установка зависимостей
- pip install -r requirements.txt 

## Настройка переменных окружения
Создай файл .env в корне проекта:

- Database: DB_URL=postgresql+asyncpg://user:password@localhost:5432/task_manager

- Kafka: 
KAFKA_BOOTSTRAP_SERVER=localhost:9092 и KAFKA_TOPIC=task_events

## Запуск инфраструктуры (Docker)

- Запусти PostgreSQL и Kafka: docker-compose up -d

- Проверь, что все сервисы запущены: docker-compose ps

## Запуск приложения

- Запусти FastAPI приложение: uvicorn app.cmd.main:app --reload

## API Документация

После запуска приложения доступны:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health