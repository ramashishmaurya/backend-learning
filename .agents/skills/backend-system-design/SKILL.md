---
name: backend-system-design
description: >-
  Comprehensive guide, mental models, and engineering framework for Backend Engineering and System Design in Python/FastAPI.
  Use when designing backend architectures, debugging bottlenecks, analyzing failure modes, discussing distributed systems,
  concurrency, database optimization, caching, asynchronous workflows, or preparing for backend system design interviews.
---

# Backend Engineering & System Design Skill

This skill acts as a specialized pair-programming and architectural guide for designing, building, and scaling production-grade backend systems using Python, FastAPI, PostgreSQL, Redis, and modern distributed systems patterns.

---

## 1. Core Architectural Mental Models

When evaluating any backend architecture or design question, evaluate these 5 dimensions:

1. **Throughput & Latency Requirements:**
   - Read vs. Write ratio (e.g., 99:1 read-heavy vs 50:50 write-heavy).
   - Latency SLA/SLO (p95 and p99 expectations, e.g., < 50ms for OLTP APIs).
2. **Data Consistency & Isolation:**
   - Strong Consistency (ACID) vs. Eventual Consistency (BASE).
   - Transaction Isolation levels (Read Committed, Repeatable Read, Serializable).
3. **Concurrency & Failure Modes:**
   - Where will the race condition occur? (Multiple workers updating same balance/inventory).
   - What happens when a downstream dependency (DB, Redis, external API) times out or dies?
4. **State Management & Scaling:**
   - Stateless app servers (FastAPI nodes behind a reverse proxy / load balancer).
   - Stateful data stores (PostgreSQL primary-replica, Redis clusters).
5. **Observability First:**
   - Structured JSON logs with correlation IDs (`X-Request-ID`).
   - Latency histograms (p50, p90, p99) and error rates.

---

## 2. Concurrency & Data Integrity Checklist

### Concurrency Primitives
- **Pessimistic Locking (`SELECT ... FOR UPDATE`):**
  - Use when collision probability is high (e.g., flash sale inventory, bank balance transfer).
  - Keeps the row locked until the transaction commits or aborts.
  - *Beware of Deadlocks:* Always lock rows in a consistent order across transactions (e.g., sort user IDs before locking multiple rows).
- **Optimistic Concurrency Control (OCC):**
  - Use version column (`version_id`).
  - `UPDATE items SET stock = stock - 1, version = version + 1 WHERE id = :id AND version = :current_version;`
  - If rows affected == 0, retry or abort. Ideal for low-to-medium contention.
- **Atomic Redis Operations & Lua Scripts:**
  - Execute multi-step checks atomically inside Redis single thread without network round trips.
  - Example: Check balance and deduct in a single Lua script.

### Idempotency Pattern
- Protect state-altering endpoints (`POST /orders`, `POST /transfers`) from network retries.
- Client sends `X-Idempotency-Key: <UUID>`.
- Use Redis with short TTL (e.g., 120s):
  1. `SET idempotency:<key> "PROCESSING" NX EX 120`
  2. If key exists: Return 409 Conflict or wait/return cached response.
  3. Process business logic inside DB transaction.
  4. Save response in Redis: `SET idempotency:<key> <cached_response> EX 86400`.

---

## 3. Database Deep-Dive (PostgreSQL + SQLAlchemy Async)

### Indexing Strategies
- **B-Tree (Default):** For equality and range queries (`=`, `<`, `>`, `BETWEEN`).
- **Composite Index Ordering:** Order matters! Place high-cardinality equality filter first, range filter last.
  - Query: `WHERE user_id = 5 AND created_at > '2026-01-01'` $\to$ Index on `(user_id, created_at)`.
- **GIN Index:** For JSONB, full-text search, and array containment.
- **Profiling with EXPLAIN ANALYZE:**
  - Look for `Seq Scan` (bad on large tables) vs `Index Scan` / `Bitmap Index Scan`.
  - Check buffer hits (`EXPLAIN (ANALYZE, BUFFERS)`): high disk reads indicate missing memory or unindexed joins.

