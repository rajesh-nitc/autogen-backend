import logging

from autogen_agentchat import EVENT_LOGGER_NAME


def setup_logging(level: int = logging.INFO) -> None:
    """Setup logging for the application.

    :param level: logging level
    """
    logging.basicConfig(level=level)
    logger = logging.getLogger(EVENT_LOGGER_NAME)
    logger.setLevel(level)
