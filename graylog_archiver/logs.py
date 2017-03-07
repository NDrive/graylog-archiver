import logging
import sys


def create_logger():
    formater = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    logger = logging.getLogger('graylog_archiver')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formater)
    logger.addHandler(console_handler)

    return logger
