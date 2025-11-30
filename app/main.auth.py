from fastapi import FastAPI
from app.schemas import ChatRequest, ChatResponse, UploadRequest
from app.chains import get_response
from app.vector_store import embed_and_store

app = FastAPI() #This "app" is what uvicorn looks for
@app.get("/")
def read_root():
    return {"message": "AI counselor API is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response=get_response(request.text, request.user_id)
    return ChatResponse(user_id=request.user_id, message=response)


@app.post("/upload")
def upload(request: UploadRequest):
    embed_and_store(request.text, user_id="default")
    return {"message": "Text uploaded and embedded successfully"}

