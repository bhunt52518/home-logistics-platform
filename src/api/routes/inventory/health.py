from fastapi import APIRouter

from src.core.config import get_settings

router = APIRouter(tags=["Inventory"])

@router.get("/inventory/health")
def get_status():
    return "It is working"
   