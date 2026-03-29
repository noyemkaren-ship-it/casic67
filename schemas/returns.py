from pydantic import BaseModel

class Message(BaseModel):
    name: str
    text: str

    
