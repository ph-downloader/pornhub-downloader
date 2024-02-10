#!/usr/bin/env python3


import logging


import db
from config import get_models

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    models = get_models()
    logger.info(f"Got {len(models)} models: {models}")

    db.init()
    db.update_models(models)
    logger.info("Models have been updated")


if __name__ == "__main__":
    main()
