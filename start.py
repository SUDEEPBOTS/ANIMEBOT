from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.utils import to_small_caps # Importing helper

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    # converting user name to small caps
    user_name = to_small_caps(message.from_user.first_name)
    
    # Message Text in Small Caps
    text = (
        f"👋 **ʜᴇʟʟᴏ {user_name}!**\n\n"
        "🤖 **ɪ ᴀᴍ ᴀɴ ᴀɴɪᴍᴇ ꜰɪɴᴅᴇʀ ʙᴏᴛ.**\n"
        "ᴊᴜꜱᴛ ᴛʏᴘᴇ ᴛʜᴇ ᴀɴɪᴍᴇ ɴᴀᴍᴇ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ (ᴇ.ɢ. 'ɴᴀʀᴜᴛᴏ ɪɴ ʜɪɴᴅɪ') "
        "ᴀɴᴅ ɪ ᴡɪʟʟ ꜰɪɴᴅ ᴛʜᴇ ʟɪɴᴋ ꜰᴏʀ ʏᴏᴜ!\n\n"
        "⚡ **ᴘᴏᴡᴇʀᴇᴅ ʙʏ:** ᴀɴɪᴍᴇ ᴅɪꜱᴄᴏᴠᴇʀʏ ᴀᴘɪ"
    )
    
    # Button Text in Small Caps
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ", url="https://t.me/YourBotUser?startgroup=true")]
    ])
    
    await message.reply_text(text, reply_markup=buttons)
  
