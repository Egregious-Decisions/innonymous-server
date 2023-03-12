from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Item = TypeVar("Item")
Identity = TypeVar("Identity")


class AnyRepository(ABC, Generic[Item, Identity]):
    @abstractmethod
    async def save(self, item: Item, /) -> Item:
        pass

    @abstractmethod
    async def exists(self, identity: Identity, /) -> bool:
        pass

    @abstractmethod
    async def get(self, identity: Identity, /) -> Item | None:
        pass

    @abstractmethod
    async def get_or_default(self, identity: Identity, /, *, default: Item) -> Item:
        pass

    @abstractmethod
    async def get_all(self, /) -> list[Item]:
        pass

    @abstractmethod
    async def update(self, item: Item, /) -> Item | None:
        pass

    @abstractmethod
    async def delete(self, identity: Identity, /) -> bool:
        pass
