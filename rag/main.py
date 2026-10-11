
import os

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer, CrossEncoder

load_dotenv()

# -----------------------------
# 1. Initialize clients/models
# -----------------------------

groq_client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)

groq_model = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)

# Embedding model: converts text into vectors
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Cross-encoder: scores query-document relevance
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

# Persistent local ChromaDB database
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="knowledge_base"
)


# -----------------------------
# 2. Add documents to ChromaDB
# -----------------------------

def add_documents(documents):
    if not documents:
        return

    ids = [f"doc_{i}" for i in range(len(documents))]

    embeddings = embedding_model.encode(
        documents,
        normalize_embeddings=True,
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
    )


# -----------------------------
# 3. Retrieve candidate chunks
# -----------------------------

def retrieve_candidates(query, top_k=10):
    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    candidates = []

    for i, text in enumerate(results["documents"][0]):
        candidates.append({
            "id": results["ids"][0][i],
            "text": text,
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return candidates


# -----------------------------
# 4. Rerank retrieved candidates
# -----------------------------

def rerank_documents(query, candidates, top_n=3):
    if not candidates:
        return []

    pairs = [
        (query, candidate["text"])
        for candidate in candidates
    ]

    scores = reranker.predict(pairs)

    ranked = []

    for candidate, score in zip(candidates, scores):
        ranked.append({
            **candidate,
            "rerank_score": float(score),
        })

    ranked.sort(
        key=lambda item: item["rerank_score"],
        reverse=True,
    )

    return ranked[:top_n]


# -----------------------------
# 5. Generate answer using Groq
# -----------------------------

def answer_question(query):
    candidates = retrieve_candidates(
        query,
        top_k=10,
    )

    if not candidates:
        return "Bhai, database mein abhi koi documents nahi hain."

    final_docs = rerank_documents(
        query,
        candidates,
        top_n=3,
    )

    context = "\n\n".join(
        doc["text"] for doc in final_docs
    )

    prompt = f"""
Answer the question using the context below.
If the answer is not supported by the context,
say that the available documents do not contain
enough information.

Context:
{context}

Question:
{query}
"""

    response = groq_client.chat.completions.create(
        model=groq_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful RAG assistant. "
                    "Use the supplied context and do not "
                    "invent unsupported facts."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
    )

    print("\n--- Reranked documents ---")

    for doc in final_docs:
        print(
            f"\nID: {doc['id']}"
            f"\nScore: {doc['rerank_score']:.4f}"
            f"\nText: {doc['text']}"
        )

    return response.choices[0].message.content


# -----------------------------
# 6. Try it
# -----------------------------

if collection.count() == 0:
    add_documents([
        "RAG combines document retrieval with a language model "
        "to answer questions using external knowledge.",
        "ChromaDB stores embeddings and supports vector similarity search.",
        "Groq provides API access to language models for fast inference.",
        "A cross-encoder jointly processes a query and a document "
        "to produce a relevance score.",
        "Reranking sorts retrieved candidates by relevance before "
        "sending selected context to the language model.",
        "Production deployment can use monitoring, logging, "
        "authentication, and cloud infrastructure.",
    ])

question = (
    "How does a cross-encoder improve a RAG system?"
)

answer = answer_question(question)

print("\n--- Final answer ---")
print(answer)
