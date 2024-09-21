# Admin Shop

## Описание

Admin Shop — это проект для управления администраторами магазина. Проект включает в себя CRUD операции для администраторов, аутентификацию и авторизацию с использованием JWT токенов.

## Установка

### Требования

- Python 3.8+
- PostgreSQL

### Установка зависимостей

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/admin_shop.git
    cd admin_shop
    ```

2. Создайте виртуальное окружение:

    ```bash
    python -m venv .venv
    ```

3. Активируйте виртуальное окружение:

    - На Windows:

        ```bash
        .venv\Scripts\activate
        ```

    - На macOS и Linux:

        ```bash
        source .venv/bin/activate
        ```

4. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

### Настройка базы данных

1. Создайте базу данных PostgreSQL:

    ```sql
    CREATE DATABASE admin_shop;
    ```

2. Настройте переменные окружения в файле `.env`:

    ```env
    DATABASE_URL=postgresql://username:password@localhost/admin_shop
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

### Запуск сервера

Запустите сервер с помощью Uvicorn:

```bash

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

```
и переходите по адресу:

``` curl

    http://0.0.0.0:8000/docs

```

## Использование

 ### API Endpoints
    - POST /api_version_1/admin/crud/sign_in: Аутентификация администратора.
    - GET /api_version_1/admin/crud/admins/: Получение списка всех администраторов.
    - GET /api_version_1/admin/crud/admins/{admin_id}: Получение информации об администраторе по ID.
    - POST /api_version_1/admin/crud/admins/: Создание нового администратора.
    - PUT /api_version_1/admin/crud/admins/{admin_id}: Обновление информации об администраторе по ID.
    - DELETE /api_version_1/admin/crud/admins/{admin_id}: Удаление администратора по ID.
    -
## Примеры запросов

 ### Аутентификация администратора

 ```curl
 curl -X POST "http://127.0.0.1:8000/api_version_1/admin/crud/sign_in" -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=password"
 ```
 ### Получение списка всех администраторов
 
 ```curl
 curl -X GET "http://127.0.0.1:8000/api_version_1/admin/crud/admins/" -H "Authorization: Bearer <your_access_token>"
 ```
## Лицензия
 Этот проект лицензирован под лицензией MIT. Подробности смотрите в файле LICENSE.

## Контакты
 Если у вас есть вопросы или предложения, пожалуйста, свяжитесь с нами по адресу andreyharfild@gmail.com.