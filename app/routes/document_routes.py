from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from sqlalchemy.orm import Session

from app.services.azure_document_service import analyze_invoice

from app.services.storage_service import (
    upload_file_to_blob,
    create_container_if_not_exists
)

from app.services.workflow_service import (
    apply_workflow_rules
)

from app.database.database import get_db

from app.database.models import (
    Document,
    User
)

from app.auth.security import get_current_user

import json
import uuid


router = APIRouter()

# =========================
# FILE VALIDATION
# =========================
ALLOWED_EXTENSIONS = [
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png"
]

ALLOWED_CONTENT_TYPES = [
    "application/pdf",
    "image/jpeg",
    "image/png"
]

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


# =========================
# ANALYZE INVOICE
# =========================
@router.post("/analyze-invoice")
async def analyze_invoice_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # =========================
    # FILE EXTENSION VALIDATION
    # =========================
    file_extension = f".{file.filename.split('.')[-1].lower()}"

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed types: {ALLOWED_EXTENSIONS}"
        )

    # =========================
    # MIME TYPE VALIDATION
    # =========================
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file content type."
        )

    # =========================
    # READ FILE
    # =========================
    file_bytes = await file.read()

    # =========================
    # FILE SIZE VALIDATION
    # =========================
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10MB limit."
        )

    # =========================
    # UNIQUE FILE NAME
    # =========================
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    # =========================
    # CREATE CONTAINER
    # =========================
    create_container_if_not_exists()

    # =========================
    # UPLOAD TO AZURE BLOB
    # =========================
    file_url = upload_file_to_blob(
        file_bytes,
        unique_filename
    )

    # =========================
    # ANALYZE DOCUMENT
    # =========================
    result = analyze_invoice(file_bytes)

    # =========================
    # APPLY WORKFLOW RULES
    # =========================
    workflow_result = apply_workflow_rules(
        result
    )

    # =========================
    # SAVE TO DATABASE
    # =========================
    document = Document(
        filename=file.filename,
        file_url=file_url,
        document_type="invoice",
        extracted_data=json.dumps(result, default=str),
        workflow_status=workflow_result["status"],
        workflow_reason=workflow_result["reason"],
        user_id=current_user.id
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    # =========================
    # API RESPONSE
    # =========================
    return {
        "status": "success",
        "document_id": document.id,
        "filename": file.filename,
        "file_url": file_url,
        "uploaded_by": current_user.email,
        "workflow": workflow_result,
        "extracted_data": result
    }


# =========================
# GET USER DOCUMENTS
# =========================
@router.get("/documents")
async def get_all_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    documents = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .all()
    )

    return {
        "status": "success",
        "total": len(documents),
        "documents": documents
    }


# =========================
# GET SINGLE DOCUMENT
# =========================
@router.get("/documents/{document_id}")
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == current_user.id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return {
        "status": "success",
        "document": document
    }