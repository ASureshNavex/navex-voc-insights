# Build from the repository root: docker build -f services/ingestion/Dockerfile .
FROM python:3.13-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /bin/uv
WORKDIR /repo
COPY pyproject.toml uv.lock ./
COPY packages/voc-data packages/voc-data
COPY services/ingestion services/ingestion
RUN uv sync --frozen --no-dev --package ingestion --no-editable

FROM python:3.13-slim
RUN useradd --system --uid 10001 voc
COPY --from=build /repo/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
USER voc
CMD ["python", "-m", "ingestion"]
