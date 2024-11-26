import aiohttp
import time
import requests
from Alex import app
from config import BOT_USERNAME
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
 
# Generate a detailed prompt for image creation
def generate_long_query(query):
    return f"{query}."

@app.on_message(filters.command(["draw"], prefixes=["", "!", "/", "."]))
async def draw_image(client, message):
    if len(message.command) < 2:
        await message.reply_text("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ǫᴜᴇʀʏ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀɴ ɪᴍᴀɢᴇ.")
        return

    # Generate a long query for better image results
    user_query = message.text.split(" ", 1)[1]
    query = generate_long_query(user_query)

    # Send initial message
    wait_message = await message.reply_text("<b>ɢᴇɴᴇʀᴀᴛɪɴɢ ɪᴍᴀɢᴇ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ . . .</b>")

    # Asynchronous request using aiohttp
    url = f"https://text2img.codesearch.workers.dev/?prompt={query}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.json()
                    if "imageUrl" in image_data:
                        image_url = image_data["imageUrl"]
                        await wait_message.delete()  # Delete wait message
                        await message.reply_photo(photo=image_url, caption=f"<b>Generated Image for:</b> {user_query}")
                    else:
                        await wait_message.edit_text("ɴᴏ ɪᴍᴀɢᴇs ᴡᴇʀᴇ ʀᴇᴛᴜʀɴᴇᴅ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")
                else:
                    await wait_message.edit_text("<b>ᴇʀʀᴏʀ:</b> ᴜɴᴀʙʟᴇ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ɪᴍᴀɢᴇ ᴀᴛ ᴛʜɪs ᴛɪᴍᴇ. ᴘʟᴇᴀsᴇ ᴛʀʏ ʟᴀᴛᴇʀ.")
    except Exception as e:
        # Try to edit or delete the message only if it exists
        try:
            await wait_message.edit_text(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ: {e}")
        except Exception:
            await message.reply_text(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ: {e}")

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
                        f"⥤ ʀᴇsᴜʟᴛ :\n➥    {result}\n\n"
                        f"⬤ ᴀɴsᴡᴇʀɪɴɢ ʙʏ ➠ [Nova UI](t.me/novauibot)\n\n"
                        f"⏱️ ʀᴇsᴘᴏɴsᴇ ᴛɪᴍᴇ: {telegram_ping}",
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True
                    )
                else:
                    await message.reply_text("ɴᴏ ᴠᴀʟɪᴅ ʀᴇsᴘᴏɴsᴇ ғʀᴏᴍ ᴛʜᴇ ɢᴇᴍɪɴɪ.")
            except Exception as e:
                await message.reply_text(f"ᴇʀʀᴏʀ ᴘʀᴏᴄᴇssɪɴɢ ʀᴇsᴘᴏɴsᴇ: {e}")
    except Exception as e:
        await message.reply_text(f"Error - {e}")
Updated ai