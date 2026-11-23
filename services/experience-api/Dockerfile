# Build from the repository root: docker build -f services/experience-api/Dockerfile .
FROM python:3.13-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /bin/uv
WORKDIR /repo
COPY pyproject.toml uv.lock ./
COPY packages/voc-data packages/voc-data
COPY services/experience-api services/experience-api
RUN uv sync --frozen --no-dev --package experience-api --no-editable

FROM python:3.13-slim
RUN useradd --system --uid 10001 voc
COPY --from=build /repo/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
USER voc
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
