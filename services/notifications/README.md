# Notification task

An ECS Fargate task started by an EventBridge rule on `run.published`, and by EventBridge Scheduler for digests.

```bash
cp .env.example .env
uv run python -m notifier alerts --run-id <run uuid>
```

| Job | Status |
|---|---|
| `alerts`: one batched email per owner per run, marked "Action needed" or "FYI", never sent twice | Built and tested |
| `digests`: scheduled digests by audience | Unit NTF-02 |
| Knowledge hub decision emails | Unit NTF-03 |

Mail goes through the `Mailer` port in `ports.py`. `SesMailer` is the adapter in place; a Microsoft 365 adapter can replace it without touching `alerts.py`. HTML templates are escaped automatically.
