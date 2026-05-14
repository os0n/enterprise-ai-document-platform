from pydantic import BaseModel, EmailStr


# =========================
# USER REGISTER SCHEMA
# =========================
class UserRegister(BaseModel):

    email: EmailStr

    full_name: str

    password: str


# =========================
# USER LOGIN SCHEMA
# =========================
class UserLogin(BaseModel):

    email: EmailStr

    password: str