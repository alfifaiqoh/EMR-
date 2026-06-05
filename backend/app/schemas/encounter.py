from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class EncounterStatus(str, Enum):
    WAITING = "WAITING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class EncounterCreate(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    chief_complaint: Optional[str] = None
    status: EncounterStatus = EncounterStatus.WAITING

class EncounterUpdate(BaseModel):
    doctor_id: Optional[int] = None
    chief_complaint: Optional[str] = None
    status: Optional[EncounterStatus] = None


class EncounterResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: Optional[int]
    chief_complaint: Optional[str]
    status: EncounterStatus
    created_at: datetime

    class Config:
        from_attributes = True

