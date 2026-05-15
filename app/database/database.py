from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from app.config.settings import DATABASE_URL


# =========================
# SQLALCHEMY ENGINE
# =========================
engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True,

    pool_recycle=300,

    pool_size=5,

    max_overflow=10
)


# =========================
# SESSION LOCAL
# =========================
SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine
)


# =========================
# BASE MODEL
# =========================
Base = declarative_base()


# =========================
# DATABASE DEPENDENCY
# =========================
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()