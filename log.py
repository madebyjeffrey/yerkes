"""
Central logging configuration for Yerkes.

All modules obtain their logger via the standard ``logging.getLogger(__name__)``
pattern, so they are all children of the root "yerkes" hierarchy and can be
controlled together or individually.

Usage
-----
Enable before running game code::

    from log import configure_logging
    configure_logging()                        # INFO to stdout
    configure_logging(level="DEBUG")           # verbose
    configure_logging(enabled=False)           # silence everything

The logger is disabled by default — importing any game module produces no
output until ``configure_logging()`` is called.
"""

import logging
import sys
from typing import Optional


LOGGER_NAME = "yerkes"

# A NullHandler is the library-safe default: no output until the caller opts in.
logging.getLogger(LOGGER_NAME).addHandler(logging.NullHandler())


def get_logger(name: str) -> logging.Logger:
    """Return a logger guaranteed to be under the yerkes hierarchy.

    Use this instead of ``logging.getLogger(__name__)`` so the logger is
    always reachable by ``configure_logging()``.

    Examples
    --------
    >>> from log import get_logger
    >>> _logger = get_logger(__name__)   # e.g. "yerkes.game", "yerkes.main"
    >>> _logger = get_logger("combat")   # becomes "yerkes.combat"
    """
    # Strip any existing "yerkes." prefix to avoid doubling it.
    clean = name.removeprefix(f"{LOGGER_NAME}.")
    return logging.getLogger(f"{LOGGER_NAME}.{clean}")


def configure_logging(
    enabled: bool = True,
    level: str = "INFO",
    fmt: Optional[str] = None,
) -> None:
    """Configure the Yerkes logger.

    Parameters
    ----------
    enabled:
        Set to ``False`` to silence all Yerkes log output.
    level:
        Standard level name: ``"DEBUG"``, ``"INFO"``, ``"WARNING"``, etc.
    fmt:
        Optional format string.  Defaults to a compact timestamped format.
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.handlers.clear()

    if not enabled:
        logger.addHandler(logging.NullHandler())
        logger.propagate = False
        return

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric_level)

    formatter = logging.Formatter(
        fmt or "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

