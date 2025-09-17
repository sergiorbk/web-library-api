from fastapi import FastAPI

from src.container import Container
from src.router import init_api_routers

container = Container()
container.wire(modules=["src.api.v1.routers.user_router", "src.api.v1.routers.auth_router"])

app = FastAPI()
init_api_routers(app)
app.container = container