from pydantic import BaseModel
 
class Info_client_url(BaseModel):
    url: str = 'test_url'
    login: str = 'test_login'
