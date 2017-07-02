import contextlib
import logging
import sys


_FORMAT = "%(levelname)s - %(funcName)s(%(lineno)d) %(message)s"


@contextlib.contextmanager
def set_logger(logger, level, stream=sys.stdout):
    """ Context manager for setting a logger to a given logging level and
    an output stream.

    Parameters
    ----------
    logger : logging.Logger
        Logger to be set.
    level : int
        Logging level.
    stream : file-like object
        Output stream for the logger.
    """
    old_level = logger.level
    old_handlers = list(logger.handlers)

    new_handler = logging.StreamHandler(stream=stream)
    new_handler.setLevel(level)
    new_handler.setFormatter(logging.Formatter(fmt=_FORMAT))

    logger.handlers = [new_handler]
    logger.setLevel(level)

    try:
        yield
    finally:
        logger.level = old_level
        logger.handlers = old_handlers
