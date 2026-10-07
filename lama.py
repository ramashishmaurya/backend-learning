import os
from dotenv import load_dotenv

load_dotenv()


# =========================================================
# 1. LLM
# =========================================================

from llama_index.llms.groq import Groq

llm = Groq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
)


# =========================================================
# 2. Embedding Model
# =========================================================

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)


# =========================================================
# 3. Configure LlamaIndex
# =========================================================

from llama_index.core import Settings

Settings.llm = llm
Settings.embed_model = embed_model


# =========================================================
# 4. Load Resume
# =========================================================

from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader(
    input_files=["data_folder/ashishmauryab.pdf"]
).load_data()

print(f"Loaded documents: {len(documents)}")




##########################################

from llama_index.core.node_parser import SentenceSplitter

splitter = SentenceSplitter(

    chunk_size= 100 , 
    chunk_overlap= 50 
)


nodes = splitter.get_nodes_from_documents(documents)

#_______________________________________________________
# =========================================================
# 5. Create Vector Index
# =========================================================

from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(
    documents
)


# =========================================================
# 6. Create Retriever
# =========================================================

retriever = index.as_retriever(
    similarity_top_k=5
)


# =========================================================
# 7. Get User Query
# =========================================================

user_query = input("\nAsk your question: ")


# =========================================================
# 8. Retrieve Relevant Chunks
# =========================================================

nodes = retriever.retrieve(user_query)


print("\n" + "=" * 60)
print("RETRIEVED CHUNKS")
print("=" * 60)


for i, node in enumerate(nodes):

    print(f"\n--- CHUNK {i + 1} ---")

    print(node.text)

    print(f"\nSCORE: {node.score}")


# =========================================================
# 9. Build Context
# =========================================================

context = "\n\n".join(
    node.text
    for node in nodes
)


print("\n" + "=" * 60)
print("FINAL CONTEXT")
print("=" * 60)

print(context)


# =========================================================
# 10. Create Prompt
# =========================================================

system_prompt = """
You are a resume question-answering assistant.

You must answer the user's question using ONLY the provided resume context.

Rules:

1. Do not use outside knowledge.
2. Do not invent information.
3. Words such as "bhai", "bro", "yaar",
   "okay", and "please" are conversational words.
   They are NOT part of the user's actual information request.
4. Understand the user's intent naturally.
5. If the user asks for projects, list the projects
   that are present in the provided context.
6. If the user asks for ALL projects, include every
   project available in the provided context.
7. If the requested information is not present in
   the context, say:
   "Information not found in the resume."
8. Keep the answer concise and directly answer the question.
"""


prompt = f"""
{system_prompt}

================ RESUME CONTEXT ================

{context}

================ USER QUESTION ================

{user_query}

================ ANSWER ================
"""


# =========================================================
# 11. Print Prompt For Debugging
# =========================================================

print("\n" + "=" * 60)
print("PROMPT SENT TO LLM")
print("=" * 60)

print(prompt)


# =========================================================
# 12. Send Prompt + Context To Groq
# =========================================================

response = llm.complete(prompt)


# =========================================================
# 13. Final Answer
# =========================================================

print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)

print(response)


# from llama_index.readers.file import PyMuPDFReader

# loader = PyMuPDFReader()

# documents = loader.load_data(
#     file_path="data_folder/ashishmauryab.pdf"
# )

# print(documents[0].text)