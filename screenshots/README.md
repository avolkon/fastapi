# Скриншоты для отчёта

Сюда сохраните PNG по списку в **`llm_p/README.md`** (раздел про скриншоты). В кадрах с формами виден email

`student_surname@email.com`

(можно использовать ваш реальный студенческий ящик в том же формате имени файла методички).

Не выкладывайте необрезанные секретные токены и ключи провайдеров.

## Имена файлов (текущий набор)

**Обязательные по методичке** (`llm_p/README.md`):

- **`01-register.png`** — `POST /auth/register`, успех **201**
- **`02-login-token.png`** — `POST /auth/login`, **200**, `access_token`
- **`03-swagger-authorize.png`** — окно **Authorize**, статус **Authorized**
- **`04-chat-post.png`** — `POST /chat`, **200**, ответ с `answer`
- **`05-history-get.png`** — `GET /chat/history`, **200**, пары user/assistant
- **`06-history-delete.png`** — `DELETE /chat/history` (запрос / документация эндпоинта)

**Дополнительно** (другие ракурсы): `00-openapi-swagger-overview.png`, `04a-…`, `04b-…`, `05a-…`, `05b-…`, `05c-…`, `07-auth-me-profile.png`, `07a-auth-me-schema-example.png`, `08-chat-history-empty-after-delete.png` — точные имена см. в папке.
