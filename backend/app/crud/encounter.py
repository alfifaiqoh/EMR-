from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.models.encounter import Encounter

from app.schemas.encounter import EncounterCreate


def create_encounter(
    db: Session,
    encounter: EncounterCreate,
    doctor_id: int
):
    patient = (
        db.query(Patient)
        .filter(
            Patient.id == encounter.patient_id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db_encounter = Encounter(
        **encounter.model_dump(),
        doctor_id=doctor_id
    )

    db.add(db_encounter)
    db.commit()
    db.refresh(db_encounter)

    return db_encounter

def get_encounters(db: Session):
    return db.query(Encounter).all()


def get_encounter_by_id(
    db: Session,
    encounter_id: int
):
    return (
        db.query(Encounter)
        .filter(Encounter.id == encounter_id)
        .first()
    )


def update_encounter(
    db: Session,
    encounter_id: int,
    encounter: EncounterUpdate
):
    db_encounter = get_encounter_by_id(
        db,
        encounter_id
    )

    if not db_encounter:
        return None

    update_data = encounter.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_encounter,
            key,
            value
        )

    db.commit()
    db.refresh(db_encounter)

    return db_encounter


def delete_encounter(
    db: Session,
    encounter_id: int
):
    db_encounter = get_encounter_by_id(
        db,
        encounter_id
    )

    if not db_encounter:
        return None

    db.delete(db_encounter)
    db.commit()

    return True
