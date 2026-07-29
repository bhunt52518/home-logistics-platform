from fastapi import FastAPI

from src.api.routes.health import router as health_router
from src.api.routes.inventory.health import router as inventory_router
from src.api.routes.inventory.allocations import router as allocations_router
from src.api.routes.inventory.households import router as households_router
from src.api.routes.inventory.category import router as category_router
from src.core.config import get_settings
from src.database.init_db import initialize_database




settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Intelligent household resource management platform.",
)

app.include_router(health_router)
app.include_router(allocations_router, prefix="/inventory",tags=["Inventory"])
app.include_router(inventory_router, prefix="/inventory",tags=["Inventory"])
app.include_router(category_router, prefix="/inventory", tags=["Inventory"])

@app.on_event("startup")
def startup() -> None:
    initialize_database()


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": f"{settings.app_name} API",
        "docs": "/docs",
        "health": "/health",
        "status": "/inventory/health", 
    }

app.include_router(
    households_router,
    prefix="/inventory",
    tags=["Inventory"],
)
