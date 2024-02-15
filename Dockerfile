FROM python:3.11-alpine

RUN apk add poetry
COPY poetry.lock pyproject.toml runner.sh pornhub-downloader/
COPY pornhub_downloader/ pornhub-downloader/pornhub_downloader/

WORKDIR /pornhub-downloader

RUN poetry install

CMD ["./runner.sh"]
