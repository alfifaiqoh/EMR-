from pydantic import BaseModel
from typing import Optional


class DiagnosisHistory(BaseModel):
    diagnosis_name: str
    icd_code: Optional[str] = None

    class Config:
        from_attributes = True


class TreatmentHistory(BaseModel):
    treatment_name: str
    price: Optional[float] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class SOAPHistory(BaseModel):
    id: int
    subjective: Optional[str]
    objective: Optional[str]
    assessment: Optional[str]
    plan: Optional[str]

    diagnoses: list[
        DiagnosisHistory
    ] = []

    treatments: list[
        TreatmentHistory
    ] = []

    class Config:
        from_attributes = True


class EncounterHistory(BaseModel):
    id: int
    status: str

    soaps: list[
        SOAPHistory
    ] = []

    class Config:
        from_attributes = True


class PatientHistoryResponse(BaseModel):
    id: int
    fullname: str

    encounters: list[
        EncounterHistory
    ] = []

    class Config:
        from_attributes = True