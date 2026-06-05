from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DiagnosisCreate(BaseModel):
    soap_id: int
    diagnosis_name: str
    icd_code: Optional[str] = None


class DiagnosisUpdate(BaseModel):
    diagnosis_name: Optional[str] = None
    icd_code: Optional[str] = None


class DiagnosisResponse(BaseModel):
    id: int
    soap_id: int
    diagnosis_name: str
    icd_code: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True