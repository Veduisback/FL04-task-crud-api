from fastapi import APIRouter, Header, HTTPException

from supabase_client import supabase

router = APIRouter(tags=["Protected"])


@router.get("/public/info")
def public_info():
    return {
        "message": "This is public information",
        "authenticated": False,
    }


@router.get("/protected/profile")
def protected_profile(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Bearer token required"
        )

    token = authorization.removeprefix("Bearer ").strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Bearer token required"
        )

    try:
        response = supabase.auth.get_user(token)

        if response.user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        return {
            "message": "Protected profile",
            "authenticated": True,
            "user_id": response.user.id,
            "email": response.user.email,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )