import requests
import streamlit as st


# =========================
# API URLS
# =========================
BASE_URL = st.secrets["API_BASE_URL"]

DOCUMENTS_API = (
    f"{BASE_URL}/api/v1/documents/documents"
)

ANALYZE_API = (
    f"{BASE_URL}/api/v1/documents/analyze-invoice"
)


# =========================
# AUTH HEADERS
# =========================
def get_auth_headers(token):

    return {
        "Authorization": f"Bearer {token}"
    }


# =========================
# LOAD DOCUMENTS
# =========================
def load_documents(token):

    response = requests.get(
        DOCUMENTS_API,
        headers=get_auth_headers(token),
        timeout=60
    )

    return response


# =========================
# ANALYZE DOCUMENT
# =========================
def analyze_document(
    token,
    uploaded_file
):

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    response = requests.post(
        ANALYZE_API,
        files=files,
        headers=get_auth_headers(token),
        timeout=120
    )

    return response