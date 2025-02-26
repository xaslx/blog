from fastapi import APIRouter, status
from src.repositories.post import PostRepository
from src.services.cache_service import CacheService
from src.models.post import Post
from src.schemas.post import PostCreate, PostUpdate
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.exceptions import PostNotFoundException


router = APIRouter(prefix='/posts', tags=['Posts'])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Создать пост",
)
@inject
async def create_post(
    post_create: PostCreate,
    post_repository: Depends[PostRepository],
    cache_service: Depends[CacheService],
) -> Post:
    
    post = Post(title=post_create.title, content=post_create.content)
    
    await post_repository.add(model=post)
    
    cache_service.delete_posts_cache(key="posts")
    cache_service.increment_post_stat(key="posts")
    
    return post


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Получить все посты",
)
@inject
async def get_all_posts(
    post_repository: Depends[PostRepository],
    cache_service: Depends[CacheService],
) -> list[Post] | None:
    
    cached_posts = cache_service.get_cached_posts()
    
    if cached_posts:
        return cached_posts

    posts = await post_repository.get_all()
    cache_service.cache_posts([post.dict() for post in posts])
    
    return posts


@router.get(
    "/stats",
    status_code=status.HTTP_200_OK,
    description="Эндпоинт для получения статистики создания постов",
)
@inject
async def get_post_stats(cache_service: Depends[CacheService]) -> dict:
    
    return cache_service.get_post_stats()


@router.get(
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    description="Эндпоинт для получения поста",
)
@inject
async def get_post(
    post_id: int,
    post_repository: Depends[PostRepository],
    cache_service: Depends[CacheService],
) -> Post | None:
    
    cached_post = cache_service.get_cached_post(post_id)
    
    if cached_post:
        return cached_post


    post = await post_repository.get_by_id(post_id)
    
    if not post:
        raise PostNotFoundException()
    
    cache_service.cache_post(post_id, post.dict())
    
    return post


@router.put(
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    description="Эндпоинт для обновления поста",
)
@inject
async def update_post(
    post_id: int, post_update: PostUpdate,
    post_repository: Depends[PostRepository],
    cache_service: Depends[CacheService],
) -> Post | None:
    
    post = await post_repository.update(post_id, post_update.title, post_update.content)
    
    if not post:
        raise PostNotFoundException()
    
    cache_service.delete_posts_cache(key=f"post:{post_id}")
    cache_service.delete_posts_cache(key="posts")
    
    return post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    description="Эндпоинт для удаления поста",
)
@inject
async def delete_post(
    post_id: int,
    post_repository: Depends[PostRepository],
    cache_service: Depends[CacheService],
) -> Post | None:
    
    post = await post_repository.delete(post_id)
    
    if not post:
        raise PostNotFoundException()
    
    cache_service.delete_posts_cache(key=f"post:{post_id}")
    cache_service.delete_posts_cache(key="posts")
    
    return post
