"""Entry point of the ECS task: `python -m notifier alerts --run-id <uuid>`."""

import argparse
import asyncio
import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from notifier.alerts import send_status_alerts
from notifier.config import get_settings
from notifier.ports import SesMailer


async def _alerts(run_id: UUID) -> None:
    settings = get_settings()
    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    mailer = SesMailer(settings.sender_address, settings.aws_region)
    try:
        async with async_sessionmaker(engine, expire_on_commit=False)() as session:
            sent = await send_status_alerts(session, mailer, run_id, settings.app_base_url)
        logging.getLogger(__name__).info("Alert emails sent: %d", sent)
    finally:
        await engine.dispose()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(prog="notifier")
    jobs = parser.add_subparsers(dest="job", required=True)
    alerts = jobs.add_parser("alerts", help="Send change-of-status alerts for a published run")
    alerts.add_argument("--run-id", type=UUID, required=True)
    jobs.add_parser("digests", help="Send the digests that are due (unit NTF-02)")
    args = parser.parse_args()

    if args.job == "alerts":
        asyncio.run(_alerts(args.run_id))
    else:
        parser.error("The digests job is not built yet: unit NTF-02.")


if __name__ == "__main__":
    main()
