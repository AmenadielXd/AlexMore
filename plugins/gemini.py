from pyrogram.types import Message
from pyrogram.enums import ChatAction
from pyrogram import Client, filters
import requests
import asyncio
from Alex.utils.database import get_fsub # Assuming database functions (like FSUB, get_fsub) are defined here
import aiohttp
from Alex import app



# Generate a detailed prompt for image creation
def generate_long_query(query):
    return f"{query}."

@app.on_message(filters.command("draw"))
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



BASE_URL = "https://chatwithai.codesearch.workers.dev/?chat="

def ask_query(query: str) -> str:
    try:
        # Send GET request to the API
        response = requests.get(f"{BASE_URL}{query}")
        response.raise_for_status()
        # Parse JSON response
        data = response.json()  # Convert the response to a JSON object
        # Extract and return the "data" field if present
        return data.get("data", "⚠️ Error: Unexpected response format")
    except requests.exceptions.RequestException as e:
        return f"<b>ᴇʀʀᴏʀ:</b> {str(e)}"
    except json.JSONDecodeError:
        return "<b>ᴇʀʀᴏʀ:</b> ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴇᴄᴏᴅᴇ ᴛʜᴇ ʀᴇsᴘᴏɴsᴇ ғʀᴏᴍ ᴛʜᴇ sᴇʀᴠᴇʀ."

async def send_typing_action(client: Client, chat_id: int, duration: int = 1):
    await client.send_chat_action(chat_id, ChatAction.TYPING)
    await asyncio.sleep(duration)

@app.on_message(filters.command(["ai", "ask", "gemini"], prefixes=[".", "!", "/", ""]))
async def ask_query_command(client: Client, message: Message):
    if FSUB and not await get_fsub(client, message):
        return
    query = message.text.split(" ", 1)
    if len(query) > 1:
        await send_typing_action(client, message.chat.id)
        reply = ask_query(query[1])
        await message.reply_text(f"{message.from_user.mention}, {reply} 🚀")
    else:
        await message.reply_text("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ǫᴜᴇʀʏ ᴛᴏ ᴀsᴋ <b>ɢᴘᴛ-𝟺</b>. ᴅᴏɴ'ᴛ ʙᴇ sʜʏ, ʟᴇᴛ's ᴄʜᴀᴛ!")

@app.on_message(filters.mentioned & filters.group)
async def handle_mention(client: Client, message: Message):
    if FSUB and not await get_fsub(client, message):
        return
    user_text = (
        message.reply_to_message.text.strip()
        if message.reply_to_message
        else message.text.split(" ", 1)[1].strip()
        if len(message.text.split(" ", 1)) > 1
        else ""
    )
    if user_text:
        await send_typing_action(client, message.chat.id)
        reply = ask_query(user_text)
        await message.reply_text(f"{message.from_user.mention}, {reply} 🚀")
    else:
        await message.reply("ᴘʟᴇᴀsᴇ ᴀsᴋ ᴀ ǫᴜᴇsᴛɪᴏɴ ᴀғᴛᴇʀ ᴍᴇɴᴛɪᴏɴɪɴɢ ᴍᴇ! ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ!")