import os
from dotenv import load_dotenv
from datasets import Dataset
from langchain_google_genai import ChatGoogleGenerativeAI
from ragas import evaluate
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextRecall,
    ContextPrecision,
)
from ragas.llms.base import LangchainLLMWrapper

# Load .env
load_dotenv()

# Check API key
if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = "mock"

# Create Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)
# Note: In older metrics, it automatically wrapped Langchain models.
# But let's wrap it just in case.
llm_wrapped = LangchainLLMWrapper(llm)

# Evaluation data
data = {
    "question": ["How many days can employees work from home?"],
    "answer": ["Employees can work from home up to 3 days per week."],
    "contexts": [["Employees can work remotely up to 3 days per week.", "Remote work requires manager approval."]],
    "ground_truth": ["Employees can work from home up to 3 days per week."],
}
dataset = Dataset.from_dict(data)

try:
    metrics = [
        Faithfulness(llm=llm_wrapped),
        AnswerRelevancy(llm=llm_wrapped),
        ContextRecall(llm=llm_wrapped),
        ContextPrecision(llm=llm_wrapped),
    ]
    print("Old Metrics initialized successfully with LangchainLLMWrapper!")
except Exception as e:
    print("Error initializing old metrics:")
    print(e)
