import logging
from logging import handlers, StreamHandler, Logger, getLogger, DEBUG, Formatter
import sys
from .common import LOG_FILE
import os

FORMATTER = Formatter(
    "%(asctime)s - %(name)-22s - %(levelname)-8s - %(message)s", "%Y-%m-%d %H:%M:%S")


def set_file(file_name: str) -> None:
    """settings the logging file for all loggers

    Args:
        file_name (str): name of file to use for logging
    """
    LOG_FILE = file_name


def get_console_handler() -> logging.StreamHandler:
    """gets the console stream handler

    Returns:
        StreamHandler[typing.TextIO]: the console stream handler
    """
    console_handler = StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler() ->  handlers.TimedRotatingFileHandler:
    """gets the file handler

    Returns:
        handlers.TimedRotatingFileHandler: the file handler
    """
    if not os.path.exists(LOG_FILE):
        parent, file = os.path.split(LOG_FILE)
        os.makedirs(name = parent, exist_ok=True)
    file_handler = handlers.TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name: str) -> Logger:
    """gets the specified logger by name

    Args:
        logger_name (str): name of logger

    Returns:
        Logger: returns needed logger
    """
    logger = getLogger(logger_name)
    # better to have too much log than not enough
    logger.setLevel(DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger