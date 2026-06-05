from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TreatmentCreate(BaseModel):
    soap_id: int
    treatment_name: str
    price: Optional[Decimal] = None
    notes: Optional[str] = None


class TreatmentUpdate(BaseModel):
    treatment_name: Optional[str] = None
    price: Optional[Decimal] = None
    notes: Optional[str] = None


class TreatmentResponse(BaseModel):
    id: int
    soap_id: int
    treatment_name: str
    price: Optional[Decimal]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True