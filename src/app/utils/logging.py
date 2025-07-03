import logging


logger = logging.getLogger("TextAnalyzer")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)
console_handler.setFormatter(formatter)

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
