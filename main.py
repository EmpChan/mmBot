from fastapi import FastAPI, Request
from db import saveLog
from utils import sendMessage

app = FastAPI()

@app.post("/") # get Messages
async def getMessage(request: Request):
    data = await request.json()
    saveLog(data["text"])
    
    sendMessage(data, 'https://meeting.ssafy.com/hooks/ctpgdnzg93dtxdz4p8jtir13ir')
    