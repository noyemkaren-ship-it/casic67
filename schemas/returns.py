from pydantic import BaseModel

class Message(BaseModel):
    name: str
    text: str

class UserReturn(BaseModel):
    user: str
    

class Error(BaseModel):
    name: str
    text: str
    
