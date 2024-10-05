from typing import Annotated

from bson import ObjectId
from fastapi import Request, Depends

from app.models.config import ConfigValidator, ConfigModel, CurrentDataType
from app.models.image import ImageValidator, ImageModel
from app.services.qdrant import Qdrant


async def get_qdrant(request: Request):
    return request.app.qdrant


AnnotatedQdrant = Annotated[Qdrant, Depends(get_qdrant)]


async def get_current_config_from_db() -> ConfigValidator:
    return await ConfigModel.find_one()


AnnotatedConfig = Annotated[ConfigValidator, Depends(get_current_config_from_db)]


async def get_current_media_info_from_db(config: AnnotatedConfig) -> ImageValidator | None:
    if config.currentMedia is None:
        return None

    return await ImageModel.find_one(file_name=config.currentMedia)


AnnotatedCurrentMediaInfo = Annotated[ImageValidator | None, Depends(get_current_media_info_from_db)]


async def get_all_for_current_data_type_from_db(
        config: AnnotatedConfig,
        current_media: AnnotatedCurrentMediaInfo
) -> list[ImageValidator]:
    filter_ = {} if config.currentDataType == CurrentDataType.ALL_MEDIA else {"description": None}
    limit = 10

    if not current_media:
        current_media = await ImageModel.find_one()  # take first media if current media is not set

    # get media before current media
    before = await ImageModel.get_many(
        limit_=limit,
        sort_=("_id", -1),
        **{"_id": {"$lt": ObjectId(current_media.id)}, **filter_}
    )
    before.reverse()

    # if there's not enough media before current media, get media in the end of the list
    if len(before) < limit:
        remaining = limit - len(before)
        end_records = await ImageModel.get_many(
            limit_=remaining,
            sort_=("_id", -1),
            **filter_
        )
        end_records.reverse()
        before.extend(end_records)

    # get media after current media
    after = await ImageModel.get_many(
        limit_=limit,
        sort_=("_id", 1),
        **{"_id": {"$gt": ObjectId(current_media.id)}, **filter_}
    )

    # if there's not enough media after current media, get media in the beginning of the list
    if len(after) < limit:
        remaining = limit - len(after)
        start_records = await ImageModel.get_many(
            limit_=remaining,
            sort_=("_id", 1),
            **filter_
        )
        after.extend(start_records)

    return before + [current_media] + after


AnnotatedAllForCurrentDataType = Annotated[list[ImageValidator], Depends(get_all_for_current_data_type_from_db)]


async def get_hashes_data(request: Request) -> list[str]:
    if not getattr(request.app, "hashes_list", None):
        data = await ImageModel.get_many()
        request.app.hashes_list = [image.hash for image in data]
    return request.app.hashes_list


AnnotatedHashesData = Annotated[list[str], Depends(get_hashes_data)]
