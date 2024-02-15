FROM python:3.12.2-alpine3.19

RUN apk add git poetry
RUN git clone https://github.com/ph-downloader/pornhub-downloader.git

WORKDIR /pornhub-downloader

RUN poetry install

CMD ["./runner.sh"]
