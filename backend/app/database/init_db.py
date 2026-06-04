from app.database.base import Base
from app.database.connection import engine

# import semua model
from app.models.patient import Patient

Base.metadata.create_all(bind=engine)

print("✅ Tables Created")