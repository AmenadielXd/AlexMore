import asyncio
from pyrogram import filters, enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ChatPrivileges

from Alex import app
from Alex.misc import SUDOERS
from Alex.utils.database import get_assistant

links = {}


def get_keyboard(command):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes", callback_data=f"{command}_yes"),
         InlineKeyboardButton("No", callback_data=f"{command}_no")]
    ])


@app.on_message(filters.command("deleteall"))
async def deleteall_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    assistant = await get_assistant(chat_id)
    assid = assistant.id

    bot = await app.get_chat_member(chat_id, app.me.id)
    if not (
        bot.privileges.can_delete_messages and
        bot.privileges.can_promote_members and
        bot.privileges.can_invite_users
    ):
        await message.reply(
            "I don't have enough permissions to perform mass deletion.\n\n"
            "Permissions required:\n"
            "- Delete messages\n"
            "- Promote members\n"
            "- Invite users"
        )
        return

    confirm_msg = await message.reply(
        f"{message.from_user.mention}, are you sure you want to delete all group messages?",
        reply_markup=get_keyboard("deleteall")
    )


@app.on_callback_query(filters.regex(r"^deleteall_(yes|no)$"))
async def handle_callback(client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    assistant = await get_assistant(chat_id)
    assid = assistant.id

    # Check if the user is the group owner or a sudo user
    owner_id = None
    async for admin in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if admin.status == ChatMemberStatus.OWNER:
            owner_id = admin.user.id
    if user_id != owner_id and user_id not in SUDOERS:
        await callback_query.answer("Only the group owner can confirm this action.", show_alert=True)
        return

    if callback_query.data == "deleteall_yes":
        await callback_query.answer("Delete all process started...", show_alert=True)

        # Invite assistant if not already in the group
        try:
            await app.get_chat_member(chat_id, assid)
        except UserNotParticipant:
            try:
                chat = await app.get_chat(chat_id)
                if chat.username:
                    # Public group - join via username
                    await assistant.join_chat(f"https://t.me/{chat.username}")
                else:
                    # Private group - join via invite link
                    if chat_id in links:
                        invitelink = links[chat_id]
                    else:
                        try:
                            invitelink = await app.export_chat_invite_link(chat_id)
                        except ChatAdminRequired:
                            await callback_query.message.edit("I need invite permission to add the assistant.")
                            return
                        links[chat_id] = invitelink
                    await assistant.join_chat(invitelink)
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(chat_id, assid)
                except Exception as e:
                    await callback_query.message.edit(f"Error approving invite: {e}")
                    return
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                await callback_query.message.edit(f"Error inviting assistant: {e}")
                return

        # Promote the assistant with the required privileges
        await app.promote_chat_member(
            chat_id,
            assid,
            privileges=ChatPrivileges(
                can_manage_chat=False,
                can_delete_messages=True,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_promote_members=False,
            )
        )

        # Delete all messages
        try:
            async for msg in assistant.get_chat_history(chat_id):
                try:
                    await assistant.delete_messages(chat_id, msg.id)
                except Exception as e:
                    print(f"Failed to delete message {msg.id}: {e}")
                    continue
            await callback_query.answer("All messages deleted successfully.", show_alert=False)
        except Exception as e:
            await callback_query.message.edit(f"An error occurred: {e}")

    elif callback_query.data == "deleteall_no":
        await callback_query.message.edit("Delete all process canceled.")