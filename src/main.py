from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.container import AppProvider
from src.routers.post import router as post_router
from src.database.db import create_db_and_tables
from dishka.integrations import fastapi as fastapi_integration
from dishka import AsyncContainer, make_async_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    create_db_and_tables()
    
    yield


def create_app() -> FastAPI:
    
    container: AsyncContainer = make_async_container(AppProvider())
    
    app: FastAPI = FastAPI(
        lifespan=lifespan,
    )
    app.include_router(router=post_router)
    fastapi_integration.setup_dishka(container=container, app=app)
    
    return app