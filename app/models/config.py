from enum import Enum

from pydantic import BaseModel

from app.models.base_db import BaseDb
from env import env


class CurrentDataType(str, Enum):
    ALL_MEDIA = "allMedia"
    UNDESCRIBED_MEDIA = "undiscribedMedia"


class ConfigValidator(BaseModel):
    imagesUrlPrefix: str
    duplicateImagesUrlPrefix: str = f"{env.API_PREFIX}/duplicates/image/"
    currentDataType: CurrentDataType = CurrentDataType.ALL_MEDIA
    currentMedia: str | None = None
    promptParts: list[str] = []


class ConfigModel(BaseDb):
    Validator = ConfigValidator
    __mongo_collection__ = BaseDb.db["config"]

    @classmethod
    async def set_current_media(cls, file_name: str):
        if not (config := await cls.find_one()):
            raise ValueError("Config not found, please create one first.")
        config.currentMedia = file_name
        await cls.update_one(config)
