@echo off
setlocal

REM Установите переменные окружения
set DB_HOST=0.0.0.0
set DB_PORT=5432
set DB_USER=postgres
set DB_PASSWORD=postgres
set DB_NAME=admin_shop
set DOCKER_DB_HOST=0.0.0.0
set DOCKER_DB_PORT=5432
set DOCKER_DB_USER=postgres
set DOCKER_DB_PASSWORD=postgres
set DOCKER_DB_NAME=admin_shop
set BACKUP_FILE=backup.sql

REM Создание дампа базы данных
echo Creating database dump...
pg_dump -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -F c -b -v -f %BACKUP_FILE% %DB_NAME%

REM Восстановление дампа в Docker-контейнере PostgreSQL
echo Restoring database dump to Docker PostgreSQL...
docker exec -i your_postgres_container_name psql -h %DOCKER_DB_HOST% -p %DOCKER_DB_PORT% -U %DOCKER_DB_USER% -d %DOCKER_DB_NAME% -f %BACKUP_FILE%

echo Database backup and restore completed.

endlocal
