import datetime
import logging
import os
from typing import List

from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model as DbModel,
    SqliteDatabase,
)

from definition import ROOT_DIR
from config import VideoMetadata


DB_FILE_PATH = os.path.join(ROOT_DIR, "..", "downloads", "metadata.db")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


db = SqliteDatabase(DB_FILE_PATH)


class BaseModel(DbModel):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)


class Model(BaseModel):
    username = CharField(unique=True)
    is_active = BooleanField(index=True, default=True)


class Video(BaseModel):
    model = ForeignKeyField(Model, backref="videos")
    view_key = CharField(index=True, unique=True)
    title = CharField()
    url = CharField()
    is_downloaded = BooleanField(default=False)


def init() -> None:
    db.connect()
    db.create_tables([Model, Video])


def update_models(models: List[str]) -> None:
    for model in models:
        model_in_db, created = Model.get_or_create(username=model)
        if created:
            logger.info(f"Created model {model}")
        elif model_in_db.is_active:
            logger.info(f"Model {model} already exists")
        else:
            model_in_db.is_active = True
            model_in_db.save()
            logger.info(f"Set model {model} to active")

    active_models_in_db = Model.select().where(Model.is_active)
    models_set = set(models)
    for active_model_in_db in active_models_in_db:
        if active_model_in_db.username not in models_set:
            active_model_in_db.is_active = False
            active_model_in_db.save()
            logger.info(f"Set model {active_model_in_db.username} to inactive")


def insert_videos(username: str, video_metadatas: List[VideoMetadata]) -> None:
    model = Model.get_or_none(username=username)
    if not model or not model.is_active:
        raise RuntimeError(f"Model {username} doesn't exist or is inactive.")

    for video_metadata in video_metadatas:
        view_key = extract_view_key(video_metadata.url)
        if Video.get_or_none(view_key=view_key):
            logger.info(
                f"Video '{video_metadata.title}' for model {model.username} already exists. Skipping"
            )
        else:
            Video.create(
                model=model,
                view_key=view_key,
                title=video_metadata.title,
                url=video_metadata.url,
            )
            logger.info(
                f"Inserted video '{video_metadata.title}' for model {model.username}."
            )


def extract_view_key(url: str) -> str:
    return url.strip().split("=")[-1]
