# llm-p

Сервер на **FastAPI** с JWT, SQLite (async через SQLAlchemy + aiosqlite) и запросами к LLM через **OpenRouter**.

- **Python**: 3.11+
- **Зависимости**: см. `pyproject.toml` в этом каталоге; рекомендуемый установщик — [uv](https://github.com/astral-sh/uv).

Код приложения — пакет `app/` в каталоге **`llm_p/`** рядом с `pyproject.toml` (слои: api → usecases → repositories / services), см. **`llm_p/Структура_FastAPI_llm.txt`**.

Документы курса: **`Разработка/ТЗ_0.txt`**, **`Разработка/Критерии_оценки_fastapi_llm.txt`**, а также архитектура и эпики в **`Разработка/`**.

## Пошаговая проверка окружения перед запуском (шаги 1–6)

Сначала один раз подставьте вместо **`<REPO>`** абсолютный путь к **корню вашего git-репозитория** (родитель каталога `llm_p`, не сам `llm_p`).

Примеры:

- Windows: `C:\Users\you\Documents\GitHub\pymephi\fastapi`
- macOS / Linux: `/home/you/src/fastapi` или `$HOME/Documents/GitHub/pymephi/fastapi`

### Шаги 1–3

Выполните **в одном сеансе терминала подряд три команды** из блока вашей ОС. Успех: в выводе есть **`DIR_OK`**, **`PYTHON_OK …`**, **`FILES_OK …`**.

### Windows (PowerShell) — три команды подряд

```powershell
Set-Location "<REPO>\llm_p"; Write-Output "DIR_OK $(Get-Location)"
```

```powershell
python -c "import sys; v=sys.version_info; assert v>=(3,11), f'Need Python 3.11+, got {v.major}.{v.minor}'; print(f'PYTHON_OK {v.major}.{v.minor}.{v.micro}')"
```

```powershell
foreach ($f in 'pyproject.toml','.env') { if (-not (Test-Path -LiteralPath $f)) { throw "Missing file: $f" } }; Write-Output 'FILES_OK pyproject.toml .env'
```

*(После первой команды текущая папка — `llm_p`; вторая и третья выполняются уже в ней.)*

### macOS (Terminal, bash/zsh) — три команды подряд

```bash
cd "<REPO>/llm_p" && echo "DIR_OK $(pwd)"
```

```bash
python3 -c "import sys; v=sys.version_info; assert v>=(3,11), f'Need Python 3.11+, got {v.major}.{v.minor}'; print(f'PYTHON_OK {v.major}.{v.minor}.{v.micro}')"
```

```bash
test -f pyproject.toml && test -f .env && echo "FILES_OK pyproject.toml .env" || { echo "Missing file"; exit 1; }
```

Если команда `python3` не найдена, замените её на `python` (при условии, что это Python 3.11+).

### Linux (bash) — три команды подряд

```bash
cd "<REPO>/llm_p" && echo "DIR_OK $(pwd)"
```

```bash
python3 -c "import sys; v=sys.version_info; assert v>=(3,11), f'Need Python 3.11+, got {v.major}.{v.minor}'; print(f'PYTHON_OK {v.major}.{v.minor}.{v.micro}')"
```

```bash
test -f pyproject.toml && test -f .env && echo "FILES_OK pyproject.toml .env" || { echo "Missing file"; exit 1; }
```

При необходимости используйте `python` вместо `python3`, если в системе так настроен интерпретатор 3.11+.

### Шаг 4. Установка зависимостей через pip

Пакеты ставятся в **то окружение Python**, которое вызываете командой `python` / `python3` (глобально или из активированного venv). Перечень совпадает с типовой установкой из **«Быстрого старта»**: FastAPI, Uvicorn, SQLAlchemy, aiosqlite, Pydantic, JWT, bcrypt-стек, httpx, ruff и др.

Выполните **одну** команду из блока вашей ОС. Успех: в конце вывода есть строка **`DEPS_OK`**. (Сообщение pip о доступном обновлении можно игнорировать.)

Рекомендуется виртуальное окружение (`python -m venv .venv` и активация) или **uv** — см. **«Быстрый старт»**; для быстрой проверки достаточно команд ниже.

#### Windows (PowerShell) — одна команда

```powershell
Set-Location "<REPO>\llm_p"; python -m pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite "pydantic[email]" pydantic-settings "python-jose[cryptography]" cryptography "passlib[bcrypt]" httpx python-multipart greenlet "bcrypt==4.3.0" ruff; python -c "import fastapi, uvicorn, sqlalchemy; print('DEPS_OK')"
```

#### macOS (Terminal, bash/zsh) — одна команда

```bash
cd "<REPO>/llm_p" && python3 -m pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite "pydantic[email]" pydantic-settings "python-jose[cryptography]" cryptography "passlib[bcrypt]" httpx python-multipart greenlet "bcrypt==4.3.0" ruff && python3 -c "import fastapi, uvicorn, sqlalchemy; print('DEPS_OK')"
```

Если `python3` не найден, замените оба вхождения на `python` (интерпретатор 3.11+).

#### Linux (bash) — одна команда

```bash
cd "<REPO>/llm_p" && python3 -m pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite "pydantic[email]" pydantic-settings "python-jose[cryptography]" cryptography "passlib[bcrypt]" httpx python-multipart greenlet "bcrypt==4.3.0" ruff && python3 -c "import fastapi, uvicorn, sqlalchemy; print('DEPS_OK')"
```

При необходимости замените `python3` на `python`.

### Шаг 5. Запуск HTTP-сервера (Uvicorn)

Сервер работает, пока процесс запущен: терминал будет **занят**, остановка — **Ctrl+C**.

**Выполняйте шаг 5 в отдельном окне терминала**, которое можно **не закрывать**, пока нужен API (шаги 1–4 уже можно не повторять).

Ожидайте в логе строки **`Uvicorn running on http://127.0.0.1:8000`** и **`Application startup complete`**. Swagger: **`http://127.0.0.1:8000/docs`**.

#### Windows (PowerShell) — одна команда

```powershell
Set-Location "<REPO>\llm_p"; python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### macOS (Terminal, bash/zsh) — одна команда

```bash
cd "<REPO>/llm_p" && python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

При необходимости замените `python3` на `python`.

#### Linux (bash) — одна команда

```bash
cd "<REPO>/llm_p" && python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

При необходимости замените `python3` на `python`.

### Шаг 6. Проверка `GET /health`

Запрос нужно отправить **пока сервер из шага 5 запущен**. Используйте **ещё одно отдельное окно терминала** (не то, где работает `uvicorn`).

Успех: в ответе видны поля **`status`** (ожидается `ok`) и **`env`** (как в вашем `.env`, по умолчанию из примера — `local`).

#### Windows (PowerShell) — одна команда

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get
```

#### macOS (Terminal, bash/zsh) — одна команда

```bash
curl -sS "http://127.0.0.1:8000/health"
```

#### Linux (bash) — одна команда

```bash
curl -sS "http://127.0.0.1:8000/health"
```

После успешных шагов 5–6 раздел **«Быстрый старт»** можно использовать как справочник (копирование `.env.example`, вариант с **uv**, приёмка со скриншотами). Если зависимости уже установлены на **шаге 4**, **пункт 3** в «Быстром старте» с повторным `pip install` можно не выполнять; **пункт 4** дублирует **шаг 5** при запуске из `llm_p`.

## Быстрый старт

Дальше команды выполняйте из каталога **`llm_p/`** (там же `pyproject.toml` и каталог `app`).

1. Перейти в каталог приложения и скопировать пример переменных окружения:

   ```powershell
   cd llm_p
   copy .env.example .env
   ```

   (POSIX: `cd llm_p && cp .env.example .env`.)

2. Отредактировать **`.env`** в этом же каталоге: задать `JWT_SECRET`, при необходимости `OPENROUTER_API_KEY` и прочие поля из примера.

3. Установить зависимости (**уже находясь в `llm_p/`**; быстрый вариант с **pip**, если нет uv):

   ```text
   python -m pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite
   python -m pip install "pydantic[email]" pydantic-settings "python-jose[cryptography]"
   python -m pip install cryptography "passlib[bcrypt]" httpx python-multipart greenlet "bcrypt==4.3.0" ruff
   ```

   С **uv** из **`llm_p/`** (пример):

   ```text
   cd llm_p
   uv venv
   uv pip compile pyproject.toml -o reqs.txt && uv pip install -r reqs.txt
   ```

4. Запуск приложения (**рабочий каталог — `llm_p/`**):

   ```text
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Либо из **`llm_p/`**: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.

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

Просмотр SQLite при `SQLITE_PATH=./app.db` (файл создаётся в **`llm_p/`**, откуда вы запускали сервер):

```text
cd llm_p
sqlite3 app.db ".tables"
```

## Качество кода

Из каталога **`llm_p/`**:

```text
cd llm_p
python -m ruff check app
```

Ожидаемый результат: **`All checks passed!`**.
