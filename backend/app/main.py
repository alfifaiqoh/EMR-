from fastapi import FastAPI
from sqlalchemy import text
from app.routers import auth
from app.database.connection import engine
from app.routers.patient import router as patient_router
from app.routers.encounter import (
    router as encounter_router
)
from fastapi.exceptions import (
    RequestValidationError
)

from app.routers.soap import (
    router as soap_router
)

from app.core.exception_handler import (
    validation_exception_handler
)

from app.routers.diagnosis import (
    router as diagnosis_router
)

from app.routers.treatment import (
    router as treatment_router
)

# Create FastAPI app
app = FastAPI(
    title="Oriskin EMR API",
    version="1.0.0"
)
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.include_router(auth.router)

app.include_router(
    encounter_router,
    prefix="/api/v1"
)

app.include_router(
    soap_router,
    prefix="/api/v1"
)

app.include_router(
    diagnosis_router,
    prefix="/api/v1"
)

app.include_router(
    treatment_router,
    prefix="/api/v1"
)

# Register routes
app.include_router(
    patient_router,
    prefix="/api/v1"
)


@app.get("/")
def root():
    return {
        "message": "Oriskin EMR API Running"
    }


@app.get("/health")
def health():
    db_status = "down"

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"

    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "app": "running",
        "database": db_status
    }


