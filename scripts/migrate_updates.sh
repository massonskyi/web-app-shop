#!/bin/bash

# Название базы данных
DB_NAME="admin_shop"

# Название пользователя PostgreSQL
DB_USER="postgres"

# Пароль пользователя PostgreSQL
DB_PASSWORD="postgres"

# Хост PostgreSQL
DB_HOST="0.0.0.0"

# Порт PostgreSQL
DB_PORT="5432"

# Путь к виртуальному окружению
VENV_PATH="../.venv/bin/activate"

# Проверка наличия PostgreSQL
if ! command -v psql &> /dev/null
then
    echo "PostgreSQL не установлен. Пожалуйста, установите PostgreSQL и попробуйте снова."
    exit 1
fi

# Проверка подключения к PostgreSQL
echo "Проверка подключения к PostgreSQL..."
if ! PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -c "\l" &> /dev/null
then
    echo "Не удалось подключиться к PostgreSQL. Пожалуйста, проверьте настройки подключения."
    exit 1
fi

# Проверка существования базы данных
echo "Проверка существования базы данных $DB_NAME..."
if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1; then
    echo "База данных $DB_NAME существует."
else
    echo "База данных $DB_NAME не существует. Создание базы данных..."
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -c "CREATE DATABASE \"$DB_NAME\";"
    if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1; then
        echo "База данных $DB_NAME успешно создана."
    else
        echo "Не удалось создать базу данных $DB_NAME."
        exit 1
    fi
fi

# Проверка наличия виртуального окружения
if [ ! -f "$VENV_PATH" ]; then
    echo "Виртуальное окружение не найдено по пути $VENV_PATH. Пожалуйста, проверьте путь."
    exit 1
fi

# Активация виртуального окружения
source $VENV_PATH

# Проверка наличия Alembic
if ! command -v alembic &> /dev/null
then
    echo "Alembic не установлен. Пожалуйста, установите Alembic и попробуйте снова."
    exit 1
fi

# Создание новой миграции
echo "Создание новой миграции..."
alembic revision --autogenerate -m "Initial migration"

# Применение миграций
echo "Применение миграций..."
alembic upgrade head

# Откат миграций (если необходимо)
# echo "Откат миграций..."
# alembic downgrade -1

echo "Миграции успешно применены."

# Деактивация виртуального окружения
deactivate
