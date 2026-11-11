"""
================================================================================
TOPIC 06: RESPONSE DESIGN & RFC 7807 ERROR ENVELOPES
================================================================================
Run command:
    uvicorn api_mastery.topic06_response_and_errors:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
BEST PRACTICES:
1. CONSISTENT SUCCESS ENVELOPE:
   - Frontend developers don't have to guess response structures.
   - Standard keys: { "success": true, "message": "...", "data": {...}, "timestamp": "..." }
2. DATA HIDING VIA RESPONSE SCHEMAS:
   - Use FastAPI's `response_model` to automatically filter out internal passwords, tokens, or private flags.
3. STANDARDIZED ERROR FORMAT (RFC 7807 Problem Details):
   - Never send random error strings.
   - Include error_code, details array, and `request_id` for instant production log tracing.
================================================================================
"""

import uuid
from datetime import datetime, timezone
from typing import Generic, Optional, TypeVar, List
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Topic 06: Response & Error Envelopes")

T = TypeVar("T")

# 1. Standard Success Envelope
class StandardResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: Optional[T] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# 2. Standard Error Details (RFC 7807 style)
class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str

class ErrorResponse(BaseModel):
    success: bool = False
    error_code: str
    message: str
    details: Optional[List[ErrorDetail]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    request_id: str

# 3. Data Hiding Model (Does NOT include hashed_password or internal_role)
class UserPublicProfile(BaseModel):
    id: str
    name: str
    email: EmailStr

# --- GLOBAL ERROR HANDLERS ---
@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    """Intercepts Pydantic 422 errors and formats into our standard envelope"""
    err_list = []
    for err in exc.errors():
        loc = ".".join(str(l) for l in err.get("loc", []) if l != "body")
        err_list.append(ErrorDetail(field=loc or "body", message=err.get("msg", "Invalid")))

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error_code="VALIDATION_ERROR",
            message="Input data validation failed",
            details=err_list,
            request_id=f"req_{uuid.uuid4().hex[:8]}",
        ).model_dump(mode="json")
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Intercepts HTTPExceptions and formats into our standard envelope"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_code=f"HTTP_{exc.status_code}",
            message=str(exc.detail),
            request_id=f"req_{uuid.uuid4().hex[:8]}",
        ).model_dump(mode="json")
    )

# --- ROUTES ---
@app.get("/users/{user_id}", response_model=StandardResponse[UserPublicProfile], tags=["Response Design"])
def get_user_profile(user_id: str):
    """
    Demonstrates:
    1. Returns standard envelope.
    2. Even though internal DB record has password_hash and salary, response_model hides them!
    """
    if user_id != "usr_101":
        raise HTTPException(status_code=404, detail="User account not found")

    # Raw database row with sensitive internal attributes
    raw_db_row = {
        "id": "usr_101",
        "name": "Vikram Seth",
        "email": "vikram@example.com",
        "password_hash": "$2b$12$e9XU1...sensitive...hash",
        "monthly_salary": 250000,
        "is_superadmin": True,
    }

    # Automatically filtered by UserPublicProfile!
    return StandardResponse(
        message="User profile retrieved",
        data=raw_db_row
    )
