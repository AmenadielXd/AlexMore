import asyncio, os, time, aiohttp
from asyncio import sleep
from Alex import app
from pyrogram import filters, Client, enums
from pyrogram.enums import ParseMode
from pyrogram.types import *
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from typing import Union, Optional
from pyrogram.types import Message


# user information 
INFO_TEXT = """
<u><b>ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b></u>
<b>● ᴜsᴇʀ ɪᴅ ➠</b> <code>{}</code>
<b>● ᴜsᴇʀɴᴀᴍᴇ ➠</b> <code>@{}</code>
<b>● ᴍᴇɴᴛɪᴏɴ ➠</b> {}
<b>● ᴜsᴇʀ sᴛᴀᴛᴜs ➠</b> {}
<b>● ᴜsᴇʀ ᴅᴄ ɪᴅ ➠</b> {}
"""

# --------------------------------------------------------------------------------- #

async def userstatus(user_id):
   try:
      user = await app.get_users(user_id)
      x = user.status
      if x == enums.UserStatus.RECENTLY:
         return "recently."
      elif x == enums.UserStatus.LAST_WEEK:
          return "last week."
      elif x == enums.UserStatus.LONG_AGO:
          return "seen long ago."
      elif x == enums.UserStatus.OFFLINE:
          return "User is offline."
      elif x == enums.UserStatus.ONLINE:
         return "User is online."
   except:
        return "**✦ sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ !**"

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(["info", "information", "userinfo"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def userinfo(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not message.reply_to_message and len(message.command) == 2:
        try:
            user_id = message.text.split(None, 1)[1]
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            await app.send_message(chat_id, text=INFO_TEXT.format(
                id, username, mention, status, dc_id), reply_to_message_id=message.id)
        except Exception as e:
            await message.reply_text(str(e))        

    elif not message.reply_to_message:
        try:
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            await app.send_message(chat_id, text=INFO_TEXT.format(
                id, username, mention, status, dc_id), reply_to_message_id=message.id)
        except Exception as e:
            await message.reply_text(str(e))


    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            await app.send_message(chat_id, text=INFO_TEXT.format(
                id, username, mention, status, dc_id), reply_to_message_id=message.id)
        except Exception as e:
            await message.reply_text(str(e))


# channel/group/user IDs 
@app.on_message(filters.command(["id"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def getid(client, message):
    chat = message.chat
    reply = message.reply_to_message

    # Initialize text based on reply or direct /id command
    if reply:
        # Check if there is a reply and add replied user ID in the desired format
        replied_user_name = reply.from_user.first_name
        replied_user_id = reply.from_user.id
        text = f"User {replied_user_name}'s ID is <code>{replied_user_id}</code>.\n"

        # Check if there is a forwarded message from a channel and add the channel ID in the desired format
        if reply.forward_from_chat:
            forwarded_channel_name = reply.forward_from_chat.title
            forwarded_channel_id = reply.forward_from_chat.id
            text += f"The forwarded channel, {forwarded_channel_name}, has an ID of <code>{forwarded_channel_id}</code>.\n\n"

        # Check if the reply is from a chat/channel and add its ID
        if reply.sender_chat:
            sender_chat_name = reply.sender_chat.title
            sender_chat_id = reply.sender_chat.id
            text += f"The replied chat/channel, {sender_chat_name}, has an ID of <code>{sender_chat_id}</code>."

    else:
        # If no reply, show only the chat ID
        text = f"This chat's ID is: <code>{chat.id}</code>."

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
    )


# chat information

# Command to get group information based on username
@app.on_message(filters.command("groupinfo", prefixes="/"))
async def get_group_status(_, message: Message):
    if len(message.command) != 2:
        await message.reply("Please provide a group username. Example: `/groupinfo YourGroupUsername`")
        return

    group_username = message.command[1]

    try:
        group = await app.get_chat(group_username)
    except Exception as e:
        await message.reply(f"Error: {e}")
        return

    total_members = await app.get_chat_members_count(group.id)
    group_description = group.description
    premium_acc = banned = deleted_acc = bot = 0  # You should replace these variables with actual counts.

    response_text = (
        f"<b><u>⬤ ɢʀᴏᴜᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ </u>𐏓</b>\n\n"
        f"<b>● ɢʀᴏᴜᴘ ɴᴀᴍᴇ ➠</b> {group.title}\n"
        f"<b>● ɢʀᴏᴜᴘ ɪᴅ ➠</b> {group.id}\n"
        f"<b>● ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs ➠</b> {total_members}\n"
        f"<b>● ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{group_username}\n"
        f"<b>● ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ➠</b> \n{group_description or 'N/A'}"
    )

    await message.reply(response_text)


# Command to get the status of the current group
@app.on_message(filters.command("status") & filters.group)
async def group_status(client, message: Message):
    chat = message.chat  # Chat where the command was sent
    status_text = (
        f"<b>● ɢʀᴏᴜᴘ ɪᴅ ➠</b> {chat.id}\n"
        f"<b>● ᴛɪᴛʟᴇ ➠</b> {chat.title}\n"
        f"<b>● ᴛʏᴘᴇ ➠</b> {chat.type}\n"
    )

    if chat.username:  # Not all groups have a username
        status_text += f"<b>● ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{chat.username}\n"
    else:
        status_text += "<b>● ᴜsᴇʀɴᴀᴍᴇ ➠</b> None\n"

    await message.reply_text(status_text)


# Running the bot
if __name__ == "__main__":
    app.run()
