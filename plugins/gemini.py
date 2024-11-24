import time
import requests
from Alex import app
from config import BOT_USERNAME

from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters


@app.on_message(filters.command(["chatgpt", "ai", "ask", "gpt", "solve", "gemini"], prefixes=["!", ".", "/", ""]))
async def chat_gpt(bot, message):
    try:
        start_time = time.time()
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "⬤ <b>ᴇxᴀᴍᴘʟᴇ ➠</b> <code>/ask What is Python?</code>"
            )
        else:
            query = message.text.split(' ', 1)[1]

            # Fetch response from the new API
            response = requests.get(f'https://search.codesearch.workers.dev/?query={query}')

            try:
                # Check if response is valid
                if response.status_code == 200:
                    result = response.text  # Assuming the API returns text; adjust if it returns JSON or another format.
                    end_time = time.time()
                    telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"

                    await message.reply_text(
                        f"**⥤ ʀᴇsᴜʟᴛ :**\n➥    {result}\n\n"
                        f"⬤ **ᴀɴsᴡᴇʀɪɴɢ ʙʏ ➠ [Nova UI](t.me/novauibot)**\n\n"
                        f"⏱️ **ʀᴇsᴘᴏɴsᴇ ᴛɪᴍᴇ:** {telegram_ping}",
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True
                    )
                else:
                    await message.reply_text("ɴᴏ ᴠᴀʟɪᴅ ʀᴇsᴘᴏɴsᴇ ғʀᴏᴍ ᴛʜᴇ ɢᴇᴍɪɴɪ.")
            except Exception as e:
                await message.reply_text(f"ᴇʀʀᴏʀ ᴘʀᴏᴄᴇssɪɴɢ ʀᴇsᴘᴏɴsᴇ: {e}")
    except Exception as e:
        await message.reply_text(f"Error - {e}")