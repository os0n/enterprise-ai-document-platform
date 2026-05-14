import requests


# =========================
# API URLS
# =========================
BASE_URL = "http://127.0.0.1:8000"

LOGIN_API = f"{BASE_URL}/api/v1/auth/login"

REGISTER_API = f"{BASE_URL}/api/v1/auth/register"


# =========================
# LOGIN USER
# =========================
def login_user(email, password):

    data = {
        "username": email,
        "password": password
    }

    response = requests.post(
        LOGIN_API,
        data=data
    )

    return response


# =========================
# REGISTER USER
# =========================
def register_user(
    email,
    full_name,
    password
):

    payload = {
        "email": email,
        "full_name": full_name,
        "password": password
    }

    response = requests.post(
        REGISTER_API,
        json=payload
    )

    return response