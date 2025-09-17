from fastapi import FastAPI

from src.api.v1.routers.auth_router import router as auth_router_v1
from src.api.v1.routers.user_router import router as user_router_v1
from src.api.v1.routers.book_router import router as book_router_v1

def init_api_routers(app: FastAPI):
    app.include_router(auth_router_v1)
    app.include_router(user_router_v1)
    app.include_router(book_router_v1)