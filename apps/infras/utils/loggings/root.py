import logging
from pythonjsonlogger.json import JsonFormatter


def get_logger():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(
        JsonFormatter(
            json_ensure_ascii=False,
        )
    )

    logger.addHandler(handler)
    return logger


logger = get_logger()

# logger.info("Logging using pythonjsonlogger!", extra={"more_data": True})
