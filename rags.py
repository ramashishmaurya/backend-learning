import asyncio
import os

from dotenv import load_dotenv
from synapsekit import RAG


rag = RAG(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    provider="groq",
)

rag.add("""
Python is a high-level programming language.

It is commonly used for web development,
automation, data science, machine learning,
and artificial intelligence.
""")


async def main():

    # Async
    # answer = await rag.ask("what is the advantage of learning python?")
    # print("AI:", answer)

    print("\n--- Streaming ---")

    # Streaming
    async for token in rag.stream("is python best for development"):
        print(token, end="", flush=True)

    print("\n")


# Run async code
asyncio.run(main())

