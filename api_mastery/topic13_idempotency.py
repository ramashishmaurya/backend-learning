"""
================================================================================
TOPIC 13: IDEMPOTENCY (THE STRIPE DUPLICATE-PROTECTION PATTERN)
================================================================================
Run command:
    uvicorn api_mastery.topic13_idempotency:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
THE PROBLEM:
- A customer clicks "Pay ₹5,000".
- Their mobile network drops before the HTTP 200 response reaches their phone.
- The user thinks it failed and clicks "Pay" again!
- Without idempotency, the user gets charged ₹10,000 (disaster!).

HOW STRIPE-STYLE IDEMPOTENCY WORKS:
1. Client generates a UUID and sends header: `Idempotency-Key: 9b1deb4d-3b7d...`
2. Server checks Redis/Cache:
   - If key status == "PROCESSING": Return 409 Conflict (request currently in flight).
   - If key status == "COMPLETED": Return cached response directly without charging!
3. If new key:
   - Lock key with status "PROCESSING" (with short TTL e.g. 120s).
   - Charge bank / DB transaction.
   - Cache result in Redis for 24h with status "COMPLETED".
================================================================================
"""

import time
import uuid
from typing import Optional, Dict, Any
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Topic 13: Idempotent Payment Processing")

# In production, this dictionary is a distributed Redis cluster with TTL
IDEMPOTENCY_CACHE: Dict[str, Dict[str, Any]] = {}

class PaymentChargeRequest(BaseModel):
    user_id: str
    amount: float = Field(..., gt=0)
    order_id: str

@app.post("/payments/charge", tags=["Idempotency"])
def process_payment(
    payload: PaymentChargeRequest,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key", description="Unique client UUID")
):
    if not idempotency_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Header 'Idempotency-Key' is mandatory for state-altering financial endpoints"
        )

    # 1. Check if this key was already seen
    cached_record = IDEMPOTENCY_CACHE.get(idempotency_key)
    if cached_record:
        if cached_record["status"] == "PROCESSING":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A concurrent transaction with this Idempotency-Key is currently in progress."
            )
        # Replay cached result! No double billing!
        return {
            "idempotency_replay": True,
            "message": "Transaction already executed. Returning cached receipt.",
            "data": cached_record["response"]
        }

    # 2. Acquire in-flight lock (In Redis: SET key PROCESSING NX EX 120)
    IDEMPOTENCY_CACHE[idempotency_key] = {"status": "PROCESSING", "created_at": time.time()}

    # 3. Simulate processing time & external bank charge
    time.sleep(0.1)
    transaction_id = f"txn_{uuid.uuid4().hex[:10]}"
    receipt = {
        "transaction_id": transaction_id,
        "order_id": payload.order_id,
        "user_id": payload.user_id,
        "amount_charged": payload.amount,
        "status": "SETTLED"
    }

    # 4. Save completed response in cache (In Redis: SET key COMPLETED EX 86400)
    IDEMPOTENCY_CACHE[idempotency_key] = {
        "status": "COMPLETED",
        "response": receipt
    }

    return {
        "idempotency_replay": False,
        "message": "Payment successfully charged for the first time.",
        "data": receipt
    }
