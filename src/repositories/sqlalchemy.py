from src.repositories.base import BaseRepository
from sqlalchemy import select
from src.repositories.base import T


class SQLAlchemyRepository(BaseRepository):

    async def add(self, model) -> T:
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return model
    
    async def get_all(self) -> list[T] | None:
        result = self._session.execute(select(self._model))
        return result.scalars().all()

    async def get_by_id(self, post_id: int) -> T | None:
        result = self._session.execute(select(self._model).filter(self._model.id == post_id))
        return result.scalar_one_or_none()

    async def update(self, post_id: int, title: str, content: str) -> T | None:
        post = await self.get_by_id(post_id)
        if post:
            post.title = title
            post.content = content
            self._session.commit()
            self._session.refresh(post)
        return post

    async def delete(self, post_id: int) -> T | None:
        post = await self.get_by_id(post_id)
        if post:
            self._session.delete(post)
            self._session.commit()
        return post