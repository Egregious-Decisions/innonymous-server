from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable, Type, TypeVar, cast

import pymotyc
from pydantic import BaseModel

from innonymous.repository.any_repository import AnyRepository

ASCENDING_ORDER = 1

MongoModel = TypeVar("MongoModel")
ModelIdType = TypeVar("ModelIdType")
ModelType = TypeVar("ModelType", bound=BaseModel)


class MongoRepository(AnyRepository[MongoModel, ModelIdType]):
    @classmethod
    @abstractmethod
    def create(cls) -> MongoRepository[MongoModel, ModelIdType]:
        pass

    @abstractmethod
    def __init__(self, collection: pymotyc.Collection[MongoModel]) -> None:
        self.__collection = collection

    @abstractmethod
    def identity_field(self, /) -> str:
        pass

    def _identity_query(self, identity: ModelIdType, /) -> dict[str, ModelIdType]:
        return {self.identity_field(): identity}

    def _sorting_query(self) -> dict[str, int]:
        return {self.identity_field(): ASCENDING_ORDER}

    async def save(self, item: MongoModel, /) -> MongoModel:
        return await self.__collection.save(item)

    async def exists(self, identity: ModelIdType, /) -> bool:
        try:
            _ = await self.__collection.find_one(self._identity_query(identity))
        except pymotyc.errors.NotFound:
            return False
        return True

    async def get(self, identity: ModelIdType, /) -> MongoModel | None:
        try:
            return await self.__collection.find_one(self._identity_query(identity))
        except pymotyc.errors.NotFound:
            return None

    async def get_or_default(self, identity: ModelIdType, /, *, default: MongoModel) -> MongoModel:
        item = await self.get(identity)
        if item is None:
            return default
        return item

    async def get_all(self, /) -> list[MongoModel]:
        return await self.__collection.find({}, sort=self._sorting_query())

    async def update(self, item: MongoModel, /) -> MongoModel | None:
        try:
            return await self.__collection.save(item, mode="update")
        except pymotyc.errors.NotFound:
            return None

    async def delete(self, identity: ModelIdType, /) -> bool:
        try:
            await self.__collection.delete_one(self._identity_query(identity))
        except pymotyc.errors.NotFound:
            return False
        return True


def make_mongo_repository_type(
        mongo_model: Type[ModelType],
        collection: pymotyc.Collection[ModelType],
        id_reference: Callable[[], int | str],
) -> Type[MongoRepository[ModelType, int | str]]:
    def create(cls) -> Any:  # noqa: ANN001
        return cls(collection)

    def constructor(self, c: pymotyc.Collection[ModelType]) -> None:  # noqa: ANN001
        super(type(self), self).__init__(c)

    def identity_field(self, /) -> int | str:  # noqa: ARG001, ANN001
        return id_reference()

    new_type = type(
        mongo_model.__name__ + "Repository",
        (MongoRepository,),
        {"__init__": constructor, "create": classmethod(create), "identity_field": identity_field},
    )
    return cast(Type[MongoRepository[ModelType, int | str]], new_type)
