from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.router import api_router
from app.websocket.router import ws_router
from app.webhook.telegram import webhook_router

app = FastAPI(title="Telegram CRM", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(ws_router)
app.include_router(webhook_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
