from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    text: str


class ChatResponse(BaseModel):
    user_id: str
    message: str




class UploadRequest(BaseModel):
   text: str

   
