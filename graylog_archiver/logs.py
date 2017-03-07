import logging
import sys


def configure_logs():
    formater = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # Root Logger
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formater)
    logger.addHandler(console_handler)
