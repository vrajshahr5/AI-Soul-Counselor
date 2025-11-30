from __future__ import annotations
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")

SQL_ECHO = os.getenv("SQL_ECHO", "0").lower() in {"1","true","yes","on"}

# Define connect_args based on the database type
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else{}

engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=SQL_ECHO,future=True)

Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    future=True,
    bind=engine
)

def get_db()->Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db()->None:
    from app import models
    models.Base.metadata.create_all(bind=engine)