### Connection Pooling & Session Lifecycle
- Never create a new DB engine per request. Keep a shared async engine (`create_async_engine`).
- Configure connection pool:
  - `pool_size`: baseline open connections.
  - `max_overflow`: burst capacity.
  - `pool_timeout`: fast fail instead of hanging.
- **Session Scope:** 1 session per HTTP request using FastAPI `Depends()`, commit on success, auto-rollback on exception.

---

## 4. Caching & Mitigation of Edge Cases

### Caching Patterns
- **Cache-Aside (Lazy Loading):** Read from Cache $\to$ If miss, Read DB $\to$ Write to Cache $\to$ Return.
- **Write-Invalidate:** On DB write/update, invalidate (delete) the cache key instead of updating it to avoid race conditions.

### Cache Stampede / Thundering Herd Solution
When a hot cache key expires and 10,000 concurrent requests simultaneously query the database:
- **Solution 1 (Distributed Mutex):** The first request acquires a Redis lock to query the DB and update the cache; other requests either wait or return a stale cached value.
- **Solution 2 (Early Expiry / Probabilistic XFetch):** Refresh cache in the background slightly before the TTL expires.

---

## 5. Asynchronous Workflows & Message Queues

### When to Offload to Background Tasks?
- CPU-intensive tasks (image resizing, ML inference, PDF generation).
- Long I/O tasks (batch emails, external webhook notifications, third-party API syncing).

### Worker Patterns (Celery / Arq / RabbitMQ)
- **At-Least-Once Delivery:** Consumers MUST be idempotent (processing the same message twice should not cause double-debit or corrupt data).
- **Dead Letter Queue (DLQ):** After $N$ failed retries with exponential backoff, send message to a DLQ for manual inspection/alerting.
- **Graceful Shutdown:** Handle `SIGTERM` in worker pods by pausing consumption and finishing in-flight jobs.

---

## 6. Resilience, Security & Production Reliability

- **Circuit Breaker Pattern:**
  - Closed (normal) $\to$ Open (failing, fail fast without calling dependency) $\to$ Half-Open (test single canary request).
- **Rate Limiting:**
  - Sliding Window Counter using Redis sorted sets (`ZADD`, `ZREMRANGEBYSCORE`, `ZCARD`).
- **Graceful Degradation:**
  - If recommendation service fails, fallback to static/trending list rather than throwing HTTP 500.
- **Event Loop Hygiene in FastAPI:**
  - NEVER run blocking synchronous code (e.g. `requests.get()`, `time.sleep()`, synchronous DB calls) inside `async def`.
  - Use `run_in_threadpool(sync_func)` or async equivalents (`httpx.AsyncClient`, `asyncio.sleep()`).

---

## 7. System Design Interview Framework

When tackling any system design problem, follow this structured blueprint:

1. **Scope & Functional Requirements:** Clarify core features (2-3 main APIs) and out-of-scope items.
2. **Non-Functional Requirements:** Scalability (DAU/MAU, RPS), Latency, Availability vs. Consistency (CAP theorem), Durability.
3. **Back-of-the-Envelope Estimation:**
   - Write QPS = total daily writes / 86400.
   - Peak QPS = 2x - 5x average QPS.
   - Storage estimation for 5 years.
4. **Data Model & Schema:** Entities, relationships, choice of SQL vs. NoSQL, indexing.
5. **High-Level Design:** Clients $\to$ CDN / Reverse Proxy (Nginx) $\to$ API Gateway / Load Balancers $\to$ FastAPI Services $\to$ Caching / DBs / Message Brokers.
6. **Deep-Dive & Bottleneck Mitigation:** Address single points of failure (SPOF), partition keys, replication lag, and cache invalidation.
