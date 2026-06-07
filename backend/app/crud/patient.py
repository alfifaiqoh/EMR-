from sqlalchemy.orm import (
    Session,
    joinedload
)

from app.models.patient import Patient
from app.models.encounter import Encounter
from app.models.soap import SOAP

from app.schemas.patient import (
    PatientCreate,
    PatientUpdate
)


def create_patient(
    db: Session,
    patient: PatientCreate
):
    existing_patient = (
        db.query(Patient)
        .filter(
            Patient.nik == patient.nik
        )
        .first()
    )

    if existing_patient:
        return None

    db_patient = Patient(
        nik=patient.nik,
        fullname=patient.full_name,
        gender=patient.gender,
        phone=patient.phone
    )

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return db_patient


def get_patients(
    db: Session,
    search: str = None,
    page: int = 1,
    limit: int = 10
):
    query = db.query(Patient)

    if search:
        query = query.filter(
            (Patient.fullname.ilike(
                f"%{search}%"
            ))
            |
            (Patient.nik.ilike(
                f"%{search}%"
            ))
        )

    skip = (
        page - 1
    ) * limit

    patients = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return patients


def get_patient(
    db: Session,
    patient_id: int
):
    return (
        db.query(Patient)
        .filter(
            Patient.id == patient_id
        )
        .first()
    )


def update_patient(
    db: Session,
    patient_id: int,
    patient: PatientUpdate
):
    db_patient = get_patient(
        db,
        patient_id
    )

    if not db_patient:
        return None

    update_data = patient.model_dump(
        exclude_unset=True
    )

    field_mapping = {
        "full_name": "fullname"
    }

    for key, value in update_data.items():

        db_field = field_mapping.get(
            key,
            key
        )

        setattr(
            db_patient,
            db_field,
            value
        )

    db.commit()
    db.refresh(db_patient)

    return db_patient


def delete_patient(
    db: Session,
    patient_id: int
):
    db_patient = get_patient(
        db,
        patient_id
    )

    if not db_patient:
        return None

    db.delete(db_patient)
    db.commit()

    return True


def get_patient_history(
    db: Session,
    patient_id: int
):
    patient = (
        db.query(Patient)
        .options(
            joinedload(
                Patient.encounters
            )
            .joinedload(
                Encounter.soaps
            )
            .joinedload(
                SOAP.diagnoses
            ),

            joinedload(
                Patient.encounters
            )
            .joinedload(
                Encounter.soaps
            )
            .joinedload(
                SOAP.treatments
            )
        )
        .filter(
            Patient.id == patient_id
        )
        .first()
    )

    return patient