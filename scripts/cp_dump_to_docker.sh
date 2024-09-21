#!/bin/bash

# Установите переменные окружения
DB_HOST=0.0.0.0
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=admin_shop
DOCKER_DB_HOST=0.0.0.0
DOCKER_DB_PORT=5432
DOCKER_DB_USER=postgres
DOCKER_DB_PASSWORD=postgres
DOCKER_DB_NAME=admin_shop
BACKUP_FILE=backup.sql

# Создание дампа базы данных
echo "Creating database dump..."
PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -F c -b -v -f $BACKUP_FILE $DB_NAME

# Восстановление дампа в Docker-контейнере PostgreSQL
echo "Restoring database dump to Docker PostgreSQL..."
docker exec -i your_postgres_container_name psql -h $DOCKER_DB_HOST -p $DOCKER_DB_PORT -U $DOCKER_DB_USER -d $DOCKER_DB_NAME -f $BACKUP_FILE

echo "Database backup and restore completed."
