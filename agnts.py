import asyncio
import os

from dotenv import load_dotenv

from synapsekit import tool, AgentExecutor, AgentConfig, LLMConfig
from synapsekit.llm.groq import GroqLLM


load_dotenv()


@tool
def check_database(user_id: int) -> str:
    """Gets the user's balance from the database."""
    # Your actual database code goes here
    return f"User {user_id} has $500."

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    if city.lower() == "tokyo":
        return "Sunny, 22°C"
    return "Cloudy, 15°C"


@tool
def get_information_personal(data: str ) ->str:
    """this is just function to get basic information """

    return f"introdunction of mine okay {data}"


# Create Groq LLM explicitly
llm = GroqLLM(
    LLMConfig(
        model="openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_API_KEY"),
        provider="groq",
    )
)


# Create agent
my_agent = AgentExecutor(
    AgentConfig(
        llm=llm,
        tools=[check_database , get_weather , get_information_personal] ,
        agent_type="function_calling",
        system_prompt="You are a helpful bank assistant.",
    )
)


async def main():
    answer = await my_agent.run(
        " this is my personal introduction okay hi i am ashish maurya completed bachelors of data science from mumbai university"
    )

    print(answer)


if __name__ == "__main__":
    asyncio.run(main())



