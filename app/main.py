from fastapi import FastAPI, WebSocket, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.database import async_session, init_db
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Notification
from app.schemas import NotificationCreate, NotificationRead
from fastapi.staticfiles import StaticFiles
from sqlalchemy import insert, select

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: dict):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """
        Send a message to all connected WebSockets
        message is typically a dict that we'll JSON_serialize via WebSocket.
        """

        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()  

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/notifications" , response_model= List[NotificationRead])
async def list_notifications(session: AsyncSession = Depends(get_session)):
    stmt = select(Notification).order_by(Notification.id.desc()).limit(7)
    result = await session.execute(stmt)
    notifications = result.scalars().all()
    return notifications

@app.post("/notifications", response_model = NotificationRead)
async def create_notification(
    notif : NotificationCreate,
    session : AsyncSession = Depends(get_session)
):
    stmt = insert(Notification).values(
        user_id = notif.user_id,
        message = notif.message
    ).returning(Notification)

    result = await session.execute(stmt)
    new_notif = result.scalar_one()
    await session.commit()

    message_to_broadcast = {
        "action": "new_notification",
        "data": {
            "id": new_notif.id,
            "user_id": new_notif.user_id,
            "message": new_notif.message,
            "created_at": str(new_notif.created_at)
        }
    }
    await manager.broadcast(message_to_broadcast)
    return new_notif

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Recieved your message: {data}")

    except Exception:
        pass
    finally:
        manager.disconnect(websocket) 
        await websocket.close()
