from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SOAPCreate(BaseModel):
    encounter_id: int
    subjective: Optional[str] = None
    objective: Optional[str] = None
    assessment: Optional[str] = None
    plan: Optional[str] = None


class SOAPUpdate(BaseModel):
    subjective: Optional[str] = None
    objective: Optional[str] = None
    assessment: Optional[str] = None
    plan: Optional[str] = None


class SOAPResponse(BaseModel):
    id: int
    encounter_id: int
    subjective: Optional[str]
    objective: Optional[str]
    assessment: Optional[str]
    plan: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True