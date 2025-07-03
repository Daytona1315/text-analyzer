class BaseAppException(Exception):

    default_message: int = "Something went"

    def __init__(
            self,
            message: str = "Something went wrong. Please, try later",
            status_code: int = 500,
    ):
        super().__init__(message, status_code)
        self.message = message
        self.status_code = status_code


class FileException(BaseAppException):
    def __init__(
            self,
            status_code=500,
            message="Failed to process the file. Please, try later."
    ):
        super().__init__(message, status_code)


class TextAnalysisException(BaseAppException):
    def __init__(
            self,
            status_code=500,
            message="Failed to run the analysis. Please, try later."
    ):
        super().__init__(message, status_code)


class CSVWriteException(BaseAppException):
    def __init__(
            self,
            status_code=500,
            message="Failed to write .csv file. Please, try later."
    ):
        super().__init__(message, status_code)


class RedisException(BaseAppException):
    def __init__(
            self,
            message="Redis error",
            status_code=500,
    ):
        super().__init__(message, status_code)


class FunctionsException(BaseAppException):
    def __init__(
            self,
            status_code=500,
            message="Failed to process. Please, try later."
    ):
        super().__init__(message, status_code)


class NLPException(BaseAppException):
    def __init__(
            self,
            status_code=500,
            message="Failed to load necessary components. Please, try later."
    ):
        super().__init__(message, status_code)
