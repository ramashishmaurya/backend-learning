import asyncio
import os

from dotenv import load_dotenv

from synapsekit.agents.base import BaseTool, ToolResult
from synapsekit.llm.base import LLMConfig
from synapsekit.llm.groq import GroqLLM
from synapsekit.agents.executor import AgentExecutor, AgentConfig


# Load environment variables from .env
load_dotenv()


# ============================================================
# 1. LOW-RISK TOOL — No Human Approval Required
# ============================================================

class GetWeatherTool(BaseTool):
    name = "get_weather"
    description = "Get the current weather for a location."

    parameters = {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name"
            }
        },
        "required": ["location"] 
    }

    async def run(self, location: str, **kwargs) -> ToolResult:
        print(f"\n[Tool Executing] Fetching weather for {location}...")

        return ToolResult(
            output=f"The weather in {location} is 25°C and sunny."
        )


# ============================================================
# 2. HIGH-RISK TOOL — Human-in-the-Loop
# ============================================================

class DropDatabaseTool(BaseTool):
    name = "drop_database_table"
    description = "Deletes a table from the production database."

    parameters = {
        "type": "object",
        "properties": {
            "table_name": {
                "type": "string",
                "description": "Name of the table to drop"
            }
        },
        "required": ["table_name"]
    }

    async def run(self, table_name: str, **kwargs) -> ToolResult:

        # Human approval required before executing the dangerous action.
        print(
            f"\n🚨 WARNING: The agent wants to run "
            f"drop_database_table on '{table_name}' 🚨"
        )

        # Use an executor so input() doesn't block the async event loop
        loop = asyncio.get_event_loop()
        human_approval = await loop.run_in_executor(
            None,
            lambda: input(f"Do you approve deleting the '{table_name}' table? (y/n): ")
        )
        human_approval = human_approval.strip().lower()

        if human_approval == "y":
            print(
                f"[Tool Executing] 💥 Dropping table {table_name}..."
            )

            # IMPORTANT:
            # This is only a demo. Don't actually execute DROP TABLE here
            # until you've added proper database safeguards.
            return ToolResult(
                output=f"Successfully deleted table {table_name}."
            )

        print("[Tool Blocked] Human denied permission.")

        return ToolResult(
            error=(
                "Human denied permission to run this tool. "
                "Do not execute the operation."
            )
        )


# ============================================================
# MAIN
# ============================================================

async def main():

    # OpenAI API key
    api_key = os.getenv("GROQ_API_KEY")

    # Create LLM
    llm = GroqLLM(
        LLMConfig(
            model="openai/gpt-oss-120b",
            api_key=api_key,
            provider="groq",
        )
    )

    # Create agent with both tools
    agent = AgentExecutor(
        AgentConfig(
            llm=llm,
            tools=[
                GetWeatherTool(),
                DropDatabaseTool()
            ],
            agent_type="function_calling", 
            system_prompt=(
                "You are a helpful database and weather assistant. "
                "You MUST use the get_weather tool for weather questions. "
                "You MUST use the drop_database_table tool when the user asks "
                "to delete, drop, or remove a database table. "
                "NEVER claim that a database table was deleted without calling "
                "the drop_database_table tool. "
                "The drop_database_table tool requires human approval before "
                "it can execute."
            )
        )
    )

    # ========================================================
    # TEST 1 — LOW RISK
    # ========================================================

    # print("\n--- TEST 1: Low Risk Task ---")

    # response1 = await agent.run(
    #     "What is the weather in Mumbai?"
    # )

    # print(f"Agent: {response1}")

    # ========================================================
    # TEST 2 — HIGH RISK
    # ========================================================

    print("\n--- TEST 2: High Risk Task ---")

    response2 = await agent.run(
        "Please delete the 'users' table from the database i want to delete user databaase brother."
    )

    print(f"Agent: {response2}")


if __name__ == "__main__":
    asyncio.run(main())
