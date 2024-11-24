from config import OWNER_ID
from Alex import app
from pyrogram import Client, filters
from pyrogram.enums import ChatMembersFilter
import asyncio


# Function to check if the user is an admin or the bot owner
async def is_administrator(user_id: int, chat_id: int, client: Client):
    # Allow the bot owner to bypass the admin check
    if user_id == OWNER_ID:
        return True
    
    administrators = []
    async for m in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)
    for admin in administrators:
        if admin.user.id == user_id:
            return True
    return False

@app.on_message(filters.command(["spam"], prefixes=[".", "/", "!",]) & filters.group)
async def spam(client, message):
    try:
        # Check if the user is an admin or the bot owner
        is_admin = await is_administrator(message.from_user.id, message.chat.id, client)
        if not is_admin:
            await message.reply("Only admins can use the spam command")
            return

        # Split the command text into components
        args = message.text.split()
        if len(args) < 3:
            await message.reply("<b>ᴜsᴀɢᴇ ➠</b> .sᴘᴀᴍ <ᴍᴇssᴀɢᴇs> <ɴᴜᴍʙᴇʀ ᴏғ ᴍᴇssᴀɢᴇs>")
            return

        # Extract the number of messages from the last argument
        try:
            number_of_messages = int(args[-1])
        except ValueError:
            await message.reply("Please enter a valid number of messages.")
            return

        # Join the remaining arguments to form the reason
        reason = " ".join(args[1:-1])

        # Validate number of messages
        if number_of_messages <= 0:
            await message.reply("Number of messages must be greater than 0.")
            return

        # Delete the original command message
        await message.delete()

        # Send messages with a 2-second interval
        for _ in range(number_of_messages):
            await message.reply_text(reason)
            await asyncio.sleep(2)  # Sleep for 2 seconds asynchronously

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")