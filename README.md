# FAQ Bot

Telegram FAQ bot with semantic search, pgvector-backed similarity lookup, and an
admin UI for managing users and questions.

## Features

- Semantic question search using external embeddings.
- PostgreSQL + pgvector storage for questions and embeddings.
- Redis-backed temporary state with separate short and long TTL scopes.
- Admin workflows for question/user CRUD, pagination, bans, and diagnostics.
- Runtime text customization via YAML (`messages`, `constants`, `commands`).
- Configurable rate limiting middleware.

## Quick Start (Local)

### 1. Prerequisites

- Python 3.12
- Poetry
- PostgreSQL with `vector` extension (`pgvector`)
- Redis

### 2. Install dependencies

```bash
poetry install
```

### 3. Configure environment

```bash
cp .env.example .env
```

Configure your embedding API request format in `config/requests.yml` and update
`.env` with real values for:

- Telegram bot token
- Database and Redis connection settings
- Embedding provider credentials
- Embedding vector dimension (`DB_SCHEMA__QUESTION_EMBEDDING_DIM`)

### 4. Start dependencies (if needed)

```bash
docker compose up -d db redis
```

### 5. Run bot

```bash
poetry run python -m app.main
```

## Quick Start (Docker Compose)

```bash
cp .env.example .env
docker compose up --build
```

This starts `db`, `redis`, and `bot`.

## Command Reference

### Public

- `/start` - welcome message and registration in users table.
- `/ask <question>` - semantic FAQ search.
- Any plain text message - treated as a question.
- Extra public commands from `config/commands.yml`.

### Admin

- `/settings` - open admin UI (users/questions CRUD + list).
- `/ban <telegram_id>`
- `/unban <telegram_id>`
- `/state ...` - inspect and mutate FSM state.

Admin routes require `admin` role and are controlled by `BOT__ADMINS` + DB role
sync at startup.

## Documentation

- [Setup and Configuration](docs/setup-and-configuration.md)
- [Architecture](docs/architecture.md)
- [Messages Customization](docs/messages.md)
- [Custom Commands](docs/commands.md)
