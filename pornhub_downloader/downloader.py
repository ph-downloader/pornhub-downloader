#!/usr/bin/env python3


import logging


import db
from config import get_models, get_videos

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    models = get_models()
    logger.info(f"Got {len(models)} models: {models}")

    db.init()
    db.update_models(models)
    logger.info("Models have been updated")

    for model in models:
        video_metadatas = get_videos(model)
        logger.info(f"Got {len(video_metadatas)} videos for model {model}")

        db.insert_videos(model, video_metadatas)
        logger.info(f"Inserted {len(video_metadatas)} videos for model {model}")


if __name__ == "__main__":
    main()
