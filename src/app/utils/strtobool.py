from src.app.utils.logging import log
from src.app.utils.custom_exceptions import BaseAppException


def strtobool(val: str) -> bool:
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        log.critical("STRTOBOOL ERROR")
        raise BaseAppException(f"Invalid truth value: {val}. Check config.")
