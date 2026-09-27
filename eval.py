import os

from dotenv import load_dotenv
from datasets import Dataset
from google import genai

from ragas import evaluate
from ragas.llms import llm_factory
from ragas.embeddings import GoogleEmbeddings

from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)


# ============================================================
# 1. Load environment variables
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env file"
    )

print("Gemini API key found: YES")


# ============================================================
# 2. Create Gemini client
# ============================================================

client = genai.Client(
    api_key=api_key
)


# ============================================================
# 3. Create Gemini LLM
# ============================================================

llm = llm_factory(
    "gemini-2.0-flash",
    provider="google",
    client=client,
)


# ============================================================
# 4. Create Gemini Embeddings
# ============================================================

embeddings = GoogleEmbeddings(
    client=client,
    model="gemini-embedding-001",
)


# ============================================================
# 5. Configure Ragas metrics
# ============================================================

faithfulness.llm = llm

answer_relevancy.llm = llm
answer_relevancy.embeddings = embeddings

context_recall.llm = llm

context_precision.llm = llm


# ============================================================
# 6. Create test dataset
# ============================================================

data = {
    "question": [
        "What is RAG?"
    ],

    "answer": [
        "RAG stands for Retrieval Augmented Generation. "
        "It retrieves relevant information from external sources "
        "and gives that information to an LLM so the LLM can generate "
        "a more grounded answer."
    ],

    "contexts": [
        [
            "RAG stands for Retrieval Augmented Generation. "
            "It is a technique where relevant documents are retrieved "
            "from an external knowledge source and provided to a language "
            "model to help generate an answer."
        ]
    ],

    "ground_truth": [
        "RAG is Retrieval Augmented Generation, a technique that retrieves "
        "relevant external information and provides it to an LLM to generate "
        "a grounded response."
    ],
}


dataset = Dataset.from_dict(data)


# ============================================================
# 7. Create metrics list
# ============================================================

metrics = [
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
]


# ============================================================
# 8. Run evaluation
# ============================================================

print("\nStarting Ragas evaluation...\n")

result = evaluate(
    dataset,
    metrics=metrics,
)


# ============================================================
# 9. Print results
# ============================================================

print("\n==============================")
print("RAGAS EVALUATION RESULT")
print("==============================\n")

print(result)


