import logging
from logging.handlers import TimedRotatingFileHandler

import sys
import os

FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)-22s - %(levelname)-8s - %(message)s", "%Y-%m-%d %H:%M:%S")
LOG_FILE = f"{os.environ.get('temp')}\AutoClicker\logs\my_app.log"


def set_file(file_name):
    LOG_FILE = file_name


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    # better to have too much log than not enough
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger