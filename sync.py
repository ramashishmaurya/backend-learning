import os
import asyncio
from dotenv import load_dotenv
import asyncio

load_dotenv()

from synapsekit import RAG

from synapsekit.llm.groq import GroqLLM
from synapsekit import LLMConfig

config = LLMConfig(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    provider="groq"
)

llm = GroqLLM(config)

async def main():
   # Stream
    async for token in llm.stream("Explain quantum computing"):
        print(token, end="", flush=True)

    print("\n")

    # Generate
    # response = await llm.generate("What is Rust?")
    # print(response)


asyncio.run(main())



