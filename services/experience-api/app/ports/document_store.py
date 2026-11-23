"""Knowledge hub files. The API issues short-lived URLs and never handles file bytes."""

import asyncio
from typing import Protocol

import boto3
from botocore.config import Config

UPLOAD_URL_SECONDS = 600
DOWNLOAD_URL_SECONDS = 120


class DocumentStore(Protocol):
    async def upload_url(self, key: str, content_type: str, size_bytes: int) -> str: ...

    async def download_url(self, key: str) -> str: ...


class S3DocumentStore:
    def __init__(self, bucket: str, region: str) -> None:
        self._bucket = bucket
        self._s3 = boto3.client(
            "s3",
            region_name=region,
            config=Config(connect_timeout=3, read_timeout=10, signature_version="s3v4"),
        )

    async def upload_url(self, key: str, content_type: str, size_bytes: int) -> str:
        # Signing the length and type means S3 rejects a different or larger file.
        params = {
            "Bucket": self._bucket,
            "Key": key,
            "ContentType": content_type,
            "ContentLength": size_bytes,
        }
        return await asyncio.to_thread(
            self._s3.generate_presigned_url,
            "put_object",
            Params=params,
            ExpiresIn=UPLOAD_URL_SECONDS,
        )

    async def download_url(self, key: str) -> str:
        return await asyncio.to_thread(
            self._s3.generate_presigned_url,
            "get_object",
            Params={"Bucket": self._bucket, "Key": key},
            ExpiresIn=DOWNLOAD_URL_SECONDS,
        )
