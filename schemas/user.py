from pydantic import BaseModel

class User(BaseModel):
    name: str
    password: str

class UserPatch(BaseModel):
    name: str 
    balance: int