from fastapi import APIRouter, Header, HTTPException

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

    return {
        "message": "Protected profile",
        "authenticated": True,
    }