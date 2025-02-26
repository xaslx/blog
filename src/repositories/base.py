from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    
    def __init__(self, session: AsyncSession, model: type[T]):
        self._session = session
        self._model = model

    @abstractmethod
    async def add(self) -> T:
        ...

    @abstractmethod
    async def get_by_id(self, obj_id: int) -> T | None:
        ...

    @abstractmethod
    async def get_all(self) -> list[T] | None:
        ...

    @abstractmethod
    async def update(self, obj_id: int, **kwargs) -> T | None:
        ...

    @abstractmethod
    async def delete(self, obj_id: int) -> T | None:
        ...
