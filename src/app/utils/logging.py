import logging
from colorlog import ColoredFormatter


LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

log = logging.getLogger("TextAnalyzer")
log.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = ColoredFormatter(LOGFORMAT)
console_handler.setFormatter(formatter)

log.addHandler(console_handler)
