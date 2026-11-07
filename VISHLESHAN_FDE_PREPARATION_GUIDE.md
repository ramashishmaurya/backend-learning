# Vishleshan — Forward Deployed Engineer (FDE) Complete Interview & Preparation Guide

> **Target Role:** Forward Deployed Engineer (0–1 Years / Freshers Welcome)  
> **Company:** Vishleshan  
> **Core Focus:** Enterprise AI Delivery, RAG, Agentic Systems (MCP/CrewAI/LangChain), ERP/CRM Integrations, Backend (Django/SQL), and Manufacturing/Supply Chain Domains.

---

## Table of Contents
1. [Understanding the Role & What Vishleshan Wants](#1-understanding-the-role--what-vishleshan-wants)
2. [Pillar 1: Core Python & Backend Engineering (Django & SQL)](#2-pillar-1-core-python--backend-engineering-django--sql)
3. [Pillar 2: Production RAG & Vector Databases](#3-pillar-2-production-rag--vector-databases)
4. [Pillar 3: Agentic Frameworks & MCP (Model Context Protocol)](#4-pillar-3-agentic-frameworks--mcp-model-context-protocol)
5. [Pillar 4: Enterprise Systems Integration (ERP / CRM / SAP / Salesforce)](#5-pillar-4-enterprise-systems-integration-erp--crm--sap--salesforce)
6. [Pillar 5: Domain Knowledge (Manufacturing, Automotive, Supply Chain, FMEG)](#6-pillar-5-domain-knowledge-manufacturing-automotive-supply-chain-fmeg)
7. [The FDE Mindset: Client-Facing Scenarios & Soft Skills](#7-the-fde-mindset-client-facing-scenarios--soft-skills)
8. [Top 25 Technical & Scenario Interview Questions (With Answers)](#8-top-25-technical--scenario-interview-questions-with-answers)
9. [Architecture Blueprint: Production Enterprise AI Agent](#9-architecture-blueprint-production-enterprise-ai-agent)
10. [7-Day Quick Preparation Roadmap](#10-7-day-quick-preparation-roadmap)

---

## 1. Understanding the Role & What Vishleshan Wants

### What makes an FDE at Vishleshan different?
In an enterprise AI company like Vishleshan:
- **Not purely a researcher:** You won't just train models or tinker with prompts in Jupyter notebooks.
- **Not purely a backend developer:** You aren't just writing generic CRUD APIs.
- **You are a Problem Solver on the Front Lines:**
  1. You sit in front of clients (plant heads, supply chain managers, IT heads).
  2. You understand their messy legacy databases (SAP, Oracle, Excel sheets, SQL servers).
  3. You design and rapidly prototype custom AI agents, RAG pipelines, or automations that solve real business bottlenecks.
  4. You deploy secure, production-grade AI directly into client infrastructure.

---

## 2. Pillar 1: Core Python & Backend Engineering (Django & SQL)

### A. Python Proficiency
- **Type Hinting & Pydantic:** Enterprise AI heavily uses `pydantic` (v2) for schema validation, structured outputs from LLMs, and API payloads.
- **AsyncIO (`async`/`await`):** Handling multiple concurrent LLM calls, streaming tokens, and async DB queries.
- **Error Handling & Retries:** Handling API rate limits (Exponential Backoff + Jitter), timeout handling, fallback models.

### B. Django & Database Foundations
- **Django REST Framework (DRF) / Django Ninja:** Building secure authenticated endpoints (`TokenAuthentication`, `JWT`).
- **Django ORM vs Raw SQL:** 
  - Complex aggregation queries, `select_related` and `prefetch_related` to avoid $N+1$ query issues.
  - Indexing (B-Tree, GIN, HNSW/IVFFlat for vector storage).
- **PostgreSQL & `pgvector`:** Storing embeddings alongside transactional relational data in a single database.
- **Background Workers:** Using Celery / Redis for long-running AI tasks (document ingestion, batch inference, reporting).

---

## 3. Pillar 2: Production RAG & Vector Databases

Do not just say "I put text in ChromaDB and queried it". Explain production-level RAG:

### The Complete Ingestion Pipeline
1. **Document Parsing:** Handling messy PDFs, scanned invoices, ERP export CSVs, tables using tools like `Unstructured`, `PyMuPDF`, or `LlamaParse`.
2. **Chunking Strategies:**
   - *Fixed-size + Overlap:* (e.g., 500 tokens, 50 overlap) - basic.
   - *Semantic Chunking:* Breaking at natural paragraph/topic boundaries.
   - *Hierarchical / Parent-Document Chunking:* Small chunks for vector retrieval, returning parent document to LLM for context.
3. **Embeddings:** `text-embedding-3-small/large` (OpenAI), `bge-large-en-v1.5`, or `voyage-ai`. Understand cosine similarity vs inner product vs euclidean distance.
4. **Vector Databases:**
   - In-memory / Dev: `Chroma`, `FAISS`.
   - Production / Cloud: `Qdrant`, `Pinecone`, `Weaviate`, or `pgvector` (PostgreSQL).

### Advanced Retrieval & Post-Processing
- **Hybrid Search:** Dense Retrieval (Vector similarity) + Sparse Retrieval (BM25 keyword search) combined via Reciprocal Rank Fusion (RRF).
- **Reranking:** Using Cohere Rerank or BGE Reranker to filter the top 20 candidate chunks down to the best top 4 chunks before passing to the LLM.
- **Guardrails & Evaluation:**
  - Metrics: Faithfulness, Answer Relevance, Context Precision (using RAGAS or TruLens).
  - Guardrails: PII masking, jailbreak prevention, schema validation (NeMo Guardrails / Llama Guard).

---

## 4. Pillar 3: Agentic Frameworks & MCP (Model Context Protocol)

### A. Agentic Frameworks
* **LangChain / LangGraph:** Ideal for stateful, cyclic agent workflows with checkpoints and human-in-the-loop validation.
* **CrewAI:** Multi-agent role-playing framework (e.g., "Researcher Agent" gathers inventory data -> "Analyst Agent" spots anomalies -> "Writer Agent" drafts report for plant manager).
* **OpenClaw / AutoGen:** Multi-agent conversational systems for complex code execution and tool utilization.

### B. MCP (Model Context Protocol) — *Huge differentiator for Vishleshan!*
* **What is MCP?** An open standard protocol introduced by Anthropic that standardizes how LLM applications connect to external tools, data sources, and services.
* **Why does enterprise care?** Instead of writing custom brittle API integration code for every single enterprise database, ERP, or file system, companies expose **MCP Servers**. The LLM client connects to the MCP Server dynamically to fetch resources, inspect prompts, and invoke tools safely.
* **Key components of MCP:**
  1. **Host:** The LLM client (Claude Desktop, custom agent backend).
  2. **Client:** Connects 1:1 with an MCP server.
  3. **Server:** Lightweight program exposing Tools, Resources (readable data), and Prompts.
  4. **Transport:** `stdio` (local subprocess) or `SSE` (Server-Sent Events over HTTP).

---

## 5. Pillar 4: Enterprise Systems Integration (ERP / CRM / SAP / Salesforce)

Enterprise clients run on ERP and CRM backbones. An FDE must understand how to extract data and trigger actions:

### Key Platforms
1. **SAP (ERP):** SAP S/4HANA or ECC. Interfacing via OData REST APIs, BAPIs, or RFC connectors.
2. **Salesforce (CRM):** REST API, Bulk API 2.0, Webhooks, SOQL queries.
3. **Oracle NetSuite / EBS:** SuiteTalk REST Web Services, SOAP APIs.

### Practical Integration Patterns
- **Read-Only Analytics/RAG:** Syncing ERP master data (Part numbers, BOM - Bill of Materials, Vendor catalogues) into a vector store via nightly batch jobs or CDC (Change Data Capture).
- **Action Agents (Function Calling):** An agent triggers an API to create a Purchase Order (PO) or update inventory in the ERP after Human-in-the-Loop confirmation.
- **Security & RBAC:** Ensuring the LLM does not leak high-level financial or employee data to unauthorized users. Integrating with OAuth2, SAML, or LDAP.

---

## 6. Pillar 5: Domain Knowledge (Manufacturing, Automotive, Supply Chain, FMEG)

Mentioning these domain use-cases will immediately set you apart from standard freshers:

### 1. Automotive & Manufacturing
- **Predictive Maintenance Knowledge Base:** Operators query past machine maintenance logs, breakdown reports, and standard operating procedures (SOPs) using natural language.
- **BOM (Bill of Materials) & CAD Spec Q&A:** Cross-referencing design documentation with assembly requirements.
- **Root Cause Analysis (8D Reports):** AI agents analyzing historical defect logs to suggest probable causes for stamping or painting defects.

### 2. Supply Chain & Logistics
- **Vendor & PO Discrepancy Matching:** Automatically comparing invoices against ERP purchase orders to detect unit price or quantity mismatches.
- **Inventory Stock-Out Prediction & Allocation:** Agents alerting warehouse managers when safety stock thresholds are breached due to supplier lead-time delays.

### 3. FMEG (Fast-Moving Electrical Goods)
- **Warranty Claim Automation:** Processing customer claims, reading technician reports, and approving/flagging fraud automatically.
- **Dealer & Distributor Assistant:** Chatbot for dealers to check order status, available credit limits, and dispatch schedules from SAP.

---

## 7. The FDE Mindset: Client-Facing Scenarios & Soft Skills

In an interview, they will test your **maturity, communication, and adaptability**:

1. **How to deal with messy client data?**
   - *Never say:* "The client gave bad data, so AI won't work."
   - *Say:* "Enterprise data is always fragmented. My first step is building robust data cleaning and schema validation pipelines, flagging anomalies, and starting with a high-confidence subset of data for initial value delivery."
2. **Handling Hallucinations in High-Stakes Environments:**
   - Strict system prompts (`Answer ONLY using the provided context. If unknown, say 'Data not available'`).
   - Temperature = 0.0 for deterministic extraction and SQL generation.
   - Grounding with page/document citations.
   - Dual-agent verification (Generator + Critic).
3. **Handling Skeptical Client Stakeholders:**
   - Start with a quick, high-impact PoC (Proof of Concept) within 1–2 weeks.
   - Quantify ROI (e.g., "Reduced manual invoice verification time from 45 mins to 2 mins with 99% accuracy").
   - Maintain full transparency with human-in-the-loop workflows.

---

## 8. Top 25 Technical & Scenario Interview Questions (With Answers)

### Part A: Python, Backend & Databases
#### Q1: How do you optimize Django when handling concurrent slow LLM requests?
**Answer:** In standard synchronous WSGI, slow LLM calls block worker threads. Solutions:
1. Use **ASGI** (Uvicorn / Daphne) with async views (`async def`) so the event loop handles thousands of concurrent I/O-bound requests without blocking.
2. For long tasks (document parsing, batch ingestion), push the work to **Celery workers** with Redis/RabbitMQ, returning an immediate `task_id` for client polling or WebSocket/SSE notification.

#### Q2: What is the difference between `select_related` and `prefetch_related` in Django?
**Answer:**
- `select_related`: Creates a SQL `JOIN` query. Used for single-valued relationships (ForeignKey, OneToOne).
- `prefetch_related`: Executes separate SQL queries and performs joining in Python. Used for many-valued relationships (ManyToMany, reverse ForeignKey).

#### Q3: Why use PostgreSQL + `pgvector` instead of a standalone vector database like Pinecone?
**Answer:**
- `pgvector` allows transactional consistency (ACID), zero data synchronization lag, joins between relational metadata (e.g., user permissions, plant IDs) and vector embeddings, and reduced infrastructure overhead.
- Standalone vector DBs (Pinecone, Qdrant) are preferred when handling 50M+ vectors requiring sub-millisecond retrieval and distributed scale.

---

### Part B: GenAI, RAG & LLMs
#### Q4: What is the "Lost in the Middle" problem in RAG, and how do you solve it?
**Answer:** LLMs pay highest attention to tokens at the very beginning and very end of the prompt context, often ignoring chunks in the middle.  
*Solutions:* Limit context window to the top 3–5 most relevant chunks; use a cross-encoder Reranker (e.g., Cohere Rerank); reorder chunks so the most critical ones are placed at the start and end.

#### Q5: How does Hybrid Search work?
**Answer:** It combines:
1. **Dense Retrieval (Semantic/Vector):** Catches conceptual meaning (e.g., "vehicle stopping problem" matches "brake malfunction").
2. **Sparse Retrieval (Keyword/BM25):** Catches exact alphanumeric part numbers, serial codes, or rare terms (e.g., "SKU-9482-B").
They are merged using **Reciprocal Rank Fusion (RRF)**:
$$\text{RRF\_Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

#### Q6: How do you evaluate a RAG pipeline quantitatively?
**Answer:** Using the **RAG Triad** (frameworks like RAGAS):
1. **Context Relevance:** Are retrieved chunks actually relevant to the question?
2. **Groundedness / Faithfulness:** Is the generated answer backed solely by the retrieved context (no hallucinations)?
3. **Answer Relevance:** Does the answer directly address the user's prompt?

---

### Part C: Agents & MCP
#### Q7: What is an Agentic Workflow, and how is it different from a simple Chain?
**Answer:**
- A **Chain** (e.g., simple LangChain prompt -> LLM -> output) follows a deterministic, hardcoded sequential path.
- An **Agent** has autonomy: it uses an LLM as a reasoning engine within a **ReAct loop (Reasoning + Acting)**. It looks at available tools, decides *which* tool to call, inspects the result, and iterates until the goal is satisfied or an exit condition is reached.

#### Q8: Can you explain Model Context Protocol (MCP) in simple terms?
**Answer:** MCP is like a "USB-C port for AI apps". Before MCP, if you had 5 AI models and 5 enterprise tools (Postgres, SAP, Google Drive, GitHub, Slack), you needed 25 custom integrations. With MCP:
- Tools expose an MCP Server interface.
- LLM apps act as MCP Clients.
- Any MCP Client can plug-and-play into any MCP Server securely, reading data (Resources) and triggering actions (Tools).

#### Q9: When would you use CrewAI vs LangGraph?
**Answer:**
- **CrewAI:** Best for role-based multi-agent collaboration (agents have roles, goals, backstories, and pass tasks between each other). Excellent for rapid prototyping.
- **LangGraph:** Best when you need strict state machine control, cyclic graphs, persistence, deterministic branching, and granular human-in-the-loop approval steps.

---

### Part D: Enterprise Systems & Client Scenarios
#### Q10: A client wants an AI assistant that answers questions from SAP ERP. How would you design it safely?
**Answer:**
1. **Data Security & RBAC:** Never dump raw ERP data into a public vector database. Check the requesting user's role/permissions before querying.
2. **Architecture:** Use a Hybrid Agent:
   - For unstructured documentation (manuals, SOPs) -> RAG pipeline.
   - For live transactional data (stock levels, PO status) -> Tool-calling agent connecting to SAP via OData/REST API or SQL views.
3. **Guardrails:** Guard against prompt injection; validate API outputs against Pydantic schemas before returning to the user.

#### Q11: How do you handle rate limits and high latency when deploying LLMs to enterprise clients?
**Answer:**
1. **Semantic Caching:** Cache previous question/answer embeddings (e.g., using GPTCache or Redis Vector Cache) to bypass LLM calls for repeated questions.
2. **Tiered Model Routing:** Use small/fast models (e.g., Claude 3.5 Haiku / GPT-4o-mini) for classification and routing, and call large models (Claude 3.5 Sonnet / GPT-4o) only for complex reasoning.
3. **Streaming & Async:** Stream tokens back to the UI immediately to lower Perceived Latency (TTFT - Time To First Token).
4. **Resilience:** Circuit breakers, retry with exponential backoff, and fallback provider endpoints.

---

## 9. Architecture Blueprint: Production Enterprise AI Agent

```
                          ┌─────────────────────────────┐
                          │   Client Enterprise User    │
                          │   (Web UI / Mobile / Teams) │
                          └──────────────┬──────────────┘
                                         │ HTTPS / SSE (Streamed)
                                         ▼
                          ┌─────────────────────────────┐
                          │      API Gateway (Django)   │
                          │   Auth, RBAC, Rate Limiting │
                          └──────────────┬──────────────┘
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   │                                           │
                   ▼                                           ▼
       ┌───────────────────────┐                   ┌───────────────────────┐
       │     RAG Subsystem     │                   │   Agent & Tool Engine │
       │  (Unstructured Docs)  │                   │  (Live Actions/APIs)  │
       └───────────┬───────────┘                   └───────────┬───────────┘
                   │                                           │
         ┌─────────┴─────────┐                       ┌─────────┴─────────┐
         │ Hybrid Search     │                       │ MCP Client / Tools│
         │ - pgvector /      │                       │ - SAP OData REST  │
         │   Qdrant          │                       │ - Salesforce API  │
         │ - BM25 Sparse     │                       │ - SQL Database    │
         │ - Cohere Rerank   │                       └───────────────────┘
         └─────────┬─────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │   LLM Reasoning Core  │
       │  (Claude 3.5 Sonnet / │
       │   GPT-4o / Gemini)    │
       └───────────┬───────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │ Guardrails & Response │
       │ - Schema Validation   │
       │ - PII Masking & Citations
       └───────────────────────┘
```

---

## 10. 7-Day Quick Preparation Roadmap

| Day | Focus Area | What to Practice / Build |
| :--- | :--- | :--- |
| **Day 1** | **Python & Backend Refresh** | Pydantic v2 schemas, `async`/`await`, Django ORM optimization (`select_related`, raw queries), REST API authentication. |
| **Day 2** | **Production RAG Deep Dive** | Implement a working RAG script with chunking, `pgvector`/Chroma, and BM25 + Vector hybrid search with Reranker. |
| **Day 3** | **Agentic Systems (LangChain / CrewAI)** | Build a 2-agent system in CrewAI: Agent 1 extracts supply chain records, Agent 2 checks safety stock rules and generates recommendations. |
| **Day 4** | **MCP (Model Context Protocol)** | Read the MCP documentation; create a simple MCP Server exposing a custom tool (e.g., query a local SQLite database of inventory). |
| **Day 5** | **Enterprise & ERP Concepts** | Study SAP OData APIs, Salesforce REST APIs, webhooks, and how enterprise role-based access control (RBAC) works. |
| **Day 6** | **Domain Deep-Dive** | Memorize 3 concrete manufacturing/supply-chain use cases (BOM search, invoice matching, predictive maintenance QA). |
| **Day 7** | **Mock Client Delivery & Pitching** | Practice explaining technical trade-offs in plain English: "Why this model?", "How do you prevent hallucinations?", "What if client data is messy?". |

---

## Summary Checklist for the Interview
- [ ] You can explain what an FDE is with enthusiasm.
- [ ] You can walk through your existing GitHub/local projects (`evals.py`, `rag/`, `agnts.py`).
- [ ] You know the difference between LangChain, CrewAI, and MCP.
- [ ] You can explain how to ingest and search enterprise PDFs and tabular data without hallucinating.
- [ ] You have 2-3 questions prepared to ask the interviewer about Vishleshan's current client deployments.
