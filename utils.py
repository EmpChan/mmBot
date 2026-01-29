import requests
from datetime import datetime, timezone, timedelta


def getCurTime():
    kst = timezone(timedelta(hours=9))
    return datetime.now(kst).isoformat()

async def sendMessage(payload, url: str):

    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=5)
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
                            "content": "TITLE!!!"   # ← 공지 첫 줄
                        }
                    }
                ]
            },
            "생성 시간": {
                "date": {
                    "start": getCurTime()
                }
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

    def chunk_text(text, size=1800):
        return [text[i:i+size] for i in range(0, len(text), size)]

    children = []

    for chunk in chunk_text(body):
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
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
