#!/bin/sh

while true
do
    echo "Current run: `date`"
    poetry run python pornhub_downloader/downloader.py
    echo "Changing ownership of the files"
    chown -R "${PUID}:${PGID}" downloads
    sleep 3600
done
