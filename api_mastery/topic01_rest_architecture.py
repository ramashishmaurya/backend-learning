"""
================================================================================
TOPIC 01: REST ARCHITECTURE & CONSTRAINTS
================================================================================
Run command:
    uvicorn api_mastery.topic01_rest_architecture:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
INTERVIEW SUMMARY:
- Coined by Roy Fielding (2000).
- REST (Representational State Transfer) is an ARCHITECTURAL STYLE, not a protocol!
- 6 Core Constraints:
  1. Client-Server: Decouples UI from data storage.
  2. Stateless: Server stores NO client session state. Every request contains full authentication & context.
  3. Cacheable: Responses explicitly state if they can be cached (ETags, Cache-Control).
  4. Uniform Interface: Standard URIs, standard HTTP verbs, standard JSON payloads.
  5. Layered System: Client doesn't know if it connects directly to the server or via proxies/load balancers.
  6. Code on Demand (Optional): Server temporarily extending client functionality (e.g. scripts).
================================================================================
"""

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Topic 01: REST Architecture Principles",
    description="Demonstrates REST Statelessness and Uniform Interface constraints."
)

# Stateless Simulation: We authenticate each request independently via a Bearer token.
# Server does NOT store "user logged in session" in memory.
class ServerStateInfo(BaseModel):
    architecture: str
    is_stateless: bool
    explanation: str

@app.get(
    "/api/rest-info",
    response_model=ServerStateInfo,
    tags=["REST Core Principles"],
    summary="Stateless REST demonstration"
)
def get_rest_info(authorization: Optional[str] = Header(None)):
    """
    In a stateless REST architecture:
    - Every request brings its own token / authorization header.
    - Any server behind a load balancer can handle this request because no session state is kept in server RAM.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Stateless API requires credentials in every request (e.g. Authorization: Bearer <token>)"
        )

    return ServerStateInfo(
        architecture="REST (Representational State Transfer)",
        is_stateless=True,
        explanation="Server does not store session cookies. All context came from client headers."
    )
