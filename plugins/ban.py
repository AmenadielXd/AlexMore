import asyncio
from contextlib import suppress

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import (
    CallbackQuery,
    ChatPermissions,
    ChatPrivileges,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from string import ascii_lowercase
from typing import Dict, Union

from Alex import app
from Alex.misc import SUDOERS
from Alex.core.mongo import mongodb
from utils.error import capture_err
from utils.keyboard import ikb
from Alex.utils.functions import (
    extract_user,
    extract_user_and_reason,
    time_converter,
)
from Alex.utils.permissions import adminsOnly, member_permissions
from config import BANNED_USERS

warnsdb = mongodb.warns


async def int_to_alpha(user_id: int) -> str:
    alphabet = list(ascii_lowercase)[:10]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text


async def get_warns_count() -> dict:
    chats_count = 0
    warns_count = 0
    async for chat in warnsdb.find({"chat_id": {"$lt": 0}}):
        for user in chat["warns"]:
            warns_count += chat["warns"][user]["warns"]
        chats_count += 1
    return {"chats_count": chats_count, "warns_count": warns_count}


async def get_warns(chat_id: int) -> Dict[str, int]:
    warns = await warnsdb.find_one({"chat_id": chat_id})
    if not warns:
        return {}
    return warns["warns"]


async def get_warn(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    if name in warns:
        return warns[name]


async def add_warn(chat_id: int, name: str, warn: dict):
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    warns[name] = warn

    await warnsdb.update_one(
        {"chat_id": chat_id}, {"$set": {"warns": warns}}, upsert=True
    )


async def remove_warns(chat_id: int, name: str) -> bool:
    warnsd = await get_warns(chat_id)
    name = name.lower().strip()
    if name in warnsd:
        del warnsd[name]
        await warnsdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"warns": warnsd}},
            upsert=True,
        )
        return True
    return False



# ban
@app.on_message(
    filters.command(["ban"]) & ~filters.private & ~BANNED_USERS
)
@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text(
            "<u><b>ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.</b></u>\n"
            "ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ <b>/ban</b> ᴍᴜsᴛ ʙᴇ ᴜsᴇᴅ sᴘᴇᴄɪғʏɪɴɢ ᴜsᴇʀ <b>ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ/ᴍᴇɴᴛɪᴏɴ ᴏʀ ʀᴇᴘʟʏɪɴɢ</b> ᴛᴏ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs."
        )
    if user_id == app.id:
        return await message.reply_text("I can't ban myself, i can leave if you want.")
    if user_id in SUDOERS:
        return await message.reply_text("You Wanna Ban The Elevated One?, RECONSIDER!")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "I can't ban an admin, You know the rules, so do i."
        )

    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )

    msg = (
        f"<b>● ʙᴀɴɴᴇᴅ ᴜsᴇʀ ➠</b> {mention}\n"
        f"<b>● ʙᴀɴɴᴇᴅ ʙʏ ➠</b> {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"<b>● ʀᴇᴀsᴏɴ ➠</b> {reason}"
    await message.chat.ban_member(user_id)
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg)


#sban
@app.on_message(
    filters.command(["sban"]) & ~filters.private & ~BANNED_USERS
)
@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text(
            "<u><b>ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.</b></u>\n"
            "ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ <b>/ban</b> ᴍᴜsᴛ ʙᴇ ᴜsᴇᴅ sᴘᴇᴄɪғʏɪɴɢ ᴜsᴇʀ <b>ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ/ᴍᴇɴᴛɪᴏɴ ᴏʀ ʀᴇᴘʟʏɪɴɢ</b> ᴛᴏ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs."
        )
    if user_id == app.id:
        return await message.reply_text("I can't ban myself, i can leave if you want.")
    if user_id in SUDOERS:
        return await message.reply_text("You Wanna Ban The Elevated One?, RECONSIDER!")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "I can't ban an admin, You know the rules, so do i."
        )

    await message.chat.ban_member(user_id)

    # Send the "Nice knowing you!" message
    await message.reply_text("Nice knowing you!")

    # Delete only the command message, not the replied message
    await message.delete()


# dban


