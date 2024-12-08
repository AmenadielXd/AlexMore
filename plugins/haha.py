import asyncio
from pyrogram import filters, enums
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPrivileges, CallbackQuery

from Alex import app
from Alex.misc import SUDOERS
from Alex.utils.database import get_assistant

# Cache invite links to reduce API calls
links = {}


@app.on_message(filters.command("deleteall"))
async def deleteall_command(client, message):
    chat_id = message.chat.id
    assistant = await get_assistant(chat_id)
    assid = assistant.id

    # Check bot permissions
    bot = await app.get_chat_member(chat_id, app.me.id)
    if not (
        bot.privileges.can_delete_messages and
        bot.privileges.can_promote_members and
        bot.privileges.can_invite_users
    ):
        await message.reply(
            "❌ I need the following permissions:\n"
            "- Delete Messages\n"
            "- Promote Members\n"
            "- Invite Users"
        )
        return

    await message.reply(
        f"Are you sure you want to delete all messages in {message.chat.title}?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Yes", callback_data="deleteall_yes"),
             InlineKeyboardButton("No", callback_data="deleteall_no")]
        ])
    )


@app.on_callback_query(filters.regex(r"^deleteall_(yes|no)$"))
async def handle_callback(client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    assistant = await get_assistant(chat_id)
    assid = assistant.id

    # Check if the user is the owner or sudoer
    async for member in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if member.status == enums.ChatMemberStatus.OWNER:
            owner_id = member.user.id

    if user_id not in SUDOERS and user_id != owner_id:
        await callback_query.answer("❌ Only the group owner can confirm this action.", show_alert=True)
        return

    if callback_query.data == "deleteall_yes":
        await callback_query.answer("Deleting all messages...")

        # Ensure assistant is in the group
        try:
            await app.get_chat_member(chat_id, assid)
        except UserNotParticipant:
            try:
                chat = await app.get_chat(chat_id)
                if chat.username:  # Public group
                    try:
                        await assistant.join_chat(f"https://t.me/{chat.username}")
                    except Exception as e:
                        await callback_query.message.edit(f"❌ Public group invite failed: {str(e)}")
                        return
                else:  # Private group
                    if chat_id not in links:
                        try:
                            invite_link = await app.export_chat_invite_link(chat_id)
                            links[chat_id] = invite_link
                        except ChatAdminRequired:
                            await callback_query.message.edit("❌ I need invite link permissions to add the assistant.")
                            return
                    try:
                        await assistant.join_chat(links[chat_id])
                    except Exception as e:
                        await callback_query.message.edit(f"❌ Private group invite failed: {str(e)}")
                        return
            except Exception as e:
                await callback_query.message.edit(f"❌ Failed to invite assistant: {str(e)}")
                return

        # Promote assistant with the required privileges
        try:
            await app.promote_chat_member(chat_id, assid, ChatPrivileges(
                can_delete_messages=True
            ))
        except Exception as e:
            await callback_query.message.edit(f"❌ Failed to promote assistant: {str(e)}")
            return

        # Delete all messages
        try:
            async for msg in assistant.get_chat_history(chat_id):
                try:
                    await assistant.delete_messages(chat_id, msg.id)
                except Exception as e:
                    print(f"Failed to delete message {msg.id}: {e}")
                    continue
            await callback_query.message.edit("✅ Successfully deleted all messages.")
        except Exception as e:
            await callback_query.message.edit(f"❌ Error during deletion: {str(e)}")

    elif callback_query.data == "deleteall_no":
        await callback_query.message.edit("❌ Delete all operation canceled.")