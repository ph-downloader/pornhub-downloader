import logging


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    return logging.getLogger(name)
