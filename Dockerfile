# Используем облегчённый образ Python на Alpine
FROM python:3.11-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем необходимые системные зависимости
RUN apk add --no-cache gcc musl-dev python3-dev sqlite

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт (но Railway сам задает $PORT)
EXPOSE 8000

# Запускаем сервер (учитываем переменную $PORT)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
