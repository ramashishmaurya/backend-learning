"""
================================================================================
TOPIC 08: OPENAPI & INTERACTIVE API DOCUMENTATION
================================================================================
Run command:
    uvicorn api_mastery.topic08_openapi_documentation:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
Visit ReDoc:
    http://localhost:8000/redoc
================================================================================
WHAT IS OPENAPI (OAS)?
- OpenAPI Specification (OAS 3.0 / 3.1) is a machine-readable JSON/YAML standard
  that describes the entire API surface: endpoints, query params, schemas, security.
- FastAPI automatically generates `/openapi.json` behind the scenes!
- Tools like Swagger UI and ReDoc read this JSON to render interactive documentation.
================================================================================
"""

from fastapi import FastAPI, status
from pydantic import BaseModel, Field

# Enriching FastAPI app with rich OpenAPI metadata
app = FastAPI(
    title="E-Commerce Payment Gateway API",
    description="""
## Production Payment Gateway
This API allows merchant partners to initiate payments, verify transactions,
and inspect audit logs.

### Key Highlights:
- **PCI-DSS Compliant** payloads
- **Interactive Testing** via Swagger UI
    """,
    version="2.4.0",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "Backend Platform Engineering Team",
        "email": "backend-support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)

class PaymentInitiateRequest(BaseModel):
    order_id: str = Field(..., example="ord_882194", description="Merchant order reference")
    amount_inr: float = Field(..., gt=0, example=1999.00, description="Amount in Indian Rupees")
    customer_email: str = Field(..., example="buyer@example.com")

class PaymentResponse(BaseModel):
    transaction_id: str = Field(..., example="txn_77192847")
    status: str = Field(..., example="PENDING_CAPTURE")
    checkout_url: str = Field(..., example="https://pay.gateway.com/checkout/txn_77192847")

@app.post(
    "/v1/payments/initiate",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Payments & Billing"],
    summary="Initiate Merchant Payment",
    description="Creates a secure payment transaction session and returns a hosted checkout URL."
)
def initiate_payment(payload: PaymentInitiateRequest):
    return PaymentResponse(
        transaction_id="txn_77192847",
        status="PENDING_CAPTURE",
        checkout_url="https://pay.gateway.com/checkout/txn_77192847"
    )
