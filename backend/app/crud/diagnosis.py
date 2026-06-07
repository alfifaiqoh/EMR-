from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.soap import SOAP
from app.models.diagnosis import Diagnosis

from app.schemas.diagnosis import (
    DiagnosisCreate,
    DiagnosisUpdate
)


def create_diagnosis(
    db: Session,
    diagnosis: DiagnosisCreate
):
    soap = (
        db.query(SOAP)
        .filter(
            SOAP.id == diagnosis.soap_id
        )
        .first()
    )

    if not soap:
        raise HTTPException(
            status_code=404,
            detail="SOAP not found"
        )

    db_diagnosis = Diagnosis(
        **diagnosis.model_dump()
    )

    db.add(db_diagnosis)
    db.commit()
    db.refresh(db_diagnosis)

    return db_diagnosis


def get_diagnoses(db: Session):
    return db.query(Diagnosis).all()


def get_diagnosis_by_id(
    db: Session,
    diagnosis_id: int
):
    return (
        db.query(Diagnosis)
        .filter(
            Diagnosis.id == diagnosis_id
        )
        .first()
    )


def update_diagnosis(
    db: Session,
    diagnosis_id: int,
    diagnosis: DiagnosisUpdate
):
    db_diagnosis = get_diagnosis_by_id(
        db,
        diagnosis_id
    )

    if not db_diagnosis:
        return None

    update_data = diagnosis.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_diagnosis,
            key,
            value
        )

    db.commit()
    db.refresh(db_diagnosis)

    return db_diagnosis


def delete_diagnosis(
    db: Session,
    diagnosis_id: int
):
    db_diagnosis = get_diagnosis_by_id(
        db,
        diagnosis_id
    )

    if not db_diagnosis:
        return None

    db.delete(db_diagnosis)
    db.commit()

    return True