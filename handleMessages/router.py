import requests
from fastapi import APIRouter, Response
from .models import InputModel
from db.db_crud import *
import asyncio
from util import getCurTime, refineText, parseText

message_router = APIRouter(prefix="/api/messages")

async def sendMessage(payload:InputModel, url:str):
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json={
            "text" : payload.text
        }, headers=headers, timeout=5)
    print(response)

async def postAnnouncement(title, body):
    SECRET_KEY=""
    DB_KEY=""
    
    url = "https://api.notion.com/v1/pages" 

    headers = {
        "Authorization": f"Bearer {SECRET_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    payload = {
        "parent": {
            "database_id": DB_KEY
        },
        "properties": {
            "공지 제목": {
                "title": [
                    {
                        "text": {
                            "content": title   # ← 공지 첫 줄
                        }
                    }
                ]
            },
            "생성 시간": {
                "date": {
                    "start": getCurTime()
                }
            },
            "카테고리": {
                "multi_select": [
                    { "name": "공지" },  # 예: "공지", "이벤트", "시스템"
                ]
            }
        }
    }

    res = requests.post(url, headers=headers, json=payload)
    #------ todo - make it log
    print(res.status_code)
    print(res.text)
    #------ 
    page_id = res.json()["id"]

    block_url = f"https://api.notion.com/v1/blocks/{page_id}/children"

    
    def check_type(text : str) -> str:
        try:
            head = text.split()[0] # there is type [#, ##, #... , -]
            res_type = ""
            if head[0] =='#' and len(head) <= 5:
                res_type = f"heading_{len(head)}"
                text = ' '.join(text.split()[1::])
            elif head == '-':
                res_type = "bulleted_list_item"
                text = ' '.join(text.split()[1::])
            else:
                res_type = "paragraph"

            return res_type, text
        except:
            return res_type, text

    children = []

    for chunk in body.split("\n"):
        t,chunk = check_type(chunk)
        children.append({
            "object": "block",
            "type": t,
            t: {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": chunk
                        }
                    }
                ]
            }
        })

    block_payload = {
        "children": children
    }

    requests.patch(block_url, headers=headers, json=block_payload)

@message_router.post("/in")
def handleMessage(payload:InputModel):
    create_message_log(
        get_channel_by_token(payload.token).channel_id,
        refineText(payload.text)
    )
    asyncio.run(sendMessage(payload,"https://meeting.ssafy.com/hooks/ctpgdnzg93dtxdz4p8jtir13ir"))
    
    parsed_data = parseText(refineText(payload.text))
    asyncio.run(postAnnouncement(parsed_data.title, parsed_data.body))
    
    return Response(status_code=200)