# Build from the repository root: docker build -f services/account-scoring-agent/Dockerfile .
FROM python:3.13-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /bin/uv
WORKDIR /repo
COPY pyproject.toml uv.lock ./
COPY packages/voc-data packages/voc-data
COPY services/account-scoring-agent services/account-scoring-agent
RUN uv sync --frozen --no-dev --package account-scoring-agent --no-editable

FROM python:3.13-slim
RUN useradd --system --uid 10001 voc
COPY --from=build /repo/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
USER voc
EXPOSE 8080
CMD ["python", "-m", "account_scoring_agent.entrypoint"]
