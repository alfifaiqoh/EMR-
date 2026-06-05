from sqlalchemy.orm import Session

from app.models.treatment import Treatment

from app.schemas.treatment import (
    TreatmentCreate,
    TreatmentUpdate
)


def create_treatment(
    db: Session,
    treatment: TreatmentCreate
):
    db_treatment = Treatment(
        **treatment.model_dump()
    )

    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)

    return db_treatment


def get_treatments(db: Session):
    return db.query(Treatment).all()


def get_treatment_by_id(
    db: Session,
    treatment_id: int
):
    return (
        db.query(Treatment)
        .filter(
            Treatment.id == treatment_id
        )
        .first()
    )


def update_treatment(
    db: Session,
    treatment_id: int,
    treatment: TreatmentUpdate
):
    db_treatment = get_treatment_by_id(
        db,
        treatment_id
    )

    if not db_treatment:
        return None

    update_data = treatment.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_treatment,
            key,
            value
        )

    db.commit()
    db.refresh(db_treatment)

    return db_treatment


def delete_treatment(
    db: Session,
    treatment_id: int
):
    db_treatment = get_treatment_by_id(
        db,
        treatment_id
    )

    if not db_treatment:
        return None

    db.delete(db_treatment)
    db.commit()

    return True