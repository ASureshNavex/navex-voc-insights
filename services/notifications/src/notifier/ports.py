from typing import Protocol

import boto3
from botocore.config import Config


class Mailer(Protocol):
    def send(self, to: str, subject: str, text: str, html: str) -> None: ...


class SesMailer:
    def __init__(self, sender: str, region: str) -> None:
        self._sender = sender
        self._client = boto3.client(
            "sesv2", region_name=region, config=Config(connect_timeout=3, read_timeout=10)
        )

    def send(self, to: str, subject: str, text: str, html: str) -> None:
        self._client.send_email(
            FromEmailAddress=self._sender,
            Destination={"ToAddresses": [to]},
            Content={
                "Simple": {
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": text}, "Html": {"Data": html}},
                }
            },
        )
