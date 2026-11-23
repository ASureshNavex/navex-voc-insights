from ingestion.models import AccountFeedback, SourceAccount


def match_feedback(
    accounts: list[SourceAccount], feedback: list[AccountFeedback]
) -> tuple[list[AccountFeedback], int]:
    """Keep feedback whose Salesforce account ID is in the account master; count the rest."""
    known = {account.sfdc_account_id for account in accounts}
    matched = [item for item in feedback if item.sfdc_account_id in known]
    unmatched_records = sum(
        item.feedback_count for item in feedback if item.sfdc_account_id not in known
    )
    return matched, unmatched_records
