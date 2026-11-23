from enum import StrEnum


class Rating(StrEnum):
    RED = "R"
    YELLOW = "Y"
    GREEN = "G"


class Role(StrEnum):
    CXM = "CXM"
    CXM_LEADERSHIP = "CXM_LEADERSHIP"
    ACCOUNT_EXECUTIVE = "ACCOUNT_EXECUTIVE"
    ELT = "ELT"
    VOC_ADMIN = "VOC_ADMIN"


class DataScope(StrEnum):
    OWN_BOOK = "OWN_BOOK"
    TEAM = "TEAM"
    REGION = "REGION"
    ALL = "ALL"


class Ownership(StrEnum):
    """Which account ownership field a role's scope follows."""

    CXM = "cxm"
    ACCOUNT_EXECUTIVE = "ae"


class RunStatus(StrEnum):
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class DocumentStatus(StrEnum):
    DRAFT = "DRAFT"
    UPLOADING = "UPLOADING"
    CHECKING = "CHECKING"
    REJECTED_BY_CHECK = "REJECTED_BY_CHECK"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    PUBLISHED = "PUBLISHED"
    DECLINED = "DECLINED"
    WITHDRAWN = "WITHDRAWN"


class DeliveryStatus(StrEnum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"


class Urgency(StrEnum):
    ACTION_NEEDED = "ACTION_NEEDED"
    FYI = "FYI"
