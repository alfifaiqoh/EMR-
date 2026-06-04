import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔥 HARUS PALING ATAS
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("DEBUG DATABASE_URL =", DATABASE_URL)  # 🔥 sementara untuk cek

if not DATABASE_URL:
    raise Exception("DATABASE_URL tidak terbaca dari .env")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()