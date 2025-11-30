from __future__ import annotations
import os
from fastapi import Depends, HTTPException, status
from app.models import User
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_db


SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

security = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
    except JWTError:
        raise credentials_exception

    if sub is None:
        raise credentials_exception
    user = db.query(User).filter(User.email == sub).first()
    if user is None:
        raise credentials_exception
    
    return user












    
                                        
   
    

