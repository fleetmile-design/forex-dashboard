"""REST API endpoints"""
from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/status")
async def get_status():
    return {"status": "running", "version": "1.0"}


@router.get("/market-state")
async def get_market_state():
    from .websocket_server import generate_demo_data
    return generate_demo_data()


@router.get("/indicators")
async def get_indicators():
    from .websocket_server import generate_demo_data
    data = generate_demo_data()
    return data.get("momentum", {})
