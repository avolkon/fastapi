# llm-p

Сервер на **FastAPI** с JWT, SQLite (async через SQLAlchemy + aiosqlite) и запросами к LLM через **OpenRouter**.

- **Python**: 3.11+
- **Зависимости**: см. `pyproject.toml` в корне репозитория; рекомендуемый установщик — [uv](https://github.com/astral-sh/uv).

Код приложения — пакет `app/` в **корне репозитория** (слои: api → usecases → repositories / services), как в **ТЗ_0**.

## Быстрый старт

Дальше команды выполняйте из **корня репозитория** (где лежат `pyproject.toml` и каталог `app`).

1. Скопировать пример переменных окружения:

   ```text
   copy .env.example .env
   ```

   (PowerShell: `Copy-Item .env.example .env`)

   Если у вас остался старый файл `project\.env` после переноса каталога — достаточно один раз скопировать его в корень как `.env`.

2. Отредактировать **`.env` в корне**: задать `JWT_SECRET`, при необходимости `OPENROUTER_API_KEY` и прочие поля из примера.

3. Установить зависимости (быстрый вариант с **pip**, если нет uv):

   ```text
   python -m pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite
   python -m pip install "pydantic[email]" pydantic-settings "python-jose[cryptography]"
   python -m pip install cryptography "passlib[bcrypt]" httpx python-multipart greenlet "bcrypt==4.3.0" ruff
   ```

   С **uv** из корня репозитория (пример):

   ```text
   uv venv
   uv pip compile pyproject.toml -o reqs.txt && uv pip install -r reqs.txt
   ```

4. Запуск приложения (рабочий каталог — корень репозитория):

   ```text
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Либо: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.

5. Документация Swagger: открыть `http://127.0.0.1:8000/docs`.

6. Здоровье сервиса: `GET /health`.

## Основные эндпоинты

| Метод | Путь | Описание |
|------:|------|-----------|
| POST | `/auth/register` | Регистрация (JSON: email, пароль минимум 8 символов) |
| POST | `/auth/login` | Форма OAuth2 (`username`=email, `password`) → JWT |
| GET | `/auth/me` | Профиль пользователя по Bearer-токену |
| POST | `/chat` | Вопрос к LLM (`prompt`, опционально `system`, лимиты истории и температура) |
| GET | `/chat/history` | История сообщений (query `limit`, по умолчанию до 100) |
| DELETE | `/chat/history` | Полная очистка истории (ответ `204`) |

Без действительного Bearer-токена защищённые маршруты отвечают **401** (кроме ошибок домена через единый JSON `detail`).

## OpenRouter и безопасность

- Храните **JWT_SECRET** длинным и случайным; не коммитьте реальный `.env`.
- Ответ провайдера LLM переводится в **502** с безопасным текстом клиенту; токены OpenRouter в ответах не попадают.
- Пароли хешируются **bcrypt** (passlib); в логи не записываются.

## Приёмка: скриншоты (папка `./screenshots/`)

Под критерии курса сделайте и положите в репозиторий изображения (рекомендуемые имена):

- `screenshots/01-register.png` — регистрация с email вида **`student_surname@email.com`**
- `screenshots/02-login-token.png` — логин и полученный JWT
- `screenshots/03-swagger-authorize.png` — кнопка **Authorize** в Swagger и ввод Bearer
- `screenshots/04-chat-post.png` — успешный `POST /chat`
- `screenshots/05-history-get.png` — `GET /chat/history`
- `screenshots/06-history-delete.png` — `DELETE /chat/history` (можно код `204`)

Перед публикацией замажьте чувствительные части токена или ключа провайдера.

## Ручной чеклист перед сдачей

После воспроизведения локально при необходимости отметьте шаг:

- Запуск из чистого venv / uv без ошибок.
- Регистрация того же пользователя дважды → **409** с понятным `detail`.
- Неверный логин или пароль → **401** без уточнения (есть ли email в базе).
- Без заголовка `Authorization` для `/chat*` и `/auth/me` → **401**.
- `POST /chat` при недоступном OpenRouter возвращает **502**, приложение живое.
- `GET /chat/history` содержит пары user/assistant; `DELETE` очищает историю только выбранного пользователя.

Просмотр SQLite при `SQLITE_PATH=./app.db` (файл в корне репозитория):

```text
sqlite3 app.db ".tables"
```

## Качество кода

Из корня репозитория:

```text
python -m ruff check app
```

Ожидаемый результат: **`All checks passed!`**.
