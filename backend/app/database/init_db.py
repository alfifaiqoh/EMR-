from app.database.base import Base
from app.database.connection import engine

# import semua model
from app.models.patient import Patient
from app.models.user import User
from app.models.encounter import Encounter
from app.models.soap import SOAP
from app.models.diagnosis import Diagnosis
from app.models.treatment import Treatment
from app.models.practitioner import Practitioner

Base.metadata.create_all(bind=engine)

print("✅ Tables Created")

