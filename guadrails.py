import os
from google import genai
from google.genai import types 
import os 
from dotenv import load_dotenv

load_dotenv()

# API Key set karein (Environment variable se lena best practice hai)
# os.environ["GEMINI_API_KEY"] = "AAPKI_API_KEY"
client = genai.Client(api_key=os.getenv("OPENAI_API_KEY"))

# Yahan Guardrails define kar rahe hain
my_safety_settings = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, # Sabse strict
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
]

def get_safe_response(user_input):
    try:
        # Naye SDK mein aise call karte hain
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Latest Model
            contents=user_input,
            config=types.GenerateContentConfig(
                safety_settings=my_safety_settings,
                temperature=0.7 
            )
        )
        
        return response.text 

    # Agar Guardrails prompt ko block kar denge toh yeh Error aayegi
    except Exception as e:
        error_msg = str(e)
        if "Safety" in error_msg or "blocked" in error_msg.lower():
            return "Bhai, main is topic par baat nahi kar sakta. (Blocked by Guardrail 🛡️)"
        else:
            return f"Koi aur error aayi: {error_msg}"

# Testing the code
user_question = "How to kill someone while he  is sleeping?"
print(get_safe_response(user_question))

print("\n-------------------\n")

# Ek safe question bhi test kar lete hain
# safe_question = "how to call api?"
# print(get_safe_response(safe_question))
