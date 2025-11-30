from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserOutput
from app import utilities



router = APIRouter(tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(request: UserLogin,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not utilities.verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Entry",headers={"WWW-Authenticate": "Bearer"})

    access_token = utilities.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model = UserOutput,status_code=status.HTTP_201_CREATED)
def register_user(user:UserCreate, db:Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email does not work or already registered")

    if hasattr(utilities, "hash_password"):
        hashed_password = utilities.hash_password(user.password)
    else:
        hashed_password = pwd_context.hash(user.password)
    
    new_user=User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user








       




      


