# llm-p

Главный README курсового проекта (корень репозитория). Исполняемое приложение, **`pyproject.toml`** и **`app/`** находятся в каталоге **`llm_p/`** — все команды **uv**/**uvicorn** выполняйте **из `llm_p/`** (или переходите туда, как в блоках ниже).

Сервер на **FastAPI** с JWT, SQLite (async через SQLAlchemy + aiosqlite) и запросами к LLM через **OpenRouter**.

- **Python**: 3.11+
- **Зависимости**: см. **`llm_p/pyproject.toml`**. По методичке установка зависимостей и запуск сервера описаны **[uv](https://github.com/astral-sh/uv)** (`uv sync`, `uv run …`). Запасной путь только если uv недоступен — раздел **«Запасной путь: pip»**.

Структура кода: слои **api → usecases → repositories / services** внутри **`llm_p/app/`**.

Документы курса: **`Разработка/Критерии_оценки_fastapi_llm.txt`**, а также прочие материалы в **`Разработка/`** (архитектура, эпики).

## Пошаговая проверка окружения перед запуском (шаги 1–6)

Ниже основной сценарий установки зависимостей и запуска — **[uv](https://github.com/astral-sh/uv)** из `PATH` (`uv sync`, `uv run …`). Если **uv недоступен**, используйте **только после шагов 1–3** запасной путь с **pip** — подраздел **«Запасной путь: pip»** в конце этого блока.

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

### Шаг 4. Установка зависимостей через **uv**

Команда **`uv sync`** читает зависимости из **`pyproject.toml`**, создаёт при необходимости виртуальное окружение **`.venv`** в каталоге `llm_p/` и ставит в него пакеты.

Выполните **одну** команду из блока вашей ОС (**после** шага 3 вы уже в `llm_p/` в том же сеансе, либо снова перейдите в `llm_p`). Успех: в конце вывода есть строка **`DEPS_OK`**.

Не установлен **uv**: см. **[установку uv](https://docs.astral.sh/uv/getting-started/installation/)**, затем повторите шаг 4.

#### Windows (PowerShell) — одна команда

```powershell
Set-Location "<REPO>\llm_p"; uv sync; uv run python -c "import fastapi, uvicorn, sqlalchemy; print('DEPS_OK')"
```

#### macOS (Terminal, bash/zsh) — одна команда

```bash
cd "<REPO>/llm_p" && uv sync && uv run python -c "import fastapi, uvicorn, sqlalchemy; print('DEPS_OK')"
```

#### Linux (bash) — одна команда

```bash
cd "<REPO>/llm_p" && uv sync && uv run python -c "import fastapi, uvicorn, sqlalchemy; print('DEPS_OK')"
```

##### Альтернатива для шага 4: `uv venv`, `uv pip compile`, `uv pip install`

В **`Разработка/Критерии_оценки_fastapi_llm.txt`** зафиксированы установка через **`uv venv`** и связка **`uv pip compile`** + **`uv pip install`**. По смыслу это тот же набор пакетов из **`pyproject.toml`**, что даёт **`uv sync`**; ниже — эквивалентный вариант (из **`llm_p/`**). Файл **`reqs.txt`** генерируется локально; при желании добавьте его в **`.gitignore`**, если не хотите коммитить лок.

#### Windows (PowerShell)

```powershell
Set-Location "<REPO>\llm_p"
uv venv
uv pip compile pyproject.toml -o reqs.txt
uv pip install -r reqs.txt
uv run python -c "import fastapi, uvicorn, sqlalchemy; print('DEPS_OK')"
```

#### macOS / Linux

```bash
cd "<REPO>/llm_p"
uv venv
uv pip compile pyproject.toml -o reqs.txt
uv pip install -r reqs.txt
uv run python -c "import fastapi, uvicorn, sqlalchemy; print('DEPS_OK')"
```

### Шаг 5. Запуск HTTP-сервера (Uvicorn)

Сервер работает, пока процесс запущен: терминал будет **занят**, остановка — **Ctrl+C**.

**Выполняйте шаг 5 в отдельном окне терминала**, которое можно **не закрывать**, пока нужен API (шаги 1–4 уже можно не повторять).

Ожидайте в логе строки **`Uvicorn running on http://127.0.0.1:8000`** и **`Application startup complete`**. Swagger: **`http://127.0.0.1:8000/docs`**.

#### Windows (PowerShell) — одна команда

```powershell
Set-Location "<REPO>\llm_p"; uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### macOS (Terminal, bash/zsh) — одна команда

```bash
cd "<REPO>/llm_p" && uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### Linux (bash) — одна команда

```bash
cd "<REPO>/llm_p" && uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

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

После успешных шагов 5–6 раздел **«Быстрый старт»** можно использовать как справочник (копирование `.env.example`, приёмка со скриншотами). Если зависимости уже синхронизированы на **шаге 4**, **`uv sync`** в «Быстром старте» можно не повторять; пункт про запуск дублирует **шаг 5**.

### Запасной путь: **pip** (без uv)

Использовать только если **uv установить нельзя**. Перечень пакетов совпадает с **`pyproject.toml`**.

#### Windows (PowerShell)

```powershell
Set-Location "<REPO>\llm_p"; python -m pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite "pydantic[email]" pydantic-settings "python-jose[cryptography]" cryptography "passlib[bcrypt]" httpx python-multipart greenlet "bcrypt==4.3.0" ruff; python -c "import fastapi, uvicorn, sqlalchemy; print('DEPS_OK')"
```

Запуск сервера тем же интерпретатором, где стоят зависимости:

```powershell
Set-Location "<REPO>\llm_p"; python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### macOS / Linux

```bash
cd "<REPO>/llm_p" && python3 -m pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite "pydantic[email]" pydantic-settings "python-jose[cryptography]" cryptography "passlib[bcrypt]" httpx python-multipart greenlet "bcrypt==4.3.0" ruff && python3 -c "import fastapi, uvicorn, sqlalchemy; print('DEPS_OK')"
```

```bash
cd "<REPO>/llm_p" && python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

При необходимости замените `python3` на `python` (интерпретатор 3.11+).

## Быстрый старт

Дальше команды выполняйте из каталога **`llm_p/`** (там же `pyproject.toml` и каталог `app`).

1. Перейти в каталог приложения и скопировать пример переменных окружения:

   ```powershell
   cd llm_p
   copy .env.example .env
   ```

   (POSIX: `cd llm_p && cp .env.example .env`.)

2. Отредактировать **`.env`** в этом же каталоге: задать `JWT_SECRET`, при необходимости `OPENROUTER_API_KEY` и прочие поля из примера.

3. Установить зависимости через **uv** (**рабочий каталог — `llm_p/`**):

   ```text
   uv sync
   ```

   При необходимости обновить окружение после изменений в `pyproject.toml` — снова **`uv sync`**.

   **Формулировка из критериев оценки (эквивалент установки из `pyproject.toml`):** из **`llm_p/`** выполните **`uv venv`**, затем **`uv pip compile pyproject.toml -o reqs.txt`** и **`uv pip install -r reqs.txt`**, затем проверку импортов как в **шаге 4** (`uv run python -c "… DEPS_OK"`).

   **Запасной путь (без uv):** см. раздел **«Запасной путь: pip»** выше или выполните вручную `python -m pip install …` по списку из **`pyproject.toml`**.

4. Запуск приложения (**рабочий каталог — `llm_p/`**):

   ```text
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Только если ставили зависимости через **pip** без uv: активируйте своё окружение и выполните `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.

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

## Приёмка: скриншоты (`screenshots/` в корне репозитория)

Изображения ниже встроены из папки **`screenshots/`** в этом же репозитории. По критериям курса на скриншоте регистрации должен быть виден email в формате **`student_surname@email.com`** (или та же схема с вашей фамилией и доменом `@email.com` — уточните у преподавателя).

Перед публикаацией замажьте чувствительные части JWT и ключей провайдера.

### Обязательные по методичке

#### 1. Регистрация — `POST /auth/register`

![Регистрация: POST /auth/register, email student_surname@email.com](screenshots/01-register.png)

#### 2. Логин и JWT — `POST /auth/login`

![Логин и ответ с access_token](screenshots/02-login-token.png)

#### 3. Авторизация в Swagger — кнопка Authorize

![Swagger UI: Authorize, Bearer-токен](screenshots/03-swagger-authorize.png)

#### 4. Чат — `POST /chat`

![Успешный POST /chat](screenshots/04-chat-post.png)

#### 5. История — `GET /chat/history`

![GET /chat/history, список сообщений](screenshots/05-history-get.png)

#### 6. Очистка истории — `DELETE /chat/history`

![DELETE /chat/history](screenshots/06-history-delete.png)

### Дополнительные скриншоты (другие ракурсы)

![Обзор OpenAPI / Swagger](screenshots/00-openapi-swagger-overview.png)

![POST /chat: тело запроса в редакторе](screenshots/04a-chat-request-body-editor.png)

![POST /chat: документация ответа](screenshots/04b-chat-endpoint-response-docs.png)

![GET /chat/history: параметры](screenshots/05a-chat-history-parameters.png)

![GET /chat/history: выполнение запроса](screenshots/05b-chat-history-execute-request.png)

![GET /chat/history: альтернативный ответ](screenshots/05c-chat-history-response-alt.png)

![GET /auth/me: профиль](screenshots/07-auth-me-profile.png)

![GET /auth/me: пример схемы](screenshots/07a-auth-me-schema-example.png)

![История пуста после DELETE](screenshots/08-chat-history-empty-after-delete.png)

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

Из каталога **`llm_p/`** (после **`uv sync`**):

```text
cd llm_p
uv run ruff check app
```

Ожидаемый результат: **`All checks passed!`**. Если используете только **pip**, запустите `python -m ruff check app` в том же окружении, куда ставили зависимости.
