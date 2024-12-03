from config import OWNER_ID, SUDO_USERS
from Alex import app
from pyrogram import Client, filters
from pyrogram.enums import ChatMembersFilter
import asyncio

# Function to check if the user is an admin, sudo user, or the bot owner
async def is_administrator_or_sudo(user_id: int, chat_id: int, client: Client):
    # Allow the bot owner to bypass the admin check
    if user_id == OWNER_ID:
        return True

    # Check if the user is in the list of sudo users
    if user_id in SUDO_USERS:
        return True

    # Check if the user is an administrator
    async for m in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if m.user.id == user_id:
            return True
    return False

@app.on_message(filters.command(["spam"], prefixes=[".", "/", "!"]) & filters.group)
async def spam(client, message):
    try:
        user_id = message.from_user.id

        # Check if the user is an admin, sudo user, or the bot owner
        is_allowed = await is_administrator_or_sudo(user_id, message.chat.id, client)
        if not is_allowed:
            await message.reply("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ, ʏᴏᴜ ᴍᴜsᴛ ʜᴀᴠᴇ sᴜᴅᴏ ᴛᴏ sᴘᴀᴍ.")
            return

        # Split the command text into components
        args = message.text.split()
        if len(args) < 3:
            await message.reply("<b>ᴜsᴀɢᴇ</b>\n➥  .sᴘᴀᴍ <ᴍᴇssᴀɢᴇs> <ɴᴜᴍʙᴇʀ ᴏғ ᴍᴇssᴀɢᴇs>")
            return

        # Extract the number of messages from the last argument
        try:
            number_of_messages = int(args[-1])
        except ValueError:
            await message.reply("ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ᴏғ ᴍᴇssᴀɢᴇs.")
            return

        # Join the remaining arguments to form the message text
        spam_text = " ".join(args[1:-1])

        # Validate the number of messages
        if number_of_messages <= 0:
            await message.reply("ɴᴜᴍʙᴇʀ ᴏғ ᴍᴇssᴀɢᴇs ᴍᴜsᴛ ʙᴇ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ 0")
            return

        # Delete the original command message
        await message.delete()

        # Send messages with a 2-second interval
        for _ in range(number_of_messages):
            await message.reply_text(spam_text)
            await asyncio.sleep(2)  # Sleep for 2 seconds asynchronously

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")