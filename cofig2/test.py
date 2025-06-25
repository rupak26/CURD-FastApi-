from logging_config import setup_logging

setup_logging()

import logging
logger = logging.getLogger(__name__)
logger.info("App started")
logger.debug("Debugging info")
logger.error("Something went wrong")

