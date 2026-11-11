# 🚀 Complete API Design & API Features Master Cheatsheet

This guide covers **Module 3.2 (API Design)** and **Module 3.3 (API Features)** with clear mental models, real-world analogies, and the exact answers you need to ace backend engineering interviews.

---

## 📑 MODULE 3.2: API DESIGN

### 1. REST Architecture
- **What is it?** REpresentational State Transfer — an architectural style (coined by Roy Fielding in 2000) for designing networked systems over HTTP.
- **The 6 Core Constraints:**
  1. **Client-Server:** Decoupled UI from backend data storage.
  2. **Stateless:** Every HTTP request contains all context needed. The server does NOT store session state across calls.
  3. **Cacheable:** Responses must define if they can be cached (using `Cache-Control`, `ETag`).
  4. **Uniform Interface:** Consistent URIs, standard HTTP methods, and standard media types (JSON).
  5. **Layered System:** Client doesn't know if it's hitting a reverse proxy (Nginx), API gateway, or app server.
  6. **Code-on-Demand (Optional):** Server sending executable scripts (rarely used in JSON APIs).
- 💬 **Interview Punchline:** *"REST is an architectural pattern, not a strict protocol. Its biggest strength is statelessness, which allows horizontal scaling behind a load balancer without needing sticky sessions."*

---

### 2. RESTful Resources & Resource Naming
- **The #1 Golden Rule:** **Nouns, NEVER Verbs.**
  - ❌ Bad: `/getUsers`, `/createUser`, `/deleteOrder`, `/api/getdata/`
  - ✅ Good: `GET /users`, `POST /users`, `DELETE /orders/{id}`
- **Plural Collections:** Always use plural nouns (`/users`, `/products`, `/orders`).
- **Hierarchy & Sub-resources:**
  - `GET /users/42/orders` (Orders belonging to User 42).
  - `GET /users/42/orders/101` (Specific Order 101 for User 42).
  - ⚠️ *Rule of thumb:* Never nest deeper than 2 levels (e.g. avoid `/users/1/orders/2/items/3/reviews/4`). Instead, flatten to `GET /reviews?order_item_id=3`.
- **Non-CRUD Actions:** When an operation isn't a simple CRUD entity (e.g. login, payment checkout, cancel order):
  - Model as a state transition or sub-resource: `POST /orders/{id}/cancel` or `POST /auth/tokens`.

---

### 3. HTTP Methods (Verbs)

| Method | Purpose | Safe? | Idempotent? | Real-life Example |
| :--- | :--- | :---: | :---: | :--- |
| **GET** | Read resource | ✅ Yes | ✅ Yes | `GET /products/10` |
| **POST** | Create new resource / trigger action | ❌ No | ❌ No | `POST /orders` |
| **PUT** | Full replacement of resource | ❌ No | ✅ Yes | `PUT /users/10` (replaces all fields) |
| **PATCH** | Partial update of resource | ❌ No | ⚠️ Usually | `PATCH /users/10` (updates only `email`) |
| **DELETE** | Remove resource | ❌ No | ✅ Yes | `DELETE /users/10` |
| **OPTIONS** | CORS preflight & allowed methods | ✅ Yes | ✅ Yes | Browser checks allowed headers |

- 💬 **Interview Punchline (Safe vs Idempotent):**
  - **Safe:** Calling it does *not* alter any server state (e.g., `GET`, `HEAD`).
  - **Idempotent:** Calling it $1$ time produces the exact same server state as calling it $1,000$ times (e.g., `PUT`, `DELETE`). `POST` is NOT idempotent because 10 requests create 10 orders!

---

### 4. Status Codes (The 5 Families)

- **2xx Success:**
  - `200 OK`: Standard success (GET, PUT, PATCH).
  - `201 Created`: Resource successfully created (POST). Include created object or `Location` header.
  - `204 No Content`: Successful request with no body returned (standard for `DELETE`).
- **3xx Redirection:**
  - `301 Moved Permanently`: URL migrated permanently.
  - `304 Not Modified`: Cached data is still fresh (saves bandwidth).
