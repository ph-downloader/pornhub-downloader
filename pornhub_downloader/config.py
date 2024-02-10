from typing import List
import logging
import os

import yaml

from definition import ROOT_DIR

CONFIG_FILE_PATH = os.path.join(ROOT_DIR, "..", "downloads", "config.yaml")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_models(config_file_path: str = CONFIG_FILE_PATH) -> List[str]:
    try:
        with open(config_file_path) as f:
            return yaml.safe_load(f)["models"]
    except FileNotFoundError:
        logger.exception("Cannot find the config file.")
    except yaml.YAMLError:
        logger.exception("Cannot parse the config file.")
