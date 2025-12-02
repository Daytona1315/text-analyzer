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


class ExceptionMessages(StrEnum):
    """Exception messages"""

    default_exception_msg = "Something went wrong. Please, try later."
    file_exception_msg = "Failed to process the file. Please, try later."
    analysis_exception_msg = "Failed to run the analysis. Please, try later."
    csv_exception_msg = "Failed to process the .csv file. Please, try later."
    redis_exception_msg = "Operation not found. Please, try again later."
    analytics_exception_msg = "Failed to run the analytics. Please, try again."
    nlp_exception_msg = "Failed to load necessary components. Please, try later."
    lang_exception_msg = "Language is undefined or not supported."
