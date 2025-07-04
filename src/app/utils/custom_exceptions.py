from src.app.utils.logging import logger


class BaseAppException(Exception):
    default_message = "Something went wrong. Please, try later."
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
            logger.exception(
                f"{self.__class__.__name__} raised.",
                exc_info=exception,
            )
        else:
            logger.error(f"{self.__class__.__name__} raised.")

        super().__init__(self.message)


class FileException(BaseAppException):
    default_message = "Failed to process the file. Please, try later."


class TextAnalysisException(BaseAppException):
    default_message = "Failed to run the analysis. Please, try later."


class CSVWriteException(BaseAppException):
    default_message = "Failed to write .csv file. Please, try later."


class RedisException(BaseAppException):
    default_message = "Operation not found. Please, try later."


class FunctionsException(BaseAppException):
    default_message = "Failed to process. Please, try later."


class NLPException(BaseAppException):
    default_message = "Failed to load necessary components. Please, try later."
