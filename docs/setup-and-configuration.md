# Setup and Configuration

This guide documents how to run and configure the FAQ bot in local and Docker
environments.

## Prerequisites

- Python 3.12
- Poetry
- PostgreSQL (with `pgvector` extension)
- Redis
- Telegram bot token
- Embedding API credentials

## Local Setup

### 1. Install dependencies

```bash
poetry install
```

### 2. Configure environment

```bash
cp .env.example .env
```

Set required values in `.env`:

- `BOT__TOKEN`
- DB connection (`DB__NAME`, `DB__USER`, `DB__PASSWORD`, `DB__HOST`)
- Redis connection (`REDIS__HOST`, `REDIS__PASSWORD`)
- Embedding API values (`REQUESTS__FOLDER_ID`, `REQUESTS__IAM_TOKEN`)
- `DB_SCHEMA__QUESTION_EMBEDDING_DIM`

### 3. Start infra

Option A: use local services.

Option B: start infra only with Docker:

```bash
docker compose up -d db redis
```

### 4. Run the bot

```bash
poetry run python -m app.main
```

## Docker Setup (Full Stack)

```bash
cp .env.example .env
docker compose up --build
```

The compose stack includes:

- `db` (`pgvector/pgvector:pg17`)
- `redis` (`redis:7.4-alpine`)
- `bot` (from `app/Dockerfile`)

## Environment Variables

### Path Overrides

- `PATHS__LOGGING` (default `./config/logging.yml`)
- `PATHS__CONSTANTS` (default `./config/constants.yml`)
- `PATHS__MESSAGES` (default `./config/messages.yml`)
- `PATHS__COMMANDS` (default `./config/commands.yml`)
- `PATHS__REQUESTS` (default `./config/requests.yml`)

### Bot

- `BOT__TOKEN` (required)
- `BOT__ADMINS` (default `[]`)

### Database

- `DB__NAME` (required)
- `DB__USER` (required)
- `DB__PASSWORD` (required)
- `DB__HOST` (required)

### Redis

- `REDIS__HOST` (required)
- `REDIS__PASSWORD` (required)
- `REDIS__LONG_TTL` (default `86400`)
- `REDIS__SHORT_TTL` (default `300`)

### Questions/Search

- `QUESTIONS__SIMILAREST_THRESHOLD` (default `0.7`)
- `QUESTIONS__SIMILAR_THRESHOLD` (default `0.4`)
- `QUESTIONS__MAX_SIMILAR_AMOUNT` (default `7`)
- `QUESTIONS__MAX_POPULAR_AMOUNT` (default `7`)
- `QUESTIONS__MAX_AMOUNT` (default `7`)

Validation rule:

- `MAX_SIMILAR_AMOUNT <= MAX_AMOUNT`
- `MAX_POPULAR_AMOUNT <= MAX_AMOUNT`

### Rate Limiting

- `RATE_LIMIT__ENABLED` (default `true`)
- `RATE_LIMIT__MAX_REQUESTS` (default `5`)
- `RATE_LIMIT__WINDOW` (default `10`)
- `RATE_LIMIT__SKIP_ADMIN` (default `true`)

### Embeddings Request Variables

- `REQUESTS__FOLDER_ID` (required by example `config/requests.yandex.yml`)
- `REQUESTS__IAM_TOKEN` (required by example `config/requests.yandex.yml`)

### DB Schema Constraints

- `DB_SCHEMA__QUESTION_TEXT_MAX_LEN` (default `384`)
- `DB_SCHEMA__ANSWER_TEXT_MAX_LEN` (default `384`)
- `DB_SCHEMA__QUESTION_EMBEDDING_DIM` (required)

## YAML Configuration Files

Files with the `.example.yml` suffix fully match the built-in default values used
by the application. They are useful as reference templates and as a starting
point for customization.

### `config/requests.yml` (required)

Defines how embeddings are requested and parsed:

- HTTP method/url/headers/body template
- `text_path`: where question text is injected
- `embedding_path`: where embedding vector is read from response

The app requires the `embedding` template section.

Has provided the example embedding request template for the Yandex Cloud API. You can use it as a
reference when configuring `config/requests.yml` for Yandex Cloud.

### `config/messages.yml` (optional)

Overrides user/admin texts, parse mode, formatting, and button labels.

See [messages.md](messages.md).

Reference defaults: `config/messages.example.yml`

### `config/constants.yml` (optional)

Provides constant placeholders used in messages and commands.

Reference defaults: `config/constants.example.yml`

### `config/commands.yml` (optional)

Adds dynamic public commands.

See [commands.md](commands.md).

Reference defaults: `config/commands.example.yml`

### Logging config (`config/logging.*.yml`)

Set via `PATHS__LOGGING`.
Supports stdout/file/telegram sinks, duplicate suppression, and throttling.

## Startup Sequence

At boot (`app/main.py`):

1. Logging setup
2. Table creation (`Base.metadata.create_all`)
3. Schema constraint reconciliation
4. Admin role sync from `BOT__ADMINS`
5. Middleware registration
6. Router registration
7. Polling start

## Important Operational Notes

- Admin sync promotes users already present in DB; new admins usually need to
  run `/start` first, then bot restart/sync.
- Reducing question/answer varchar limits fails if existing rows exceed limits.
- Changing embedding dimension triggers automatic vector migration:
  - empty `questions` table: direct type change
  - non-empty table: embeddings are recomputed for all rows

## Troubleshooting

- Startup error about missing embedding settings:
  check `REQUESTS__*` env values and `config/requests.yml`.
- `vector` type errors:
  ensure `init.sql` ran and extension exists in PostgreSQL.
- Admin commands not available:
  verify `BOT__ADMINS`, user presence in DB, and role sync.
