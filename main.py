from fastapi import FastAPI

from src.container import Container
from src.router import init_api_routers
from src.api.v1.handlers import register_exception_handlers

container = Container()
container.wire(modules=[
    "src.api.v1.routers.user_router",
    "src.api.v1.routers.auth_router",
    "src.api.v1.routers.book_router",
    "src.api.v1.routers.client_router",
    "src.api.v1.routers.checkout_router"
])

app = FastAPI(
    title="Library Management System",
    description="A comprehensive library management system with user authentication, book management, and checkout functionality",
    version="1.0.0"
)

# Register exception handlers
register_exception_handlers(app)

# Initialize API routers
init_api_routers(app)

# Attach container to app
app.container = container