@echo off
setlocal

REM Название базы данных
set DB_NAME=admin-shop

REM Название пользователя PostgreSQL
set DB_USER=postgres

REM Пароль пользователя PostgreSQL
set DB_PASSWORD=postgres

REM Хост PostgreSQL
set DB_HOST=127.0.0.1

REM Порт PostgreSQL
set DB_PORT=5432

REM Проверка наличия PostgreSQL
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PostgreSQL не установлен. Пожалуйста, установите PostgreSQL и попробуйте снова.
    exit /b 1
)

REM Проверка подключения к PostgreSQL
echo Проверка подключения к PostgreSQL...
psql -h %DB_HOST% -U %DB_USER% -c "\l" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Не удалось подключиться к PostgreSQL. Пожалуйста, проверьте настройки подключения.
    exit /b 1
)

REM Проверка существования базы данных
echo Проверка существования базы данных %DB_NAME%...
for /f "delims=" %%i in ('psql -h %DB_HOST% -U %DB_USER% -tc "SELECT 1 FROM pg_database WHERE datname = '%DB_NAME%'"') do (
    if "%%i"=="1" (
        echo База данных %DB_NAME% уже существует.
        exit /b 1
    )
)

REM Создание базы данных
echo Создание базы данных %DB_NAME%...
psql -h %DB_HOST% -U %DB_USER% -c "CREATE DATABASE \"%DB_NAME%\";"

REM Проверка успешного создания базы данных
echo Проверка успешного создания базы данных %DB_NAME%...
for /f "delims=" %%i in ('psql -h %DB_HOST% -U %DB_USER% -tc "SELECT 1 FROM pg_database WHERE datname = '%DB_NAME%'"') do (
    if "%%i"=="1" (
        echo База данных %DB_NAME% успешно создана.
    ) else (
        echo Не удалось создать базу данных %DB_NAME%.
        exit /b 1
    )
)

endlocal
