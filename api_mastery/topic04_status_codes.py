"""
================================================================================
TOPIC 04: HTTP STATUS CODES & THE 5 FAMILIES
================================================================================
Run command:
    uvicorn api_mastery.topic04_status_codes:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
CRUCIAL INTERVIEW QUESTIONS:
1. 401 Unauthorized vs 403 Forbidden:
   - 401 = Unauthenticated ("Who are you? Token is missing or invalid").
   - 403 = Unauthorized ("I know who you are, but you lack permission to do this").
2. 400 Bad Request vs 422 Unprocessable Entity:
   - 400 = Malformed request syntax (e.g. broken JSON syntax).
   - 422 = Valid JSON syntax, but violates business/type rules (e.g. age must be > 18).
3. When to use 201 vs 204?
   - 201 = Resource created (POST). Return created item or its URI.
   - 204 = Action completed successfully with NO return body (DELETE or empty action).
4. When to use 409 Conflict?
   - Business conflict (e.g. registering with an email that is already taken).
================================================================================
"""

from fastapi import FastAPI, HTTPException, status, Header, Response
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict

app = FastAPI(title="Topic 04: HTTP Status Codes Explained")

USERS: Dict[str, dict] = {
    "admin@company.com": {"email": "admin@company.com", "role": "ADMIN"},
    "intern@company.com": {"email": "intern@company.com", "role": "INTERN"}
}

class RegisterRequest(BaseModel):
    email: EmailStr
    name: str

@app.post("/register", status_code=status.HTTP_201_CREATED, tags=["Status Codes"])
def register_user(payload: RegisterRequest):
    """
    Returns 201 Created on success.
    Returns 409 Conflict if user email already exists.
    """
    if payload.email in USERS:
        # 409 Conflict: Business state collision
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{payload.email}' is already registered."
        )
    
    USERS[payload.email] = {"email": payload.email, "role": "USER", "name": payload.name}
    return {"message": "User registered", "email": payload.email}

@app.delete("/users/{email}", status_code=status.HTTP_204_NO_CONTENT, tags=["Status Codes"])
def delete_user(email: str):
    """
    Returns 204 No Content: Successful deletion with empty response body.
    """
    if email not in USERS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    del USERS[email]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/admin/salary-data", tags=["Status Codes"])
def get_confidential_salaries(authorization: Optional[str] = Header(None)):
    """
    Demonstrates 401 Unauthorized vs 403 Forbidden:
    - If no header is sent -> 401 Unauthorized (Who are you?)
    - If non-admin token sent -> 403 Forbidden (You don't have permission!)
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token missing. Please supply Authorization header."
        )
    
    # Simulate token check
    if "intern-token" in authorization:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Interns are not permitted to view salary metrics."
        )

    return {"secret_salaries": {"CEO": 5000000, "VP": 3500000}}
