from __future__ import annotations
from fastapi import APIRouter, Depends
from app.auth_dependency import get_current_user
from app.models import User



router = APIRouter(prefix="/protected", tags=["protected routes"])

@router.get("/")
def protected_route(current_user: User=Depends(get_current_user)):
    name=current_user.username or current_user.email or "user"
    return{"message":f"Hello, {name}!"}









