import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "123456")) # Telegram API ID
API_HASH = os.getenv("API_HASH", "your_hash_here")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# Ye tera FastAPI ka URL hai (Jahan main.py chal raha hai)
API_URL = os.getenv("API_URL", "http://localhost:8000") 

# 🟢 Groq API Key (AI Check ke liye)
# Isko apni .env file mein zaroor add karna: GROQ_API_KEY=gsk_...
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")
