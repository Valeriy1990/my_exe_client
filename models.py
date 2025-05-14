from pydantic import BaseModel
 
class Info(BaseModel):
    url: str
    login: str
