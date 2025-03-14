# Используем легкий образ Python на основе Alpine
FROM python:3.11-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt для кэширования зависимостей
COPY requirements.txt .

# Устанавливаем зависимости для PostgreSQL и Python
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

# Копируем только необходимые файлы проекта
COPY main.py database.py models.py ./

# Устанавливаем переменную окружения для логов в реальном времени
ENV PYTHONUNBUFFERED=1

# Запускаем приложение через Uvicorn
# local Docker
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

# For Railway
# Добавляем проверку порта через скрипт
CMD ["sh", "-c", "PORT=${PORT:-8000}; if ! [[ \"$PORT\" =~ ^[0-9]+$ ]]; then PORT=8000; fi; uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1"]