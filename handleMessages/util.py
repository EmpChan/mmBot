from datetime import datetime, timezone, timedelta
import re
from .models import ParsedText

def getCurTime():
    kst = timezone(timedelta(hours=9))
    return datetime.now(kst).isoformat()

def refineText(text : str) -> str:
    return re.sub(r":[^:\s]+:", " ", text)

def parseText(text: str) -> ParsedText:
    text=text.strip("@all @here\n")
    title = text.split('\n')[0].strip("# :")
    body = refineText(text)

    res = ParsedText(
        title=title,
        body=body
    )
    print(res.title, res.body)

    return res