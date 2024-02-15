#!/usr/bin/env python3

import logging
import os

import yt_dlp

import db
from config import get_models, get_videos
from definition import ROOT_DIR


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DOWNLOADS_PATH = os.path.join(ROOT_DIR, "..", "downloads")


def download_video(model: str, url: str) -> None:
    with yt_dlp.YoutubeDL(
        {"paths": {"home": os.path.join(DOWNLOADS_PATH, model)}}
    ) as ydl:
        logger.info(f"Downloading {url} for model {model}")
        ydl.download([url])


def download_videos():
    undownloaded_videos = db.get_undownloaded_videos()
    logger.info(f"{len(undownloaded_videos)} videos pending downloading")

    downloaded_videos = []
    count = 0
    for undownloaded_video in undownloaded_videos:
        try:
            download_video(undownloaded_video.model.username, undownloaded_video.url)
            downloaded_videos.append(undownloaded_video)
            count += 1
        except Exception as e:
            logger.exception(e)

    logger.info(f"{count} videos were downloaded")
    db.update_undownloaded_videos(downloaded_videos)


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

    download_videos()


if __name__ == "__main__":
    main()
