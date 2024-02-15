#!/bin/sh

while true
do
    date
    poetry run python pornhub_downloader/downloader.py
    sleep 3600
done
