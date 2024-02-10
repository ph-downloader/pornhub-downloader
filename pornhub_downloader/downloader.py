#!/usr/bin/env python3


import logging

from config import get_models

logger = logging.getLogger(__name__)


def main():
    models = get_models()
    print(models)


if __name__ == "__main__":
    main()