@app.on_message(
    filters.command(["dban"]) & ~filters.private & ~BANNED_USERS
)
@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text(
            "<u><b>ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.</b></u>\n"
            "ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ <b>/ban</b> ᴍᴜsᴛ ʙᴇ ᴜsᴇᴅ sᴘᴇᴄɪғʏɪɴɢ ᴜsᴇʀ <b>ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ/ᴍᴇɴᴛɪᴏɴ ᴏʀ ʀᴇᴘʟʏɪɴɢ</b> ᴛᴏ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs."
        )
    if user_id == app.id:
        return await message.reply_text("I can't ban myself, i can leave if you want.")
    if user_id in SUDOERS:
        return await message.reply_text("You Wanna Ban The Elevated One?, RECONSIDER!")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "I can't ban an admin, You know the rules, so do i."
        )

    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )

    msg = (
        f"<b>● ʙᴀɴɴᴇᴅ ᴜsᴇʀ ➠</b> {mention}\n"
        f"<b>● ʙᴀɴɴᴇᴅ ʙʏ ➠</b> {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"<b>● ʀᴇᴀsᴏɴ ➠</b> {reason}"

    await message.chat.ban_member(user_id)

    # Delete the user's message if it was a reply
    replied_message = message.reply_to_message
    if replied_message:
        await replied_message.delete()

    # Delete the ban command message
    await message.delete()

    # Optionally send the ban notification
    sent_msg = await message.reply_text(msg)

    # Delete the ban notification after a few seconds (optional)
    await asyncio.sleep(5)
    await sent_msg.delete()


# tban
@app.on_message(filters.command(["tban"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def tban(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == app.id:
        return await message.reply_text("I can't ban myself.")
    if user_id in SUDOERS:
        return await message.reply_text("You wanna ban the elevated one?, RECONSIDER!")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "I can't ban an admin, You know the rules, so do I."
        )

    mention = (await app.get_users(user_id)).mention
    keyboard = ikb({"Unban": f"unban_{user_id}"})

    # Handling the temporary ban
    split = reason.split(None, 1)
    time_value = split[0]
    temp_reason = split[1] if len(split) > 1 else ""
    temp_ban = await time_converter(message, time_value)
    msg = (
        f"<b>● Banned User ➠</b> {mention}\n"
        f"<b>● Banned By ➠</b> {message.from_user.mention if message.from_user else 'Anon'}\n"
        f"<b>● Banned For ➠</b> {time_value}\n"
    )

    if temp_reason:
        msg += f"<b>● Reason ➠</b> {temp_reason}"

    try:
        if len(time_value[:-1]) < 3:
            await message.chat.ban_member(
                user_id,
                until_date=temp_ban,
            )
            replied_message = message.reply_to_message
            if replied_message:
                message = replied_message
            await message.reply_text(msg, reply_markup=keyboard)
        else:
            await message.reply_text("You can't use more than 99")
    except AttributeError:
        pass



# unban 
@app.on_message(filters.command("unban") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def unban_func(_, message: Message):
    reply = message.reply_to_message
    user_id = await extract_user(message)

    # Check if user ID is found, otherwise return custom message
    if not user_id:
        return await message.reply_text(
            "<b><u>ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.</b></u>\n"
            "ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ <b>/unban</b> ᴍᴜsᴛ ʙᴇ ᴜsᴇᴅ sᴘᴇᴄɪғʏɪɴɢ ᴜsᴇʀ <b>ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ/ᴍᴇɴᴛɪᴏɴ ᴏʀ ʀᴇᴘʟʏɪɴɢ</b> ᴛᴏ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs."
        )

    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await message.reply_text("You cannot unban a channel")

    await message.chat.unban_member(user_id)
    umention = (await app.get_users(user_id)).mention
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(f"Unbanned! {umention}")



# Mute members
@app.on_message(filters.command(["mute", "tmute"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def mute(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == app.id:
        return await message.reply_text("I can't mute myself.")
    if user_id in SUDOERS:
        return await message.reply_text("You wanna mute the elevated one?, RECONSIDER!")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "I can't mute an admin, You know the rules, so do i."
        )
    mention = (await app.get_users(user_id)).mention
    keyboard = ikb({"Unmute": f"unmute_{user_id}"})
    msg = (
        f"<b>● Muted User ➠</b> {mention}\n"
        f"<b>● Muted By ➠</b> {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0] == "tmute":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_mute = await time_converter(message, time_value)
        msg += f"<b>● Muted For ➠</b> {time_value}\n"
        if temp_reason:
            msg += f"<b>● Reason ➠</b> {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.restrict_member(
                    user_id,
                    permissions=ChatPermissions(),
                    until_date=temp_mute,
                )
                replied_message = message.reply_to_message
                if replied_message:
                    message = replied_message
                await message.reply_text(msg, reply_markup=keyboard)
            else:
                await message.reply_text("You can't use more than 99")
        except AttributeError:
            pass
        return
    if reason:
        msg += f"<b>● Reason ➠</b> {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg, reply_markup=keyboard)


# smute
@app.on_message(filters.command("smute") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def smute(_, message: Message):
    user_id, _ = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == app.id:
        return await message.reply_text("I can't mute myself.")
    if user_id in SUDOERS:
        return await message.reply_text("You wanna mute the elevated one?, RECONSIDER!")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text("I can't mute an admin, You know the rules, so do I.")

    await message.chat.restrict_member(user_id, permissions=ChatPermissions())

    # Delete the smute command message
    await message.delete()


# dmute 
@app.on_message(filters.command(["dmute"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def mute(_, message: Message):
    # Check if the command was used as a reply to a message
    if not message.reply_to_message:
        return await message.reply_text("You have to reply to a message to delete it and mute the user.")

    user_id, reason = await extract_user_and_reason(message)

    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == app.id:
        return await message.reply_text("I can't mute myself.")
    if user_id in SUDOERS:
        return await message.reply_text("You wanna mute the elevated one?, RECONSIDER!")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "I can't mute an admin, You know the rules, so do I."
        )

    mention = (await app.get_users(user_id)).mention
    keyboard = ikb({"Unmute": f"unmute_{user_id}"})
    msg = (
        f"<b>● Muted User ➠</b> {mention}\n"
        f"<b>● Muted By ➠</b> {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"<b>● Reason ➠</b> {reason}"

    await message.chat.restrict_member(user_id, permissions=ChatPermissions())

    # Delete the replied message
    replied_message = message.reply_to_message
    await replied_message.delete()

    await message.reply_text(msg, reply_markup=keyboard)



# unmute command 
@app.on_message(filters.command("unmute") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def unmute(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    await message.chat.unban_member(user_id)
    umention = (await app.get_users(user_id)).mention
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(f"Unmuted! {umention}")


# handler for the unmute button
@app.on_callback_query(filters.regex(r"unmute_(\d+)"))
async def unmute_button_handler(_, query: CallbackQuery):
    from_user = query.from_user
    chat_id = query.message.chat.id
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_restrict_members"

    # Check if the user who clicked the button has 'can_restrict_members' permission
    if permission not in permissions:
        return await query.answer(
            "You don't have enough permissions to perform this action\n"
            + f"Permission needed: {permission}",
            show_alert=True,
        )

    # Unmute the user if permission is valid
    user_id = int(query.data.split("_")[1])
    await query.message.chat.unban_member(user_id)

    # Get the user's mention
    user_mention = (await app.get_users(user_id)).mention

    # Edit the original message to reflect the unmute action
    await query.message.edit_text(f"Unmuted! {user_mention}")

    # Notify the user who pressed the button
    await query.answer("User has been unmuted.")


# kickme
@app.on_message(filters.command("kickme") & ~filters.private & ~BANNED_USERS)
async def kick_me(_, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    mention = message.from_user.mention
    
    # Check if the user is an admin
    is_admin = False
    async for member in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if member.user.id == user_id:
            is_admin = True
            break
    
    if is_admin:
        # Message if an admin tries to use the command
        await message.reply_text("Ha, I'm not kicking you, you're an admin! You're stuck with everyone here.")
    else:
        # Message for non-admins
        await message.chat.ban_member(user_id)
        await message.reply_text("Yeah, you're right - get out.")
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)

# kick
@app.on_message(filters.command("kick") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def kickFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ")
    if user_id == app.id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴍʏsᴇʟғ, ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ ɪғ ʏᴏᴜ ᴡᴀɴᴛ.")
    if user_id in SUDOERS:
        return await message.reply_text("ʏᴏᴜ ᴡᴀɴɴᴀ ᴋɪᴄᴋ ᴛʜᴇ ᴇʟᴇᴠᴀᴛᴇᴅ ᴏɴᴇ ?")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴀɴ ᴀᴅᴍɪɴ, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇs, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇs, sᴏ ᴅᴏ ɪ "
        )
    mention = (await app.get_users(user_id)).mention
    msg = f"""
<b>ᴋɪᴄᴋᴇᴅ ᴜsᴇʀ ➠</b> {mention}
<b>ᴋɪᴄᴋᴇᴅ ʙʏ ➠</b> {message.from_user.mention if message.from_user else 'ᴀɴᴏɴᴍᴏᴜs'}
<b>ʀᴇᴀsᴏɴ ➠</b> {reason or 'ɴᴏ ʀᴇᴀsᴏɴ ᴘʀᴏᴠɪᴅᴇᴅ'}"""
    await message.chat.ban_member(user_id)
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)


# skick
@app.on_message(filters.command("skick") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def skickFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)

    # Delete the command message after triggering
    await message.delete()

    if not user_id:
        return
    if user_id == app.id:
        return
    if user_id in SUDOERS:
        return
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return

    # Kick the user without sending any confirmation message in the chat
    await message.chat.ban_member(user_id)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)


# dkick
@app.on_message(filters.command("dkick") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def dkickFunc(_, message: Message):
    # Ensure that the command is used as a reply to a message
    if not message.reply_to_message:
        return await message.reply_text("ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ ɪᴛ ᴀɴᴅ ᴋɪᴄᴋ ᴛʜᴇ ᴜsᴇʀ.")

    user_id = message.reply_to_message.from_user.id
    reason = await extract_user_and_reason(message)
    
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == app.id:
        return await message.reply_text("I can't kick myself, but I can leave if you want.")
    if user_id in SUDOERS:
        return await message.reply_text("You wanna kick the elevated one?")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "I can't kick an admin, you know the rules."
        )

    mention = (await app.get_users(user_id)).mention
    msg = f"""
<b>Kicked User ➠</b> {mention}
<b>Kicked By ➠</b> {message.from_user.mention if message.from_user else 'Anonymous'}
<b>Reason ➠</b> {reason or 'No reason provided'}"""

    # Delete the replied-to message and kick the user
    await message.reply_to_message.delete()
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)



# purge
@app.on_message(filters.command("purge") & ~filters.private)
@adminsOnly("can_delete_messages")
async def purgeFunc(_, message: Message):
    repliedmsg = message.reply_to_message
    await message.delete()

    if not repliedmsg:
        return await message.reply_text("Reply to a message to purge from.")

    cmd = message.command
    if len(cmd) > 1 and cmd[1].isdigit():
        purge_to = repliedmsg.id + int(cmd[1])
        if purge_to > message.id:
            purge_to = message.id
    else:
        purge_to = message.id

    chat_id = message.chat.id
    message_ids = []

    for message_id in range(
        repliedmsg.id,
        purge_to,
    ):
        message_ids.append(message_id)

        # Max message deletion limit is 100
        if len(message_ids) == 100:
            await app.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,  # For both sides
            )

            # To delete more than 100 messages, start again
            message_ids = []

    # Delete if any messages left
    if len(message_ids) > 0:
        await app.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )


# del
@app.on_message(filters.command("del") & ~filters.private)
@adminsOnly("can_delete_messages")
async def deleteFunc(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply To A Message To Delete It")
    await message.reply_to_message.delete()
    await message.delete()



# swarn
@app.on_message(filters.command("swarn") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def swarn_user(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    chat_id = message.chat.id
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ")
    if user_id == app.id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴍʏsᴇʟғ, ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ ɪғ ʏᴏᴜ ᴡᴀɴᴛ.")
    if user_id in SUDOERS:
        return await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴍʏ ᴍᴀɴᴀɢᴇʀ's, ʙᴇᴄᴀᴜsᴇ ʜᴇ ᴍᴀɴᴀɢᴇ ᴍᴇ!"
        )
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴀɴ ᴀᴅᴍɪɴ, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇs sᴏ ᴅᴏ ɪ."
        )
    
    user, warns = await asyncio.gather(
        app.get_users(user_id),
        get_warn(chat_id, await int_to_alpha(user_id)),
    )
    if warns:
        warns = warns["warns"]
    else:
        warns = 0

    if warns >= 2:
        await message.chat.ban_member(user_id)
        await message.reply_text(f"ɴᴜᴍʙᴇʀ ᴏғ ᴡᴀʀɴs ᴏғ {user.mention} ᴇxᴄᴇᴇᴅᴇᴅ, ʙᴀɴɴᴇᴅ!")
        await remove_warns(chat_id, await int_to_alpha(user_id))
    else:
        warn = {"warns": warns + 1}
        await add_warn(chat_id, await int_to_alpha(user_id), warn)
    
    await message.delete()  # Delete the command message for silent warning



# dwarn
@app.on_message(filters.command("dwarn") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def delete_and_warn_user(_, message: Message):
    # Check if the command is a reply
    if not message.reply_to_message:
        return await message.reply_text("You have to reply to a message to delete it and warn the user.")
    
    user_id, reason = await extract_user_and_reason(message)
    chat_id = message.chat.id
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ")
    if user_id == app.id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴍʏsᴇʟғ, ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ ɪғ ʏᴏᴜ ᴡᴀɴᴛ.")
    if user_id in SUDOERS:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴍʏ ᴍᴀɴᴀɢᴇʀ's, ʙᴇᴄᴀᴜsᴇ ʜᴇ ᴍᴀɴᴀɢᴇs ᴍᴇ!")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴀɴ ᴀᴅᴍɪɴ, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇs sᴏ ᴅᴏ ɪ.")

    user, warns = await asyncio.gather(
        app.get_users(user_id),
        get_warn(chat_id, await int_to_alpha(user_id)),
    )
    mention = user.mention
    keyboard = ikb({"ʀᴇᴍᴏᴠᴇ ᴡᴀʀɴ (ᴀᴅᴍɪɴ ᴏɴʟʏ)": f"unwarn_{user_id}"})
    warns = warns["warns"] if warns else 0

    if warns >= 2:
        await message.chat.ban_member(user_id)
        await message.reply_text(f"ɴᴜᴍʙᴇʀ ᴏғ ᴡᴀʀɴs ᴏғ {mention} ᴇxᴄᴇᴇᴅᴇᴅ, ʙᴀɴɴᴇᴅ!")
        await remove_warns(chat_id, await int_to_alpha(user_id))
    else:
        warn = {"warns": warns + 1}
        msg = f"""
<b>● ᴡᴀʀɴᴇᴅ ᴜsᴇʀ ➠</b> <a href="tg://user?id={user_id}">{user.first_name}</a>
<b>● ᴡᴀʀɴᴇᴅ ʙʏ ➠</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name if message.from_user else 'ᴀɴᴏɴʏᴍᴏᴜs'}</a>
<b>● ʀᴇᴀsᴏɴ ➠</b> {reason or 'ɴᴏ ʀᴇᴀsᴏɴ ᴘʀᴏᴠɪᴅᴇᴅ'}
<b>● ᴡᴀʀɴs ➠</b> {warns + 1}/3
"""
        # Delete the user's message
        await message.reply_to_message.delete()
        await message.reply_text(msg, reply_markup=keyboard)
        await add_warn(chat_id, await int_to_alpha(user_id), warn)


# warn
@app.on_message(filters.command("warn") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def warn_user(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    chat_id = message.chat.id
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ")
    if user_id == app.id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴍʏsᴇʟғ, ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ ɪғ ʏᴏᴜ ᴡᴀɴᴛ.")
    if user_id in SUDOERS:
        return await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴍʏ ᴍᴀɴᴀɢᴇʀ's, ʙᴇᴄᴀᴜsᴇ ʜᴇ ᴍᴀɴᴀɢᴇ ᴍᴇ!"
        )
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴀɴ ᴀᴅᴍɪɴ, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇs sᴏ ᴅᴏ ɪ."
        )
    user, warns = await asyncio.gather(
        app.get_users(user_id),
        get_warn(chat_id, await int_to_alpha(user_id)),
    )
    mention = user.mention
    keyboard = ikb({"ʀᴇᴍᴏᴠᴇ ᴡᴀʀɴ (ᴀᴅᴍɪɴ ᴏɴʟʏ)": f"unwarn_{user_id}"})
    if warns:
        warns = warns["warns"]
    else:
        warns = 0

    if warns >= 2:
        await message.chat.ban_member(user_id)
        await message.reply_text(f"ɴᴜᴍʙᴇʀ ᴏғ ᴡᴀʀɴs ᴏғ {mention} ᴇxᴄᴇᴇᴅᴇᴅ, ʙᴀɴɴᴇᴅ!")
        await remove_warns(chat_id, await int_to_alpha(user_id))
    else:
        warn = {"warns": warns + 1}
        msg = f"""
<b>● ᴡᴀʀɴᴇᴅ ᴜsᴇʀ ➠</b> <a href="tg://user?id={user_id}">{user.first_name}</a>
<b>● ᴡᴀʀɴᴇᴅ ʙʏ ➠</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name if message.from_user else 'ᴀɴᴏɴʏᴍᴏᴜs'}</a>
<b>● ʀᴇᴀsᴏɴ ➠</b> {reason or 'ɴᴏ ʀᴇᴀsᴏɴ ᴘʀᴏᴠɪᴅᴇᴅ'}
<b>● ᴡᴀʀɴs ➠</b> {warns + 1}/3
"""
        replied_message = message.reply_to_message
        if replied_message:
            message = replied_message
        await message.reply_text(msg, reply_markup=keyboard)
        await add_warn(chat_id, await int_to_alpha(user_id), warn)


@app.on_callback_query(filters.regex("unwarn_") & ~BANNED_USERS)
async def remove_warning(_, cq: CallbackQuery):
    from_user = cq.from_user
    chat_id = cq.message.chat.id
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await cq.answer(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ\n"
            + f"ᴘᴇʀᴍɪssɪᴏɴ ɴᴇᴇᴅᴇᴅ: {permission}",
            show_alert=True,
        )
    user_id = cq.data.split("_")[1]
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if not warns or warns == 0:
        return await cq.answer("ᴜsᴇʀ ʜᴀs ɴᴏ ᴡᴀʀɴɪɴɢs.")
    warn = {"warns": warns - 1}
    await add_warn(chat_id, await int_to_alpha(user_id), warn)
    text = cq.message.text
    text = f"<strike>{text}</strike>\n\n"
    text += f"<i>ᴡᴀʀɴ ʀᴇᴍᴏᴠᴇᴅ ʙʏ {from_user.mention}</i>"
    await cq.message.edit(text)

# remove all warns selected one users 
@app.on_message(filters.command("resetwarn") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def remove_warnings(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    mention = (await app.get_users(user_id)).mention
    chat_id = message.chat.id
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if warns == 0 or not warns:
        await message.reply_text(f"{mention} ʜᴀs ɴᴏ ᴡᴀʀɴɪɴɢs.")
    else:
        await remove_warns(chat_id, await int_to_alpha(user_id))
        await message.reply_text(f"ʀᴇᴍᴏᴠᴇᴅ ᴡᴀʀɴɪɴɢs ᴏғ {mention}.")


# resetwarns
@app.on_message(filters.command("resetallwarns") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def remove_all_warnings(_, message: Message):
    chat_id = message.chat.id
    # Fetch all warned users for the chat
    warned_users = await get_all_warned_users(chat_id)
    if not warned_users:
        return await message.reply_text("ɴᴏ ᴏɴᴇ ᴡᴀs ᴡᴀʀɴᴇᴅ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ.")
    
    # Remove warnings for all warned users
    for user_id in warned_users:
        await remove_warns(chat_id, await int_to_alpha(user_id))
    
    await message.reply_text("ᴀʟʟ ᴜsᴇʀs' ᴡᴀʀɴᴇʀs ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ.")


# checking warns
@app.on_message(filters.command("warns") & ~filters.private & ~BANNED_USERS)
@capture_err
async def check_warns(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.")
    warns = await get_warn(message.chat.id, await int_to_alpha(user_id))
    mention = (await app.get_users(user_id)).mention
    if warns:
        warns = warns["warns"]
    else:
        return await message.reply_text(f"{mention} ʜᴀs ɴᴏ ᴡᴀʀɴɪɴɢs.")
    return await message.reply_text(f"{mention} ʜᴀs {warns}/3 ᴡᴀʀɴɪɴɢs")

# invite link
@app.on_message(filters.command("link") & ~BANNED_USERS)
@adminsOnly("can_invite_users")
async def invite(_, message):
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        link = (await app.get_chat(message.chat.id)).invite_link
        if not link:
            link = await app.export_chat_invite_link(message.chat.id)
        text = f"ʜᴇʀᴇ's ᴛʜᴇ ɢʀᴏᴜᴘ ɪɴᴠɪᴛᴇ ʟɪɴᴋ \n\n{link}"
        if message.reply_to_message:
            await message.reply_to_message.reply_text(
                text, disable_web_page_preview=True
            )
        else:
            await message.reply_text(text, disable_web_page_preview=True)