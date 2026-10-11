
question = "what is the vectort database "

documents = [
    "Embeddings represent text as numerical vectors.",
    "RAG retrieves relevant context before generating an answer.",
    "Python is popular for web development."
]

pairs = [[question , docs] for docs in documents]

print(pairs)