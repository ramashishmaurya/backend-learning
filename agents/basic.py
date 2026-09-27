import os
import json

from google import genai
from google.genai import types

from dotenv import load_dotenv

load_dotenv()


# =========================================================
# 1. GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


# =========================================================
# 2. OUR ACTUAL TOOL
# =========================================================

def get_bank_balance(account_number: int) -> dict:
    """
    User ke bank account ka balance return karta hai.
    """

    # Dummy database
    accounts = {
        12345: 25000,
        67890: 50000,
        11111: 10000
    }

    # Account nahi mila
    if account_number not in accounts:
        return {
            "success": False,
            "error": "Account not found"
        }

    # Account mila
    return {
        "success": True,
        "account_number": account_number,
        "balance": accounts[account_number],
        "currency": "INR"
    }


# =========================================================
# 3. TOOL DEFINITION
# =========================================================
# Ye Gemini ko batata hai:
# - tool ka naam kya hai
# - tool kya karta hai
# - kaunsa input chahiye
# =========================================================

bank_tool = {
    "name": "get_bank_balance",

    "description": (
        "Gets the current bank balance for a user's "
        "bank account number."
    ),

    "parameters": {
        "type": "object",

        "properties": {
            "account_number": {
                "type": "integer",
                "description": "The user's bank account number."
            }
        },

        "required": ["account_number"]
    }
}


# =========================================================
# 4. GEMINI CONFIG
# =========================================================

config = types.GenerateContentConfig(
    tools=[
        types.Tool(
            function_declarations=[
                bank_tool
            ]
        )
    ],

    # Learning ke liye automatic calling OFF
    # Hum khud tool call execute karenge.
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    )
)


# =========================================================
# 5. USER MESSAGE
# =========================================================

user_message = (
    "Mera account number 12345 hai, "
    "mera balance batao."
)


# =========================================================
# 6. FIRST LLM CALL
# =========================================================

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_message,
    config=config
)


# =========================================================
# 7. CHECK KARO GEMINI NE TOOL CALL KIYA YA NAHI
# =========================================================

function_call = None

for part in response.candidates[0].content.parts:

    if part.function_call:
        function_call = part.function_call
        break


# =========================================================
# 8. AGAR GEMINI NE TOOL CALL KIYA
# =========================================================

if function_call:

    print("\nGemini wants to call:")
    print(function_call.name)

    print("\nArguments:")
    print(function_call.args)


    # -----------------------------------------------------
    # 9. TOOL KA ARGUMENT NIKALO
    # -----------------------------------------------------

    account_number = function_call.args["account_number"]


    # -----------------------------------------------------
    # 10. ACTUAL PYTHON FUNCTION RUN KARO
    # -----------------------------------------------------

    tool_result = get_bank_balance(account_number)


    print("\nTool result:")
    print(tool_result)


    # -----------------------------------------------------
    # 11. TOOL RESULT GEMINI KO WAPAS DO
    # -----------------------------------------------------

    function_response_part = types.Part.from_function_response(
        name=function_call.name,

        response={
            "result": tool_result
        }
    )


    # -----------------------------------------------------
    # 12. ORIGINAL GEMINI RESPONSE + TOOL RESULT
    # -----------------------------------------------------

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=user_message
                )
            ]
        ),

        # Gemini ka previous response
        response.candidates[0].content,

        # Tool ka result
        types.Content(
            role="user",
            parts=[
                function_response_part
            ]
        )
    ]


    # =====================================================
    # 13. GEMINI KO FINAL ANSWER BANANE DO
    # =====================================================

    final_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config 
    )


    # =====================================================
    # 14. FINAL ANSWER
    # =====================================================

    print("\nFinal answer:")
    print(final_response.text)


else:

    # Gemini ne tool call nahi kiya
    print("\nGemini response:")
    print(response.text)


from langgraph.graph import StateGraph

app = StateGraph()

from langchain_aws import ChatBedrock

from typing import TypedDict

class Graphstate(TypedDict):
    messages : list 


from langgraph.graph import StateGraph , START , END

workflow = StateGraph(Graphstate)

def resuletsumedata():
    return "result sum the data"

def substractdata():
    return "subtract data"

workflow.add_node("sum" , resuletsumedata)
workflow.add_node("substract" , substractdata)

workflow.add_edge(START , "sum")
workflow.add_edge("substract" , "sum")



def conditionfunction():
    return "this is condition function okay "


workflow.add_conditional_edges(
    "sum" ,

    conditionfunction , 

)

