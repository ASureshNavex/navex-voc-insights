"""Account master from Snowflake. One read per run, key-pair authentication over PrivateLink."""

import asyncio
from typing import Any

import snowflake.connector

from ingestion.models import SourceAccount

# Field name here -> column in the NAVEX view. Column names are confirmed with the NAVEX data team.
COLUMNS: dict[str, str] = {
    "sfdc_account_id": "SFDC_ACCOUNT_ID",
    "name": "ACCOUNT_NAME",
    "segment": "SEGMENT",
    "team": "CXM_TEAM",
    "region": "REGION",
    "arr": "ARR",
    "next_renewal_date": "NEXT_RENEWAL_DATE",
    "cxm_owner_upn": "CXM_OWNER_EMAIL",
    "ae_owner_upn": "AE_OWNER_EMAIL",
    "exec_sponsor": "EXEC_SPONSOR",
    "super_product_family": "SUPER_PRODUCT_FAMILY",
    "churn_score": "CHURN_SCORE",
    "churn_score_as_of": "CHURN_SCORE_AS_OF",
    "nps_category": "NPS_CATEGORY",
    "nps_date": "NPS_DATE",
    "issue_status": "ISSUE_STATUS",
}


class SnowflakeAccountSource:
    def __init__(
        self, account: str, user: str, private_key: bytes, warehouse: str, view: str
    ) -> None:
        self._connect_args: dict[str, Any] = {
            "account": account,
            "user": user,
            "private_key": private_key,
            "warehouse": warehouse,
            "login_timeout": 30,
            "network_timeout": 120,
        }
        self._view = view

    def _read(self) -> list[SourceAccount]:
        select_list = ", ".join(f"{column} AS {field}" for field, column in COLUMNS.items())
        with snowflake.connector.connect(**self._connect_args) as connection:
            cursor = connection.cursor(snowflake.connector.DictCursor)
            # IDENTIFIER(%s) binds the view name; nothing is interpolated into the statement.
            cursor.execute(f"SELECT {select_list} FROM IDENTIFIER(%s)", (self._view,))  # noqa: S608
            rows = cursor.fetchall()
        return [
            SourceAccount.model_validate({key.lower(): value for key, value in row.items()})
            for row in rows
        ]

    async def fetch_accounts(self) -> list[SourceAccount]:
        return await asyncio.to_thread(self._read)
