import requests


# =========================
# API URLS
# =========================
BASE_URL = "https://enterprise-ai-document-platform.onrender.com"
DOCUMENTS_API = f"{BASE_URL}/api/v1/documents/documents"

ANALYZE_API = f"{BASE_URL}/api/v1/documents/analyze-invoice"


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
        headers=get_auth_headers(token)
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
        headers=get_auth_headers(token)
    )

    return response