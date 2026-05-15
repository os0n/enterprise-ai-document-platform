import requests
import streamlit as st


# =========================
# API URLS
# =========================
BASE_URL = st.secrets["API_BASE_URL"]

REGISTER_API = (
    f"{BASE_URL}/api/v1/auth/register"
)

LOGIN_API = (
    f"{BASE_URL}/api/v1/auth/login"
)


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
        data=data,
        timeout=60
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
        json=payload,
        timeout=60
    )

    return response