# Используем легковесный образ Python (Alpine)
FROM python:3.11-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (sqlite3, gcc)
RUN apk add --no-cache libsqlite3-dev gcc musl-dev

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache

# Открываем порт (но Railway сам задает $PORT)
EXPOSE 8000

# Запускаем сервер с правильным портом
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
