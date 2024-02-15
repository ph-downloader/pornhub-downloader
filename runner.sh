#!/bin/sh

while true
do
    echo "Current run: `date`"
    poetry run python pornhub_downloader/downloader.py
    sleep 3600
done
