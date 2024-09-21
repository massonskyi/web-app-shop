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

REM Путь к виртуальному окружению
set VENV_PATH=..\.venv\Scripts\activate.bat

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
    ) else (
        echo База данных %DB_NAME% не существует. Создание базы данных...
        psql -h %DB_HOST% -U %DB_USER% -c "CREATE DATABASE \"%DB_NAME%\";"
        for /f "delims=" %%i in ('psql -h %DB_HOST% -U %DB_USER% -tc "SELECT 1 FROM pg_database WHERE datname = '%DB_NAME%'"') do (
            if "%%i"=="1" (
                echo База данных %DB_NAME% успешно создана.
            ) else (
                echo Не удалось создать базу данных %DB_NAME%.
                exit /b 1
            )
        )
    )
)

REM Проверка наличия виртуального окружения
if not exist "%VENV_PATH%" (
    echo Виртуальное окружение не найдено по пути %VENV_PATH%. Пожалуйста, проверьте путь.
    exit /b 1
)

REM Активация виртуального окружения
call "%VENV_PATH%"

REM Проверка наличия Alembic
where alembic >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Alembic не установлен. Пожалуйста, установите Alembic и попробуйте снова.
    exit /b 1
)

REM Создание новой миграции
echo Создание новой миграции...
alembic revision --autogenerate -m "Initial migration"

REM Применение миграций
echo Применение миграций...
alembic upgrade head

REM Откат миграций (если необходимо)
REM echo Откат миграций...
REM alembic downgrade -1

echo Миграции успешно применены.

REM Деактивация виртуального окружения
deactivate

endlocal