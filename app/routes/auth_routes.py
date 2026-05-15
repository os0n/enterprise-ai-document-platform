from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session

from sqlalchemy.exc import SQLAlchemyError

from app.database.database import get_db

from app.database.models import User

from app.schemas.user_schema import UserRegister

from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter()


# =========================
# REGISTER
# =========================
@router.post("/register")
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    try:

        existing_user = (
            db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_user:

            raise HTTPException(
                status_code=400,
                detail="Email already registered."
            )

        hashed_password = hash_password(
            user.password
        )

        new_user = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password
        )

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        return {
            "message": "User registered successfully."
        }

    except HTTPException:
        raise

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Server Error: {str(e)}"
        )


# =========================
# LOGIN
# =========================
@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    try:

        existing_user = (
            db.query(User)
            .filter(User.email == form_data.username)
            .first()
        )

        if not existing_user:

            raise HTTPException(
                status_code=401,
                detail="Invalid email or password."
            )

        valid_password = verify_password(
            form_data.password,
            existing_user.hashed_password
        )

        if not valid_password:

            raise HTTPException(
                status_code=401,
                detail="Invalid email or password."
            )

        access_token = create_access_token({
            "sub": existing_user.email
        })

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Login Error: {str(e)}"
        )