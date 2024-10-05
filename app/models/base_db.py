from typing import Type, Annotated, TypeVar, Generic, Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from pydantic import BaseModel, BeforeValidator, Field, ConfigDict, create_model

from app.utils.mongo import db

PyObjectId = Annotated[str, BeforeValidator(str)]

T = TypeVar('T', bound=BaseModel)


class BaseDb(Generic[T]):
    db: AsyncIOMotorDatabase = db
    __mongo_collection__: AsyncIOMotorCollection
    Validator: Type[T]

    @classmethod
    def __set_validator(cls):
        return create_model(
            'SetValidator',
            model_config=(
                ConfigDict,
                ConfigDict(
                    arbitrary_types_allowed=True,
                    json_encoders={ObjectId: str}
                )
            ),
            __base__=cls.Validator,
        )

    @classmethod
    def __get_validator(cls):
        return create_model(
            'GetValidator',
            id=(
                PyObjectId | None,
                Field(alias='_id', default=None)
            ),
            model_config=(
                ConfigDict,
                ConfigDict(
                    populate_by_name=True,
                    arbitrary_types_allowed=True,
                )
            ),
            __base__=cls.Validator,
        )

    @classmethod
    def get_set_validator(cls) -> Type[T]:
        return cls.__set_validator()

    @classmethod
    async def find_one(cls, **query: Any) -> T | None:
        document = await cls.__mongo_collection__.find_one(query)
        if document:
            return cls.__get_validator()(**document)

        return None

    @classmethod
    async def get_many(cls, limit_: int = None, sort_: tuple = None, **query: Any) -> list[T]:
        documents = cls.__mongo_collection__.find(query)
        if sort_:
            documents = documents.sort(*sort_)
        if limit_:
            documents = documents.limit(limit_)
        return [cls.__get_validator()(**document) async for document in documents]

    @classmethod
    async def insert_one(cls, set_validator: T) -> T:
        """
        Parameters:
            - set_validator: T - a pydantic model instance that was created using the set_validator method

        Returns:
            - T: the set_validator instance that was inserted into the database
        """
        await cls.__mongo_collection__.insert_one(set_validator.model_dump())
        return set_validator

    @classmethod
    async def insert_many(cls, set_validators: list[T]) -> list[T]:
        """
        Parameters:
            - set_validators: list[T] - a list of pydantic model instances that were created using the set_validator method

        Returns:
            - list[T]: the set_validators instances that were inserted into the database
        """
        await cls.__mongo_collection__.insert_many([set_validator.model_dump() for set_validator in set_validators])
        return set_validators

    @classmethod
    async def update_one(cls, updated_document: T, **query: Any) -> T:
        await cls.__mongo_collection__.update_one(query, {'$set': updated_document.model_dump()})
        return updated_document

    @classmethod
    async def delete_one(cls, **query: Any) -> None:
        await cls.__mongo_collection__.delete_one(query)
