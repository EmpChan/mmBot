from pydantic import BaseModel,ConfigDict

class InputModel(BaseModel):
    text:str
    token:str
    
class ParsedText(BaseModel):
    title:str
    body:str