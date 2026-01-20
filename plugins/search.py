import asyncio
import requests
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from groq import AsyncGroq  # 🟢 Groq Import
from config import API_URL, GROQ_API_KEY # 🟢 Config me GROQ_API_KEY daal dena
from plugins.utils import to_small_caps

# 🟢 Setup Groq Client
groq_client = AsyncGroq(api_key=GROQ_API_KEY)

# Trigger Words List (Purana wala)
TRIGGERS = ["in hindi", "dubbed", "dual audio", "english sub", "season", "s1", "s2", "hindi", "anime"]

# --- AI CHECK FUNCTION ---
async def is_anime_query(text):
    """
    Groq se puchta hai ki text Anime hai ya nahi.
    Returns: True/False
    """
    try:
        completion = await groq_client.chat.completions.create(
            model="llama3-8b-8192", # Ya koi bhi fast model jo available ho
            messages=[
                {
                    "role": "system",
                    "content": "You are a classifier. Check if the user text is a search query for an Anime, Manga, Donghua, or Cartoon. Ignore casual conversation like 'hello', 'how are you', 'kya hal hai'. If it is a likely Anime title/search, reply exactly 'YES'. Otherwise reply 'NO'."
                },
                {
                    "role": "user",
                    "content": f"Text: {text}"
                }
            ],
            temperature=0,
            max_tokens=5
        )
        answer = completion.choices[0].message.content.strip().upper()
        return "YES" in answer
    except Exception as e:
        print(f"Groq Error: {e}")
        return False

# 🟢 Filter hata diya, ab har group message check hoga
@Client.on_message(filters.group & filters.text)
async def group_search(client, message):
    raw_query = message.text.lower().strip()
    
    # Ignore very short messages to save API
    if len(raw_query) < 2: return

    # --- LOGIC START ---
    
    # 1. Pehle purane Triggers check karo (Fastest Way)
    has_trigger = any(trig in raw_query for trig in TRIGGERS)
    
    clean_query = raw_query
    should_search = False

    if has_trigger:
        # Agar trigger word hai, toh purana logic
        should_search = True
        for word in TRIGGERS:
            clean_query = clean_query.replace(word, "").strip()
    else:
        # 2. Agar Trigger nahi hai, toh Groq se pucho (AI Way)
        # Sirf tab pucho agar message bahut lamba na ho (spam prevention)
        if len(raw_query) < 50: 
            is_anime = await is_anime_query(raw_query)
            if is_anime:
                should_search = True
                clean_query = raw_query # Naam wahi hai, koi "dubbed" word nahi hatana
    
    # Agar dono checks fail ho gaye (na trigger tha, na anime naam), toh return kardo
    if not should_search:
        return

    # --- SEARCH LOGIC (Same as your old code) ---

    # Status Message
    status_text = to_small_caps("searching...")
    status_msg = await message.reply_text(f"🔍 **{status_text}**", quote=True)

    try:
        # 🔗 API CALL
        response = requests.get(f"{API_URL}/api/search?query={clean_query}", timeout=25)
        data = response.json()

        if data.get("status") == "success":
            anime = data["data"]
            title = anime["title"]
            website_link = anime["website_link"]
            direct_links = anime.get("links", [])
            
            slug = website_link.split("/")[-1]

            # Small Caps Conversion
            sc_title = to_small_caps(title)
            sc_query = to_small_caps(clean_query)
            sc_found = to_small_caps("links found! select below.")
            sc_title_lbl = to_small_caps("title")
            sc_search_lbl = to_small_caps("search")

            caption = (
                f"🎬 **{sc_title_lbl}:** {sc_title}\n"
                f"🔎 **{sc_search_lbl}:** {sc_query}\n\n"
                f"⚡ **{sc_found}**"
            )

            # Buttons
            buttons = []
            row = []
            for i, link in enumerate(direct_links):
                btn_lbl = to_small_caps(f"source {i+1}")
                row.append(InlineKeyboardButton(f"📺 {btn_lbl}", url=link))
                if len(row) == 2:
                    buttons.append(row)
                    row = []
            if row: buttons.append(row)

            btn_web = to_small_caps("website / backup")
            buttons.append([InlineKeyboardButton(f"🌐 {btn_web}", url=website_link)])

            buttons.append([
                InlineKeyboardButton("💝 ɪɴᴅᴇx", url="https://t.me/+ztVvubasBehjZDA1"),
                InlineKeyboardButton("🍷ᴀᴅᴅ ᴍᴇ", url="https://t.me/ANIMEFINDRRBOT?startgroup=true")
            ])

            btn_report = to_small_caps("report")
            btn_close = to_small_caps("close")
            buttons.append([
                InlineKeyboardButton(f"⚠️ {btn_report}", callback_data=f"report_{slug}"),
                InlineKeyboardButton(f"❌ {btn_close}", callback_data="close_msg")
            ])

            final_msg = await message.reply_text(
                caption,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            
            await status_msg.delete()

            await asyncio.sleep(999)
            try: await final_msg.delete()
            except: pass

        else:
            # Agar Groq ne kaha Anime hai, par API me nahi mila
            error_text = to_small_caps("not found! check spelling.")
            await status_msg.edit_text(f"❌ **{error_text}**")
            await asyncio.sleep(10)
            await status_msg.delete()

    except Exception as e:
        print(f"Error: {e}")
        api_err_text = to_small_caps("api error. try again later.")
        await status_msg.edit_text(f"⚠️ **{api_err_text}**")
        await asyncio.sleep(5)
        await status_msg.delete()

# Callback Handlers same rahenge...
