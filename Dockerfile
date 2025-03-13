# Используем еще более легкий образ Python на основе Alpine
FROM python:3.11-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

RUN apk add --no-cache gcc musl-dev python3-dev libpq-dev

# Копируем файлы проекта
COPY . .

# Копируем только файлы, необходимые для установки зависимостей
# COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install --no-cache-dir -r requirements.txt && \
#    rm -rf /root/.cache

# Копируем оставшиеся файлы проекта
# COPY . /app

# Открываем порт 8000
EXPOSE 8000

# Запускаем сервер
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]