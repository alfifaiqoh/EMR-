from pydantic import BaseModel

from app.schemas.patient import PatientResponse
from app.schemas.encounter import EncounterResponse
from app.schemas.soap import SOAPResponse
from app.schemas.diagnosis import DiagnosisResponse
from app.schemas.treatment import TreatmentResponse


class EncounterSummaryResponse(BaseModel):
    patient: PatientResponse
    encounter: EncounterResponse
    soap: SOAPResponse | None = None
    diagnoses: list[DiagnosisResponse] = []
    treatments: list[TreatmentResponse] = []

    model_config = {
        "from_attributes": True
    }