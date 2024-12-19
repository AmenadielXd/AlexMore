import random
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ChatAdminRequired
from Alex import app
from Alex.utils.database import add_served_chat, get_assistant

LOG_GROUP_ID = -1002063031380

@app.on_message(filters.new_chat_members, group=-10)
async def join_watcher(_, message):
    try:
        userbot = await get_assistant(message.chat.id)
        chat = message.chat
        for member in message.new_chat_members:
            if member.id == app.id:
                try:
                    invitelink = await app.export_chat_invite_link(chat.id)
                    link = f"<a href='{invitelink}'>ɢᴇᴛ ʟɪɴᴋ</a>"
                except ChatAdminRequired:
                    link = "No Link"

                try:
                    groups_photo = await app.download_media(
                        chat.photo.big_file_id, file_name=f"chatpp{chat.id}.png"
                    )
                    chat_photo = groups_photo if groups_photo else "Alex/assets/nodp.png"
                except AttributeError:
                    chat_photo = "Alex/assets/nodp.png"

                count = await app.get_chat_members_count(chat.id)
                username = chat.username if chat.username else "ᴘ-ᴄʜᴀᴛ"
                msg = (
                    f"<b>⬤ ʙᴏᴛ ᴀᴅᴅᴇᴅ ɪɴ ᴀ #ɴᴇᴡ_ɢʀᴏᴜᴘ</b>\n\n"
                    f"<b>● ɢʀᴏᴜᴘ ɴᴀᴍᴇ ➠</b> {chat.title}\n"
                    f"<b>● ɢʀᴏᴜᴘ ɪᴅ ➠</b> <code>{chat.id}</code>\n"
                    f"<b>● ɢʀᴏᴜᴘ ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{username}\n"
                    f"<b>● ɢʀᴏᴜᴘ ʟɪɴᴋ ➠ {link}</b>\n"
                    f"<b>● ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs ➠</b> {count}\n"
                    f"<b>⬤ ᴀᴅᴅᴇᴅ ʙʏ ➠</b> {message.from_user.mention}"
                )

                await app.send_photo(
                    LOG_GROUP_ID,
                    photo=chat_photo,
                    caption=msg,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                            f"{message.from_user.first_name}",
                                            user_id=message.from_user.id)]]))
                await add_served_chat(chat.id)
                await userbot.join_chat(f"{username}")

    except Exception as e:
        print(f"Error: {e}")


LEFT = [
    "https://unitedcamps.in/Images/file_4107.jpg",
    "https://unitedcamps.in/Images/file_4106.jpg",
    "https://unitedcamps.in/Images/file_4105.jpg",
    "https://unitedcamps.in/Images/file_4104.jpg",    
]

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        remove_by = message.from_user.mention if message.from_user else "𝐔ɴᴋɴᴏᴡɴ 𝐔sᴇʀ"
        title = message.chat.title
        username = f"@{message.chat.username}" if message.chat.username else "𝐏ʀɪᴠᴀᴛᴇ 𝐂ʜᴀᴛ"
        chat_id = message.chat.id
        left = f"<b>⬤ ʙᴏᴛ #ʟᴇғᴛ_ɢʀᴏᴜᴘ ʙʏ ᴀ ᴄʜᴜᴛɪʏᴀ ⬤</b>\n\n<b>● ɢʀᴏᴜᴘ ɴᴀᴍᴇ ➠</b> {title}\n\n<b>● ɢʀᴏᴜᴘ ɪᴅ ➠</b> <code>{chat_id}</code>\n\n<b>● ʙᴏᴛ ʀᴇᴍᴏᴠᴇᴅ ʙʏ ➠</b> {remove_by}"
        await app.send_photo(LOG_GROUP_ID, photo=random.choice(LEFT), caption=left, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/{app.username}?startgroup=true")]
         ]))

#welcome