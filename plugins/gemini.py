from pyrogram import Client, filters
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