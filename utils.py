import requests

async def sendMessage(payload, url: str):

    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=5)
    print(response)

