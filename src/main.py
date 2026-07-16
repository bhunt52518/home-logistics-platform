from fastapi import FastAPI

from src.api.routes.health import router as health_router
from src.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Intelligent household resource management platform.",
)

app.include_router(health_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": f"{settings.app_name} API",
        "docs": "/docs",
        "health": "/health",
    }