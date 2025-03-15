import logging

from autogen_agentchat import EVENT_LOGGER_NAME


def setup_logging(level=logging.INFO):
    logging.basicConfig(level=level)
    logger = logging.getLogger(EVENT_LOGGER_NAME)
    logger.setLevel(level)
