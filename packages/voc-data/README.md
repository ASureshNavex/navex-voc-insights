# voc-data

The serving store schema shared by the Experience API, the ingestion task, the Account Scoring Agent and the notification task.

| File | Purpose |
|---|---|
| `src/voc_data/models.py` | SQLAlchemy tables. Meanings are in `docs/02-architecture/lld.md`, section 3.2 |
| `src/voc_data/enums.py` | Rating, role, data scope and status values used across services |
| `src/voc_data/scope.py` | `scope_filter`: the one place a data scope becomes a SQL condition |
| `alembic/` | Migrations for PostgreSQL |

## Changing the schema

```bash
docker compose up -d postgres
cd packages/voc-data
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "add <what>"
uv run alembic upgrade head
```

Review every generated revision before committing it. Set `DATABASE_URL` to point at another database.
