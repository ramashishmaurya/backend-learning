import os

from dotenv import load_dotenv

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    Settings,
)

from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


# Load .env
load_dotenv()

# -----------------------------
# 1. Configure Groq LLM
# -----------------------------

api_key = os.getenv("GROQ_API_KEY")

llm = Groq(
    model="openai/gpt-oss-120b",
    api_key=api_key,
)

Settings.llm = llm


# -----------------------------
# 2. Configure embedding model
# -----------------------------

# Settings.embed_model = HuggingFaceEmbedding(
#     model_name="BAAI/bge-small-en-v1.5"
# )


# -----------------------------
# 3. Load your documents
# -----------------------------

documents = SimpleDirectoryReader(
    "./data_folder"
).load_data()


# -----------------------------
# 4. Create vector index
# -----------------------------

index = VectorStoreIndex.from_documents(
    documents
)


# -----------------------------
# 5. Create query engine
# -----------------------------

query_engine = index.as_query_engine()


# -----------------------------
# 6. Ask question
# -----------------------------

question = "Ek saal mein total kitni paid leaves milti hain?"

response = query_engine.query(question)

print(response)



from langchain_text_splitters import RecursiveJsonSplitter

splitter = RecursiveJsonSplitter()


