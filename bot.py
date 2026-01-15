from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

class AnimeBot(Client):
    def __init__(self):
        super().__init__(
            "AnimeFinderBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins") # ✨ AUTO LOADER MAGIC
        )

    async def start(self):
        await super().start()
        print("✅ Bot Started & Plugins Loaded!")

    async def stop(self, *args):
        await super().stop()
        print("❌ Bot Stopped")

if __name__ == "__main__":
    app = AnimeBot()
    app.run()
  
