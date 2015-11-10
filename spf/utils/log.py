#!/usr/bin/env python
import logging
import sys
DEFAULT_LEVEL = 'noset'


def get_logger(name, filename=None, level=DEFAULT_LEVEL):
    logger = logging.getLogger(name)
    if filename is None:
        logger.addHandler(logging.StreamHandler(sys.stderr))
    else:
        logger.addHandler(logging.StreamHandler(open(filename, "w")))

    if level == "error":
        logger.setLevel(logging.ERROR)
    elif level == "warn":
        logger.setLevel(logging.WARN)
    elif level == "info":
        logger.setLevel(logging.INFO)
    elif level == "debug":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.DEBUG)

    return logger
