"""
================================================================================
TOPIC 05: JSON APIS & REQUEST VALIDATION (PYDANTIC V2)
================================================================================
Run command:
    uvicorn api_mastery.topic05_request_validation:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
KEY CONCEPTS:
- In production, NEVER trust client input!
- Schema-first validation intercepts invalid payloads BEFORE your DB/business code runs.
- Features demonstrated:
  1. Field bounds: ge=18 (greater than or equal), max_length=50.
  2. Built-in types: EmailStr, UUID, HttpUrl.
  3. Custom validation logic via `@field_validator`.
================================================================================
"""

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, field_validator
import re

app = FastAPI(title="Topic 05: Request Validation with Pydantic v2")

class EmployeeCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Full legal name")
    email: EmailStr = Field(..., description="Corporate email address")
    age: int = Field(..., ge=18, le=70, description="Must be working age (18 to 70)")
    pan_card: str = Field(..., description="Indian PAN Card format (e.g. ABCDE1234F)")
    department: str = Field(..., description="Sales, Engineering, or HR")

    # Custom Field Validator for PAN Card format
    @field_validator("pan_card")
    @classmethod
    def validate_pan(cls, value: str) -> str:
        value = value.strip().upper()
        pan_regex = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
        if not re.match(pan_regex, value):
            raise ValueError("Invalid PAN card format. Expected 5 letters, 4 digits, 1 letter (e.g. ABCDE1234F)")
        return value

    # Custom Validator for allowed department
    @field_validator("department")
    @classmethod
    def validate_dept(cls, value: str) -> str:
        allowed = {"Engineering", "Sales", "HR"}
        capitalized = value.strip().title()
        if capitalized not in allowed:
            raise ValueError(f"Department must be one of: {allowed}")
        return capitalized

@app.post("/employees", tags=["Validation"])
def onboard_employee(payload: EmployeeCreateSchema):
    """
    If any field fails validation:
    FastAPI immediately responds with 422 Unprocessable Entity and detailed error paths.
    """
    return {
        "status": "success",
        "message": f"Employee {payload.name} onboarded to {payload.department}",
        "data": payload.model_dump()
    }
