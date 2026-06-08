from sqlalchemy.orm import Session

from app.models.practitioner import Practitioner

from app.schemas.practitioner import (
    PractitionerCreate,
    PractitionerUpdate
)


def create_practitioner(
    db: Session,
    practitioner: PractitionerCreate
):
    db_practitioner = Practitioner(
        full_name=practitioner.full_name,
        nik=practitioner.nik,
        sip_number=practitioner.sip_number,
        str_number=practitioner.str_number,
        specialization=practitioner.specialization
    )

    db.add(db_practitioner)
    db.commit()
    db.refresh(db_practitioner)

    return db_practitioner


def get_practitioners(
    db: Session,
    search: str = None,
    page: int = 1,
    limit: int = 10
):
    query = db.query(Practitioner)

    if search:
        query = query.filter(
            Practitioner.full_name.ilike(
                f"%{search}%"
            )
        )

    skip = (
        page - 1
    ) * limit

    return (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_practitioner(
    db: Session,
    practitioner_id: int
):
    return (
        db.query(Practitioner)
        .filter(
            Practitioner.id == practitioner_id
        )
        .first()
    )


def update_practitioner(
    db: Session,
    practitioner_id: int,
    practitioner: PractitionerUpdate
):
    db_practitioner = get_practitioner(
        db,
        practitioner_id
    )

    if not db_practitioner:
        return None

    update_data = practitioner.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_practitioner,
            key,
            value
        )

    db.commit()
    db.refresh(db_practitioner)

    return db_practitioner


def delete_practitioner(
    db: Session,
    practitioner_id: int
):
    db_practitioner = get_practitioner(
        db,
        practitioner_id
    )

    if not db_practitioner:
        return None

    db.delete(db_practitioner)
    db.commit()

    return True