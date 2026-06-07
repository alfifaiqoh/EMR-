from fastapi import HTTPException

from app.models.encounter import Encounter
from app.models.soap import SOAP
from app.models.diagnosis import Diagnosis
from app.models.treatment import Treatment


def get_encounter_summary(
    db,
    encounter_id: int
):
    encounter = (
        db.query(Encounter)
        .filter(
            Encounter.id == encounter_id
        )
        .first()
    )

    if not encounter:
        raise HTTPException(
            status_code=404,
            detail="Encounter not found"
        )

    soap = (
        db.query(SOAP)
        .filter(
            SOAP.encounter_id == encounter_id
        )
        .first()
    )

    diagnoses = []
    treatments = []

    if soap:
        diagnoses = (
            db.query(Diagnosis)
            .filter(
                Diagnosis.soap_id == soap.id
            )
            .all()
        )

        treatments = (
            db.query(Treatment)
            .filter(
                Treatment.soap_id == soap.id
            )
            .all()
        )

    return {
        "patient": encounter.patient,
        "encounter": encounter,
        "soap": soap,
        "diagnoses": diagnoses,
        "treatments": treatments
    }