- **4xx Client Errors:**
  - `400 Bad Request`: Generic syntax/malformed payload error.
  - `401 Unauthorized`: **Unauthenticated** (Who are you? Token is missing or invalid).
  - `403 Forbidden`: **Unauthorized** (I know who you are, but you don't have permission).
  - `404 Not Found`: Resource does not exist.
  - `409 Conflict`: Business logic conflict (e.g., duplicate email registration, state conflict).
  - `422 Unprocessable Entity`: Syntactically valid JSON, but fails validation (Pydantic validation error).
  - `429 Too Many Requests`: Client exceeded rate limit.
- **5xx Server Errors:**
  - `500 Internal Server Error`: Unhandled crash/bug in backend code.
  - `502 Bad Gateway`: Backend server or upstream service is down.
  - `503 Service Unavailable`: Server overloaded or in maintenance mode.
  - `504 Gateway Timeout`: Upstream dependency took too long to respond.

---

### 5. JSON APIs & Request Validation
- **Serialization & Deserialization:** Converting HTTP JSON strings to strongly-typed Python objects.
- **Pydantic v2:**
  - Enforce bounds: `Field(ge=18, le=100)`, `EmailStr`, `min_length=3`.
  - Custom validations with `@field_validator`.
  - Type coercion & instant validation error messages before hitting the database layer.

---

### 6. Response Design & Standard Envelopes
- **Consistent Envelope Pattern:**
  ```json
  {
    "success": true,
    "message": "User fetched successfully",
    "data": { ... },
    "timestamp": "2026-11-11T12:00:00Z"
  }
  ```
- **Data Hiding / Filtering:** Never expose internal database columns like `password_hash`, `stripe_customer_secret`, or internal flags. Always use output schemas (`response_model` in FastAPI).

---

### 7. Error Responses (RFC 7807 Problem Details)
- Avoid returning raw strings like `{"error": "something failed"}`.
- Standard error envelope:
  ```json
  {
    "success": false,
    "error_code": "DUPLICATE_EMAIL",
    "message": "Email already exists in system",
    "details": [{"field": "email", "message": "already taken"}],
    "request_id": "req_88f91a2b"
  }
  ```
- **Why `request_id`?** Allows frontend to show an incident ID to the customer, enabling backend engineers to grep logs instantly.

---

### 8. API Versioning
- **Strategies:**
  1. **URI Path (Most common):** `/api/v1/users` vs `/api/v2/users`. Easy to test, route in Nginx/Gateway, and cache.
  2. **Header Versioning (Stripe style):** `X-API-Version: 2026-01-01`. Keeps URLs clean.
  3. **Accept Header (Content Negotiation):** `Accept: application/vnd.company.v1+json`.
- 💬 **Interview Punchline:** *"Never introduce breaking changes in a minor release. Use path versioning `/v1` when major schema or contract breaks occur to ensure backward compatibility for mobile clients."*

---

### 9. OpenAPI & API Documentation
- **What is OpenAPI (OAS)?** Machine-readable specification standard (JSON/YAML) defining all endpoints, parameters, schemas, and responses.
- **Swagger UI (`/docs`):** Interactive sandbox for developers to test APIs directly.
- **ReDoc (`/redoc`):** Clean, publication-ready documentation.

---

## ⚡ MODULE 03.3: API FEATURES

### 1. Pagination: Offset vs Cursor

| Feature | Offset Pagination (`?page=2&page_size=20`) | Cursor Pagination (`?cursor=eyJpZ...&limit=20`) |
| :--- | :--- | :--- |
| **SQL** | `SELECT * FROM tbl LIMIT 20 OFFSET 20` | `SELECT * FROM tbl WHERE id > :cursor LIMIT 20` |
| **Performance** | $O(N)$ — Gets slower on large pages | $O(1)$ — Fast index seek regardless of depth |
| **Page Drift** | ❌ Prone to duplicate or missed items on inserts | ✅ Immune to inserts/deletions |
| **Page Numbers** | ✅ Can jump directly to "Page 15" | ❌ Only supports "Next" and "Previous" |
| **Best For** | Admin dashboards, internal tools | High-scale APIs (Stripe, Twitter feed, Slack) |

- 💬 **Interview Punchline:** *"Offset pagination scans and discards $N$ rows in PostgreSQL. At 1,000,000 rows, `OFFSET 990000` requires reading 990,000 rows into memory. Cursor pagination uses a B-Tree index seek `WHERE id > :last_id`, running in constant sub-millisecond time."*

---

### 2. Filtering, Sorting & Searching
- **Filtering:** Use query parameters (`?category=shoes&min_price=500`).
- **Sorting:** Support asc/desc with prefix `-` or dedicated query params:
  - `?sort=-price,created_at` (Minus sign = descending).
- **Searching:** Full-text search (PostgreSQL `tsvector` or trigram `pg_trgm`) vs simple `ILIKE %term%`.

---

### 3. Bulk Operations
- **When to use?** Inserting or updating hundreds of items without opening hundreds of HTTP connections.
- **Design Options:**
  1. **Atomic (All-or-Nothing):** Wrap in a single database transaction. If row 99 fails, rollback everything (Return 400/500).
  2. **Partial Success (Best-Effort):** Insert valid rows, report errors for invalid rows using HTTP `207 Multi-Status`.

---

### 4. Idempotency (The Stripe Pattern)
- **Problem:** User clicks "Pay ₹5,000". Connection drops before response reaches browser. User clicks "Pay" again. Double charge!
- **Solution:**
  1. Client sends a unique UUID: `Idempotency-Key: 9b1deb4d-...`.
  2. Server checks Redis: `SET idempotency:<key> "PROCESSING" NX EX 120`.
  3. If key exists: Return 409 Conflict (if in-flight) or return the cached completed response.
  4. Server completes payment and stores response in Redis for 24 hours.
  5. Any retry receives the cached response without re-executing business logic.

---

### 5. Rate Limiting
- **Why?** Protect against DDoS, brute-force attacks, scraping, and downstream LLM/database exhaustion.
- **Key Algorithms:**
  - **Token Bucket:** Tokens added at fixed rate. Allows small bursts.
  - **Leaky Bucket:** Requests processed at smooth constant rate.
  - **Sliding Window Counter:** Accurate, prevents edge bursts at boundary of fixed windows.
- **Standard Headers:**
  - `X-RateLimit-Limit`: Maximum requests allowed in window.
  - `X-RateLimit-Remaining`: Requests left in current window.
  - `X-RateLimit-Reset`: Unix timestamp when quota refreshes.
  - `Retry-After`: Seconds to wait when receiving `429 Too Many Requests`.

---

### 6. API Keys (Machine-to-Machine Auth)
- Used for partner/developer access (e.g. `sk_live_...`).
- Passed via `X-API-Key` or `Authorization: Bearer <key>`.
- **Security Rule:** **Never store plain text API keys in DB!** Store `SHA-256(api_key)` and compare hashes.

---

### 7. Webhooks (Push vs Pull)
- **Concept:** Instead of client polling every 5 seconds (`GET /order/status`), the server sends an HTTP `POST` to the client's URL when an event happens.
- **Security:** Use **HMAC-SHA256 Signatures**:
  - Server hashes payload with shared secret: `signature = HMAC_SHA256(secret, raw_payload)`.
  - Server sends signature in `X-Webhook-Signature` header.
  - Client recomputes HMAC and uses `hmac.compare_digest()` to prevent replay attacks and tampering.
- **Reliability:** Implement Exponential Backoff Retries + Dead Letter Queue (DLQ).

---

### 8. Backward Compatibility & Graceful Deprecation
- **Additive Changes are Safe:** Adding new optional response fields or optional query parameters does NOT break clients.
- **Breaking Changes:** Removing fields, renaming fields, or making optional parameters mandatory.
- **Deprecation Workflow:**
  1. Never delete fields immediately.
  2. Send HTTP standard headers:
     - `Deprecation: true`
     - `Sunset: Wed, 31 Dec 2026 23:59:59 GMT`
     - `Warning: 299 - "This endpoint/field is deprecated"`
  3. Announce migration period to mobile and external consumers.
