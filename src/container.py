from dishka import Provider, Scope, provide
from redis import Redis
from sqlmodel import Session
from src.database.db import engine
from src.repositories.post import PostRepository
from src.services.cache_service import CacheService
from src.models.post import Post


class AppProvider(Provider):
    
    @provide(scope=Scope.APP)
    def get_redis_client(self) -> Redis:
        return Redis(host="redis", port=6379, db=0, decode_responses=True)

    
    @provide(scope=Scope.REQUEST)
    def get_sqlmodel_session(self) -> Session:
        with Session(engine) as session:
            return session
            
    
    @provide(scope=Scope.REQUEST)
    def get_post_repository(self, session: Session) -> PostRepository:
        return PostRepository(session=session, model=Post)
    
    
    @provide(scope=Scope.REQUEST)
    def get_cache_service(self, redis: Redis) -> CacheService:
        return CacheService(client=redis)
    