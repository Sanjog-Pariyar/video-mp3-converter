from fastapi import APIRouter, HTTPException, Form, Request

import httpx
from app.schemas import UserRegister


router = APIRouter(prefix='/user', tags=["users"])

auth_service="http://auth-service:8000"

@router.post('/register')
async def register(user_in: UserRegister):
    register_url = f"{auth_service}/users/signup"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(register_url, json=user_in.dict(), timeout=10.0)
        except httpx.RequestError as exc:
            # Network-level errors (e.g., service down or unreachable)
            raise HTTPException(
                status_code=503,
                detail=f"Auth service not reachable: {exc}"
            )

    # Check HTTP status codes
    if response.status_code == 200 or response.status_code == 201:
        return {
            "success": True,
            "message": "User registered successfully",
            "data": response.json(),
        }
    else:
        # Try to extract error details from auth-service
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text

        raise HTTPException(
            status_code=response.status_code,
            detail={
                "success": False,
                "message": "User registration failed",
                "error": error_detail,
            },
        )


@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    """
    Forward login request to auth-service and return its response.
    """

    # Internal Docker network URL for auth-service
    login_url = f"{auth_service}/login/access-token"

    # Prepare OAuth2PasswordRequestForm-compatible payload
    data = {
        "username": email,
        "password": password,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(login_url, data=data, timeout=10.0)
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Auth service not reachable: {exc}"
            )

    # Handle response
    if response.status_code == 200:
        return {
            "success": True,
            "message": "Login successful",
            "data": response.json(),
        }
    else:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text

        raise HTTPException(
            status_code=response.status_code,
            detail={
                "success": False,
                "message": "Login failed",
                "error": error_detail,
            },
        )

@router.get("/me")
async def current_user(request: Request):
    """
    Forward the request to auth-service with the Authorization header
    """
    current_user_url = f"{auth_service}/users/me"

    # Get the Authorization header from the incoming request
    headers = {}
    auth_header = request.headers.get("Authorization")
    if auth_header:
        headers["Authorization"] = auth_header

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(current_user_url, headers=headers, timeout=10.0)
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Auth service not reachable: {exc}"
            )

    if response.status_code == 200:
        return response.json()
    else:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text

        raise HTTPException(
            status_code=response.status_code,
            detail=error_detail,
        )