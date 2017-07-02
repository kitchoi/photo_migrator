import contextlib
import logging


_FORMAT = "%(levelname)s - %(funcName)s(%(lineno)d) %(message)s"


@contextlib.contextmanager
def set_logger(logger, level):
    old_level = logger.level
    old_handlers = list(logger.handlers)

    new_handler = logging.StreamHandler()
    new_handler.setLevel(level)
    new_handler.setFormatter(logging.Formatter(fmt=_FORMAT))

    logger.handlers = [new_handler]
    logger.setLevel(level)

    try:
        yield
    finally:
        logger.level = old_level
        logger.handlers = old_handlers
