import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "123456")) # Telegram API ID
API_HASH = os.getenv("API_HASH", "your_hash_here")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# Ye tera FastAPI ka URL hai (Jahan main.py chal raha hai)
# Agar local hai toh http://localhost:8000
# Agar Render/Vercel pe hai toh uska link daal
API_URL = os.getenv("API_URL", "http://localhost:8000") 
