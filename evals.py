import os

# 1. Yeh line sabse upar honi chahiye (Python 3.14 Protobuf Error ko fix karne ke liye)
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Yahan apni Gemini ki API key daalein
os.environ["GOOGLE_API_KEY"] = os.getenv("OPENAI_API_KEY")

from datasets import Dataset
from ragas import evaluate

# 2. Warning Fix: Naye RAGAS version mein metrics ab yahan se import hoti hain
from ragas.metrics.collections import faithfulness, answer_relevancy, context_precision
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Gemini Setup
gemini_judge = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Sample Data
data_samples = {
    'question': ['How many sick leaves do I get in a year?'],
    'answer': ['You get 12 sick leaves in a calendar year according to the HR policy.'],
    'contexts': [
        ["According to the 2024 HR policy, every employee is entitled to 12 sick leaves."]
    ],
    'ground_truth': ['Employees are entitled to 12 sick leaves per year.']
}

dataset = Dataset.from_dict(data_samples)

print("Gemini Judge ko use karke evaluation start ho rahi hai...")

# Ragas Evaluation
score = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
    llm=gemini_judge,
    embeddings=gemini_embeddings
)

print("\n--- Evaluation Results ---")
print(score)


