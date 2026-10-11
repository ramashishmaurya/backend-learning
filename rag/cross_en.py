from sentence_transformers import CrossEncoder

# this models help to compare and assign the valeus 
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
) 

question = "What are embeddings in RAG?"

documents = [
    "Embeddings represent text as numerical vectors.",
    "Python is popular for web development.",
    "RAG retrieves relevant context before generating an answer."
]

pairs = [[question, doc] for doc in documents]

scores = reranker.predict(pairs)

ranked_docs = sorted(
    zip(documents, scores),
    key=lambda item: item[1],
    reverse=True
)

for doc, score in ranked_docs:
    print(round(float(score), 3), doc)

