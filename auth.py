from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["Authentication"])


class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/signup", status_code=201)
def signup(data: AuthRequest):
    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
        })

        if response.user is None:
            raise HTTPException(
                status_code=400,
                detail="Signup failed"
            )

        return {
            "message": "Signup successful",
            "user_id": response.user.id,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(data: AuthRequest):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password,
        })

        if response.session is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )