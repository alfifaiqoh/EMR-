from fastapi import FastAPI
from sqlalchemy import text

from app.database.connection import engine
from app.routers.patient import router as patient_router

# Create FastAPI app
app = FastAPI(
    title="Oriskin EMR API",
    version="1.0.0"
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