from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio

from api.websocket_server import manager, generate_demo_data
from api.rest_api import router as api_router

app = FastAPI(title="Forex Trader Dashboard", version="1.0")
templates = Jinja2Templates(directory="dashboard")

app.mount("/static", StaticFiles(directory="dashboard"), name="static")
app.include_router(api_router)


@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = generate_demo_data()
            await websocket.send_json(data)
            await asyncio.sleep(60)  # Kas 1 minutę
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.websocket("/ws/fast")
async def websocket_fast(websocket: WebSocket):
    """Greitas WebSocket testavimui (kas 5 sek)"""
    await manager.connect(websocket)
    try:
        while True:
            data = generate_demo_data()
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
