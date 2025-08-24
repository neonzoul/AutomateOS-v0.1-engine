# Draft

### **AutomateOS Engine: A lightweight, plugin-driven workflow engine. Built to be extended.**

A clear separation of concerns is at the heart of this design. With distinct layers for the API, engine, database models, and schemas, the codebase is crafted to be easy to understand, maintain, and contribute to.

At its core, the engine is a lean **Orchestrator** designed to dynamically load and run any node, providing maximum flexibility to build the automations.

## Run with Docker

The project ships with a complete Docker setup: FastAPI API, RQ worker, Redis, and PostgreSQL.

-   Build and start everything:

```powershell
docker compose up -d --build
```

-   Open the API docs: http://localhost:8000/docs

-   Tail logs:

```powershell
docker compose logs -f api
docker compose logs -f worker
```

-   Stop the stack:

```powershell
docker compose down
```

Environment used in containers:

-   DATABASE_URL=postgresql+psycopg2://automateos:automateos@db:5432/automateos_db
-   REDIS_URL=redis://redis:6379/0

## Local development (Windows)

Local dev defaults to SQLite and a local Redis unless you set env vars.

-   Install deps:

```powershell
pip install -r .\requirement.txt
```

-   Run API:

```powershell
uvicorn main:app --reload
```

-   Run worker (listens on default queue):

```powershell
python worker.py
```

To use Postgres locally, set DATABASE_URL (and install ps ycopg2-binary or libpq tooling). Otherwise, stick with SQLite (default).

## Notes

-   The Docker images install dependencies from `requirements.txt` (includes psycopg2-binary).
-   Local development uses `requirement.txt` which omits psycopg2-binary to avoid Windows build issues.
-   Code reads configuration from env:
    -   `DATABASE_URL` in `app/db/session.py` (falls back to local SQLite file)
    -   `REDIS_URL` in `app/core/queue.py` and `worker.py` (falls back to `redis://localhost:6379/0`)

## Troubleshooting

-   Docker compose warning about `version` key: removed; modern Compose ignores it.
-   If `psycopg2-binary` fails on Windows during local installs, ensure you’re installing from `requirement.txt` (without psycopg2-binary) or install Postgres client tools providing `pg_config`.
