class FileProcessingError(Exception):
    """
    Just a custom exception for easier delivery to front-end
    """
    def __init__(self, message):
        self.message = message
