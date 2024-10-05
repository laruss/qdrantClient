from fastapi import APIRouter, Response
from pydantic import BaseModel

from app.models.config import ConfigModel, ConfigValidator, CurrentDataType
from app.annotations import AnnotatedConfig
from app.utils.logger import logger
from env import env

router = APIRouter(
    prefix="/config",
    tags=["config"],
    responses={404: {"description": "Not found"}},
)


async def create_config_if_not_exists():
    config = await ConfigModel.find_one()
    if not config:
        await ConfigModel.insert_one(ConfigValidator(imagesUrlPrefix=f"{env.API_PREFIX}/media/"))
        logger.info("Config created")
    else:
        logger.info("Config already exists")


@router.get("",
            operation_id="getConfig",
            response_model=ConfigValidator,
            response_model_exclude={"currentMedia"}
            )
async def get_config(config: AnnotatedConfig) -> ConfigValidator:
    return config


class SetDataTypeRequest(BaseModel):
    dataType: CurrentDataType


@router.post("/dataType", operation_id="setDataType")
async def set_data_type(config: AnnotatedConfig, data: SetDataTypeRequest):
    config.currentDataType = data.dataType
    config.currentMedia = None
    await ConfigModel.update_one(config)

    return Response(status_code=204)


class SetPromptPartsPayload(BaseModel):
    parts: list[str]


@router.post("/propmts", operation_id="setPromptParts")
async def set_prompt_parts(config: AnnotatedConfig, payload: SetPromptPartsPayload):
    config.promptParts = payload.parts
    await ConfigModel.update_one(config)

    return Response(status_code=204)
