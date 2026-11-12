# Event Ticketing API

Серверное приложение для продажи билетов на мероприятия (вариант 6).
Стек: Python 3.11+, FastAPI. PostgreSQL, Alembic и Docker запланированы
для следующих лабораторных.

ЛР1 — архитектура в `ARCHITECTURE.md`, ЛР2 — контракт в `openapi.yaml`.
ЛР3 — базовый каркас, конфигурация и `GET /api/v1/health`.

## Структура

```text
.
├── cmd/
│   └── app/
│       └── main.py          # Точка входа, сборка приложения и запуск
├── internal/
│   ├── config/
│   │   └── settings.py      # Настройки из .env и окружения
│   ├── controller/
│   │   └── health.py        # Transport / HTTP: запрос и JSON-ответ
│   ├── service/
│   │   └── health.py        # Логика проверки состояния
│   └── repository/          # Слой БД для следующих лабораторных
├── docs/diagrams/           # Диаграммы из ЛР1
├── .env.example
├── .gitignore
├── requirements.txt        # Зависимости Python
├── openapi.yaml
├── ARCHITECTURE.md
└── README.md
```

Контроллер вызывает сервис. Сервис не зависит от FastAPI и HTTP.
Репозиторий пока пустой: проверка работы процесса не требует базы данных.
Файл `.gitkeep` сохраняет пустой каталог в Git.

## Запуск (PowerShell, из корня проекта)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe cmd/app/main.py
```

Если `.venv` и `.env` уже созданы, достаточно последней команды.
Существующий `.env` не перезаписывать. Остановка — `Ctrl+C`.

Открыть в браузере:

- [Health-check](http://127.0.0.1:8000/api/v1/health).
- [Swagger UI](http://127.0.0.1:8000/docs).

Или проверить статус и заголовки в другом терминале:

```powershell
curl.exe -i http://127.0.0.1:8000/api/v1/health
```

Ожидается `200 OK`, `Content-Type: application/json` и ответ:

```json
{
  "status": "pass",
  "app": "Event Ticketing API",
  "version": "1.0.0",
  "environment": "development",
  "uptime": 12.345
}
```

`uptime` — время работы приложения в секундах, при перезапуске отсчёт начинается заново.
Остальные операции из `openapi.yaml` пока только спроектированы.

## Конфигурация

В `.env.example` указан шаблон:

```dotenv
APP_NAME="Event Ticketing API"
APP_VERSION=1.0.0
APP_ENV=development
HTTP_HOST=127.0.0.1
HTTP_PORT=8000
```

`.env` читается из корня проекта; переменные окружения процесса имеют приоритет.
`APP_ENV`: `development`, `test`, `production`. Порт: от 1 до 65535.
Изменить настройки можно без правки кода, после изменения перезапустить сервер.
`.env`, `.venv` и файлы IDE исключены через `.gitignore`.
