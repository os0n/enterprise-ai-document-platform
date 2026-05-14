from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.database import Base


# =========================
# DOCUMENT MODEL
# =========================
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(
        String,
        nullable=False
    )

    file_url = Column(
        String,
        nullable=False
    )

    document_type = Column(
        String,
        nullable=False
    )

    extracted_data = Column(
        Text,
        nullable=True
    )

    status = Column(
        String,
        default="processed"
    )

    # =========================
    # WORKFLOW STATUS
    # =========================
    workflow_status = Column(
        String,
        default="pending"
    )

    workflow_reason = Column(
        String,
        nullable=True
    )

    # =========================
    # USER RELATION
    # =========================
    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="documents"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )


# =========================
# USER MODEL
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    full_name = Column(
        String,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="user"
    )

    # =========================
    # DOCUMENT RELATION
    # =========================
    documents = relationship(
        "Document",
        back_populates="owner"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )