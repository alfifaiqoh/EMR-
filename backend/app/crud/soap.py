from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.soap import SOAP
from app.models.encounter import Encounter

from app.schemas.soap import (
    SOAPCreate,
    SOAPUpdate
)


def create_soap(
    db: Session,
    soap: SOAPCreate
):
    encounter = (
        db.query(Encounter)
        .filter(
            Encounter.id == soap.encounter_id
        )
        .first()
    )

    if not encounter:
        raise HTTPException(
            status_code=404,
            detail="Encounter not found"
        )

    db_soap = SOAP(
        **soap.model_dump()
    )

    db.add(db_soap)
    db.commit()
    db.refresh(db_soap)

    return db_soap

def get_soaps(db: Session):
    return db.query(SOAP).all()


def get_soap_by_id(
    db: Session,
    soap_id: int
):
    return (
        db.query(SOAP)
        .filter(SOAP.id == soap_id)
        .first()
    )


def update_soap(
    db: Session,
    soap_id: int,
    soap: SOAPUpdate
):
    db_soap = get_soap_by_id(
        db,
        soap_id
    )

    if not db_soap:
        return None

    update_data = soap.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_soap,
            key,
            value
        )

    db.commit()
    db.refresh(db_soap)

    return db_soap


def delete_soap(
    db: Session,
    soap_id: int
):
    db_soap = get_soap_by_id(
        db,
        soap_id
    )

    if not db_soap:
        return None

    db.delete(db_soap)
    db.commit()

    return True