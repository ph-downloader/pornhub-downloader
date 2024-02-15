FROM python:3.12.2-alpine3.19

RUN apk add git poetry
COPY poetry.lock pyproject.toml runner.sh pornhub-downloader/
COPY pornhub_downloader/ pornhub-downloader/pornhub_downloader/

WORKDIR /pornhub-downloader

RUN poetry install

CMD ["./runner.sh"]
