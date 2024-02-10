import datetime
import logging
import os
from typing import List

from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    Model as DbModel,
    SqliteDatabase,
)

from definition import ROOT_DIR

DB_FILE_PATH = os.path.join(ROOT_DIR, "..", "downloads", "metadata.db")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


db = SqliteDatabase(DB_FILE_PATH)


class BaseModel(DbModel):
    class Meta:
        database = db


class Model(BaseModel):
    username = CharField(unique=True)
    is_active = BooleanField(index=True, default=True)
    created_at = DateTimeField(default=datetime.datetime.now)


def init() -> None:
    db.connect()
    db.create_tables([Model])


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
