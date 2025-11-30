from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, SoulSettings
from app.auth_dependency import get_current_user
from app.schemas import SoulSettingsUpdate, SoulSettingsResponse

router = APIRouter(prefix="/soul", tags=["Soul Settings"])

def get_soul_settings(db: Session, user: User) -> SoulSettings:
    "Get or create the soul settings for the user"
    settings = db.query(SoulSettings).filter(SoulSettings.user_id == user.id).first()
    if settings:
        return settings

    settings = SoulSettings(user_id=user.id)
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings

@router.get("/settings", response_model=SoulSettingsResponse)
def read_soul_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    settings: SoulSettings = get_soul_settings(db, current_user)
    return settings

@router.put("/settings", response_model=SoulSettingsResponse)
def update_soul_settings(
    settings_update: SoulSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    settings = get_soul_settings(db, current_user)

    if settings_update.tone is not None:
        settings.tone = settings_update.tone
    if settings_update.empathy_level is not None:
        settings.empathy_level = settings_update.empathy_level
    if settings_update.reasoning_depth is not None:
        settings.reasoning_depth = settings_update.reasoning_depth
    if settings_update.memory_aggressiveness is not None:
        settings.memory_aggressiveness = settings_update.memory_aggressiveness
    if settings_update.boundaries is not None:
        settings.boundaries = settings_update.boundaries
    if settings_update.creativity_level is not None:
        settings.creativity_level = settings_update.creativity_level

    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings









    





