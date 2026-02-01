from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from db.db_crud import saveLog
from handleMessages.router import message_router


app = FastAPI(title="mmBot Admin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message_router)

@app.get("/")
def welcome():
    return {"data":"Welcome I'm mattermost Bot for handle message about \"SSAFY 15 Gwangju class 4\""}
