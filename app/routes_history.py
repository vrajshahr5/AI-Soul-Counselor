from __future__ import annotations
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List, Literal, Optional
from app.models import ChatMessage, User
from app.schemas import HistoryItem, HistoryAppend, HistoryList
from app.auth_dependency import get_current_user

router = APIRouter(prefix="/history", tags=["History"])

@router.get("/", response_model=HistoryList)
def get_history(
    limit: int = Query(10, ge=1, le=1000,description="Max items to return"),
    offset: int = Query(0, ge=0, description="Items to skip"),
    role: Optional[Literal["user","bot"]] = Query(
        None, description= "filter by role"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    q = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == current_user.id)
    )
    if role:
        q = q.filter(ChatMessage.role == role)
    
    q = q.order_by(ChatMessage.timestamp.asc(), ChatMessage.id.asc())
    rows:List[ChatMessage] = q.offset(offset).limit(limit).all()
    items = [HistoryItem.model_validate(row) for row in rows]
    next_offset = offset + len(items) if len(items) == limit else None
    return HistoryList(user_id=current_user.id, items=items, total=next_offset)


@router.get("/count")
def count_history(
role: Optional[Literal["user","assistant"]] = Query(
    None, description="Count the role only if provided"
),
db: Session=Depends(get_db),
current_user: User = Depends(get_current_user),
):
   q=db.query(ChatMessage).filter(ChatMessage.user_id == current_user.id)
   if role:
       q=q.filter(ChatMessage.role == role)
       return{"total":q.count()}
   
@ router.post("/",response_model=HistoryItem,status_code=status.HTTP_201_CREATED)
def append_history(
    body: HistoryAppend,
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if body.role not in ("user","assistant"):
        raise HTTPException(status_code=422,detail="role must be 'user' or 'assistant'")
    msg = ChatMessage(user_id=current_user.id, role=body.role, content=body.content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_history(
    db:Session=Depends(get_db),
    current_user: User=Depends(get_current_user),
):
    #Delete all messages for all users
    db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).delete(synchronize_session=False)
    db.commit()

@router.delete("/before", status_code=status.HTTP_204_NO_CONTENT)
def delete_history_before(
    before:datetime=Query(...,Description="Delete this history before this UTC timestamp"),
    db:Session=Depends(get_db),
    current_user: User=Depends(get_current_user),
):

    """
    Delete all messages for the current user created before the given timestamp.
    Use ISO 8601, e.g. ?before=2025-08-20T00:00:00Z

    """

    db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id,
        ChatMessage.created_at < before,
    ).delete(synchronize_session=False)
    db.commit()

    
    


   







       
       









    
    






