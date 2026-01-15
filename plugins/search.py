import asyncio
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import API_URL
from plugins.utils import to_small_caps # Helper for Small Caps

# Trigger Words List (Standard English for matching logic)
TRIGGERS = ["in hindi", "dubbed", "dual audio", "english sub", "season", "s1", "s2", "hindi", "anime"]

# Function to verify if message should trigger the bot
def should_trigger(_, __, message):
    if not message.text: return False
    text = message.text.lower()
    # Check if any trigger word is present in the message
    return any(trig in text for trig in TRIGGERS)

# Create a custom filter
trigger_filter = filters.create(should_trigger)

@Client.on_message(filters.group & trigger_filter)
async def group_search(client, message):
    raw_query = message.text.lower()
    
    # 🧹 CLEANING: Remove trigger words to get the clean anime name
    clean_query = raw_query
    for word in TRIGGERS:
        clean_query = clean_query.replace(word, "").strip()
    
    # If query is too short after cleaning, ignore it
    if len(clean_query) < 2:
        return

    # Status Message (In Small Caps)
    status_text = to_small_caps("searching...")
    status_msg = await message.reply_text(f"🔍 **{status_text}**", quote=True)

    try:
        # 🔗 API CALL to your FastAPI Backend
        response = requests.get(f"{API_URL}/api/search?query={clean_query}")
        data = response.json()

        if data.get("status") == "success":
            anime = data["data"]
            title = anime["title"] # Official Title from API
            website_link = anime["website_link"] # Link from API
            
            # Converting Data to Small Caps
            sc_title = to_small_caps(title)
            sc_query = to_small_caps(clean_query)
            sc_result_text = to_small_caps("result found! click below to watch.")
            sc_title_label = to_small_caps("title")
            sc_search_label = to_small_caps("search")

            # Final Caption Construction
            caption = (
                f"🎬 **{sc_title_label}:** {sc_title}\n"
                f"🔎 **{sc_search_label}:** {sc_query}\n\n"
                f"⚡ **{sc_result_text}**"
            )

            # Buttons (Small Caps Text)
            btn_open_text = to_small_caps("open link")
            btn_close_text = to_small_caps("close")

            buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton(f"🚀 {btn_open_text}", url=website_link)],
    [
        InlineKeyboardButton("💝 ɪɴᴅᴇx", callback_data="support"),
        InlineKeyboardButton("🍷ᴀᴅᴅ ᴍᴇ", url="https://t.me/ANIMEFINDRRBOT?startgroup=true")
    ],
    [InlineKeyboardButton(f"❌ {btn_close_text}", callback_data="close_msg")]
])

            # Send Final Result
            final_msg = await message.reply_text(
                caption,
                reply_markup=buttons
            )
            
            # Delete "Searching..." status
            await status_msg.delete()

            # ⏳ AUTO DELETE (2 Minutes / 120 Seconds)
            await asyncio.sleep(999)
            try:
                await final_msg.delete()
                # Optional: Delete user's message too
                # await message.delete() 
            except:
                pass # Pass if message is already deleted

        else:
            # Not Found Error (Small Caps)
            error_text = to_small_caps("not found! check spelling.")
            await status_msg.edit_text(f"❌ **{error_text}**")
            await asyncio.sleep(10)
            await status_msg.delete()

    except Exception as e:
        print(f"Error: {e}")
        # API Error (Small Caps)
        api_err_text = to_small_caps("api error. try again later.")
        await status_msg.edit_text(f"⚠️ **{api_err_text}**")
        await asyncio.sleep(5)
        await status_msg.delete()

# --- CLOSE BUTTON LOGIC ---
@Client.on_callback_query(filters.regex("close_msg"))
async def close_button(client, callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
    except:
        pass
      
