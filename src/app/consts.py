from enum import StrEnum


class SessionKeys(StrEnum):
    """Keys for flask.session"""

    USER_ID = "user_id"
    ACTIVE_ANALYSIS_ID = "active_analysis_id"
    INIT = "init"


class HtmxEvents(StrEnum):
    """Events for HX-Trigger header"""

    HISTORY_UPDATE = "historyNeedsUpdate"


class TaskStatus(StrEnum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    REVOKED = "REVOKED"
    PENDING = "PENDING"
    STARTED = "STARTED"
    RETRY = "RETRY"
