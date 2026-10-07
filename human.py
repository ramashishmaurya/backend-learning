import asyncio
import os
from dotenv import load_dotenv

# LangChain Imports for Tools and LLM
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

# Pure LangGraph Imports
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Load environment variables from .env
load_dotenv()

# ============================================================
# 1. LOW-RISK TOOL — No Human Approval Required
# ============================================================

class WeatherInput(BaseModel):
    location: str = Field(description="The city name")

class GetWeatherTool(BaseTool):
    name: str = "get_weather"
    description: str = "Get the current weather for a location."
    args_schema: type[BaseModel] = WeatherInput 

    def _run(self, location: str): 
        pass # Ignore sync run

    async def _arun(self, location: str, **kwargs) -> str: 
        print(f"\n[Tool Executing] Fetching weather for {location}...")
        return f"The weather in {location} is 25°C and sunny."


# ============================================================
# 2. HIGH-RISK TOOL — Human-in-the-Loop
# ============================================================

class DropTableInput(BaseModel):
    table_name: str = Field(description="Name of the table to drop") # state management here okay how this is will worj 

class DropDatabaseTool(BaseTool):
    name: str = "drop_database_table"
    description: str = "Deletes a table from the production database."
    args_schema: type[BaseModel] = DropTableInput

    def _run(self, table_name: str):
        pass # Ignore sync run

    async def _arun(self, table_name: str, **kwargs) -> str:
        print(f"\n🚨 WARNING: The agent wants to run drop_database_table on '{table_name}' 🚨")

        # Async-safe human input
        loop = asyncio.get_event_loop()
        human_approval = await loop.run_in_executor(
            None,
            lambda: input(f"Do you approve deleting the '{table_name}' table? (y/n): ")
        )
        human_approval = human_approval.strip().lower()

        if human_approval == "y":
            print(f"[Tool Executing] 💥 Dropping table {table_name}...")
            return f"Successfully deleted table {table_name}."
        else:
            print("User denied to make sense in code")
            print("[Tool Blocked] Human denied permission.")
            # Return string successfully so AI knows it was cancelled and doesn't retry
            return (
                "Operation cancelled. The human denied permission. "
                "Acknowledge the cancellation and DO NOT try to call this tool again."
            )


# ============================================================
# 3. DEFINE LANGGRAPH MEMORY (STATE)
# ============================================================

# The 'State' is the backpack that moves through the graph.
# add_messages ensures that old chat history is kept automatically!
class State(TypedDict):
    messages: Annotated[list, add_messages]


# ============================================================
# MAIN PROGRAM
# ============================================================

async def main():
    
    # 1. Setup LLM
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(
        model="openai/gpt-oss-120b", 
        api_key=api_key,
    )

    # 2. Setup Tools & Bind them to the Brain
    tools = [GetWeatherTool(), DropDatabaseTool()]
    llm_with_tools = llm.bind_tools(tools)

    # 3. Create the "Brain" Node
    async def call_model(state: State):  
        system_prompt = (
            "You are a helpful database and weather assistant. "
            "You MUST use the get_weather tool for weather questions. "
            "You MUST use the drop_database_table tool when the user asks to delete a table. "
            "NEVER claim that a database table was deleted without calling the tool. "
            "When the user asks to delete a table, you MUST IMMEDIATELY call the tool. "
            "DO NOT ask the user for confirmation in the chat. Just call the tool right away!"
        )
        
        # Inject System Prompt at the beginning of the messages list
        messages = [{"role": "system", "content": system_prompt}] + state["messages"] 
        
        # Ask LLM for the next move
        response = await llm_with_tools.ainvoke(messages)
        
        # Return the new AI message so it gets added to the 'State'
        return {"messages": [response]}


    # 4. Create the Routing Logic (if/else)
    def should_continue(state:  State):
        # Check the very last message in the chat
        last_message = state["messages"][-1] 
         
        # If the LLM decided to use a tool, go to the 'tools' node
        if last_message.tool_calls:
            return "tools"
        # If no tool was called, the conversation is done! End the graph.
        return END


    # 5. Build the Final Graph (This replaces AgentExecutor!)
    workflow = StateGraph(State)

    # Add Nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools)) # Prebuilt node to run our tools

    # Add Edges (Connect the flowchart)
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue)  
    workflow.add_edge("tools", "agent") # Once tool finishes, loop back to the agent brain

    # Compile the Graph!
    agent_app = workflow.compile()


    # ========================================================
    # TEST 2 — HIGH RISK
    # ========================================================
    print("\n--- TEST 2: High Risk Task ---")

    # Pass the initial message into the State Graph
    inputs = {
        "messages": [
            ("user", "Please delete the 'users' table from the database i want to delete user databaase brother.")
        ]
    }

    # Run the compiled graph!
    response = await agent_app.ainvoke(inputs )

    # Print the final message from the AI (The last one in the state)
    print(f"\nAgent: {response['messages'][-1].content}")  


if __name__ == "__main__":
    asyncio.run(main())



from langchain.agents.middleware import human_in_the_loop 

from langchain.agents.middleware import dynamic_prompt , ModelRequest

from langchain.agents.middleware import provider_tool_search

