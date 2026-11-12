# Event Ticketing API

REST API для продажи билетов на мероприятия. Индивидуальный сквозной проект
по дисциплине «Разработка серверных приложений» (вариант 6).

Организатор создаёт площадки и мероприятия, зрители покупают билеты на свободные
места. Проектируемый сервер исключает двойную продажу одного места.

В лабораторных №1–2 подготовлены архитектура и контракт API. В лабораторной №3
реализованы каркас приложения, конфигурация и публичный `GET /api/v1/health`.
Продажа билетов, авторизация и база данных будут реализованы в следующих работах.

## Стек

- Python 3.11+ (локально также проверено на Python 3.14), FastAPI, Uvicorn.
- `pydantic-settings` — чтение и валидация конфигурации.
- PostgreSQL 16, Alembic, Docker и Docker Compose — планируемые компоненты следующих работ.

## Запуск в Windows (PowerShell)

Выполнить из корня репозитория:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m app
```

Если `.env` уже существует, шаг копирования пропустить, чтобы сохранить настройки.
Активация виртуального окружения не требуется.

На Linux/macOS: создать окружение через `python3 -m venv .venv`, использовать
`.venv/bin/python` вместо `.\.venv\Scripts\python.exe` и `cp .env.example .env`.

По умолчанию сервер доступен на `http://127.0.0.1:8000`:

- Health-check: <http://127.0.0.1:8000/api/v1/health>.
- Swagger UI реализованных маршрутов: <http://127.0.0.1:8000/docs>.
- Сгенерированная схема реализованного API: <http://127.0.0.1:8000/openapi.json>.
- Полный планируемый контракт из ЛР2 с добавленным health-check: [`openapi.yaml`](openapi.yaml).

Остановить сервер: `Ctrl+C` в терминале запуска.

## Конфигурация

Образец находится в [`.env.example`](.env.example):

```dotenv
APP_NAME="Event Ticketing API"
APP_VERSION=1.0.0
APP_ENV=development
HTTP_HOST=127.0.0.1
HTTP_PORT=8000
```

`APP_ENV` принимает `development`, `test` или `production`, `HTTP_PORT` — целое
число от 1 до 65535. Некорректные значения останавливают запуск с ошибкой валидации.
Файл `.env` ищется относительно корня проекта, независимо от текущего каталога.
Переменные окружения процесса имеют приоритет над `.env`, затем используются
значения по умолчанию. После изменения конфигурации сервер нужно перезапустить.

Например, запуск на другом порту в PowerShell:

```powershell
$env:HTTP_PORT = "8080"
.\.venv\Scripts\python.exe -m app
# После остановки сервера убрать переопределение:
Remove-Item Env:HTTP_PORT
```

Локальный `.env`, виртуальное окружение, кэши и файлы IDE исключены через
`.gitignore`. В репозиторий попадает только `.env.example` без секретов.

## Проверка health-check

При работающем сервере выполнить в другом терминале:

```powershell
curl.exe -i http://127.0.0.1:8000/api/v1/health
```

Ожидается `200 OK`, `Content-Type: application/json` и JSON:

```json
{
  "status": "pass",
  "app": "Event Ticketing API",
  "version": "1.0.0",
  "environment": "development",
  "uptime": 12.345
}
```

`uptime` — время работы приложения в секундах; значение меняется при каждом запросе.
Токен и подключение к PostgreSQL для этого маршрута не требуются.

## Структура репозитория

```text
.
├── app/
│   ├── __main__.py           # Запуск Uvicorn с настройками из окружения
│   ├── main.py               # Сборка приложения и передача зависимостей
│   ├── config/settings.py    # Конфигурация из .env и окружения
│   ├── controller/health.py  # HTTP-обработчик и схема ответа
│   ├── service/health.py     # Сценарий проверки работоспособности
│   ├── domain/health.py      # Доменная модель результата
│   └── repository/           # Слой доступа к данным для следующих работ
├── tests/                    # Проверки health-check и конфигурации
├── docs/
│   ├── lab3.md               # Порядок демонстрации и контрольные вопросы
│   └── diagrams/             # Диаграммы из ЛР1
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── ARCHITECTURE.md
├── openapi.yaml
└── README.md
```

Запрос проходит через `Controller → Service → Domain`. Когда появятся сценарии
работы с данными, сервисы будут обращаться к репозиториям через интерфейсы.

## Автоматические проверки

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Проверяются публичный JSON-ответ health-check, передача настроек в приложение,
неубывающее время работы, чтение `.env`, приоритет окружения и валидация порта.

## Документация

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — описание проекта, роли, Use Cases, C4, ER-диаграмма и слои приложения.
- [`openapi.yaml`](openapi.yaml) — спецификация REST API.
- [`docs/lab3.md`](docs/lab3.md) — сдача лабораторной №3 и ответы на контрольные вопросы.
