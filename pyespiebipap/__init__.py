from .common import scrape_date_entries

import logging


def configure_logging():

    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s ::: %(name)s ::: %(threadName)s ::: "
            ":%(process)d ::: %(levelname)s ::: %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(level=logging.INFO)


configure_logging()
