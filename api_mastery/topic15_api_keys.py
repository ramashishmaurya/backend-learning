"""
================================================================================
TOPIC 15: API KEY AUTHENTICATION (MACHINE-TO-MACHINE)
================================================================================
Run command:
    uvicorn api_mastery.topic15_api_keys:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
HOW MACHINE-TO-MACHINE (M2M) API KEYS WORK:
- Used by external developer partners, scripts, or server-to-server integrations (e.g. OpenAI `sk-...`, Stripe `rk_live_...`).
- Passed in headers: `X-API-Key: <key>` or `Authorization: Bearer <key>`.

CRITICAL SECURITY RULE:
- NEVER store raw API keys in your database!
  If an attacker dumps your database, they steal all client keys.
- Store `SHA-256(api_key)` in your DB.
  When a request arrives: Hash the incoming key and look up the hash.
================================================================================
"""

import hashlib
from typing import Optional, Dict
from fastapi import FastAPI, HTTPException, Security, status, Depends
from fastapi.security.api_key import APIKeyHeader

app = FastAPI(title="Topic 15: Secure API Key Authentication")

# Simulated Database of Hashed API Keys:
# In real life, when a partner generates a key, they see it ONCE: "sk_live_enterprise_secret_999"
# We store ONLY its SHA-256 hash:
RAW_KEY_FOR_TESTING = "sk_live_enterprise_secret_999"
HASHED_KEY = hashlib.sha256(RAW_KEY_FOR_TESTING.encode("utf-8")).hexdigest()

PARTNER_DB: Dict[str, dict] = {
    HASHED_KEY: {
        "client_name": "Flipkart Logistics Partner",
        "tier": "Enterprise Tier",
        "rate_limit_rpm": 5000
    }
}

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def authenticate_api_key(api_key: Optional[str] = Security(api_key_header)) -> dict:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing required header 'X-API-Key'"
        )

    # Hash incoming key with SHA-256
    incoming_hash = hashlib.sha256(api_key.encode("utf-8")).hexdigest()
    client_record = PARTNER_DB.get(incoming_hash)

    if not client_record:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid or revoked API key"
        )
    return client_record

@app.get("/api/partner/shipments", tags=["Protected Partner Routes"])
def get_partner_shipments(client: dict = Depends(authenticate_api_key)):
    """
    To test in Swagger or cURL:
    Send header: `X-API-Key: sk_live_enterprise_secret_999`
    """
    return {
        "authenticated_client": client["client_name"],
        "tier": client["tier"],
        "active_shipments": [
            {"shipment_id": "SHP-8812", "status": "IN_TRANSIT", "destination": "Bengaluru"},
            {"shipment_id": "SHP-8813", "status": "DELIVERED", "destination": "Mumbai"},
        ]
    }
