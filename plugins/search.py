import asyncio
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import API_URL
from plugins.utils import to_small_caps # Helper for Small Caps

# Trigger Words List
TRIGGERS = ["in hindi", "dubbed", "dual audio", "english sub", "season", "s1", "s2", "hindi", "anime"]

# Function to verify if message should trigger the bot
def should_trigger(_, __, message):
    if not message.text: return False
    text = message.text.lower()
    return any(trig in text for trig in TRIGGERS)

trigger_filter = filters.create(should_trigger)

@Client.on_message(filters.group & trigger_filter)
async def group_search(client, message):
    raw_query = message.text.lower()
    
    # 🧹 CLEANING
    clean_query = raw_query
    for word in TRIGGERS:
        clean_query = clean_query.replace(word, "").strip()
    
    if len(clean_query) < 2: return

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
            website_link = anime["website_link"] # Backup Link
            direct_links = anime.get("links", []) # List of Direct Links
            
            # Slug for Report Feature (Extract from URL)
            slug = website_link.split("/")[-1]

            # Converting Data to Small Caps
            sc_title = to_small_caps(title)
            sc_query = to_small_caps(clean_query)
            sc_found = to_small_caps("links found! select below.")
            sc_title_lbl = to_small_caps("title")
            sc_search_lbl = to_small_caps("search")

            # Final Caption
            caption = (
                f"🎬 **{sc_title_lbl}:** {sc_title}\n"
                f"🔎 **{sc_search_lbl}:** {sc_query}\n\n"
                f"⚡ **{sc_found}**"
            )

            # --- DYNAMIC BUTTONS BUILDER ---
            buttons = []
            
            # 1. Direct Source Buttons (2 per row)
            # Ye API se aaye huye Telegram Links hain
            row = []
            for i, link in enumerate(direct_links):
                btn_lbl = to_small_caps(f"source {i+1}")
                row.append(InlineKeyboardButton(f"📺 {btn_lbl}", url=link))
                if len(row) == 2:
                    buttons.append(row)
                    row = []
            if row: buttons.append(row)

            # 2. Website / Backup Button
            btn_web = to_small_caps("website / backup")
            buttons.append([InlineKeyboardButton(f"🌐 {btn_web}", url=website_link)])

            # 3. Tere Custom Buttons (Index & Add Me)
            buttons.append([
                InlineKeyboardButton("💝 ɪɴᴅᴇx", url="https://t.me/+ztVvubasBehjZDA1"),
                InlineKeyboardButton("🍷ᴀᴅᴅ ᴍᴇ", url="https://t.me/ANIMEFINDRRBOT?startgroup=true")
            ])

            # 4. Report & Close Buttons
            btn_report = to_small_caps("report")
            btn_close = to_small_caps("close")
            buttons.append([
                InlineKeyboardButton(f"⚠️ {btn_report}", callback_data=f"report_{slug}"),
                InlineKeyboardButton(f"❌ {btn_close}", callback_data="close_msg")
            ])

            # Send Final Result
            final_msg = await message.reply_text(
                caption,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            
            await status_msg.delete()

            # ⏳ AUTO DELETE (999 Seconds as per your request)
            await asyncio.sleep(999)
            try: await final_msg.delete()
            except: pass

        else:
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

# --- CALLBACK HANDLERS (Close & Report) ---

@Client.on_callback_query(filters.regex(r"^close_msg"))
async def close_button(client, callback_query: CallbackQuery):
    try: await callback_query.message.delete()
    except: pass

@Client.on_callback_query(filters.regex(r"^report_"))
async def report_button(client, callback_query: CallbackQuery):
    slug = callback_query.data.split("_")[1]
    try:
        # Calls API to register report
        requests.post(f"{API_URL}/api/action/{slug}/reports")
        msg = to_small_caps("reported to admin! thanks.")
        await callback_query.answer(f"🛡️ {msg}", show_alert=True)
    except:
        await callback_query.answer("⚠️ Error reporting.", show_alert=True)
