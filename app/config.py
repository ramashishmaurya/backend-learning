import os 
from dotenv import load_dotenv

load_dotenv()

class settings : 
    DATABASE_URL = os.getenv("DATABASE_url")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


settings = settings()


