from __future__ import annotations
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth_dependency import get_current_user
from app.database import get_db
from app.models import ChatMessage, User
from app.schemas import ChatRequest, ChatResponse
from app.chains import get_response, user_chroma_dir
from app.vector_store import embed_and_store

router = APIRouter(tags=["chat"])

@router.post("", response_model=ChatResponse) 
def chat_with_soul(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
   
    user_id_int = current_user.id
    user_id = str(user_id_int)

    
    user_msg = ChatMessage(
        user_id=user_id_int,
        role="user",
        content=request.text,
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    try:
        answer = get_response(request.text, user_id)
    except RuntimeError as e:
       
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate a response: {e}"
        )
    
    bot_msg = ChatMessage(
        user_id=user_id_int,
        role="assistant",
        content=answer,
    )

    db.add(bot_msg)
    db.commit()
    db.refresh(bot_msg)

    try:
        persist_dir = user_chroma_dir(user_id)
        
        ts = datetime.utcnow().isoformat() + "Z"
        embed_and_store(
            text=f"[USER @ {ts}]\n{request.text}\n\n[ASSISTANT @ {ts}]\n{answer}",
            persist_dir=persist_dir,
            user_id=user_id,
        )
    except Exception as e:
        
        print(f"[warn] embedding failed for user {user_id}: {e}")

    return ChatResponse(response=answer, user_id=user_id)
