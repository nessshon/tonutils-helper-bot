import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logger(log_level=logging.INFO, logs_dir=".logs") -> None:
    """
    Set up logging configuration.

    :param log_level: Logging level (default is INFO).
    :param logs_dir: Directory for log files (default is ".logs").
    """
    os.makedirs(logs_dir, exist_ok=True)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
        handlers=[
            TimedRotatingFileHandler(
                filename=os.path.join(logs_dir, f"bot.log"),
                when="D",
                interval=1,
                backupCount=31,
            ),
            logging.StreamHandler(),
        ]
    )

    _set_logger_level("aiogram.event", logging.CRITICAL)


def _set_logger_level(logger_name: str, level: int) -> None:
    """
    Set the log level for a specific logger.

    :param logger_name: Name of the logger.
    :param level: Logging level.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
