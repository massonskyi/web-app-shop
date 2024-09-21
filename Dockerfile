# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости для компиляции psycopg2
RUN apt-get update && apt-get install -y postgresql postgresql-contrib libpq-dev  build-essential


# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Устанавливаем переменную окружения для указания режима отладки
ENV PYTHONUNBUFFERED=1

# Открываем порт 8000
EXPOSE 8000

# Запускаем FastAPI приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
