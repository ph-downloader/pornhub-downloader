from dataclasses import dataclass
from typing import List
import logging
import os

import yaml
import yt_dlp

from definition import ROOT_DIR

CONFIG_FILE_PATH = os.path.join(ROOT_DIR, "..", "downloads", "config.yaml")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dataclass
class VideoMetadata:
    title: str
    url: str


def get_models(config_file_path: str = CONFIG_FILE_PATH) -> List[str]:
    try:
        with open(config_file_path) as f:
            return yaml.safe_load(f)["models"]
    except FileNotFoundError:
        logger.exception("Cannot find the config file.")
    except yaml.YAMLError:
        logger.exception("Cannot parse the config file.")


def get_videos(model: str) -> List[VideoMetadata]:
    videos = []

    url = f"https://www.pornhub.com/model/{model}"
    ydl_opts = {"extract_flat": "in_playlist", "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        for entry in ydl.sanitize_info(info)["entries"]:
            videos.append(VideoMetadata(entry["title"], entry["url"]))

    return videos
