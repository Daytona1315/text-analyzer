from src.app.utils.logging import log
from src.app.consts import ExceptionMessages


class BaseAppException(Exception):
    default_message = ExceptionMessages.default_exception_msg
    default_status = 500

    def __init__(
        self,
        message: str = None,
        status: int = None,
        exception: Exception = None,
    ):
        self.message = message or self.__class__.default_message
        self.status = status or self.__class__.default_status
        self.exception = exception

        if exception:
            log.exception(
                f"{self.__class__.__name__} raised.",
                exc_info=exception,
            )
        else:
            log.error(f"{self.__class__.__name__} raised.")

        super().__init__(self.message)


class FileException(BaseAppException):
    default_message = ExceptionMessages.file_exception_msg


class TextAnalysisException(BaseAppException):
    default_message = ExceptionMessages.analysis_exception_msg


class CSVWriteException(BaseAppException):
    default_message = ExceptionMessages.csv_exception_msg


class RedisException(BaseAppException):
    default_message = ExceptionMessages.redis_exception_msg


class AnalyticsException(BaseAppException):
    default_message = ExceptionMessages.analytics_exception_msg


class NLPException(BaseAppException):
    default_message = ExceptionMessages.nlp_exception_msg

class LangException(BaseAppException):
    default_message = ExceptionMessages.lang_exception_msg