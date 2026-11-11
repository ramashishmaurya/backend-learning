"""
================================================================================
TOPIC 16: WEBHOOKS & HMAC-SHA256 SIGNATURE VERIFICATION
================================================================================
Run command:
    uvicorn api_mastery.topic16_webhooks:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
WHAT ARE WEBHOOKS?
- Reverse API (Push model): Instead of the client polling your server every 3 seconds
  ("Did payment succeed yet? Did payment succeed yet?"),
  your server pushes an HTTP POST request to the client's webhook URL as soon as the event happens!

HOW TO SECURE WEBHOOKS (THE HMAC-SHA256 SIGNATURE):
- Problem: An attacker could send a fake POST request to the client saying:
  `{"order_id": "123", "status": "PAID"}`. The client would ship goods for free!
- Solution:
  1. Server & Client share a webhook secret (e.g. `whsec_mysecret123`).
  2. Server signs the raw JSON body: `signature = HMAC_SHA256(secret, raw_body)`.
  3. Server sends header: `X-Webhook-Signature: <hex_signature>`.
  4. Client recomputes signature on raw bytes and verifies it with `hmac.compare_digest()`.
================================================================================
"""

import hmac
import hashlib
import json
import time
from typing import Optional
from fastapi import FastAPI, Request, Header, HTTPException, status

app = FastAPI(title="Topic 16: Webhook Delivery & HMAC Signature Verification")

WEBHOOK_SHARED_SECRET = "whsec_super_secret_signing_key_456"

# 1. SENDER SIMULATOR (How your server generates signed events)
@app.post("/webhooks/simulate-event-dispatch", tags=["Webhook Dispatcher"])
def simulate_webhook_dispatch(event_type: str = "payment.captured"):
    """
    Simulates your backend triggering an event.
    Returns the exact payload and HMAC-SHA256 signature to test the receiver!
    """
    event_payload = {
        "event_id": f"evt_{int(time.time())}",
        "event_type": event_type,
        "created_at": int(time.time()),
        "data": {
            "order_id": "ord_99012",
            "amount_paid": 5499.00,
            "currency": "INR"
        }
    }
    # Raw payload bytes
    raw_bytes = json.dumps(event_payload, separators=(',', ':')).encode("utf-8")

    # Generate HMAC-SHA256 signature
    signature = hmac.new(
        key=WEBHOOK_SHARED_SECRET.encode("utf-8"),
        msg=raw_bytes,
        digestmod=hashlib.sha256
    ).hexdigest()

    return {
        "instructions": "Copy 'generated_signature' and pass it in header 'X-Webhook-Signature' to /webhooks/incoming-receiver",
        "generated_signature": signature,
        "raw_json_payload": event_payload
    }

# 2. RECEIVER (How clients verify incoming webhook authenticity)
@app.post("/webhooks/incoming-receiver", tags=["Webhook Receiver"])
async def receive_webhook(
    request: Request,
    x_webhook_signature: Optional[str] = Header(None, alias="X-Webhook-Signature")
):
    if not x_webhook_signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing required header 'X-Webhook-Signature'"
        )

    # Read raw body bytes
    raw_body = await request.body()

    # Recompute expected signature
    expected_signature = hmac.new(
        key=WEBHOOK_SHARED_SECRET.encode("utf-8"),
        msg=raw_body,
        digestmod=hashlib.sha256
    ).hexdigest()

    # Constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(expected_signature, x_webhook_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature verification failed! Payload has been tampered with or secret is wrong."
        )

    event_data = json.loads(raw_body.decode("utf-8"))
    return {
        "status": "verified_and_processed",
        "event_id": event_data.get("event_id"),
        "event_type": event_data.get("event_type"),
        "message": "Webhook authenticated successfully via HMAC-SHA256!"
    }
